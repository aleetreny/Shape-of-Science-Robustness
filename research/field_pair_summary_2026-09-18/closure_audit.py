"""Verify this delivery and preserved predecessor without rerunning analyses."""
import csv
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = Path(__file__).resolve().parent
DATA = ROOT / 'data/field_pair_summary_v1'
REPORT = ROOT / 'reports/field_pair_summary_v1'


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_text())


def main():
    target = RESEARCH / 'closure_audit.json'
    target.write_text(json.dumps({'all_complete': False, 'state': 'checking'}) + '\n')
    audit = read(DATA / 'audit.json')
    assert audit['all_complete'] and audit['csv_tables'] == 12
    for name, expected in audit['files'].items(): assert sha(ROOT / name) == expected, name
    manifest = read(DATA / 'manifest.json')
    for name, expected in manifest['source_files'].items():
        assert sha(ROOT / name) == sha(DATA / 'source_snapshot' / name) == expected, name
    for name, expected in manifest['parent_files'].items(): assert sha(ROOT / name) == expected, name
    independent = read(DATA / 'independent_audit.json')
    assert independent['all_complete'] and independent['contrast_values_verified'] == 442000
    assert independent['source_sha256'] == sha(ROOT / 'sos_pair_summary/audit.py')
    assert independent['data_audit_sha256'] == sha(DATA / 'audit.json')
    tests = read(RESEARCH / 'tests.json')
    assert tests['passed'] == 11 and tests['failed'] == 0 and tests['observed_exit_code'] == 0
    for name, expected in tests['source_files'].items(): assert sha(ROOT / name) == expected

    old = ROOT / 'data/morphology_pilot_v1'
    old_audit = read(old / 'audit.json')
    for name, expected in old_audit['files'].items(): assert sha(old / name) == expected, name
    old_manifest = read(old / 'manifest.json')
    for name, expected in old_manifest['source_files'].items():
        assert sha(ROOT / name) == sha(old / 'source_snapshot' / name) == expected, name
    for name, expected in old_manifest['parent_files'].items(): assert sha(ROOT / name) == expected, name
    old_catalog = read(ROOT / 'reports/morphology_pilot_v1/catalog.json')
    for name, expected in old_catalog['files'].items():
        assert sha(ROOT / 'reports/morphology_pilot_v1' / name) == expected, name
    assert old_catalog['export_source_sha256'] == sha(ROOT / 'sos_morphology/report.py')
    baseline = read(RESEARCH / 'baseline_documents/manifest.json')
    assert sha(ROOT / baseline['preceding_closure']) == baseline['preceding_closure_sha256']
    for name, expected in baseline['files'].items():
        assert sha(RESEARCH / 'baseline_documents' / name) == expected, name

    catalog = read(REPORT / 'catalog.json')
    assert catalog['report_source_sha256'] == sha(ROOT / 'sos_pair_summary/report.py')
    assert catalog['scientific_audit_sha256'] == sha(DATA / 'audit.json')
    assert catalog['independent_audit_sha256'] == sha(DATA / 'independent_audit.json')
    assert len(catalog['files']) == 19
    for name, expected in catalog['files'].items(): assert sha(REPORT / name) == expected, name
    assert len(list(REPORT.glob('*.csv'))) == 12
    assert all(len(list(REPORT.glob('*.' + ext))) == 2 for ext in ['png', 'pdf', 'svg'])
    visual = read(RESEARCH / 'visual_review.json')
    assert visual['all_figures_inspected'] and len(visual['files']) == 2
    for name, detail in visual['files'].items(): assert sha(REPORT / name) == detail['sha256']

    with (REPORT / 'pair_summary.csv').open() as f: pairs = list(csv.DictReader(f))
    for metric, counts in [('angle_p50', (42, 262, 21)), ('pr', (54, 221, 50))]:
        rows = [r for r in pairs if r['metric'] == metric]
        assert len(rows) == len({(r['field_a'], r['field_b']) for r in rows}) == 325
        assert tuple(sum(r['class'] == cls for r in rows) for cls in ['unanimous', 'contradiction', 'unresolved']) == counts
    for metric, field, expected in [('angle_p50', 35, 24), ('pr', 21, 22)]:
        rows = [r for r in pairs if r['metric'] == metric]
        smaller = sum((int(r['field_a']) == field and r['positive_count'] == '10') or
                      (int(r['field_b']) == field and r['negative_count'] == '10') for r in rows)
        assert smaller == expected

    live_names = sorted(set(baseline['files']) | {'FIELD_PAIR_RESULTS.md', 'FIELD_PAIR_PROTOCOL.md', 'METHODS_FIELD_PAIRS.md'})
    documents = [ROOT / name for name in live_names if name.endswith('.md')]
    broken, link_count = [], 0
    for document in documents:
        for target_link in re.findall(r'\]\(([^)]+)\)', document.read_text()):
            target_link = target_link.strip().split(' "')[0].strip('<>')
            if not target_link or target_link.startswith('#') or urlsplit(target_link).scheme: continue
            local = unquote(target_link.split('#')[0].split('?')[0]); link_count += 1
            if not (document.parent / local).exists():
                broken.append({'document': str(document.relative_to(ROOT)), 'target': target_link})
    assert not broken, broken
    subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)
    assert subprocess.run(['git', 'check-ignore', '-q', 'data/field_pair_summary_v1/contrasts.npz'], cwd=ROOT).returncode == 0
    active = []
    for line in subprocess.check_output(['ps', '-axo', 'pid=,command=']).decode().splitlines():
        if re.search(r'python\S*\s+-m\s+sos_(?:pair_summary|morphology)\.(?:analyze|run|parallel_run|report|audit)\b', line):
            active.append(line.strip().split(maxsplit=1)[0])
    assert not active, active
    evidence = [DATA / n for n in ['manifest.json', 'audit.json', 'independent_audit.json']]
    evidence += [REPORT / 'catalog.json', RESEARCH / 'tests.json', RESEARCH / 'visual_review.json', Path(__file__)]
    result = {'all_complete': True, 'created_at': datetime.now(timezone.utc).isoformat(),
        'pairs_per_property': 325, 'properties': 2, 'model_pair_decisions': 6500,
        'independent_contrasts_verified': 442000, 'rule_tests_passed': 11,
        'report_files_verified': 19, 'tables': 12, 'figures': 2, 'visual_review_verified': True,
        'previous_report_files_unchanged': len(old_catalog['files']),
        'previous_scientific_sources_unchanged': len(old_manifest['source_files']),
        'previous_closure_unchanged': True, 'baseline_documents_verified': len(baseline['files']),
        'headline_counts_and_stable_examples_verified': True,
        'local_markdown_links_checked': link_count, 'broken_links': broken,
        'data_ignored_by_git': True, 'active_calculations': active,
        'git_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
        'evidence_hashes': {str(p.relative_to(ROOT)): sha(p) for p in evidence},
        'current_documents': {str(p.relative_to(ROOT)): sha(p) for p in documents},
        'scope': 'Numerical reconciliation, provenance and presentation. No population inference, semantic validation, manuscript or new publication.'}
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ['evidence_hashes', 'current_documents']}, ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
