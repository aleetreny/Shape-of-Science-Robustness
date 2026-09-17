"""Separate, resumable length controls; reuse only identical verified inputs.

Never mutates the original corpus, encoders, configurations or model outputs.
"""
import argparse
from collections import OrderedDict
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import torch

from sos_embed.common_text import common_fragment
from sos_embed.models import Encoder, snapshot_path
from sos_embed.runner import (CACHE, INPUT, META_COLUMNS, config, environment,
                              source_files, snapshot_sources, verify_assets)
from sos_embed.storage import (Store, file_sha, object_sha, run_lock, utcnow,
                               write_json)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "config/analysis_v1.json"
OUTPUT = ROOT / "data/analysis_v1/controls"
COMMON = OUTPUT / "common_text_52k"


def sources():
    return {**source_files(), str(Path(__file__).relative_to(ROOT)): file_sha(__file__),
            str(DESIGN.relative_to(ROOT)): file_sha(DESIGN)}


def prepare_common():
    from transformers import AutoTokenizer
    design = json.loads(DESIGN.read_text())
    selection = {"design_sha256": file_sha(DESIGN), "source_sha256": file_sha(INPUT),
                 "seed": design["common_text_seed"], "per_cell": design["common_text_per_cell"],
                 "method": "lowest SHA256(seed + work_id) within each Field/period"}
    with run_lock(COMMON):
        saved = COMMON / "input_manifest.json"
        if saved.exists():
            manifest = json.loads(saved.read_text())
            if manifest["selection"] != selection or file_sha(COMMON / "input.parquet") != manifest["input_sha256"]:
                raise ValueError("Common input changed")
            return manifest
        metadata = pq.read_table(INPUT, columns=META_COLUMNS).to_pylist()
        cells = {}
        for r in metadata:
            rank = hashlib.sha256((selection["seed"] + r["work_id"]).encode()).digest()
            cells.setdefault((r["field_id"], r["period_start"]), []).append((rank, r["row_index"]))
        indices = sorted(i for values in cells.values() for _, i in sorted(values)[:selection["per_cell"]])
        if len(cells) != 130 or len(indices) != design["common_text_rows"]:
            raise ValueError("Incomplete common sample")
        table = pq.read_table(INPUT).take(pa.array(indices))
        pq.write_table(table, COMMON / "native_input.parquet", compression="zstd")
        specs = config()["models"]
        pairs = [(m, AutoTokenizer.from_pretrained(snapshot_path(CACHE, m), local_files_only=True,
                                                   trust_remote_code=False, use_fast=True)) for m in specs]
        rows = table.to_pylist()
        changed = titles = 0
        for i, r in enumerate(rows):
            title, abstract = common_fragment(r["title"], r["abstract"], pairs)
            r["source_text_sha256"] = r["text_sha256"]
            changed += (title, abstract) != (r["title"], r["abstract"])
            titles += title != r["title"]
            r["title"], r["abstract"] = title, abstract
            r["text_sha256"] = hashlib.sha256((title + "\n\n" + abstract).encode()).hexdigest()
            if (i + 1) % 1000 == 0:
                print(f"Fragmento común: {i+1:,}/{len(rows):,}", flush=True)
        temporary = COMMON / ".input.partial.parquet"
        pq.write_table(pa.Table.from_pylist(rows), temporary, compression="zstd")
        os.replace(temporary, COMMON / "input.parquet")
        manifest = {"selection": selection, "rows": len(rows), "input_sha256": file_sha(COMMON / "input.parquet"),
                    "native_input_sha256": file_sha(COMMON / "native_input.parquet"),
                    "changed_rows": changed, "titles_shortened": titles, "completed_at": utcnow()}
        write_json(saved, manifest)
        return manifest


class NativeBlocks:
    """Small read-only cache. Verify original shards before using any row."""
    def __init__(self, key):
        catalog = json.loads((ROOT / "research/embedding_final_audit_2026-09-17/catalog.json").read_text())
        audit = json.loads((ROOT / "research/embedding_final_audit_2026-09-17/audit_summary.json").read_text())
        if file_sha(ROOT / "research/embedding_final_audit_2026-09-17/catalog.json") != audit["catalog_sha256"]:
            raise ValueError("Original catalog changed")
        self.model = catalog["models"][key]
        if file_sha(ROOT / self.model["manifest_path"]) != self.model["manifest_sha256"]:
            raise ValueError("Native manifest changed")
        self.cache = OrderedDict()

    def row(self, index):
        block = index // 1024
        if block not in self.cache:
            shard = self.model["shards"][block]
            if file_sha(ROOT / shard["rows_path"]) != shard["rows_sha256"]:
                raise ValueError("Native rows changed")
            vectors = {}
            for name, vector in shard["vectors"].items():
                path = ROOT / vector["path"]
                if file_sha(path) != vector["sha256"]:
                    raise ValueError("Native vectors changed")
                vectors[name] = np.load(path, mmap_mode="r", allow_pickle=False)
            self.cache[block] = (pq.read_table(ROOT / shard["rows_path"]).to_pylist(), vectors)
            if len(self.cache) > 16:
                self.cache.popitem(last=False)
        self.cache.move_to_end(block)
        rows, vectors = self.cache[block]
        offset = index - block * 1024
        return rows[offset], {name: array[offset] for name, array in vectors.items()}


