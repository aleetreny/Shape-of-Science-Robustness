"""Recompute persistent Field-pair classifications from saved per-condition values.

Only the Python standard library is used. This reproduces the aggregation in
Figure 4, not the upstream embeddings or geometric measurements.
"""
import argparse
import collections
import csv
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOLERANCE = 1e-10


def sign(values, cutoff):
    if all(v > cutoff + TOLERANCE for v in values):
        return 1
    if all(v < -cutoff - TOLERANCE for v in values):
        return -1
    return 0


def label(signs):
    if all(s == 1 for s in signs) or all(s == -1 for s in signs):
        return 'unanimous'
    if 1 in signs and -1 in signs:
        return 'contradiction'
    return 'unresolved'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    provenance = json.loads((HERE / 'provenance.json').read_text())
    compressed = (HERE / 'metrics.csv.gz').read_bytes()
    if hashlib.sha256(compressed).hexdigest() != provenance['csv_gz_sha256']:
        raise ValueError('Input checksum does not match the frozen export.')
    with gzip.open(HERE / 'metrics.csv.gz', 'rt', newline='') as f:
        rows = list(csv.DictReader(f))
    models = sorted({r['model'] for r in rows})
    fields = sorted({int(r['field_id']) for r in rows})
    conditions = sorted({(r['kind'], int(r['repeat']), int(r['n'])) for r in rows})
    assert len(rows) == 13520 and len(models) == 10 and len(fields) == 26
    assert len(conditions) == 26
    assert collections.Counter(c[0] for c in conditions) == {'primary': 1, 'half': 20, 'external': 5}
    index = {(r['representation'], r['model'], int(r['field_id']),
              r['kind'], int(r['repeat']), int(r['n'])): r for r in rows}
    assert len(index) == len(rows), 'Duplicate condition.'
    for model, field, condition in itertools.product(models, fields, conditions):
        a = index[('original', model, field, *condition)]
        b = index[('global_centered', model, field, *condition)]
        assert a['selection_sha256'] == b['selection_sha256']
    pairs = list(itertools.combinations(fields, 2))
    signs = {}
    counts = []
    for representation, metric, cutoff in itertools.product(
            ['original', 'global_centered'], ['angle_p50', 'pr'], [0.0, 0.05]):
        all_signs = []
        for a, b in pairs:
            per_model = []
            for model in models:
                differences = []
                for condition in conditions:
                    x = float(index[(representation, model, a, *condition)][metric])
                    y = float(index[(representation, model, b, *condition)][metric])
                    assert math.isfinite(x) and math.isfinite(y) and min(x, y) > 0
                    differences.append(2.0 * (y - x) / (x + y))
                per_model.append(sign(differences, cutoff))
            all_signs.append(per_model)
        signs[(representation, metric, cutoff)] = all_signs
        c = collections.Counter(map(label, all_signs))
        counts.append({'representation': representation, 'metric': metric,
                       'cutoff': cutoff, **{k: c[k] for k in
                       ['unanimous', 'contradiction', 'unresolved']}})
    retained = []
    for metric in ['angle_p50', 'pr']:
        old = signs[('original', metric, 0.0)]
        new = signs[('global_centered', metric, 0.0)]
        same_class = same_witness = new_oppositions = 0
        for a, b in zip(old, new):
            same_class += label(a) == label(b) == 'contradiction'
            stable = [x if x == y else 0 for x, y in zip(a, b)]
            same_witness += label(stable) == 'contradiction'
            new_oppositions += label(a) != 'contradiction' and label(b) == 'contradiction'
        retained.append({'metric': metric, 'retained_opposition_class': same_class,
                         'same_fixed_witness_directions_retained': same_witness,
                         'new_oppositions': new_oppositions})
    result = {'models': len(models), 'fields': len(fields), 'pairs': len(pairs),
              'conditions': len(conditions), 'counts': counts, 'centering_retention': retained}
    expected = json.loads((HERE / 'expected.json').read_text())
    if result != expected:
        raise AssertionError('Recomputed results differ from the frozen publication summaries.')
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print('PASS: 8 classifications of 325 pairs and 2 model-witness retention checks.')
    print('Recomputed from 13,520 measurements; no network or project imports.')


if __name__ == '__main__':
    main()
