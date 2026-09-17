"""Small independent fixtures; no model downloads or inference."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from sos_analysis import EmbeddingCorpus, IntegrityError
from sos_analysis.reader import sha256


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.meta = pa.table({
            "row_index": [0, 1, 2, 3, 4], "work_id": ["W0", "W1", "W2", "W3", "W4"],
            "text_sha256": ["t0", "t1", "t2", "t3", "t4"],
            "cohort": ["base", "base", "base", "extra", "extra"],
            "field_id": [1, 2, 1, 1, 2], "publication_year": [2001, 2002, 2006, 2001, 2006],
            "period_start": [2000, 2000, 2005, 2000, 2005],
            "duplicate_text": [False, True, False, False, True]})
        pq.write_table(self.meta, self.root / "metadata.parquet")
        self.catalog = {"schema_version": 1, "status": "verified", "rows": 5,
                        "normalization": "none", "source_input_sha256": "input",
                        "cohort_counts": {"base": 3, "extra": 2},
                        "metadata_path": "metadata.parquet",
                        "metadata_sha256": sha256(self.root / "metadata.parquet"), "models": {}}
        for key, dim, pool in (("a", 3, "cls"), ("b", 2, "mean")):
            folder = self.root / key
            folder.mkdir()
            manifest = {"model": {"key": key}, "input_sha256": "input", "rows": 5,
                        "dimension": dim, "poolings": [pool], "dtype": "float32",
                        "scope": "full", "postprocessing": "none"}
            self.write(folder / "manifest.json", manifest)
            model = {"dimension": dim, "poolings": [pool], "manifest_path": f"{key}/manifest.json",
                     "manifest_sha256": sha256(folder / "manifest.json"), "shards": []}
            for start, end in ((0, 3), (3, 5)):
                shard = folder / str(start)
                shard.mkdir()
                pq.write_table(self.meta.slice(start, end - start), shard / "rows.parquet")
                array = np.repeat(np.arange(start + 1, end + 1, dtype=np.float32)[:, None], dim, axis=1)
                np.save(shard / f"{pool}.npy", array)
                commit = {"start": start, "end": end, "files": {
                    "rows.parquet": sha256(shard / "rows.parquet"),
                    f"{pool}.npy": sha256(shard / f"{pool}.npy")},
                    "manifest_sha256": hashlib.sha256(json.dumps(manifest, sort_keys=True,
                                                                 separators=(",", ":")).encode()).hexdigest()}
                self.write(shard / "commit.json", commit)
                model["shards"].append({"start": start, "end": end,
                    "rows_path": f"{key}/{start}/rows.parquet", "rows_sha256": commit["files"]["rows.parquet"],
                    "commit_path": f"{key}/{start}/commit.json", "commit_sha256": sha256(shard / "commit.json"),
                    "vectors": {pool: {"path": f"{key}/{start}/{pool}.npy", "sha256": commit["files"][f"{pool}.npy"]}}})
            self.catalog["models"][key] = model
        self.save_catalog()

    def write(self, path, data):
        path.write_text(json.dumps(data))

    def save_catalog(self):
        self.write(self.root / "catalog.json", self.catalog)

    def reader(self):
        return EmbeddingCorpus(self.root, "catalog.json", catalog_sha256=sha256(self.root / "catalog.json"))

    def refresh_shard_digests(self, key="a", start=0):
        shard = next(s for s in self.catalog["models"][key]["shards"] if s["start"] == start)
        commit_path = self.root / shard["commit_path"]
        commit = json.loads(commit_path.read_text())
        shard["rows_sha256"] = sha256(self.root / shard["rows_path"])
        commit["files"]["rows.parquet"] = shard["rows_sha256"]
        for pool, vector in shard["vectors"].items():
            vector["sha256"] = sha256(self.root / vector["path"])
            commit["files"][f"{pool}.npy"] = vector["sha256"]
        self.write(commit_path, commit)
        shard["commit_sha256"] = sha256(commit_path)
        self.save_catalog()

    def test_all_rows_different_dimensions_and_read_only(self):
        blocks = list(self.reader().iter_aligned({"a": "cls", "b": "mean"}))
        self.assertEqual([len(meta) for meta, _ in blocks], [3, 2])
        for meta, arrays in blocks:
            self.assertIn("duplicate_text", meta.column_names)
            for key, array in arrays.items():
                np.testing.assert_array_equal(array[:, 0], meta["row_index"].to_numpy() + 1)
                self.assertEqual(array.shape[1], 3 if key == "a" else 2)
                with self.assertRaises(ValueError):
                    array[0, 0] = 0

    def test_filters_preserve_alignment_and_quality(self):
        blocks = list(self.reader().iter_aligned({"a": "cls", "b": "mean"},
                     cohorts=["extra"], field_ids=[2], periods=[2005]))
        self.assertEqual(blocks[0][0]["work_id"].to_pylist(), ["W4"])
        self.assertEqual(blocks[0][0]["duplicate_text"].to_pylist(), [True])
        self.assertEqual(float(blocks[0][1]["a"][0, 0]), 5.0)
        self.assertFalse(blocks[0][1]["a"].flags.writeable)
        self.assertEqual(list(self.reader().iter_aligned({"a": "cls"}, cohorts=[])), [])

    def test_invalid_selection_and_filter(self):
        for selection in ({}, {"a": None}, {"a": "mean"}, {"missing": "cls"}):
            with self.assertRaises(ValueError):
                list(self.reader().iter_aligned(selection))
        for filters in ({"cohorts": "base"}, {"cohorts": ["typo"]}, {"field_ids": [99]}):
            with self.assertRaises(ValueError):
                list(self.reader().iter_aligned({"a": "cls"}, **filters))

    def test_modified_file_rejected(self):
        with (self.root / "a/0/cls.npy").open("ab") as stream:
            stream.write(b"changed")
        with self.assertRaisesRegex(IntegrityError, "Changed file"):
            list(self.reader().iter_aligned({"a": "cls"}))

    def test_wrong_ids_rejected_even_with_matching_digests(self):
        path = self.root / "a/0/rows.parquet"
        pq.write_table(pq.read_table(path).take(pa.array([1, 0, 2])), path)
        self.refresh_shard_digests()
        with self.assertRaisesRegex(IntegrityError, "Paper alignment"):
            list(self.reader().iter_aligned({"a": "cls", "b": "mean"}))

    def test_gap_rejected(self):
        self.catalog["models"]["a"]["shards"][1]["start"] = 4
        self.save_catalog()
        with self.assertRaisesRegex(IntegrityError, "Gap"):
            list(self.reader().iter_aligned({"a": "cls"}))

    def test_invalid_vectors_rejected_with_matching_digests(self):
        cases = [np.ones((3, 2), dtype=np.float32), np.ones((3, 3), dtype=np.float64),
                 np.zeros((3, 3), dtype=np.float32), np.full((3, 3), np.nan, dtype=np.float32)]
        for array in cases:
            with self.subTest(shape=array.shape, dtype=array.dtype):
                np.save(self.root / "a/0/cls.npy", array)
                self.refresh_shard_digests()
                with self.assertRaises(IntegrityError):
                    list(self.reader().iter_aligned({"a": "cls"}))

    def test_changed_metadata_and_catalog_anchor_rejected(self):
        with self.assertRaisesRegex(IntegrityError, "Changed file"):
            EmbeddingCorpus(self.root, "catalog.json", catalog_sha256="incorrect")
        with (self.root / "metadata.parquet").open("ab") as stream:
            stream.write(b"changed")
        with self.assertRaisesRegex(IntegrityError, "Changed file"):
            self.reader()


if __name__ == "__main__":
    unittest.main()
