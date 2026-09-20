"""Independent ratio-based verification against saved morphology values."""
import csv
import hashlib
import itertools
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/field_pair_summary_v1'
OUT = ROOT / 'reports/field_pair_summary_v1'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def csv_rows(name):
    with (OUT / (name + '.csv')).open() as f:
        return list(csv.DictReader(f))


def label(signs):
    unique = set(signs)
    if unique in ({1}, {-1}): return 'unanimous'
    if 1 in unique and -1 in unique: return 'contradiction'
    return 'unresolved'


def main():
    cfg = load(ROOT / 'config/field_pairs_v1.json')
    audit = load(DATA / 'audit.json')
    assert audit['all_complete']
    for name, expected in audit['files'].items():
        assert digest(ROOT / name) == expected, name
    frozen = load(DATA / 'manifest.json')
    for name, expected in frozen['source_files'].items():
        assert digest(ROOT / name) == digest(DATA / 'source_snapshot' / name) == expected, name
    for name, expected in frozen['parent_files'].items():
        assert digest(ROOT / name) == expected, name
    old_manifest = load(ROOT / 'data/morphology_pilot_v1/manifest.json')
    for name, expected in old_manifest['source_files'].items():
        assert digest(ROOT / name) == expected, name
    preserved = ROOT / 'research/field_pair_summary_2026-09-18/baseline_documents'
    baseline = load(preserved / 'manifest.json')
    for name, expected in baseline['files'].items():
        assert digest(preserved / name) == expected, name
    assert digest(ROOT / baseline['preceding_closure']) == baseline['preceding_closure_sha256']

    raw = pq.read_table(ROOT / cfg['parent']).to_pylist()
    r = {(x['model'], x['kind'], x['field_id'], x['repeat'], x['n']): x for x in raw if x['period'] == 0}
    models = cfg['models']
    fields = sorted({x['field_id'] for x in raw if x['kind'] == 'primary'})
    pairs = list(itertools.combinations(fields, 2))
    assert len(pairs) == 325
    assert len(csv_rows('pair_summary')) == 650

    def value(model, field, kind, repeat, metric):
        n = 2000 if kind in ['primary', 'external', 'common', 'common_native', 'minilm512'] else 950 if kind.startswith('trim_') else 1000
        if kind.startswith('size'):
            n, kind = int(kind[4:]), 'size'
        return r[model, kind, field, repeat, n][metric]

    keys = [('primary', 0)] + [('half', i) for i in range(20)] + [('external', i) for i in range(5)]
    rules = {'all_saved': keys, 'primary_only': keys[:1],
             'primary_and_half': keys[:21], 'primary_and_external': keys[:1] + keys[21:]}

    def direction(model, a, b, metric, selected, floor=0.):
        # Independent algebra: contrast > t iff B/A > (2+t)/(2-t).
        t = floor + cfg['relative_tolerance']
        cutoff = (2 + t) / (2 - t)
        ratios = [value(model, b, k, rep, metric) / value(model, a, k, rep, metric) for k, rep in selected]
        if min(ratios) > cutoff: return 1
        if max(ratios) < 1 / cutoff: return -1
        return 0

    computed = {}
    for metric in cfg['primary_metrics']:
        for a, b in pairs:
            for model in models:
                for rule, selected in rules.items():
                    for floor in cfg['minimum_relative_differences']:
                        computed[metric, a, b, model, rule, floor] = direction(model, a, b, metric, selected, floor)
    sensitivity_rows = csv_rows('pair_sensitivity')
    assert len(sensitivity_rows) == 10400
    for row in sensitivity_rows:
        metric, a, b = row['metric'], int(row['field_a']), int(row['field_b'])
        signs = [computed[metric, a, b, model, row['rule'], float(row['minimum_relative_difference'])] for model in models]
        assert label(signs) == row['class']
        assert signs.count(1) == int(row['positive_models']) and signs.count(-1) == int(row['negative_models'])
    for row in csv_rows('classification_summary'):
        selected_rows = [x for x in sensitivity_rows if all(x[k] == row[k] for k in ['metric', 'rule', 'minimum_relative_difference'])]
        assert len(selected_rows) == 325
        for cls in ['unanimous', 'contradiction', 'unresolved']:
            assert sum(x['class'] == cls for x in selected_rows) == int(row[cls])
    detail_rows = csv_rows('model_pair_directions')
    assert len(detail_rows) == 6500
    max_error = 0.
    for row in detail_rows:
        m, metric, a, b = row['model'], row['metric'], int(row['field_a']), int(row['field_b'])
        va, vb = value(m, a, 'primary', 0, metric), value(m, b, 'primary', 0, metric)
        max_error = max(max_error, abs(vb - va - float(row['raw_difference_b_minus_a'])))
        assert int(row['direction']) == computed[metric, a, b, m, 'all_saved', 0.]
        for floor in cfg['minimum_relative_differences']:
            assert int(row[f'direction_minimum_{floor:g}']) == computed[metric, a, b, m, 'all_saved', floor]
    assert max_error < 1e-12

    joint = {}
    for metric in cfg['primary_metrics']:
        for a, b in pairs:
            for m in models:
                s = computed[metric, a, b, m, 'all_saved', 0.]
                for alternative in cfg['alternatives'][metric]:
                    alt_keys = keys if metric == 'angle_p50' else [('primary', 0), ('half', 0), ('external', 0)]
                    if direction(m, a, b, alternative, alt_keys) != s: s = 0
                joint[metric, a, b, m] = s
    for row in csv_rows('alternative_support'):
        metric, a, b = row['metric'], int(row['field_a']), int(row['field_b'])
        assert label([joint[metric, a, b, m] for m in models]) == row['class']

    control_by_key = {(x['metric'], x['condition'], int(x['field_a']), int(x['field_b'])): x for x in csv_rows('control_pairs')}
    controls_checked = 0
    for spec in cfg['controls']:
        condition, reference = spec['condition'], spec['reference']
        affected = cfg['word_bert_models'] if condition.startswith('pool_') else ['minilm'] if condition == 'minilm512' else models
        for metric in cfg['primary_metrics']:
            for a, b in pairs:
                before, after, supported, retained = [], [], [], []
                for m in models:
                    s = computed[metric, a, b, m, 'all_saved', 0.]
                    bs = direction(m, a, b, metric, [(reference, 0)])
                    cs = direction(m, a, b, metric, [(condition if m in affected else reference, 0)])
                    before.append(bs); after.append(cs)
                    supported.append(s if bs == s else 0)
                    retained.append(s if bs == s and cs == s else 0)
                row = control_by_key[metric, condition, a, b]
                assert row['reference_class'] == label(before) and row['changed_class'] == label(after)
                assert (row['original_contradiction_supported_in_reference'] == 'True') == (label(supported) == 'contradiction')
                assert (row['same_original_witness_pair_retained'] == 'True') == (label(retained) == 'contradiction')
                flips = sum(before[models.index(m)] * after[models.index(m)] == -1 for m in affected)
                assert int(row['affected_model_direction_flips']) == flips
                controls_checked += 1
    assert controls_checked == 7150
    for row in csv_rows('model_panel_summary'):
        members = models if row['panel'] == 'all_ten' else cfg['similarity_models'] if row['panel'] == 'six_similarity' else [m for m in models if m != row['panel'][5:]]
        metric, floor = row['metric'], float(row['minimum_relative_difference'])
        labels = [label([computed[metric, a, b, m, 'all_saved', floor] for m in members]) for a, b in pairs]
        for cls in ['unanimous', 'contradiction', 'unresolved']: assert int(row[cls]) == labels.count(cls)

    # Check all stored contrasts against original values and saved axis metadata.
    ix = load(DATA / 'contrast_index.json')
    with np.load(DATA / 'contrasts.npz', allow_pickle=False) as arrays:
        contrast_values_checked = 0
        for metric in arrays.files:
            arr = arrays[metric]
            assert arr.shape == tuple(ix['metrics'][metric]['shape'])
            for j, m in enumerate(models):
                for k, (kind, rep) in enumerate(ix['metrics'][metric]['keys']):
                    va = np.array([value(m, a, kind, rep, metric) for a, b in pairs])
                    vb = np.array([value(m, b, kind, rep, metric) for a, b in pairs])
                    expected = (vb - va) / ((va + vb) / 2.)
                    np.testing.assert_allclose(arr[:, j, k], expected, atol=1e-12, rtol=0)
                    contrast_values_checked += len(pairs)
    result = {'all_complete': True, 'created_at': datetime.now(timezone.utc).isoformat(),
        'field_pairs': 325, 'properties': 2, 'sensitivity_pair_rows_verified': 10400,
        'model_pair_rows_verified': 6500, 'control_pair_rows_verified': controls_checked,
        'contrast_values_verified': contrast_values_checked, 'baseline_documents_verified': len(baseline['files']),
        'alternative_same_model_witnesses_verified': True, 'panel_summaries_verified': 96,
        'raw_difference_max_error': max_error, 'prior_sources_and_results_unchanged': True,
        'source_sha256': digest(Path(__file__)), 'data_audit_sha256': digest(DATA / 'audit.json'),
        'scope': 'Independent ratio-based arithmetic and complete record reconciliation, not semantic validation.'}
    (DATA / 'independent_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
