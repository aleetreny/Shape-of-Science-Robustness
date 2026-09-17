"""Verified original vectors, cached in bounded RAM for repeated comparisons."""
from collections import OrderedDict
import json
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq

from .reader import EmbeddingCorpus, sha256


class NativeData:
    def __init__(self, root, max_bytes=16 * 1024**3):
        self.root = Path(root).resolve()
        self.design = json.loads((self.root / "config/analysis_v1.json").read_text())
        self.reader = EmbeddingCorpus(self.root, catalog_sha256=self.design["catalog_sha256"])
        self.metadata = self.reader.metadata
        self.cache = OrderedDict()
        self.max_bytes = max_bytes
        self.cached_bytes = 0

    def get(self, name, indices):
        # Name form model/pooling. Explicit choices prevent accidental defaults.
        if name not in self.cache:
            model, pooling = name.split("/")
            dimension = self.reader.catalog["models"][model]["dimension"]
            needed = len(self.metadata) * dimension * 4
            while self.cache and self.cached_bytes + needed > self.max_bytes:
                _, old = self.cache.popitem(last=False)
                self.cached_bytes -= old.nbytes
            matrix = np.empty((len(self.metadata), dimension), dtype=np.float32)
            for meta, arrays in self.reader.iter_aligned({model: pooling}):
                start = meta["row_index"][0].as_py()
                matrix[start:start + len(meta)] = arrays[model]
            matrix.setflags(write=False)
            self.cache[name] = matrix
            self.cached_bytes += matrix.nbytes
        self.cache.move_to_end(name)
        return self.cache[name][indices]

    def dimensions(self, names):
        return [self.reader.catalog["models"][n.split("/")[0]]["dimension"] for n in names]

    def cells(self):
        fields = self.metadata["field_id"].to_numpy()
        periods = self.metadata["period_start"].to_numpy()
        return {(int(f), int(p)): np.flatnonzero((fields == f) & (periods == p))
                for f in np.unique(fields) for p in np.unique(periods)}


def load_control(root, directory, model, pooling):
    """Read a completed separate control, validating every file and identity."""
    from sos_embed.storage import Store
    # This helper runs under .venv-embed, or callers can read via catalog exports.
    folder = Path(root) / directory / model
    manifest = json.loads((folder / "manifest.json").read_text())
    path = Path(root) / ("data/corpus_clean_v1/embedding_input.parquet" if
                       manifest["control"] == "minilm512" else str(Path(directory) / "input.parquet"))
    if sha256(path) != manifest["input_sha256"]:
        raise ValueError("Control input changed")
    expected = pq.read_table(path, columns=["row_index", "work_id", "text_sha256"])
    report = Store(folder, manifest).scan(expected)
    if not report["complete"]:
        raise ValueError("Control incomplete")
    return expected, np.concatenate([np.load(p / (pooling + ".npy"), allow_pickle=False)
                                    for p in sorted((folder / "shards").glob("[0-9]*"))])
