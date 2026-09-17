"""Describe exclusions by Field without treating alerts as ground truth."""
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'research/cleaning_2026-09-15'
manifest = json.loads((ROOT/'data/corpus_clean_v1/embedding_manifest.json').read_text())
assert manifest['status'] == 'prepared_and_verified'
original = {int(r['field_id']): r for r in csv.DictReader((ROOT/'research/corpus_audit_2026-09-15/field_summary.csv').open())}
final = {int(r['field_id']): r for r in csv.DictReader((OUT/'field_summary.csv').open())}
counts = defaultdict(Counter)
for r in csv.DictReader((OUT/'original_records_not_selected.csv').open()):
    c = counts[int(r['field_id'])]
    reasons = r['reason'].split(';')
    c['original_not_selected'] += 1
    if reasons == ['not_reselected_after_clean_base_and_reallocation']:
        c['valid_not_reselected_due_to_allocation'] += 1
    else:
        c['original_excluded_by_quality'] += 1
        c['clear_non_english'] += int('clear_non_english_abstract' in reasons)
        c['content_or_notice'] += int(any(x != 'clear_non_english_abstract' for x in reasons))
output = []
for field in sorted(original):
    before = int(original[field]['total'])
    c = counts[field]
    output.append(dict(field_id=field,field_name=final[field]['field_name'],original_total=before,
        final_total=int(final[field]['total']),original_not_selected=c['original_not_selected'],
        original_excluded_by_quality=c['original_excluded_by_quality'],
        quality_excluded_percent=round(100*c['original_excluded_by_quality']/before,4),
        clear_non_english=c['clear_non_english'],content_or_notice=c['content_or_notice'],
        valid_not_reselected_due_to_allocation=c['valid_not_reselected_due_to_allocation']))
assert sum(r['original_not_selected'] for r in output) == manifest['original_records_not_reselected']
assert sum(r['original_total'] for r in output) == sum(r['final_total'] for r in output) == 500000
with (OUT/'cleaning_impact_by_field.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(output[0]));w.writeheader();w.writerows(output)
result = dict(original_quality_excluded=sum(r['original_excluded_by_quality'] for r in output),
    valid_not_reselected_due_to_allocation=sum(r['valid_not_reselected_due_to_allocation'] for r in output),
    largest_quality_exclusion_percent=sorted(output,key=lambda r:r['quality_excluded_percent'],reverse=True)[:3],
    note='Language and content reasons can overlap. Rates describe the original selected corpus, not OpenAlex-wide error rates.')
(OUT/'cleaning_impact_summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
