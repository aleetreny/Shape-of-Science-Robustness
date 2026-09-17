"""Frozen-design shape comparisons; checkpoint every Field/period and stage."""
import argparse
import csv
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import time

import numpy as np

from sos_embed.storage import file_sha, object_sha, run_lock, utcnow, write_json
from .geometry import (prepare, shape_scores, rsa_scores, scores_from_moments,
                       streamed_moments)
from .native_data import NativeData

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/analysis_v1/shape"
WORD = {"scibert", "bert", "pubmedbert", "biobert"}


def seed_for(label):
    return int.from_bytes(hashlib.sha256(("20260917/" + label).encode()).digest()[:8], "little")


def save_result(path, value):
    write_json(path, value)
    write_json(path.with_suffix(".sha.json"), {"sha256": file_sha(path)})


def complete(path, manifest):
    if not path.exists():
        return False
    check = path.with_suffix(".sha.json")
    if not check.exists() or json.loads(check.read_text())["sha256"] != file_sha(path):
        raise ValueError(f"Unverified result: {path}")
    if json.loads(path.read_text())["manifest_sha256"] != object_sha(manifest):
        raise ValueError("Result belongs to different analysis")
    return True


def freeze():
    files = ["config/analysis_v1.json", "requirements-analysis.txt", "sos_analysis/run_shape.py",
             "sos_analysis/geometry.py", "sos_analysis/native_data.py", "sos_analysis/reader.py"]
    manifest = {"schema_version": 1, "files": {f: file_sha(ROOT / f) for f in files},
                "packages": {m: importlib.metadata.version(m) for m in ("numpy", "scipy", "pyarrow")}}
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "manifest.json"
    if path.exists():
        if json.loads(path.read_text()) != manifest:
            raise ValueError("Analysis changed: use a new version, do not overwrite")
    else:
        for name in files:
            target = OUT / "source_snapshot" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        write_json(path, manifest)
    return manifest


def strict_quality(data):
    meta = data.metadata
    mask = np.ones(len(meta), dtype=bool)
    for name in data.design["quality_sensitivity_flags"]:
        mask &= ~meta[name].to_numpy()
    parent = np.arange(len(meta))

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for name in ("doi", "normalized_text_group"):
        seen = {}
        for i, value in enumerate(meta[name].to_pylist()):
            if not value:
                continue
            value = value.lower().strip() if name == "doi" else value
            if value in seen:
                a, b = root(i), root(seen[value])
                parent[max(a, b)] = min(a, b)
            else:
                seen[value] = i
    representative = np.asarray([root(i) for i in range(len(meta))])
    mask &= representative == np.arange(len(meta))
    return mask


def names_for(data, stage):
    return [f"{key}/{stage if stage in ('cls','sep') and key in WORD else pool}"
            for key, pool in data.design["poolings"].items()]


def cell_run(data, manifest, stage, *, max_cells=None):
    names = names_for(data, stage)
    quality = strict_quality(data) if stage == "quality" else None
    total = 0
    for (field, period), full_ids in data.cells().items():
        path = OUT / stage / f"{field}_{period}.json"
        if complete(path, manifest):
            continue
        started = time.monotonic()
        ids = full_ids if quality is None else full_ids[quality[full_ids]]
        if len(ids) < 4:
            raise ValueError("Too few rows after quality filter")
        arrays = [data.get(name, ids) for name in names]
        if stage == "stability":
            arrays = [prepare(x) for x in arrays]
            results, selections = [], []
            for size in data.design["shape_sample_sizes"]:
                if size > len(ids):
                    raise ValueError("Predeclared stability size exceeds cell")
                for repeat in range(data.design["shape_resamples"]):
                    seed = seed_for(f"stability/{field}/{period}/{size}/{repeat}")
                    chosen = np.sort(np.random.default_rng(seed).choice(len(ids), size, replace=False))
                    rows = shape_scores([x[chosen] for x in arrays], names, normalize=False, procrustes=False)
                    results.extend({**r, "repeat": repeat, "sample_size": size} for r in rows)
                    selections.append({"size": size, "repeat": repeat, "seed": seed,
                                       "indices_sha256": hashlib.sha256(ids[chosen].astype('<i8').tobytes()).hexdigest()})
            result = {"scores": results, "selection_records": selections}
        else:
            normalized = stage != "raw"
            # All controls keep the same three score definitions. RSA uses cosine,
            # so it is unchanged by per-row L2 and need not be repeated for raw.
            rows = shape_scores(arrays, names, normalize=normalized, procrustes=True)
            result = {"scores": rows}
            if stage == "primary":
                rsa = rsa_scores(data.get, ids, names, count=data.design["rsa_pairs"],
                                 seed=seed_for(f"rsa/{field}/{period}"))
                for r in rows:
                    r["rsa_spearman"] = rsa[r["model_a"], r["model_b"]]
                shuffled = [x[np.random.default_rng(seed_for(f"null/{field}/{period}/{name}")).permutation(len(x))]
                            for name, x in zip(names, arrays)]
                result["null_scores"] = shape_scores(shuffled, names, procrustes=True)
                # One reference permutation is diagnostic, never a p-value.
        result.update({"stage": stage, "field_id": field, "period_start": period, "n": len(ids),
                       "rows_before_filter": len(full_ids), "manifest_sha256": object_sha(manifest),
                       "indices_sha256": hashlib.sha256(ids.astype('<i8').tobytes()).hexdigest(),
                       "completed_at": utcnow(), "seconds": time.monotonic() - started})
        save_result(path, result)
        total += 1
        print(f"{stage}: Field {field}, {period}, n={len(ids):,}, {result['seconds']:.1f}s", flush=True)
        if max_cells and total >= max_cells:
            break


