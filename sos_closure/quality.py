"""Existing quality filter applied to exact matched-query neighbor searches."""
import gc,time
import numpy as np
from sos_analysis.native_data import NativeData
from sos_analysis.run_shape import strict_quality
from sos_analysis.neighbors import exact_neighbors,independent_neighbors
from sos_embed.storage import run_lock
from .common import *
from .fast_neighbors import overlaps
from .inputs import load_inputs
OLD=ROOT/'data/analysis_v1/neighbors/local'

def candidates(source,clean,queries,n,label):
 order=rng(label).permutation(np.sort(source));remaining=order[~np.isin(order,queries)]
 original=np.sort(np.concatenate([queries,remaining[:n-len(queries)]]));filtered=np.sort(np.concatenate([queries,remaining[clean[remaining]][:n-len(queries)]]))
 assert len(original)==len(filtered)==n and np.all(clean[filtered]);assert set(queries).issubset(original) and set(queries).issubset(filtered)
 return original,filtered

def prepare(folder,data,clean):
 target=folder/'selections';target.mkdir(exist_ok=True);records=[]
 for (f,p),ids in data.cells().items():
  valid=ids[clean[ids]];queries=np.sort(rng(f'quality/queries/{f}/{p}').choice(valid,100,replace=False));arrays={'original_all':ids,'filtered_all':valid,'queries':queries}
  for n in [1024,2048]:
   if len(valid)<n:continue
   original,filtered=candidates(ids,clean,queries,n,f'quality/candidates/{f}/{p}/{n}');arrays[f'original_{n}']=original;arrays[f'filtered_{n}']=filtered
  path=target/f'{f}_{p}.npz'
  if path.exists():
   old=np.load(path);assert all(np.array_equal(old[k],v) for k,v in arrays.items())
  else:np.savez(path,**arrays)
  for k,v in arrays.items():records.append({'field_id':f,'period':p,'selection':k,'rows':len(v),'selection_sha256':ids_sha(v),'seed_base':f'quality/queries|candidates/{f}/{p}'})
 save_csv(target/'records.csv',records)

def native(folder,data,clean):
 prepare(folder,data,clean)
 for model in MODELS:
  target=folder/'models'/model;target.mkdir(parents=True,exist_ok=True)
  if committed(target):continue
  start=time.monotonic();raw=data.get(model+'/'+POOLS[model],slice(None));proofs=0
  for (f,p) in data.cells():
   dest=target/f'{f}_{p}.npz';cp=dest.with_suffix('.json')
   if dest.exists() and cp.exists():
    c=json.loads(cp.read_text());assert file_sha(dest)==c['sha256'];proofs+=c['independent_queries'];continue
   sels=np.load(folder/'selections'/dest.name);ids=sels['filtered_all'];result={}
   nn,_=exact_neighbors(raw[ids],ids,k=50);chosen=np.linspace(0,len(ids)-1,5,dtype=int)
   check=independent_neighbors(raw[ids],ids,raw[ids[chosen]],ids[chosen],k=50);assert np.array_equal(nn[chosen],check),(model,f,p)
   result['filtered_all']=nn;queries=sels['queries'];count=5
   for n in [1024,2048]:
    if f'original_{n}' not in sels:continue
    for typ in ['original','filtered']:
     ref=sels[f'{typ}_{n}'];neighbors,_=exact_neighbors(raw[ref],ref,queries=raw[queries],query_ids=queries,k=50)
     test=independent_neighbors(raw[ref],ref,raw[queries[:2]],queries[:2],k=50);assert np.array_equal(neighbors[:2],test)
     result[f'{typ}_{n}']=neighbors;count+=2
   np.savez(dest,**result);write_json(cp,{'sha256':file_sha(dest),'selection_sha256':file_sha(folder/'selections'/dest.name),'independent_queries':count});proofs+=count
  commit(target,independent_queries=proofs,seconds=time.monotonic()-start)
  print(f'QUALITY {model}: {time.monotonic()-start:.1f}s',flush=True)
 rows=[]
 for (f,p) in data.cells():
  sels=np.load(folder/'selections'/f'{f}_{p}.npz');original_ids=sels['original_all'];valid=sels['filtered_all'];positions=np.searchsorted(original_ids,valid);assert np.array_equal(original_ids[positions],valid)
  old=[];new=[np.load(folder/'models'/m/f'{f}_{p}.npz') for m in MODELS]
  for m in MODELS:
   source=OLD/f'{f}_{p}'/m;c=json.loads((source/'commit.json').read_text())
   for n,h in c['files'].items():assert file_sha(source/n)==h
   assert np.array_equal(np.load(source/'query_row_index.npy'),original_ids)
   old.append(np.load(source/'neighbors.npy'))
  old=np.stack(old);tests=[('all',old[:,positions],np.stack([a['filtered_all'] for a in new]),len(original_ids),len(valid),len(valid))]
  original_all=overlaps(old,PAIRS)
  for n in [1024,2048]:
   if f'original_{n}' in sels:tests.append((str(n),np.stack([a[f'original_{n}'] for a in new]),np.stack([a[f'filtered_{n}'] for a in new]),n,n,100))
  for scope,a,b,na,nb,nq in tests:
   before=overlaps(a,PAIRS);after=overlaps(b,PAIRS)
   for pi,(i,j) in enumerate(PAIRS):
    for ki,k in enumerate([10,25,50]):
     v=float(before[pi,ki]);w=float(after[pi,ki]);rows.append({'scope':scope,'field_id':f,'period':p,'model_a':MODELS[i],'model_b':MODELS[j],'k':k,'queries':nq,'original_candidates':na,'filtered_candidates':nb,'original_all_queries_overlap':float(original_all[pi,ki]) if scope=='all' else None,'original_same_queries_overlap':v,'filtered_overlap':w,'change_pp':100*(w-v),'absolute_change_pp':100*abs(w-v),'original_adjusted':(v-k/(na-1))/(1-k/(na-1)),'filtered_adjusted':(w-k/(nb-1))/(1-k/(nb-1))})
 save_csv(folder/'native_comparisons.csv',rows)
 return len(rows)

