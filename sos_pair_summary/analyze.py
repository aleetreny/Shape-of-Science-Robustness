"""Summarize every Field pair without reading or recomputing embeddings."""
from __future__ import annotations

import csv
import hashlib
import itertools
import json
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/field_pair_summary_v1'
OUT = ROOT / 'reports/field_pair_summary_v1'
CONFIG = ROOT / 'config/field_pairs_v1.json'
CLASSES = ('unanimous', 'contradiction', 'unresolved')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
    temp.replace(path)


def save_csv(name, rows):
    assert rows, name
    path = OUT / (name + '.csv')
    columns = list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def relative_difference(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)) or np.any(a <= 0) or np.any(b <= 0):
        raise ValueError('Properties must be finite and strictly positive.')
    return 2.0 * (b - a) / (a + b)


def persistent_direction(values, minimum=0.0, tolerance=1e-10):
    """Last axis is the set of saved repetitions; zero means unresolved."""
    x = np.asarray(values, dtype=float)
    if x.ndim == 0 or x.shape[-1] == 0 or not np.all(np.isfinite(x)):
        raise ValueError('A nonempty finite set of repetitions is required.')
    if minimum < 0 or tolerance < 0:
        raise ValueError('Negative thresholds are not defined.')
    return np.where(np.min(x, axis=-1) > minimum + tolerance, 1,
                    np.where(np.max(x, axis=-1) < -minimum - tolerance, -1, 0)).astype(np.int8)


def classify(signs):
    """Last axis is the fixed model panel. No voting or significance test."""
    s = np.asarray(signs)
    if s.ndim == 0 or s.shape[-1] < 2 or not np.all(np.isin(s, [-1, 0, 1])):
        raise ValueError('At least two model directions in {-1,0,1} are required.')
    positive, negative = np.sum(s == 1, axis=-1), np.sum(s == -1, axis=-1)
    return np.where((positive == s.shape[-1]) | (negative == s.shape[-1]), 'unanimous',
                    np.where((positive > 0) & (negative > 0), 'contradiction', 'unresolved'))


def count_classes(signs):
    labels = classify(signs)
    result = {name: int(np.count_nonzero(labels == name)) for name in CLASSES}
    result['pairs'] = int(len(labels))
    result['models'] = int(np.asarray(signs).shape[-1])
    assert sum(result[k] for k in CLASSES) == result['pairs']
    return result


