"""Verify delivery hashes and handoff; never run scientific computations."""
from pathlib import Path
import csv
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'research/checklist_2026-09-17'
FINAL = ROOT / 'reports/checklist_v1/final'

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def read(path):
    return json.loads(path.read_text())

catalog = read(FINAL / 'catalog.json')
audit = read(FINAL / 'audit.json')
assert catalog['all_complete'] and audit['all_complete']
for name, spec in catalog['files'].items():
    path = FINAL / name
    assert path.stat().st_size == spec['bytes'], name
    assert digest(path) == spec['sha256'], name
actual = {str(p.relative_to(FINAL)) for p in FINAL.rglob('*') if p.is_file() and p.name != 'catalog.json'}
assert actual == set(catalog['files']), (actual - set(catalog['files']), set(catalog['files']) - actual)
assert len(list((FINAL / 'tables').glob('*.csv'))) == 33
for suffix in ('png', 'pdf', 'svg'):
    assert len(list((FINAL / 'figures').glob('*.' + suffix))) == 7

source_files = {}
manifests = sorted((ROOT / 'data/checklist_v1/inputs').glob('*/*/manifest.json'))
assert len(manifests) == 30
manifests += [ROOT / 'data/checklist_v1' / name / 'manifest.json' for name in ('input_comparisons', 'input_recipes')]
for manifest in manifests:
    for name, expected in read(manifest)['source_files'].items():
        assert digest(ROOT / name) == expected, (str(manifest), name)
        source_files[name] = expected
for folder, module in [('existing_v2', 'existing_analysis_v2.py'), ('candidate_check', 'candidate_check.py')]:
    manifest = read(ROOT / 'data/checklist_v1' / folder / 'manifest.json')
    expected = manifest['source_sha256']
    assert digest(ROOT / 'sos_followup' / module) == expected
    source_files['sos_followup/' + module] = expected
profile = read(ROOT / 'data/checklist_v1/text_profile/audit.json')
assert digest(ROOT / 'sos_followup/input_text_profile.py') == profile['source_sha256']
assert digest(ROOT / 'sos_followup/report.py') == audit['exporter_sha256']

with (FINAL / 'tables/input_stability.csv').open() as f:
    stability = list(csv.DictReader(f))
with (FINAL / 'tables/input_stability_alerts.csv').open() as f:
    alerts = list(csv.DictReader(f))
assert len(stability) == 572
expected_alerts = [r for r in stability if r['passes_operational_screen'] == 'False']
assert alerts == expected_alerts and len(alerts) == 31
assert len({r['field_id'] for r in alerts}) == 17
assert all(float(r['absolute_median_change']) <= .02 for r in stability)
assert all(float(r['central95_width500']) > .04 for r in alerts)
assert audit['total_input_neighbor_queries_checked'] == 14040
assert audit['original_resume_checkpoint_unchanged']
assert audit['old_stability_alerts_retained'] == 50

log_checks = {
    'input_run.log': 'INPUT QUEUE COMPLETE; ORIGINAL CHECKPOINT UNCHANGED',
    'finish_pilot.log': 'PILOT FINISHED AND AUDITED',
    'finish_recipes.log': 'INPUT RECIPE SENSITIVITY FINISHED',
    'report_final.log': 'COMPLETE: True',
}
for name, marker in log_checks.items():
    assert marker in (OUT / name).read_text(), name
for name, number in [('tests_final.log', 6), ('recipe_tests.log', 1)]:
    text = (OUT / name).read_text()
    assert re.search(r'Ran ' + str(number) + r' tests? in ', text) and text.rstrip().endswith('OK'), name

active = []
processes = subprocess.check_output(['ps', '-axo', 'pid=,comm=,args='], text=True)
for line in processes.splitlines():
    parts = line.strip().split(None, 2)
    if len(parts) != 3:
        continue
    pid, executable, args = parts
    if 'python' not in Path(executable).name.lower():
        continue
    if re.search(r'(?:-m\s+sos_(?:followup|analysis|embed)(?:\.|\s)|checklist_2026-09-17/(?:run_inputs|finish_pilot|finish_recipes)\.py)', args):
        active.append({'pid': int(pid), 'command': args})
