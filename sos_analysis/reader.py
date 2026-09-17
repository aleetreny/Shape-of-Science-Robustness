"""Stream the same papers from selected models without changing frozen data."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq


JOIN = ["row_index", "work_id", "text_sha256", "cohort", "field_id",
        "publication_year", "period_start"]
DEFAULT_CATALOG = "research/embedding_final_audit_2026-09-17/catalog.json"


class IntegrityError(ValueError):
    """A file or its paper identities differ from the audited catalog."""


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition, message):
    if not condition:
        raise IntegrityError(message)


class EmbeddingCorpus:
    """Keep metadata in RAM and read vectors one shard at a time, read-only.

    `selections` in iter_aligned must name a pooling for every selected model.
    No normalization, quality exclusions, weighting or scientific comparisons
    are applied. File checks run before each selected shard is yielded.
    """

    def __init__(self, root, catalog_path=DEFAULT_CATALOG, *, catalog_sha256=None):
        self.root = Path(root).resolve()
        path = self._path(catalog_path)
        if catalog_sha256 is not None:
            self._check(path, catalog_sha256)
        self.catalog = json.loads(path.read_text())
        require(self.catalog["schema_version"] == 1 and
                self.catalog["status"] == "verified", "Catalog is not verified v1")
        require(self.catalog["normalization"] == "none", "Expected raw vectors")
        metadata_path = self._path(self.catalog["metadata_path"])
        self._check(metadata_path, self.catalog["metadata_sha256"])
        self.metadata = pq.read_table(metadata_path)
        require(len(self.metadata) == self.catalog["rows"], "Metadata row count")
        for name in JOIN:
            require(name in self.metadata.column_names and
                    self.metadata[name].null_count == 0, f"Missing identity: {name}")
        require(np.array_equal(self.metadata["row_index"].to_numpy(),
                               np.arange(len(self.metadata))), "Metadata row order")
        require(pc.count_distinct(self.metadata["work_id"]).as_py() ==
                len(self.metadata), "Duplicate work IDs in metadata")
        counts = self.metadata["cohort"].value_counts().to_pylist()
        require({row["values"]: row["counts"] for row in counts} ==
                self.catalog["cohort_counts"], "Metadata cohort counts")

    def _path(self, relative):
        path = (self.root / relative).resolve()
        require(path.is_relative_to(self.root), "Catalog path leaves repository")
        return path

    @staticmethod
    def _check(path, expected):
        require(sha256(path) == expected, f"Changed file: {path}")

    def _model(self, key, pooling):
        if key not in self.catalog["models"]:
            raise ValueError(f"Unknown model: {key}")
        model = self.catalog["models"][key]
        if pooling not in model["poolings"]:
            raise ValueError(f"Choose an explicit saved pooling for {key}: {model['poolings']}")
        path = self._path(model["manifest_path"])
        self._check(path, model["manifest_sha256"])
        manifest = json.loads(path.read_text())
        require(manifest["model"]["key"] == key and
                manifest["input_sha256"] == self.catalog["source_input_sha256"] and
                manifest["rows"] == len(self.metadata) and manifest["scope"] == "full" and
                manifest["dimension"] == model["dimension"] and
                manifest["poolings"] == model["poolings"] and
                manifest["dtype"] == "float32" and manifest["postprocessing"] == "none",
                f"Model provenance mismatch: {key}")
        expected = 0
        for shard in model["shards"]:
            require(shard["start"] == expected and shard["end"] > expected,
                    f"Gap or overlap in {key}")
            expected = shard["end"]
        require(expected == len(self.metadata), f"Incomplete model: {key}")
        return model, hashlib.sha256(json.dumps(manifest, sort_keys=True,
                                               separators=(",", ":")).encode()).hexdigest()

    def iter_aligned(self, selections, *, cohorts=None, field_ids=None, periods=None):
        """Yield (Arrow metadata, {model: float32 array}) in fixed paper order.

        Example: selections={"specter": "cls", "minilm": "mean"}.
        Filtered-out shards are skipped. Filters never reorder rows. Memory is
        bounded unless the caller keeps the yielded blocks. Arrays are read-only.
        """
        if not isinstance(selections, dict) or not selections:
            raise ValueError("Provide model: pooling selections explicitly")
        filters = {}
        for column, values in (("cohort", cohorts), ("field_id", field_ids),
                               ("period_start", periods)):
            if values is not None:
                if isinstance(values, (str, bytes)):
                    raise ValueError(f"{column} filter must be a collection")
                values = set(values)
                known = set(pc.unique(self.metadata[column]).to_pylist())
                if not values <= known:
                    raise ValueError(f"Unknown {column}: {values - known}")
                filters[column] = values
        models = {key: self._model(key, pool) for key, pool in selections.items()}
        bounds = None
        for model, _ in models.values():
            current = [(s["start"], s["end"]) for s in model["shards"]]
            require(bounds is None or current == bounds, "Models have different shard bounds")
            bounds = current
        for index, (start, end) in enumerate(bounds):
            metadata = self.metadata.slice(start, end - start)
            mask = np.ones(end - start, dtype=bool)
            for column, values in filters.items():
                mask &= np.isin(metadata[column].to_numpy(), list(values))
            if not mask.any():
                continue
            arrays = {}
            for key, pooling in selections.items():
                model, manifest_digest = models[key]
                shard = model["shards"][index]
                commit_path = self._path(shard["commit_path"])
                self._check(commit_path, shard["commit_sha256"])
                commit = json.loads(commit_path.read_text())
                require(commit["manifest_sha256"] == manifest_digest and
                        (commit["start"], commit["end"]) == (start, end),
                        f"Shard provenance mismatch: {key}/{start}")
                rows_path = self._path(shard["rows_path"])
                self._check(rows_path, shard["rows_sha256"])
                require(commit["files"][rows_path.name] == shard["rows_sha256"],
                        f"Row digest mismatch: {key}/{start}")
                rows = pq.read_table(rows_path, columns=JOIN)
                require(rows.equals(metadata.select(JOIN)), f"Paper alignment: {key}/{start}")
                vector = shard["vectors"][pooling]
                path = self._path(vector["path"])
                self._check(path, vector["sha256"])
                require(commit["files"][path.name] == vector["sha256"],
                        f"Vector digest mismatch: {key}/{start}")
                array = np.load(path, mmap_mode="r", allow_pickle=False)
                require(array.dtype == np.float32 and
                        array.shape == (end - start, model["dimension"]),
                        f"Vector shape or dtype: {key}/{start}")
                require(np.isfinite(array).all() and np.any(array != 0, axis=1).all(),
                        f"Invalid vector values: {key}/{start}")
                if not mask.all():
                    array = array[mask]
                array.setflags(write=False)
                arrays[key] = array
            yield metadata.filter(pa.array(mask)), arrays
