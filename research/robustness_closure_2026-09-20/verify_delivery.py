"""Read-only source, numeric-display and final-freeze verification.

Does not import or execute scientific analysis programs. The separate independent
scientific audit checks calculations; this checks their delivery and interpretation.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import csv
import hashlib
import json
import re

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = ROOT / 'reports/robustness_closure_v1'
MAN = ROOT / 'manuscript'
BASE = HERE / 'baseline_documents'

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def read(path):
    return json.loads(path.read_text())

def rows(path):
    with path.open() as stream:
        return list(csv.DictReader(stream))

def one(name, **selector):
    found = [r for r in rows(RESULTS / (name + '.csv'))
             if all(r[k] == str(v) for k, v in selector.items())]
    assert len(found) == 1, (name, selector, len(found))
    return found[0]

def f(value, places=3, scale=1):
    return f'{float(value) * scale:.{places}f}'

def table_data(name):
    output = []
    for line in (MAN / 'tables/tex' / (name + '.tex')).read_text().splitlines():
        if ' & ' in line and not line.startswith(r'\textbf'):
            cells = line.split(r'\\', 1)[0].split(' & ')
            output.append([c.strip().replace(r'\%', '%') for c in cells])
    return output

report = {'completed_at': datetime.now(timezone.utc).isoformat(), 'passed': False}
protected = read(HERE / 'protected_manifest.json')
baseline = read(HERE / 'baseline_manifest.json')
for rel, digest in protected.items():
    assert sha(ROOT / rel) == digest, ('protected result changed', rel)
for rel, digest in baseline.items():
    assert sha(BASE / rel) == digest, ('archive changed', rel)
report.update(protected_files=len(protected), archived_files=len(baseline))

# Each branch is complete and its recorded source, inputs and outputs still match.
branches = {}
for branch in ['centres', 'headline', 'morphology', 'quality', 'summary']:
    directory = ROOT / 'data/robustness_closure_v1' / branch
    audit = read(directory / 'audit.json')
    assert audit['all_complete']
    for rel, digest in audit['files'].items():
        assert sha(directory / rel) == digest, (branch, rel)
    manifest = read(directory / 'manifest.json')
    for kind in ['source_files', 'parent_files']:
        for rel, digest in manifest[kind].items():
            assert sha(ROOT / rel) == digest, (branch, kind, rel)
    branches[branch] = {'files': len(audit['files']), 'audit_sha256': sha(directory/'audit.json')}
catalog = read(RESULTS / 'catalog.json')
for rel, digest in catalog['files'].items():
    assert sha(RESULTS / rel) == digest, rel
assert sha(RESULTS/'catalog.json') == read(ROOT/'data/robustness_closure_v1/summary/audit.json')['report_catalog_sha256']
report['scientific_branches'] = branches

# The inherited claim/evidence register is checked against the original sources.
# Its earlier alternative-dimension count remains historical, not current prose.
legacy_claims = []
for r in rows(ROOT/'research/writing_blueprint_2026-09-18/claim_evidence.csv'):
    source = ROOT / r['source']
    assert sha(source) == r['source_sha256']
    expected = json.loads(r['values'])
    if r['selector']:
        selector = json.loads(r['selector'])
        found = [x for x in rows(source) if all(x[k] == v for k, v in selector.items())]
        assert len(found) == 1
        actual = {k: found[0][k] for k in expected}
    else:
        actual = read(source)
        for key in r['json_pointer'].split('/'):
            actual = actual[int(key)] if isinstance(actual, list) else actual[key]
    assert actual == expected, r['claim_id']
    legacy_claims.append(r['claim_id'])
report['inherited_claim_source_checks'] = legacy_claims

figures = read(MAN/'figures/manifest.json')
tables = read(MAN/'tables/manifest.json')
assert set(figures) == {f'figure_{i:02}' for i in range(1, 5)} | {f'figure_S{i:02}' for i in range(1, 12)}
assert set(tables) == {'T01', 'T02'} | {f'S{i:02}' for i in range(1, 21)}
attachments = 0
for folder in ['manuscript', 'manuscript_es']:
    source_root = ROOT / folder
    for kind in ['figures', 'tables']:
        for key, entry in read(source_root/kind/'manifest.json').items():
            for source in entry['sources']:
                included = source_root / source['included']
                assert sha(included) == source['sha256'], (folder, key, included)
                assert len(rows(included)) == source['rows']
                original = ROOT / source['source']
                if original.is_file():
                    assert sha(original) == source['sha256'], original
                attachments += 1
            if 'tex_sha256' in entry:
                assert sha(source_root/entry['tex']) == entry['tex_sha256']
            if 'editorial_source' in entry:
                e = entry['editorial_source']
                assert sha(source_root/e['path']) == e['sha256']
    for key, entry in read(source_root/'figures/manifest.json').items():
        assert len(entry['files']) == 4
        for rel in entry['files']:
            p = source_root / rel
            assert 0 < p.stat().st_size < 10_000_000
            if p.suffix in {'.png', '.tiff'}:
                with Image.open(p) as im:
                    assert all(abs(x-300) < .1 for x in im.info['dpi'])
report['source_attachments_verified'] = attachments

# Unchanged figures and table numbers retain their previously checked sources.
oldfigures = read(BASE/'manuscript/figures/manifest.json')
for key in oldfigures:
    if key not in ['figure_01', 'figure_04']:
        assert figures[key]['displayed_values'] == oldfigures[key]['displayed_values'], key
for p in (BASE/'manuscript/tables/tex').glob('*.tex'):
    if p.stem not in {'T01', 'S15', 'S17'}:
        assert p.read_bytes() == (MAN/'tables/tex'/p.name).read_bytes(), p.name
for key in ['observed', 'random']:
    for item in figures['figure_01']['displayed_values'][key]:
        assert item == one('centres_summary', design=item['design'], grouping=item['grouping'])
within = rows(ROOT/'reports/robustness_v2/final/tables/structure_matched_size_agreement.csv')
assert all(r in within for r in figures['figure_01']['displayed_values']['within_group_spread'])
for metric in ['angle_p50', 'pr']:
    for item in figures['figure_04']['displayed_values'][metric]:
        assert item == one('morphology_classification', metric=metric,
                           representation=item['representation'], cutoff=item['cutoff'])
for key, source in [('centres', 'centres_summary'), ('headline', 'headline_grand_repetitions')]:
    full = rows(RESULTS/(source+'.csv'))
    assert all(r in full for r in figures['figure_S11']['displayed_values'][key])
points = figures['figure_02']['displayed_values']['points']
assert len(points) == 217
assert sum(p['y'] > p['x'] for p in points) == 90
assert sum(p['y'] < p['x'] for p in points) == 127

# Compare all numeric cells in the new typeset tables to the unrounded CSVs.
s18 = table_data('S18')
designs = ['repeat256_field', 'repeat256_subfield217', 'nested26'] + [f'size{n}_{group}' for group in ['field', 'subfield183'] for n in [128, 256, 512]]
for actual, design in zip(s18[:9], designs):
    a = one('centres_summary', design=design, grouping='observed')
    b = one('centres_summary', design=design, grouping='random')
    n = re.search(r'size(\d+)', design)
    expected = [n.group(1) if n else '256', f(a['mean']), f(a['p025'])+'--'+f(a['p975']), f(b['mean'])]
    assert actual[1:] == expected, (design, actual, expected)
for actual, (recipe, k) in zip(s18[9:], [('mean', 10), ('mean', 25), ('mean', 50), ('cls', 25), ('sep', 25)]):
    get = lambda measure: one('headline_summary', recipe=recipe, k=k, measure=measure)
    a, b, c = [get(m) for m in ['model_change', 'title_only_change', 'title_minus_model']]
    expected = [str(k), f(a['mean'], 2, 100), f(b['mean'], 2, 100), f(c['mean'], 2, 100), f(c['p025'], 2, 100)+' to '+f(c['p975'], 2, 100)]
    assert actual[1:] == expected, (recipe, k, actual, expected)
    assert float(c['opposite_sign_fraction']) == 0
s19 = table_data('S19')
for actual, (scope, k) in zip(s19[:9], [(scope,k) for scope in ['all','1024','2048'] for k in [10,25,50]]):
    r = one('quality_summary', scope=scope, k=k)
    assert actual[1:] == [r['cells'], str(k), f(r['original_same_query_overlap'], 2, 100), f(r['filtered_overlap'], 2, 100), f(r['change_pp'], 2)]
for actual, k in zip(s19[9:], [10,25,50]):
    a = one('quality_input_effects', k=k, corpus='original')
    b = one('quality_input_effects', k=k, corpus='filtered')
    assert actual == [str(k), f(a['model_change'],2,100), f(b['model_change'],2,100), f(a['title_only_change'],2,100), f(b['title_only_change'],2,100)]
s20 = table_data('S20')
for actual, (metric, cutoff) in zip(s20[:8], [(m,c) for m in ['angle_p50','pr'] for c in [0.,.01,.05,.1]]):
    r = one('morphology_centering_summary', metric=metric, cutoff=cutoff)
    assert actual[1:] == [f(cutoff,0,100)+'%'] + [r[k] for k in ['original_oppositions','centered_oppositions','same_fixed_witness_directions_retained','new_oppositions','original_oppositions_now_unresolved']]
for actual, cutoff in zip(s20[8:], [0.,.01,.05,.1]):
    alt = [one('dimension_alternative_retention', cutoff=cutoff, alternative=a) for a in ['erank','d80','both']]
    assert actual == [f(cutoff,0,100)+'%',alt[0]['PR_oppositions']] + [r['same_witness_directions_retained'] for r in alt]
panels = ['all_ten','sentence_trained_six'] + ['without_'+m for m in ['specter','specter2','scincl','scibert','bert','mpnet','minilm','pubmedbert','biobert','simcse']]
actual_panels = list(dict.fromkeys(r['panel'] for r in rows(RESULTS/'model_panel_summary_full_alternatives.csv')))
# The frozen identifiers are taken from CSV; their display order is fixed below.
if set(panels) != set(actual_panels):
    panels = actual_panels
for actual, panel in zip(table_data('S15'), panels):
    a = one('model_panel_summary_full_alternatives', metric='angle_p50', panel=panel, minimum_relative_difference=0.)
    b = one('model_panel_summary_full_alternatives', metric='pr', panel=panel, minimum_relative_difference=0.)
    assert actual[1:] == [a['models'],a['contradiction'],a['contradiction_and_alternatives'],b['contradiction'],b['contradiction_and_alternatives']], (actual,panel)
report['new_typeset_numeric_rows_checked'] = len(s18)+len(s19)+len(s20)+len(table_data('S15'))

# Current manuscript numbers, history and inference limits.
main = (MAN/'main.tex').read_text()
supp = (MAN/'supplement.tex').read_text()
summary = read(RESULTS/'summary.json')
for recipe, k in [('mean',10),('mean',25),('mean',50),('cls',25),('sep',25)]:
    r = one('headline_summary',recipe=recipe,k=k,measure='title_minus_model')
    assert f(r['mean'],2,100) in main
for k in ['min','max']:
    assert f(summary['headline']['primary_k25_model_range'][k],2,100) in main
for design in designs:
    assert f(one('centres_summary',design=design,grouping='observed')['mean']) in main
for r in rows(RESULTS/'morphology_centering_summary.csv'):
    if r['cutoff'] == '0.0':
        for key in ['original_oppositions','centered_oppositions','same_fixed_witness_directions_retained']:
            assert r[key] in main
assert '2,628' in main and '8,235' in main and '31.9' in main
assert summary['local_subfield_stability']['alerts'] == 2628
assert summary['local_subfield_stability']['comparisons'] == 8235
assert not re.search(r'\b(?:196|145|218)\b', main), 'Historical partial-control count in current main prose'
for phrase in ['not confidence intervals', 'not externally preregistered', 'not establish equivalence', 'D80 counts directions as whole numbers, so ties remain unresolved', 'not merely the covariance centring', 'not every possible source error']:
    assert phrase in main, phrase
for phrase in ['proves', 'validates', 'true structure', 'statistically significant', 'independent repetitions']:
    assert not re.search(r'\b'+phrase+r'\b', main+'\n'+supp, re.I), phrase
assert 'not asserted to be exactly unbiased' in supp
assert 'neither is a confidence interval' in main
assert len(rows(HERE/'claim_audit.csv')) == 11
report['claim_checks'] = {'claims':11,'old_partial_counts_absent_from_main':True,'inference_limits_explicit':True,
    'remaining_heritage_numbers':'Unchanged results and tables retain their frozen sources and the checked claim/evidence register; new cells and plotted summaries checked separately above.'}

# Final render and extracted packages must describe the same four current PDFs.
text = read(HERE/'text_audit.json')
visual = read(HERE/'visual_review.json')
portable = read(HERE/'portable_source_audit.json')
assert visual['all_pages_inspected'] and not visual['remaining_layout_blockers']
for key, document in visual['documents'].items():
    assert sha(ROOT/document['path']) == document['sha256'] == text['documents'][key]['sha256']
    assert document['reviewed_pages'] == list(range(1,document['pages']+1))
for lang, package in portable['packages'].items():
    assert sha(ROOT/package['path']) == package['sha256']
    folder = 'manuscript' if lang == 'en' else 'manuscript_es'
    for rel, digest in package['source_hashes'].items():
        assert sha(ROOT/folder/rel) == digest, ('package source changed',lang,rel)
    for name, document in package['documents'].items():
        assert document['byte_identical'] and document['sha256'] == text['documents'][lang+'_'+name]['sha256']
report.update(passed=True,scientific_recomputation=False,publication_or_deposit=False,
              pdf_pages=visual['pages_total'],pdf_documents=text['documents'],
              csv_files_bilingually_identical=text['csv_files_bilingually_identical'])
(HERE/'presentation_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:report[k] for k in ['passed','protected_files','archived_files','source_attachments_verified','new_typeset_numeric_rows_checked','pdf_pages']},indent=2))