def run_control(kind, key, max_shards=None):
    design = json.loads(DESIGN.read_text())
    original_spec = next(m for m in config()["models"] if m["key"] == key)
    spec = copy.deepcopy(original_spec)
    if kind == "minilm512":
        if key != "minilm":
            raise ValueError("Length extension only specified for MiniLM")
        spec["max_length"] = design["extra_minilm_max_length"]
        path, output = INPUT, OUTPUT / "minilm_512"
        input_manifest = {"rows": 500000, "input_sha256": file_sha(path)}
    elif kind == "common":
        path, output = COMMON / "input.parquet", COMMON
        input_manifest = json.loads((COMMON / "input_manifest.json").read_text())
        if file_sha(path) != input_manifest["input_sha256"]:
            raise ValueError("Changed common input")
    else:
        raise ValueError(kind)
    assets = verify_assets(spec)
    native = NativeBlocks(key)
    manifest = {"schema_version": 1, "scope": "analysis_control", "control": kind, "model": spec,
                "dimension": spec["dimension"], "poolings": spec["poolings"], "rows": input_manifest["rows"],
                "input_sha256": input_manifest["input_sha256"], "input_manifest": input_manifest,
                "source_files": sources(), "environment": environment(), "asset_records": assets,
                "native_manifest_sha256": native.model["manifest_sha256"],
                "design_sha256": file_sha(DESIGN), "dtype": "float32", "device": "mps",
                "postprocessing": "none", "batch_size": 16, "shard_size": 1024, "seed": 20260917,
                "reuse": "identical source text and recipe; for length extension only originally untruncated rows"}
    with run_lock(output / key):
        snapshot_sources(output, manifest["source_files"])
        store = Store(output / key, manifest)
        expected = pq.read_table(path, columns=META_COLUMNS)
        current = store.scan(expected)
        if current["complete"]:
            print(json.dumps(current), flush=True)
            return current
        torch.set_num_threads(8)
        torch.manual_seed(20260917)
        encoder = Encoder(spec, CACHE, "mps")
        offset = committed = 0
        for batch in pq.ParquetFile(path).iter_batches(batch_size=1024):
            end = offset + batch.num_rows
            if end <= current["rows"]:
                offset = end
                continue
            if offset < current["rows"]:
                raise ValueError("Resume crosses shard boundary")
            started = time.monotonic()
            table = pa.Table.from_batches([batch])
            rows = table.to_pylist()
            arrays = {pool: np.empty((len(rows), spec["dimension"]), dtype=np.float32) for pool in spec["poolings"]}
            audits = [None] * len(rows)
            to_encode = []
            for i, row in enumerate(rows):
                old, vector = native.row(row["row_index"])
                source_hash = row.get("source_text_sha256", row["text_sha256"])
                if old["work_id"] != row["work_id"] or old["text_sha256"] != source_hash:
                    raise ValueError("Native identity mismatch")
                reuse = (row["text_sha256"] == source_hash and (kind == "common" or not old["truncated"]))
                if reuse:
                    audits[i] = {name: old[name] for name in ("tokens_original", "tokens_used", "truncated",
                        "formatted_text_sha256", "token_ids_sha256", "last_content_character", "formatted_characters")}
                    for pool in arrays:
                        arrays[pool][i] = vector[pool]
                else:
                    to_encode.append(i)
            if to_encode:
                new, audit, stats = encoder.encode([rows[i] for i in to_encode], batch_size=16)
                for pos, i in enumerate(to_encode):
                    audits[i] = audit[pos]
                    for pool in arrays:
                        arrays[pool][i] = new[pool][pos]
            if kind == "common" and any(a["truncated"] for a in audits):
                raise ValueError("Common text unexpectedly truncated")
            metadata = table.select(META_COLUMNS)
            if "source_text_sha256" in table.column_names:
                metadata = metadata.append_column("source_text_sha256", table["source_text_sha256"])
            for name in audits[0]:
                metadata = metadata.append_column(name, pa.array([a[name] for a in audits]))
            stats = {"seconds": time.monotonic() - started, "rows": len(rows), "encoded_rows": len(to_encode),
                     "reused_rows": len(rows) - len(to_encode), "truncated_rows": sum(a["truncated"] for a in audits)}
            store.commit(offset, metadata, arrays, stats)
            write_json(store.path / "progress.json", {"state": "running", "rows": end,
                       "target": manifest["rows"], "updated_at": utcnow(), "last_shard": stats})
            print(f"{kind}/{key}: {end:,}/{manifest['rows']:,}; reutilizados {stats['reused_rows']}; {stats['seconds']:.1f}s", flush=True)
            offset, committed = end, committed + 1
            if max_shards is not None and committed >= max_shards:
                break
        result = {**store.scan(expected), "updated_at": utcnow(), "manifest_sha256": object_sha(manifest)}
        write_json(store.path / "validation.json", result)
        write_json(store.path / "progress.json", {**result, "state": "complete" if result["complete"] else "paused"})
        print(json.dumps(result), flush=True)
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["prepare-common", "minilm512", "common", "common-all"])
    parser.add_argument("--model")
    parser.add_argument("--max-shards", type=int)
    args = parser.parse_args()
    if args.action == "prepare-common":
        print(json.dumps(prepare_common()), flush=True)
    elif args.action == "common-all":
        with run_lock(COMMON / "queue"):
            for model in config()["models"]:
                subprocess.run([sys.executable, "-m", "sos_analysis.extra_embeddings", "common",
                                "--model", model["key"]], cwd=ROOT, check=True)
    else:
        run_control(args.action, "minilm" if args.action == "minilm512" else args.model, args.max_shards)


if __name__ == "__main__":
    main()
