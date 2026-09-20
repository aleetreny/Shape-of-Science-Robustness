"""Check the pilot delivery without recomputing scientific results.

Run from the repository with .venv-analysis/bin/python. This verifies local
artifacts and recorded mathematical/visual checks; it is not semantic validation.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from urllib.parse import unquote, urlsplit

import numpy as np
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = Path(__file__).resolve().parent
DATA = ROOT / 'data/morphology_pilot_v1'
REPORT = ROOT / 'reports/morphology_pilot_v1'


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path):
    return json.loads(path.read_text())


def table(name: str):
    with (REPORT / (name + '.csv')).open(newline='') as stream:
        return list(csv.DictReader(stream))


def git(*args: str) -> bytes:
    return subprocess.check_output(['git', *args], cwd=ROOT)


def main():
    audit = read(DATA / 'audit.json')
    assert audit['all_complete'] and audit['rows'] == 16884
    assert len(audit['counts']) == 30 and sum(audit['counts'].values()) == 16884
    for name, digest in audit['files'].items():
        assert sha(DATA / name) == digest, name
    manifest = read(DATA / 'manifest.json')
    for name, digest in manifest['source_files'].items():
        assert sha(ROOT / name) == digest, name
        assert sha(DATA / 'source_snapshot' / name) == digest, name
    for name, digest in manifest['parent_files'].items():
        assert sha(ROOT / name) == digest, name
    executor = read(DATA / 'execution_manifest.json')
    assert executor['unchanged_scientific_manifest'] == sha(DATA / 'manifest.json')
    for parent in (ROOT, DATA / 'source_snapshot'):
        assert sha(parent / executor['source']) == executor['source_sha256']

    independent = read(DATA / 'independent_audit.json')
    assert independent['all_complete'] and independent['invalid_inputs_rejected'] == 3
    assert independent['source_sha256'] == sha(ROOT / 'sos_morphology/independent_audit.py')
    assert len(independent['real_128_checks']) == 6
    assert len(independent['real_2000_checks']) == 3
    errors = [e for row in independent['real_128_checks'] for e in row['max_errors'].values()]
    errors += [row['padding_error'] for row in independent['real_128_checks']]
    errors += [e for row in independent['real_2000_checks'] for e in row['errors'].values()]
    assert max(errors) < 1e-8
    synthetic = read(DATA / 'synthetic/audit.json')
    assert synthetic['all_checks_passed'] and synthetic['clouds'] == 9
    assert synthetic['reference_clouds'] == 15
    with np.load(DATA / 'selections.npz', allow_pickle=False) as selections:
        assert len(selections.files) == 1406

    catalog = read(REPORT / 'catalog.json')
    assert catalog['export_source_sha256'] == sha(ROOT / 'sos_morphology/report.py')
    assert catalog['source_audit_sha256'] == sha(DATA / 'audit.json')
    assert len(catalog['files']) == 36
    for name, digest in catalog['files'].items():
        assert sha(REPORT / name) == digest, name
    assert len(list(REPORT.glob('*.csv'))) == 20
    assert all(len(list(REPORT.glob('*.' + ext))) == 5 for ext in ['png', 'pdf', 'svg'])
    visual = read(RESEARCH / 'visual_review.json')
    assert visual['all_five_inspected'] and len(visual['files']) == 5
    for name, record in visual['files'].items():
        assert sha(REPORT / name) == record['sha256'], name

    # Reconcile delivery cells and central claims with stored numeric outputs.
    rows = pq.read_table(DATA / 'metrics.parquet').to_pylist()
    assert len(rows) == 16884
    primary = {(r['model'], str(r['field_id'])): r for r in rows if r['kind'] == 'primary'}
    assert len(primary) == 260
    csv_primary = table('primary_metrics')
    assert len(csv_primary) == 260
    for row in csv_primary:
        source = primary[(row['model'], row['field_id'])]
        assert int(row['n']) == source['n'] == 2000
        assert row['selection_sha256'] == source['selection_sha256']
        for key in ['angle_p50', 'pr', 'gap_25']:
            assert abs(float(row[key]) - source[key]) < 1e-12
        assert all(int(row[f'union_components_{k}']) == 1 for k in [10, 25, 50])
    stability = table('selection_stability')
    passed = {}
    for kind, metric, expected in [('half', 'angle_p50', 260), ('half', 'pr', 256),
                                  ('external', 'angle_p50', 260), ('external', 'pr', 260),
                                  ('external', 'gap_25', 209)]:
        subset = [r for r in stability if r['kind'] == kind and r['metric'] == metric]
        assert len(subset) == 260
        count = sum(r['passes_both'] == 'True' for r in subset)
        assert count == expected, (kind, metric, count)
        passed[f'{kind}/{metric}'] = count
    for row in table('illustrative_reversal'):
        sign = 1 if row['model'] == 'specter' else -1
        assert float(row['medicine_minus_arts']) * sign > 0
        if row['metric'] == 'angle_p50':
            assert row['half_same_direction_count'] == row['half_total'] == '20'
            assert row['external_same_direction_count'] == row['external_total'] == '5'
    between = table('between_model_field_ranks')
    for key, expected in [('angle_p50', .31897435897435894), ('pr', .5521367521367521),
                          ('gap_25', .7135042735042735)]:
        values = [float(r['field_rank_spearman']) for r in between if r['metric'] == key]
        assert len(values) == 45 and abs(median(values) - expected) < 1e-12

    # Retain the preceding delivery exactly, including documents changed here.
    baseline = read(RESEARCH / 'baseline_documents/manifest.json')
    assert len(baseline['files']) == 15
    for name, digest in baseline['files'].items():
        assert sha(RESEARCH / 'baseline_documents' / name) == digest, name
        assert hashlib.sha256(git('show', baseline['commit'] + ':' + name)).hexdigest() == digest
    changed = git('diff', '--name-only', baseline['commit']).decode().splitlines()
    allowed_new = {'MORPHOLOGY_PROTOCOL.md', 'MORPHOLOGY_RESULTS.md', 'METHODS_MORPHOLOGY.md',
                   'config/morphology_pilot_v1.json'}
    new_prefixes = ('sos_morphology/', 'reports/morphology_pilot_v1/', 'research/morphology_2026-09-18/')
    unexpected = [n for n in changed if n not in baseline['files'] and n not in allowed_new
                  and not n.startswith(new_prefixes)]
    assert not unexpected, unexpected
    ignored = subprocess.run(['git', 'check-ignore', '-q', 'data/morphology_pilot_v1/metrics.parquet'],
                             cwd=ROOT).returncode == 0
    assert ignored
    subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)

    bib = read(RESEARCH / 'bibliography_validation.json')
    assert bib['total_entries'] == bib['valid_entries'] == 54
    assert not bib['errors'] and not bib['duplicates'] and len(bib['warnings']) == 5
    keys = re.findall(r'(?m)^@\w+\s*\{\s*([^,\s]+)', (ROOT / 'references/references.bib').read_text())
    assert len(keys) == len(set(keys)) == 54

    # Archives preserve root-relative links as historical text; check live docs.
    documents = sorted({ROOT / n for n in baseline['files'] if n.endswith('.md')} |
                       {ROOT / n for n in allowed_new if n.endswith('.md')} |
                       set(RESEARCH.glob('*.md')))
    broken, checked = [], 0
    for path in documents:
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            target = target.strip().split(' "')[0].strip('<>')
            if not target or target.startswith('#') or urlsplit(target).scheme:
                continue
            filename = unquote(target.split('#')[0].split('?')[0])
            checked += 1
            if not (path.parent / filename).exists():
                broken.append({'document': str(path.relative_to(ROOT)), 'target': target})
    assert not broken, broken

    active = []
    for line in subprocess.check_output(['ps', '-axo', 'pid=,command=']).decode().splitlines():
        if re.search(r'python\S*\s+-m\s+sos_morphology\.(?:run|parallel_run|report|independent_audit)\b', line):
            active.append(line.strip().split(maxsplit=1)[0])
    assert not active, active
    provenance = [DATA / n for n in ['manifest.json', 'execution_manifest.json', 'audit.json',
                                    'independent_audit.json', 'synthetic/audit.json', 'selection_audit.json']]
    provenance += [REPORT / 'catalog.json', RESEARCH / 'visual_review.json',
                   RESEARCH / 'bibliography_validation.json', ROOT / 'references/references.bib',
                   ROOT / 'references/index.json', Path(__file__)]
    report = {
        'all_complete': True, 'created_at': datetime.now(timezone.utc).isoformat(),
        'metric_sets': 16884, 'completed_blocks': 30, 'primary_model_field_cells': 260,
        'selection_arrays': 1406, 'scientific_sources_and_copies_verified': len(manifest['source_files']),
        'frozen_parent_records_verified': len(manifest['parent_files']),
        'baseline_documents_verified': 15, 'prior_tracked_scientific_files_unchanged': True,
        'independent_numeric_max_error': max(errors), 'synthetic_checks_passed': True,
        'report_files_verified': 36, 'csv_tables': 20, 'figures': 5, 'visual_review_verified': True,
        'stability_pass_counts': passed, 'illustrative_reversal_verified': True,
        'bibliography': {'valid': 54, 'errors': 0, 'duplicates': 0, 'warnings_retained': 5},
        'local_markdown_links_checked': checked, 'broken_links': broken,
        'git_head_at_check': git('rev-parse', 'HEAD').decode().strip(),
        'data_ignored_by_git': ignored, 'active_calculation_processes': active,
        'evidence_hashes': {str(p.relative_to(ROOT)): sha(p) for p in provenance},
        'current_documents': {str(p.relative_to(ROOT)): sha(p) for p in documents},
        'scope': 'Artifact integrity and recorded mathematical/visual checks. Not semantic truth, population precision, or editorial acceptance.'
    }
    (RESEARCH / 'closure_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ['evidence_hashes', 'current_documents']},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
