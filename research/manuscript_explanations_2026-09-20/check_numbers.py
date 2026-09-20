"""Convert existing counts to prose percentages; no experiment is rerun."""
from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sources={};percentages=[]
def rows(rel):
 p=ROOT/rel;sources[rel]=hashlib.sha256(p.read_bytes()).hexdigest();return list(csv.DictReader(p.open()))
def add(label,n,d,source):
 percentages.append({'description':label,'numerator':int(n),'denominator':int(d),'percent':f'{100*int(n)/int(d):.1f}','source':source})
rpath='reports/robustness_closure_v1/morphology_classification.csv';r=rows(rpath)
for metric in ['angle_p50','pr']:
 for cutoff in ['0.0','0.05','0.1']:
  x=next(x for x in r if x['representation']=='original' and x['metric']==metric and x['cutoff']==cutoff)
  for cls in (['contradiction','unanimous','unresolved'] if cutoff=='0.0' else ['contradiction']):add(f'{metric}, minimum difference {cutoff}, {cls}',x[cls],x['pairs'],rpath)
x=next(x for x in r if x['representation']=='global_centered' and x['metric']=='angle_p50' and x['cutoff']=='0.0');add('centred angular opposition',x['contradiction'],x['pairs'],rpath)
rpath='reports/robustness_closure_v1/model_panel_summary_full_alternatives.csv';r=rows(rpath)
x=next(x for x in r if x['panel']=='all_ten' and x['metric']=='angle_p50' and x['minimum_relative_difference']=='0.0');add('same angular opposing pair under alternatives',x['contradiction_and_alternatives'],x['contradiction'],rpath)
for metric in ['angle_p50','pr']:
 x=next(x for x in r if x['panel']=='six_similarity' and x['metric']==metric and x['minimum_relative_difference']=='0.0');add(f'six models, {metric}',x['contradiction'],x['pairs'],rpath)
rpath='reports/robustness_closure_v1/dimension_alternative_retention.csv';r=rows(rpath)
for x in r:
 if x['cutoff']=='0.0':add(f'PR opposition retained by {x["alternative"]}',x['same_witness_directions_retained'],x['PR_oppositions'],rpath)
rpath='reports/robustness_closure_v1/morphology_centering_summary.csv';r=rows(rpath)
for x in r:
 if x['cutoff']=='0.0':add(f'same opposing pair after centring, {x["metric"]}',x['same_fixed_witness_directions_retained'],x['original_oppositions'],rpath)
rpath='reports/morphology_pilot_v1/selection_stability.csv';r=rows(rpath)
alerts={}
for metric in ['angle_p50','pr']:
 for kind in ['half','external']:
  group=[x for x in r if x['metric']==metric and x['kind']==kind];assert len(group)==260
  alerts[f'{metric}/{kind}']=sum(x['passes_both']=='False' for x in group)
assert alerts=={'angle_p50/half':0,'angle_p50/external':0,'pr/half':4,'pr/external':0}
add('PR half-sample alerts',alerts['pr/half'],260,rpath)
# Recorded scope and input counts are also preserved in the unedited baseline prose.
baseline=(HERE/'baseline/manuscript/main.tex').read_text()
assert 'Of 217 specialties, 127' in baseline and 'while 90 have higher agreement' in baseline
assert '72 out of 520 to five out of 520' in baseline
for label,n,d in [('scope lower',127,217),('scope higher',90,217),('input pilot alerts',72,520),('input expanded alerts',5,520)]:add(label,n,d,'baseline/manuscript/main.tex')
for lang,folder in [('en','manuscript'),('es','manuscript_es')]:
 text=(ROOT/folder/'main.tex').read_text()
 for x in percentages:
  s=x['percent'] if lang=='en' else x['percent'].replace('.',',')
  assert s+r'\%' in text,(lang,x)
rpath='reports/robustness_closure_v1/quality_summary.csv';q=rows(rpath);q25=next(x for x in q if x['scope']=='all' and x['k']=='25')
assert round(float(q25['original_same_query_overlap'])*100,2)==30.58
assert round(float(q25['filtered_overlap'])*100,2)==31.43
assert round(float(q25['original_same_query_overlap'])*25)==round(float(q25['filtered_overlap'])*25)==8
with (HERE/'percentage_audit.csv').open('w') as stream:
 w=csv.DictWriter(stream,fieldnames=percentages[0].keys());w.writeheader();w.writerows(percentages)
(HERE/'numeric_audit.json').write_text(json.dumps({'percentages_checked':len(percentages),'source_sha256':sources,'morphology_alerts':alerts,'illustrative_quality_neighbours_round_to_eight':True,'new_scientific_computation':False},indent=2)+'\n')
print('PASS:',len(percentages),'percentages verified against saved counts; morphology and quality examples checked.')
