"""Independent numerical audit of frozen closure outputs; no changes to results."""
from pathlib import Path
import sys,json,csv,hashlib,itertools
import numpy as np
import pyarrow.parquet as pq
sys.path.insert(0,str(Path('.').resolve()))
from sos_analysis.geometry import shape_scores
from sos_followup.pilot_statistics import cosine_grams,cka_matrix
from sos_analysis.neighbors import shared_counts
ROOT=Path('.');OUT=ROOT/'data/robustness_closure_v1';REPORT=ROOT/'reports/robustness_closure_v1';HERE=ROOT/'research/robustness_closure_2026-09-20'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
 with p.open() as f:return list(csv.DictReader(f))
models=json.loads((ROOT/'config/robustness_closure_v1.json').read_text())['models'];fields=list(range(11,37));periods=[2000,2005,2010,2015,2020]
# Confirm every old scientific source and result present at start is untouched.
protected=json.loads((HERE/'protected_manifest.json').read_text())
for name,h in protected.items():assert sha(ROOT/name)==h,name
archive=json.loads((HERE/'baseline_manifest.json').read_text())
for name,h in archive.items():assert sha(HERE/'baseline_documents'/name)==h,name
# Independent ratio inequalities, no import of the classification functions.
conditions=[('primary',0)]+[('half',i) for i in range(20)]+[('external',i) for i in range(5)]
rows=pq.read_table(OUT/'morphology/metrics.parquet').to_pylist();ix={(r['representation'],r['model'],r['field_id'],r['kind'],r['repeat']):r for r in rows};expected={};ties=0
for representation,metric in [('original','angle_p50'),('original','pr'),('original','erank'),('original','d80'),('global_centered','angle_p50'),('global_centered','pr')]:
 for m in models:
  for a,b in itertools.combinations(fields,2):
   x=np.array([ix[representation,m,a,k,r][metric] for k,r in conditions]);y=np.array([ix[representation,m,b,k,r][metric] for k,r in conditions])
   if metric=='d80':ties+=int(np.any(x==y))
   for floor in [0.,.01,.05,.1]:
    t=floor+1e-10;sign=1 if np.all((2-t)*y>(2+t)*x) else -1 if np.all((2+t)*y<(2-t)*x) else 0
    expected[representation,metric,floor,a,b,m]=sign
for r in read(REPORT/'morphology_directions.csv'):
 key=(r['representation'],r['metric'],float(r['cutoff']),int(r['field_a']),int(r['field_b']),r['model']);assert int(r['direction'])==expected[key],r
# Existing whole-cell neighbors must reproduce old saved overlaps exactly.
old={}
for f in fields:
 for p in periods:
  for r in json.loads((ROOT/f'data/analysis_v1/neighbors/overlap/local/{f}_{p}/summary.json').read_text())['scores']:old[f,p,r['model_a'],r['model_b'],r['k']]=r['mean_overlap']
maxerror=0.
for r in read(OUT/'quality/native_comparisons.csv'):
 if r['scope']=='all':
  key=(int(r['field_id']),int(r['period']),r['model_a'],r['model_b'],int(r['k']));error=abs(float(r['original_all_queries_overlap'])-old[key]);maxerror=max(maxerror,error)
assert maxerror<1e-12,maxerror
# Every new centre selection and random reassignment preserves dates and identities.
meta=pq.read_table(ROOT/'data/analysis_ready_v1/metadata.parquet',columns=['row_index','field_id','subfield_id','period_start']);p=meta['period_start'].to_numpy();f=meta['field_id'].to_numpy();sf=meta['subfield_id'].to_numpy().astype(np.int64);centre_checks=0
for file in (OUT/'centres/selections').glob('*.npz'):
 with np.load(file) as s:
  a=s['observed'];b=s['random'];assert a.shape==b.shape
  for rep,(one,two) in enumerate(zip(a,b)):
   assert np.array_equal(np.sort(one.ravel()),np.sort(two.ravel())) and np.array_equal(p[one],p[two]);assert len(np.unique(one))==one.size
   if 'groups' in s:
    labels=f if file.stem.endswith('_field') else sf
    assert np.all(labels[one]==s['groups'][:,None]);assert np.array_equal(np.stack([(p[one]==period).sum(1) for period in periods],1),s['quotas'])
   else:assert np.all(sf[one]==s['chosen_subfields'][rep//10,:,None])
   centre_checks+=1
# Independent feature formula on stored centre vectors for both group types.
ce=0.
for name in ['repeat256_field','repeat256_subfield217']:
 a=[np.load(OUT/'centres/models'/m/(name+'.npz'))['observed'][0] for m in models]
 for i,j in [(0,1),(3,7),(6,9)]:
  feature=shape_scores([a[i],a[j]],procrustes=False)[0]['cka_debiased'];kernel=cka_matrix(cosine_grams([a[i],a[j]]))[0,1];ce=max(ce,abs(feature-kernel))
assert ce<1e-10
result={'passed':True,'protected_files_unchanged':len(protected),'archived_files_intact':len(archive),'independent_direction_checks':len(expected),'D80_model_pair_cases_with_any_tie':ties,'old_neighbor_reproduction_max_error':maxerror,'centre_selection_reference_checks':centre_checks,'centre_kernel_feature_max_error':ce,'limits':'Independent numerical checks do not establish thematic correctness or population precision.'}
(HERE/'independent_scientific_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