def global_run(data, manifest):
    names = names_for(data, "primary")
    ids = np.flatnonzero(data.metadata["cohort"].to_numpy() == "base")
    for normalization in (True, False):
        label = "global_base_unit" if normalization else "global_base_raw"
        path = OUT / "global" / (label + ".json")
        if complete(path, manifest):
            continue
        started = time.monotonic()
        moments = streamed_moments(data.get, ids, names, data.dimensions(names), normalize=normalization)
        rows = scores_from_moments(moments, len(ids), data.dimensions(names), names)
        if normalization:
            rsa = rsa_scores(data.get, ids, names, count=data.design["rsa_pairs"], seed=seed_for(label))
            for r in rows:
                r["rsa_spearman"] = rsa[r["model_a"], r["model_b"]]
        save_result(path, {"stage": label, "n": len(ids), "scores": rows,
                          "manifest_sha256": object_sha(manifest), "completed_at": utcnow(),
                          "seconds": time.monotonic() - started})
        print(f"{label}: {len(ids):,} filas, {time.monotonic()-started:.1f}s", flush=True)


def centroid_run(data, manifest):
    path = OUT / "centroids" / "relations.json"
    if complete(path, manifest):
        return
    names = names_for(data, "primary")
    cells = data.cells()
    centroids = {name: {cell: prepare(data.get(name, ids)).mean(0) for cell, ids in cells.items()}
                 for name in names}
    edges, comparisons = [], []
    from scipy.stats import spearmanr
    for period in sorted({p for _, p in cells}):
        fields = sorted({f for f, p in cells if p == period})
        distances = {}
        for name in names:
            c = prepare(np.asarray([centroids[name][(f, period)] for f in fields]))
            matrix = 1 - c @ c.T
            distances[name] = matrix[np.triu_indices(len(fields), 1)]
            for i in range(len(fields)):
                for j in range(i+1, len(fields)):
                    edges.append({"period_start": period, "model": name, "field_a": fields[i],
                                  "field_b": fields[j], "cosine_distance": float(matrix[i,j])})
        for i, name in enumerate(names):
            for other in names[i+1:]:
                comparisons.append({"period_start": period, "model_a": name, "model_b": other,
                                    "centroid_edge_spearman": float(spearmanr(distances[name], distances[other]).statistic)})
    save_result(path, {"edges": edges, "scores": comparisons, "manifest_sha256": object_sha(manifest),
                       "completed_at": utcnow(), "interpretation": "325 Field-centroid relations per period; all cell papers"})
    print("Centros de las 26 áreas: completos", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["primary", "raw", "cls", "sep", "quality", "stability", "global", "centroids", "all"])
    parser.add_argument("--max-cells", type=int)
    args = parser.parse_args()
    with run_lock(OUT):
        manifest = freeze()
        data = NativeData(ROOT)
        stages = ["primary", "global", "centroids", "raw", "cls", "sep", "quality", "stability"] if args.stage == "all" else [args.stage]
        for stage in stages:
            write_json(OUT / "progress.json", {"stage": stage, "state": "running", "updated_at": utcnow()})
            if stage == "global":
                global_run(data, manifest)
            elif stage == "centroids":
                centroid_run(data, manifest)
            else:
                cell_run(data, manifest, stage, max_cells=args.max_cells)
        write_json(OUT / "progress.json", {"state": "requested_stages_complete", "stages": stages, "updated_at": utcnow()})


if __name__ == "__main__":
    main()
