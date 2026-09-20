from pathlib import Path
import json,sys,time,csv,importlib.metadata,collections
import numpy as np,pyarrow.parquet as pq
sys.path.insert(0,str(Path('.').resolve()))
from sos_analysis.native_data import NativeData
from sos_analysis.run_shape import strict_quality
from sos_deep.subfield_controls import prepared_groups
from sos_followup.pilot_statistics import cosine_grams,cka_matrix
from sos_analysis.geometry import shape_scores
from sos_embed.storage import file_sha,write_json
r=Path('.');d=NativeData(r,max_bytes=2*1024**3);m=d.metadata;g,_=prepared_groups(m);q=strict_quality(d)
f=m['field_id'].to_numpy();p=m['period_start'].to_numpy()
ids=pq.read_table('data/robustness_v2/inputs/native_input.parquet',columns=['row_index'])['row_index'].to_numpy()
counts=[{'field_id':int(a),'period':int(b),'all':int(np.sum((f==a)&(p==b))),'clean':int(np.sum(q&(f==a)&(p==b))),'input_clean':int(np.sum(q[ids]&(f[ids]==a)&(p[ids]==b)))} for a in np.unique(f) for b in np.unique(p)]
rng=np.random.default_rng(730);xs=[rng.normal(size=(37,19)),rng.normal(size=(37,13))];a=cka_matrix(cosine_grams(xs))[0,1]; b=shape_scores(xs,procrustes=False)[0]['cka_debiased']
base=Path('data/robustness_v2/centroid_scales');labels=json.loads((base/'group_labels.json').read_text());period_checks={}
for lv in ['field','subfield']:
 i=np.load(base/(lv+'_selected_ids.npy'));alloc=np.load(base/(lv+'_null_assignments.npy'));period_checks[lv]={'rows':len(i),'random_allocations':len(alloc),'period_exact':bool(all(np.array_equal(p[i],p[z]) for z in alloc)),'unique':int(len(set(i)))}
with (base/'comparisons.csv').open() as t:rr=list(csv.DictReader(t))
summary={}
for z in rr:
 key=z['condition']+'/'+z['groups'];summary.setdefault(key,[]).append(float(z['cka_debiased']))
ss={k:{'rows':len(v),'mean':float(np.mean(v))} for k,v in summary.items()}
packages={}
for name in ['numpy','scipy','pyarrow','numba','threadpoolctl','pandas','matplotlib']:
 try:packages[name]=importlib.metadata.version(name)
 except:packages[name]=None
out={'quality_retained':int(q.sum()),'quality_flags':d.design['quality_sensitivity_flags'],'cell_counts':counts,'group_counts':{lv:{'groups':sum(k[0]==lv for k in g),'eligible256':sum(k[0]==lv and len(z)>=256 for k,z in g.items()),'eligible512':sum(k[0]==lv and len(z)>=512 for k,z in g.items())} for lv in ['field','subfield']},'kernel_feature_cka_error':abs(a-b),'centroid_random_checks':period_checks,'centre_original':ss,'packages':packages,'metadata_sha256':file_sha('data/analysis_ready_v1/metadata.parquet')}
np.save('research/robustness_closure_2026-09-20/quality_mask.npy',q)
write_json('research/robustness_closure_2026-09-20/audit_probe.json',out)
print({k:v for k,v in out.items() if k not in ['cell_counts']})
print({'minimum_clean_cell':min(z['clean'] for z in counts),'minimum_input_clean_cell':min(z['input_clean'] for z in counts)})
