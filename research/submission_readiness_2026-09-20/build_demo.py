"""Export a small, local, numeric-only reproduction example; no publication."""
from pathlib import Path
import csv
import gzip
import hashlib
import io
import json
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = HERE / 'replication_demo'
source = ROOT / 'data/robustness_closure_v1/morphology/metrics.parquet'
table = pq.read_table(source)
stream = io.StringIO(newline='')
writer = csv.DictWriter(stream, fieldnames=table.column_names)
writer.writeheader()
writer.writerows(table.to_pylist())
compressed = gzip.compress(stream.getvalue().encode(), mtime=0)
(OUT / 'metrics.csv.gz').write_bytes(compressed)

def csv_rows(name):
    with (ROOT / 'reports/robustness_closure_v1' / name).open() as f:
        return list(csv.DictReader(f))

source_counts = csv_rows('morphology_classification.csv')
counts = []
for representation in ['original', 'global_centered']:
    for metric in ['angle_p50', 'pr']:
        for cutoff in [0.0, 0.05]:
            matches = [r for r in source_counts if r['representation'] == representation
                       and r['metric'] == metric and float(r['cutoff']) == cutoff]
            assert len(matches) == 1
            r = matches[0]
            counts.append({'representation': representation, 'metric': metric,
                           'cutoff': cutoff, **{k: int(r[k]) for k in
                           ['unanimous', 'contradiction', 'unresolved']}})
retention = []
for metric in ['angle_p50', 'pr']:
    r, = [r for r in csv_rows('morphology_centering_summary.csv')
          if r['metric'] == metric and float(r['cutoff']) == 0.0]
    retention.append({'metric': metric, **{k: int(r[k]) for k in
                      ['retained_opposition_class', 'same_fixed_witness_directions_retained',
                       'new_oppositions']}})
expected = {'models': 10, 'fields': 26, 'pairs': 325, 'conditions': 26,
            'counts': counts, 'centering_retention': retention}
(OUT / 'expected.json').write_text(json.dumps(expected, indent=2) + '\n')
provenance = {
    'source_path': source.relative_to(ROOT).as_posix(),
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'csv_gz_sha256': hashlib.sha256(compressed).hexdigest(),
    'rows': table.num_rows, 'columns': table.column_names,
    'scope': 'Saved measurements to pairwise classifications; not embeddings to measurements.',
    'scientific_rules': 'Existing protocol: all 26 conditions, cutoff plus 1e-10 tolerance.',
    'status': 'Local preparation, no license selected and no public deposit.',
    'expected_results_sources': {
        name: hashlib.sha256((ROOT / 'reports/robustness_closure_v1' / name).read_bytes()).hexdigest()
        for name in ['morphology_classification.csv', 'morphology_centering_summary.csv']
    },
}
(OUT / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
