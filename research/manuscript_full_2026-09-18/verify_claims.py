"""Check cited result cells and chart summaries against frozen outputs."""
from pathlib import Path
import csv,json,hashlib,statistics,math
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def csvrows(path):
 with path.open() as f:return list(csv.DictReader(f))
checks=[]
for r in csvrows(ROOT/'research/writing_blueprint_2026-09-18/claim_evidence.csv'):
 p=ROOT/r['source'];assert sha(p)==r['source_sha256']
 expected=json.loads(r['values'])
 if r['selector']:
  sel=json.loads(r['selector']);found=[a for a in csvrows(p) if all(a[k]==v for k,v in sel.items())];assert len(found)==1
  actual={k:found[0][k] for k in expected}
 else:
  actual=json.loads(p.read_text())
  for k in r['json_pointer'].split('/'):actual=actual[int(k)] if isinstance(actual,list) else actual[k]
 assert actual==expected,(r['claim_id'],actual,expected)
 checks.append({'id':r['claim_id'],'source':r['source'],'sha256':sha(p),'values':actual,'limit':r['limit']})
manifest=json.loads((ROOT/'manuscript/figures/manifest.json').read_text())
source=csvrows(ROOT/'data/robustness_v2/centroid_scales/comparisons.csv')
for group in ['real','random_period_preserved']:
 vals=[statistics.mean(float(r['cka_debiased']) for r in source if r['condition']==c and r['groups']==group) for c in ['matched_field','matched_subfield','one_subfield_per_field']]
 assert all(math.isclose(a,b,abs_tol=1e-13) for a,b in zip(vals,manifest['figure_01']['displayed_values'][group]))
 checks.append({'id':'F1_'+group,'values':vals,'source':'data/robustness_v2/centroid_scales/comparisons.csv','limit':'Means over fixed pairs and saved centre comparisons; not population intervals.'})
pts=manifest['figure_02']['displayed_values']['points'];assert len(pts)==217
assert sum(p['y']>p['x'] for p in pts)==90 and sum(p['y']<p['x'] for p in pts)==127
s=json.loads((ROOT/'reports/analysis_v1/final/summary.json').read_text())
assert round(100*s['global_neighbors']['25']['mean'],1)==17.5
assert round(s['shape_neighbor_pair_spearman'],3)==.920
checks.append({'id':'global_neighbors_and_association','values':{'global_k25':s['global_neighbors']['25']['mean'],'shape_neighbor_pair_spearman':s['shape_neighbor_pair_spearman']},'source':'reports/analysis_v1/final/summary.json','limit':'13,000 balanced queries against 400k; association across 45 dependent model-pair means.'})
result={'verified':True,'checks':checks,'figure2_points':217,'figure2_higher':90,'figure2_lower':127,'scientific_recomputation':False}
(OUT/'numeric_claim_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print('Verified',len(checks),'claim/source checks and all 217 Figure 2 directions.')