assert not active, active

names = ['AGENTS.md', 'DECISIONS.md', 'progress.md', 'task_plan.md', 'findings.md',
         'README.md', 'NEXT_STEPS.md', 'PAPER_OUTLINE.md', 'DATA_CATALOG.md',
         'CHECKLIST_RESULTS.md', 'METHODS_CHECKLIST.md', 'CHECKLIST_PROTOCOL.md',
         '02_open_questions.md', 'ANALYSIS_RESULTS.md',
         'research/checklist_2026-09-17/MODEL_PROFILES.md',
         'research/checklist_2026-09-17/RELATED_INPUT_WORK.md']
checked_links = []
for name in names:
    path = ROOT / name
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        target = target.strip().strip('<>')
        if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
            continue
        target = unquote(target.split('#', 1)[0])
        if not target:
            continue
        resolved = path.parent / target
        assert resolved.exists(), (name, target)
        checked_links.append({'document': name, 'target': target})

visual = []
for path in sorted((FINAL / 'figures').glob('*.png')):
    item = {'path': str(path.relative_to(ROOT)), 'sha256': digest(path),
            'visually_inspected_this_task': True}
    if path.name.startswith(('02_', '03_', '04_', '05_')):
        preview = ROOT / 'reports/checklist_v1/preview/figures' / path.name
        assert digest(preview) == digest(path), path.name
        item['same_as_inspected_preview_png'] = True
    else:
        item['inspection_stage'] = 'final'
    visual.append(item)

stamp = datetime.now(timezone.utc).isoformat()
status = {
    'status': 'complete', 'checked_at': stamp, 'active_scientific_processes': [],
    'protocol': 'CHECKLIST_PROTOCOL.md', 'results': 'CHECKLIST_RESULTS.md',
    'report': 'reports/checklist_v1/final', 'distinct_papers': 26000,
    'model_input_conditions': 30, 'principal_recipe': 'mean_for_four_word_BERTs',
    'new_individual_shape_stability_alerts': 31, 'old_separate_stability_alerts': 50,
    'full500k_input_rerun': 'not_started_and_not_needed_for_current_broad_claims',
    'input_queue_log': 'research/checklist_2026-09-17/input_run.log',
    'completion_driver_logs': ['research/checklist_2026-09-17/finish_pilot.log', 'research/checklist_2026-09-17/finish_recipes.log'],
    'next_step': 'Manuscript drafting when requested; retain alerts and limitations.',
    'warning': 'Do not restart inference or neighbors. Do not treat the shape stability screen as population precision or neighbor stability.'
}
(OUT / 'checklist_status.json').write_text(json.dumps(status, indent=2, ensure_ascii=False) + '\n')
result = {
    'all_passed': True, 'checked_at': stamp,
    'final_catalog_sha256': digest(FINAL / 'catalog.json'),
    'catalog_files_verified': len(catalog['files']), 'tables': 33,
    'figures_per_format': 7, 'formats': ['png', 'pdf', 'svg'],
    'current_scientific_sources_match_frozen_manifests': source_files,
    'audit_source': 'reports/checklist_v1/final/audit.json',
    'existing_test_logs_passed': {'tests_final.log': 6, 'recipe_tests.log': 1},
    'driver_completion_markers_verified': log_checks,
    'active_scientific_processes': active,
    'shape_stability_alerts_preserved': 31, 'old_separate_alerts_preserved': 50,
    'local_markdown_links_checked': len(checked_links),
    'documents_sha256': {name: digest(ROOT / name) for name in names},
    'visual_reviews': visual,
    'verifier_sha256': digest(Path(__file__)),
    'scope': 'Delivery, sources, completion and handoff verification only. No new inference, neighbors or population claim.'
}
(OUT / 'closure_audit.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({k: result[k] for k in ['all_passed','checked_at','catalog_files_verified','tables','figures_per_format','local_markdown_links_checked','active_scientific_processes']}, indent=2))
