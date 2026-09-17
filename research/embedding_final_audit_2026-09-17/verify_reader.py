"""Read every saved variant using the new reader; compute no science metrics."""
from collections import Counter
import datetime
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from sos_analysis import EmbeddingCorpus


def main():
    here = Path(__file__).resolve().parent
    audit = json.loads((here / "audit_summary.json").read_text())
    reader = EmbeddingCorpus(ROOT, catalog_sha256=audit["catalog_sha256"])
    models = reader.catalog["models"]
    # These three passes cover all 18 existing outputs. No primary recipe is chosen.
    groups = [{key: spec["poolings"][i] for key, spec in models.items()
               if len(spec["poolings"]) > i} for i in range(3)]
    results = []
    started = time.monotonic()
    for selection in groups:
        count = 0
        cohorts = Counter()
        blocks = 0
        for metadata, arrays in reader.iter_aligned(selection):
            assert metadata["row_index"][0].as_py() == count
            count += len(metadata)
            cohorts.update(metadata["cohort"].to_pylist())
            assert all(len(a) == len(metadata) for a in arrays.values())
            blocks += 1
        assert count == 500000 and cohorts == {"base": 400000, "extra": 100000}
        results.append({"selections_for_io_check_only": selection, "rows": count,
                        "cohorts": dict(cohorts), "blocks": blocks})
        print("Lectura comprobada:", selection, count, flush=True)
    result = {"verified": True, "completed_at": datetime.datetime.now(datetime.UTC).isoformat(),
              "variants_read": sum(len(g) for g in groups), "passes": results,
              "seconds": time.monotonic() - started,
              "max_resident_memory_bytes_macos": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "scientific_metrics_computed": False, "source_files_modified": False}
    (here / "reader_verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