def input_control(folder,clean):
 target=folder/'input';target.mkdir(exist_ok=True)
 if committed(target):return
 meta,arrays,parents=load_inputs(False);write_json(target/'input_manifests.json',parents)
 ids=meta['row_index'].to_numpy();fields=meta['field_id'].to_numpy();periods=meta['period_start'].to_numpy();lookup={int(i):j for j,i in enumerate(ids)}
 variants=[(m,POOLS[m],c) for c in ['title_abstract','title','abstract'] for m in MODELS];rows=[];effects=[];proofs=0;selections={}
 comparisons=PAIRS+[(i,10+i) for i in range(10)]+[(i,20+i) for i in range(10)]
 for f in FIELDS:
  start=time.monotonic();queries=[];orig=[];filt=[]
  for p in PERIODS:
   source=ids[(fields==f)&(periods==p)];eligible=source[clean[source]];q=np.sort(rng(f'quality/input/queries/{f}/{p}').choice(eligible,20,replace=False));o,c=candidates(source,clean,q,200,f'quality/input/candidates/{f}/{p}');queries.extend(q);orig.extend(o);filt.extend(c)
  queries=np.sort(queries);orig=np.sort(orig);filt=np.sort(filt);selections[f'{f}_queries']=queries;selections[f'{f}_original']=orig;selections[f'{f}_filtered']=filt
  qp=np.array([lookup[int(i)] for i in queries]);values={}
  for typ,ref in [('original',orig),('filtered',filt)]:
   rp=np.array([lookup[int(i)] for i in ref]);nn=[]
   for variant in variants:
    x=arrays[variant];neighbors,_=exact_neighbors(x[rp],ref,queries=x[qp],query_ids=queries,k=50)
    check=independent_neighbors(x[rp],ref,x[qp[:2]],queries[:2],k=50);assert np.array_equal(neighbors[:2],check);proofs+=2;nn.append(neighbors)
   values[typ]=overlaps(np.stack(nn),comparisons)
  for pi,(i,j) in enumerate(comparisons):
   for ki,k in enumerate([10,25,50]):
    v=float(values['original'][pi,ki]);w=float(values['filtered'][pi,ki]);rows.append({'field_id':f,'model_a':variants[i][0],'input_a':variants[i][2],'model_b':variants[j][0],'input_b':variants[j][2],'k':k,'queries':100,'candidates':1000,'original_overlap':v,'filtered_overlap':w,'change_pp':100*(w-v),'absolute_change_pp':100*abs(w-v)})
  for ki,k in enumerate([10,25,50]):
   for typ in ['original','filtered']:
    v=values[typ];mc=float((1-v[:45,ki]).mean());tc=float((1-v[45:55,ki]).mean());ac=float((1-v[55:65,ki]).mean());effects.append({'field_id':f,'k':k,'corpus':typ,'model_change':mc,'title_only_change':tc,'abstract_only_change':ac,'title_minus_model':tc-mc})
  print(f'QUALITY INPUT Field {f}: {time.monotonic()-start:.1f}s',flush=True)
 np.savez(target/'selections.npz',**selections);save_csv(target/'comparisons.csv',rows);save_csv(target/'effects.csv',effects);commit(target,independent_queries=proofs,fields=26)

def main():
 folder=freeze('quality',['sos_closure/quality.py','sos_closure/fast_neighbors.py','sos_closure/kernels.c','sos_closure/inputs.py','sos_analysis/run_shape.py','sos_analysis/neighbors.py','sos_analysis/native_data.py','sos_analysis/reader.py','sos_deep/input_analysis52.py'],['config/analysis_v1.json',BASE['catalog'],'data/analysis_v1/neighbors/manifest.json','data/robustness_closure_v1/technical/tests.json'])
 with run_lock(folder):
  data=NativeData(ROOT,max_bytes=2*1024**3);clean=strict_quality(data);assert clean.sum()==448886
  np.save(folder/'quality_mask.npy',clean);assert np.array_equal(clean,np.load(ROOT/'research/robustness_closure_2026-09-20/quality_mask.npy'))
  count=native(folder,data,clean);del data;gc.collect()
  input_control(folder,clean);finish(folder,quality_retained=int(clean.sum()),native_comparisons=count,cells=130,cells2048=63,input_fields=26)
if __name__=='__main__':main()
