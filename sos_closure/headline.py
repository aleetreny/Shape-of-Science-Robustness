"""Direct repeated neighbor replacement under model and text changes."""
import time
import numpy as np
from sos_analysis.neighbors import independent_neighbors
from sos_embed.storage import run_lock
from .common import *
from .inputs import load_inputs
from .fast_neighbors import full_ranks,restrict,overlaps
VARIANTS=[(m,POOLS[m],c) for c in ['title_abstract','title'] for m in MODELS]+[(m,p,c) for c in ['title_abstract','title'] for p in ['cls','sep'] for m in D['word_models']]
def index(m,c,recipe):return VARIANTS.index((m,recipe if m in D['word_models'] else POOLS[m],c))
def main():
 folder=freeze('headline',['sos_closure/headline.py','sos_closure/inputs.py','sos_closure/fast_neighbors.py','sos_closure/kernels.c','sos_deep/input_analysis52.py','sos_analysis/neighbors.py'],['data/robustness_v2/inputs/input_manifest.json','data/robustness_v2/input_comparisons/audit.json','data/robustness_v2/input_recipes/audit.json','data/robustness_closure_v1/technical/tests.json'])
 with run_lock(folder):
  meta,arrays,parents=load_inputs(alternatives=True);write_json(folder/'input_manifests.json',parents)
  ids=meta['row_index'].to_numpy();fields=meta['field_id'].to_numpy();periods=meta['period_start'].to_numpy()
  for f in FIELDS:
   target=folder/'fields'/str(f);target.mkdir(parents=True,exist_ok=True)
   if committed(target):continue
   start=time.monotonic();pos=np.flatnonzero(fields==f);fi=ids[pos];assert len(fi)==2000 and np.all(np.diff(fi)>0)
   selections=np.stack([np.sort(np.concatenate([rng(f'headline/{f}/{rep}/{p}').choice(np.flatnonzero(periods[pos]==p),200,replace=False) for p in PERIODS])) for rep in range(50)])
   np.save(target/'selected_global_ids.npy',fi[selections]);np.save(target/'full_global_ids.npy',fi)
   selection_rows=[{'field_id':f,'repeat':rep,'seed_label':f'headline/{f}/{rep}/PERIOD','selection_sha256':ids_sha(fi[s])} for rep,s in enumerate(selections)];save_csv(target/'selection_records.csv',selection_rows)
   neighbors=[];proofs=0;rank_records=[]
   for variant in VARIANTS:
    x=arrays[variant][pos];ranks=full_ranks(x,fi);nn=restrict(ranks,selections,fi)
    s=selections[0];queries=np.linspace(0,len(s)-1,5,dtype=int);check=independent_neighbors(x[s],fi[s],x[s[queries]],fi[s[queries]],k=50)
    assert np.array_equal(nn[0,queries],check),(f,variant);proofs+=len(queries)
    rank_records.append({'model':variant[0],'pool':variant[1],'input':variant[2],'rank_sha256':ids_sha(ranks),'neighbor_sha256':ids_sha(nn)})
    neighbors.append(nn)
   nn=np.stack(neighbors);del neighbors
   pair_rows=[];effects=[];grand=[]
   for rep in range(50):
    nr=np.ascontiguousarray(nn[:,rep])
    for recipe,ks in [('mean',[10,25,50]),('cls',[25]),('sep',[25])]:
     comparisons=[(index(MODELS[i],'title_abstract',recipe),index(MODELS[j],'title_abstract',recipe)) for i,j in PAIRS]+[(index(m,'title_abstract',recipe),index(m,'title',recipe)) for m in MODELS]
     ov=overlaps(nr,comparisons,ks)
     for ki,k in enumerate(ks):
      model_change=1-ov[:45,ki];input_change=1-ov[45:,ki]
      info={'field_id':f,'repeat':rep,'recipe':recipe,'k':k}
      for pi,(i,j) in enumerate(PAIRS):pair_rows.append({**info,'model_a':MODELS[i],'model_b':MODELS[j],'model_overlap':float(ov[pi,ki]),'model_change':float(model_change[pi])})
      for mi,m in enumerate(MODELS):
       own=float(np.mean([v for (i,j),v in zip(PAIRS,model_change) if mi in (i,j)]));inp=float(input_change[mi]);effects.append({**info,'model':m,'model_change':own,'title_only_change':inp,'title_minus_model':inp-own})
      grand.append({**info,'model_change':float(model_change.mean()),'title_only_change':float(input_change.mean()),'title_minus_model':float(input_change.mean()-model_change.mean())})
   save_csv(target/'model_pairs.csv',pair_rows);save_csv(target/'effects.csv',effects);save_csv(target/'field_repetitions.csv',grand);save_csv(target/'rank_audit.csv',rank_records)
   commit(target,independent_queries=proofs,representations=len(VARIANTS),repetitions=50,candidates=1000,seconds=time.monotonic()-start)
   del nn
   print(f'HEADLINE Field {f}: {time.monotonic()-start:.1f}s',flush=True)
  for name in ['model_pairs','effects','field_repetitions']:
   rows=[r for f in FIELDS for r in read_csv(folder/'fields'/str(f)/(name+'.csv'))];save_csv(folder/(name+'.csv'),rows)
  finish(folder,fields=26,repetitions=50,independent_queries=26*36*5)
if __name__=='__main__':main()