def main():
    cfg = read(CONFIG)
    source = ROOT / cfg['parent']
    prior = ROOT / 'data/morphology_pilot_v1'
    prior_audit = read(prior / 'audit.json')
    assert prior_audit['all_complete']
    for name, digest in prior_audit['files'].items():
        assert sha(prior / name) == digest, name
    source_paths = ['FIELD_PAIR_PROTOCOL.md', 'config/field_pairs_v1.json',
                    'sos_pair_summary/__init__.py', 'sos_pair_summary/analyze.py', 'sos_pair_summary/tests.py']
    parent_paths = [cfg['parent'], 'data/morphology_pilot_v1/audit.json',
                    'config/morphology_pilot_v1.json', 'reports/morphology_pilot_v1/primary_metrics.csv',
                    'reports/morphology_pilot_v1/catalog.json',
                    'research/morphology_2026-09-18/closure_audit.json',
                    'research/field_pair_summary_2026-09-18/baseline_documents/manifest.json']
    frozen = {'configuration': cfg, 'source_files': {p: sha(ROOT / p) for p in source_paths},
              'parent_files': {p: sha(ROOT / p) for p in parent_paths}}
    DATA.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path = DATA / 'manifest.json'
    if manifest_path.exists():
        assert read(manifest_path) == frozen, 'Frozen definition changed; use a new version.'
        if (DATA / 'audit.json').exists() and read(DATA / 'audit.json')['all_complete']:
            print('Summary already complete; no calculation repeated.')
            return
    else:
        write_json(manifest_path, frozen)
        for name in source_paths:
            target = DATA / 'source_snapshot' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / name).read_bytes())

    rows = pq.read_table(source).to_pylist()
    index = {(r['model'], r['kind'], r['field_id'], r['repeat'], r['n'], r['period']): r for r in rows}
    assert len(index) == len(rows) == 16884
    with (ROOT / 'reports/morphology_pilot_v1/primary_metrics.csv').open() as stream:
        names = {int(r['field_id']): r['field_name'] for r in csv.DictReader(stream)}
    fields = sorted(names)
    models = cfg['models']
    assert len(fields) == 26 and len(models) == 10
    pairs = list(itertools.combinations(fields, 2))
    assert len(pairs) == 325
    field_index = {f: i for i, f in enumerate(fields)}
    ia, ib = np.array([[field_index[a], field_index[b]] for a, b in pairs]).T
    pair_info = [{'field_a': a, 'field_b': b, 'field_a_name': names[a], 'field_b_name': names[b]}
                 for a, b in pairs]

    def get(model, kind, field, repeat=0):
        n = 2000 if kind in ['primary', 'external', 'common', 'common_native', 'minilm512'] else 950 if kind.startswith('trim_') else 1000
        if kind in ['size500', 'size4000']:
            n, kind = int(kind[4:]), 'size'
        return index[model, kind, field, repeat, n, 0]

    repeat_keys = [(kind, rep) for kind, reps in cfg['primary_repeats'].items() for rep in reps]
    assert len(repeat_keys) == 26
    # Identity alignment is checked from saved selection hashes, not assumed.
    for kind, repeat in repeat_keys:
        for field in fields:
            assert len({get(model, kind, field, repeat)['selection_sha256'] for model in models}) == 1

    metrics = cfg['primary_metrics']
    cubes, values_by_metric, metric_keys = {}, {}, {}
    all_metrics = list(dict.fromkeys(m for main in metrics for m in [main] + cfg['alternatives'][main]))
    for metric in all_metrics:
        keys = repeat_keys if metric not in ['erank', 'd80'] else [('primary', 0), ('half', 0), ('external', 0)]
        values = np.array([[[get(m, k, f, r)[metric] for k, r in keys] for f in fields] for m in models], dtype=float)
        assert np.all(np.isfinite(values)) and np.all(values > 0)
        values_by_metric[metric] = values
        cubes[metric] = relative_difference(values[:, ia, :], values[:, ib, :]).transpose(1, 0, 2)
        metric_keys[metric] = keys
    floors = cfg['minimum_relative_differences']
    tolerance = cfg['relative_tolerance']
    rules = {'all_saved': list(range(26)), 'primary_only': [0],
             'primary_and_half': list(range(21)), 'primary_and_external': [0] + list(range(21, 26))}
    baseline_signs = {metric: persistent_direction(cubes[metric], tolerance=tolerance) for metric in metrics}
    summaries, sensitivities = [], []
    for metric in metrics:
        for rule, selected in rules.items():
            for floor in floors:
                directions = persistent_direction(cubes[metric][:, :, selected], floor, tolerance)
                summaries.append({'metric': metric, 'rule': rule, 'minimum_relative_difference': floor,
                                  'observations_per_model_pair': len(selected), **count_classes(directions)})
                labels = classify(directions)
                for i, info in enumerate(pair_info):
                    sensitivities.append({'metric': metric, 'rule': rule, 'minimum_relative_difference': floor,
                        'field_a': info['field_a'], 'field_b': info['field_b'], 'class': str(labels[i]),
                        'positive_models': int(np.sum(directions[i] == 1)), 'negative_models': int(np.sum(directions[i] == -1)),
                        'unresolved_models': int(np.sum(directions[i] == 0))})
    save_csv('classification_summary', summaries)
    save_csv('pair_sensitivity', sensitivities)

    alternative_signs, alternative_rows = {}, []
    alternative_summary = []
    for metric, cube in cubes.items():
        directions = persistent_direction(cube, tolerance=tolerance)
        alternative_signs[metric] = directions
        alternative_summary.append({'metric': metric, 'saved_conditions': len(metric_keys[metric]), **count_classes(directions)})
    save_csv('alternative_metric_summary', alternative_summary)
    joint_signs = {}
    for metric in metrics:
        s = baseline_signs[metric]
        valid = np.ones_like(s, dtype=bool)
        for alt in cfg['alternatives'][metric]:
            valid &= (alternative_signs[alt] == s)
        joint_signs[metric] = np.where(valid, s, 0)
        labels = classify(joint_signs[metric])
        for i, info in enumerate(pair_info):
            alternative_rows.append({'metric': metric, **info, 'class': str(labels[i]),
                'positive_models': int(np.sum(joint_signs[metric][i] == 1)),
                'negative_models': int(np.sum(joint_signs[metric][i] == -1)),
                'unresolved_models': int(np.sum(joint_signs[metric][i] == 0)),
                'alternative_conditions': 26 if metric == 'angle_p50' else 3})
    save_csv('alternative_support', alternative_rows)

    # Individual model decisions retain effect magnitudes and all repeat ranges.
    model_rows, pair_rows, field_rows, witness_rows, example_rows = [], [], [], [], []
    for metric in metrics:
        cube, signs = cubes[metric], baseline_signs[metric]
        labels = classify(signs)
        joint_labels = classify(joint_signs[metric])
        point_labels = classify(persistent_direction(cube[:, :, :1], tolerance=tolerance))
        strict5 = persistent_direction(cube, .05, tolerance)
        raw_values = values_by_metric[metric]
        for i, info in enumerate(pair_info):
            positive = [models[j] for j in range(10) if signs[i, j] == 1]
            negative = [models[j] for j in range(10) if signs[i, j] == -1]
            unresolved = [models[j] for j in range(10) if signs[i, j] == 0]
            pair_rows.append({'metric': metric, **info, 'class': str(labels[i]),
                'positive_count': len(positive), 'negative_count': len(negative), 'unresolved_count': len(unresolved),
                'positive_models': '|'.join(positive), 'negative_models': '|'.join(negative), 'unresolved_models': '|'.join(unresolved),
                'opposing_model_pairs': len(positive) * len(negative), 'total_model_pairs': 45,
                'primary_point_class': str(point_labels[i]), 'minimum5pct_class': str(classify(strict5[i])),
                'all_alternatives_class': str(joint_labels[i]),
                'median_absolute_primary_relative_difference': float(np.median(np.abs(cube[i, :, 0]))),
                'minimum_primary_relative_difference': float(cube[i, :, 0].min()),
                'maximum_primary_relative_difference': float(cube[i, :, 0].max())})
            for j, model in enumerate(models):
                x = cube[i, j]
                va, vb = raw_values[j, ia[i], 0], raw_values[j, ib[i], 0]
                record = {'metric': metric, 'model': model, **info, 'value_a': float(va), 'value_b': float(vb),
                    'raw_difference_b_minus_a': float(vb - va), 'relative_difference_primary': float(x[0]),
                    'relative_min': float(x.min()), 'relative_max': float(x.max()),
                    'relative_q05': float(np.quantile(x, .05)), 'relative_q95': float(np.quantile(x, .95)),
                    'half_min': float(x[1:21].min()), 'half_max': float(x[1:21].max()),
                    'external_min': float(x[21:].min()), 'external_max': float(x[21:].max()),
                    'positive_repetitions': int(np.sum(x[1:] > tolerance)), 'negative_repetitions': int(np.sum(x[1:] < -tolerance)),
                    'direction': int(signs[i, j]), 'direction_and_alternatives': int(joint_signs[metric][i, j])}
                record.update({f'direction_minimum_{floor:g}': int(persistent_direction(x, floor, tolerance)) for floor in floors})
                model_rows.append(record)
                if info['field_a'] == 12 and info['field_b'] == 27:
                    example_rows.append(record)
        for field in fields:
            pick = np.array([field in p for p in pairs])
            field_rows.append({'metric': metric, 'field_id': field, 'field_name': names[field],
                **count_classes(signs[pick]), 'contradiction_minimum5pct': count_classes(strict5[pick])['contradiction'],
                'contradiction_and_alternatives': count_classes(joint_signs[metric][pick])['contradiction']})
        for j, k in itertools.combinations(range(10), 2):
            witness_rows.append({'metric': metric, 'model_a': models[j], 'model_b': models[k], 'field_pairs': 325,
                'opposite_persistent': int(np.sum(signs[:, j] * signs[:, k] == -1)),
                'opposite_minimum5pct': int(np.sum(strict5[:, j] * strict5[:, k] == -1)),
                'opposite_and_alternatives': int(np.sum(joint_signs[metric][:, j] * joint_signs[metric][:, k] == -1))})
    for name, output in [('model_pair_directions', model_rows), ('pair_summary', pair_rows),
                         ('field_summary', field_rows), ('model_pair_witnesses', witness_rows), ('example_art_medicine', example_rows)]:
        save_csv(name, output)

    panel_rows = []
    panels = {'all_ten': models, 'six_similarity': cfg['similarity_models']}
    panels.update({'omit_' + model: [m for m in models if m != model] for model in models})
    for metric in metrics:
        for panel, selected_models in panels.items():
            ix = [models.index(m) for m in selected_models]
            for floor in floors:
                s = persistent_direction(cubes[metric][:, ix, :], floor, tolerance)
                joint = np.where(joint_signs[metric][:, ix] == s, s, 0)
                panel_rows.append({'metric': metric, 'panel': panel, 'minimum_relative_difference': floor,
                    **count_classes(s), 'contradiction_and_alternatives': count_classes(joint)['contradiction'],
                    'unanimous_and_alternatives': count_classes(joint)['unanimous']})
    save_csv('model_panel_summary', panel_rows)

    control_rows, control_details = [], []
    control_alignment_checks = 0
    for spec in cfg['controls']:
        condition, reference = spec['condition'], spec['reference']
        affected = cfg['word_bert_models'] if condition.startswith('pool_') else ['minilm'] if condition == 'minilm512' else models
        affected_ix = [models.index(m) for m in affected]
        for metric in metrics:
            ref_values, new_values = [], []
            for model in models:
                new_kind = condition if model in affected else reference
                rr, nn = [], []
                for field in fields:
                    a, b = get(model, reference, field), get(model, new_kind, field)
                    if not condition.startswith('size'):
                        assert a['n'] == b['n']
                    if condition not in ['quality', 'trim_extreme', 'size500', 'size4000']:
                        assert a['selection_sha256'] == b['selection_sha256']
                    control_alignment_checks += 1
                    rr.append(a[metric]); nn.append(b[metric])
                ref_values.append(rr); new_values.append(nn)
            ref_values, new_values = np.array(ref_values), np.array(new_values)
            ref_diff = relative_difference(ref_values[:, ia], ref_values[:, ib]).T
            new_diff = relative_difference(new_values[:, ia], new_values[:, ib]).T
            for floor in floors:
                reference_sign = persistent_direction(ref_diff[:, :, None], floor, tolerance)
                new_sign = persistent_direction(new_diff[:, :, None], floor, tolerance)
                stable = persistent_direction(cubes[metric], floor, tolerance)
                # Same model witnesses must keep their original direction in
                # both matched reference and changed condition.
                baseline_witnesses = np.where(reference_sign == stable, stable, 0)
                retained_witnesses = np.where(new_sign == baseline_witnesses, baseline_witnesses, 0)
                before, after = classify(reference_sign), classify(new_sign)
                baseline_witness_class, retained_class = classify(baseline_witnesses), classify(retained_witnesses)
                flips = reference_sign[:, affected_ix] * new_sign[:, affected_ix] == -1
                control_rows.append({'metric': metric, 'condition': condition, 'reference': reference,
                    'minimum_relative_difference': floor, 'affected_models': len(affected), 'field_pairs': 325,
                    **{'reference_' + k: v for k, v in count_classes(reference_sign).items() if k in CLASSES},
                    **{'changed_' + k: v for k, v in count_classes(new_sign).items() if k in CLASSES},
                    'model_direction_flips': int(flips.sum()), 'affected_model_comparisons': 325 * len(affected),
                    'pair_class_changes': int(np.sum(before != after)),
                    'original_persistent_contradictions': count_classes(stable)['contradiction'],
                    'reference_supported_original_contradictions': int(np.sum(baseline_witness_class == 'contradiction')),
                    'same_original_witness_pair_retained': int(np.sum(retained_class == 'contradiction')),
                    'original_unanimous_retained_by_every_model': int(np.sum((classify(stable) == 'unanimous') & np.all(reference_sign == stable, axis=1) & np.all(new_sign == stable, axis=1)))})
                if floor == 0:
                    for i, info in enumerate(pair_info):
                        control_details.append({'metric': metric, 'condition': condition, 'reference': reference,
                            'field_a': info['field_a'], 'field_b': info['field_b'],
                            'reference_class': str(before[i]), 'changed_class': str(after[i]),
                            'affected_model_direction_flips': int(flips[i].sum()),
                            'original_contradiction_supported_in_reference': bool(baseline_witness_class[i] == 'contradiction'),
                            'same_original_witness_pair_retained': bool(retained_class[i] == 'contradiction')})
    save_csv('control_summary', control_rows); save_csv('control_pairs', control_details)

    # Save exact repeat contrasts in a compact local array, outside version control.
    arrays = {metric: cube for metric, cube in cubes.items()}
    np.savez_compressed(DATA / 'contrasts.npz', **arrays)
    write_json(DATA / 'contrast_index.json', {'pairs': pairs, 'models': models,
                'metrics': {m: {'keys': metric_keys[m], 'shape': list(cubes[m].shape)} for m in cubes},
                'axis_order': ['field_pair', 'model', 'saved_condition']})
    details = {
        'created_at': datetime.now(timezone.utc).isoformat(), 'field_pairs': 325, 'primary_metrics': metrics,
        'models': models, 'main': [r for r in summaries if r['rule'] == 'all_saved' and r['minimum_relative_difference'] == 0],
        'minimum5pct': [r for r in summaries if r['rule'] == 'all_saved' and r['minimum_relative_difference'] == .05],
        'alternatives_joint': {m: count_classes(joint_signs[m]) for m in metrics},
        'six_similarity': [r for r in panel_rows if r['panel'] == 'six_similarity' and r['minimum_relative_difference'] == 0],
        'controls': [r for r in control_rows if r['minimum_relative_difference'] == 0],
        'limitations': ['Fixed non-independent model panel and overlapping Field pairs.',
                        'Sample ranges are not population confidence intervals.',
                        'Point controls have no repeated-sampling certification.',
                        'No semantic correctness or number of topics follows from agreement.',
                        'Post-pilot exploratory summary; no new inference or morphology measurement.']}
    write_json(OUT / 'summary.json', details)
    files = {str(p.relative_to(ROOT)): sha(p) for p in sorted(OUT.glob('*.csv'))}
    for name in ['manifest.json', 'contrasts.npz', 'contrast_index.json']:
        files[str((DATA / name).relative_to(ROOT))] = sha(DATA / name)
    files['reports/field_pair_summary_v1/summary.json'] = sha(OUT / 'summary.json')
    write_json(DATA / 'audit.json', {'all_complete': True, 'created_at': datetime.now(timezone.utc).isoformat(),
        'pairs_per_property': 325, 'properties': 2, 'primary_model_pair_decisions': 6500,
        'saved_main_conditions': 26, 'control_alignment_checks': control_alignment_checks,
        'csv_tables': len(list(OUT.glob('*.csv'))), 'files': files,
        'no_new_inference': True, 'prior_files_unchanged': all(sha(ROOT / n) == h for n, h in frozen['parent_files'].items())})
    assert read(DATA / 'audit.json')['prior_files_unchanged']
    print(json.dumps({k: details[k] for k in ['main', 'minimum5pct', 'alternatives_joint', 'six_similarity']}, indent=2))


if __name__ == '__main__':
    main()
