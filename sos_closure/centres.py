"""Paired reselection of centres, with preserved dates and averaging references."""
import time
import numpy as np
from scipy.stats import spearmanr
from sos_analysis.native_data import NativeData
from sos_analysis.geometry import normalize_rows
from sos_followup.pilot_statistics import cosine_grams,cka_matrix
from sos_deep.subfield_controls import prepared_groups
from sos_embed.storage import run_lock
from .common import *
OLD=ROOT/'data/robustness_v2/centroid_scales'

def apportioned(counts,n):
 counts=np.array(counts,int);v=counts*n/counts.sum();a=np.floor(v).astype(int)
 order=np.lexsort((np.arange(len(a)),-(v-a)));a[order[:n-a.sum()]]+=1
 assert a.sum()==n and np.all(a<=counts);return a

def shuffled(ids,periods,label):
 flat=ids.ravel();out=flat.copy()
 for p in PERIODS:
  ix=np.flatnonzero(periods[flat]==p);out[ix]=rng(label+'/'+str(p)).permutation(flat[ix])
 assert np.array_equal(periods[flat],periods[out]) and np.array_equal(np.sort(flat),np.sort(out))
 return out.reshape(ids.shape)

def prepare(folder,data):
 groups,_=prepared_groups(data.metadata);period=data.metadata['period_start'].to_numpy();field=data.metadata['field_id'].to_numpy()
 labels=json.loads((OLD/'group_labels.json').read_text());panels={'field':[("field",str(f)) for f in FIELDS],'subfield217':[("subfield",s) for s in labels['matched_subfields']]}
 panels['subfield183']=[key for key in panels['subfield217'] if len(groups[key])>=512];assert len(panels['subfield183'])==183
 specs={};records=[]
 for level in ['field','subfield217']:
  keys=panels[level];quotas=np.array([[np.sum(period[groups[k][:256]]==p) for p in PERIODS] for k in keys])
  specs['repeat256_'+level]={'keys':keys,'quotas':quotas,'n':256,'family':'primary','repeats':50}
 for level in ['field','subfield183']:
  keys=panels[level];q512=np.array([[np.sum(period[groups[k][:512]]==p) for p in PERIODS] for k in keys]);q256=np.stack([apportioned(q,256) for q in q512]);q128=np.stack([apportioned(q,128) for q in q256])
  for n,q in [(128,q128),(256,q256),(512,q512)]:specs[f'size{n}_{level}']={'keys':keys,'quotas':q,'n':n,'family':'size','repeats':50}
 selected_dir=folder/'selections';selected_dir.mkdir(exist_ok=True)
 for name,s in specs.items():
  path=selected_dir/(name+'.npz')
  if path.exists():continue
  real=[];random=[]
  for rep in range(50):
   rows=[]
   for k,q in zip(s['keys'],s['quotas']):
    # Same per-period order across sizes makes the samples nested.
    label=f"centres/{s['family']}/{k[0]}/{k[1]}/{rep}"
    rows.append(selected(groups[k],period,q,label))
   ids=np.stack(rows).astype(np.int32);rand=shuffled(ids,period,f'centres/random/{name}/{rep}');real.append(ids);random.append(rand)
   records.append({'design':name,'repeat':rep,'outer':-1,'inner':-1,'seed_label':f"centres/{s['family']}/LEVEL/GROUP/{rep}/PERIOD",'random_seed_label':f'centres/random/{name}/{rep}/PERIOD','real_sha256':ids_sha(ids),'random_sha256':ids_sha(rand)})
  np.savez(path,observed=np.stack(real),random=np.stack(random),quotas=s['quotas'],groups=np.array([int(k[1]) for k in s['keys']]))
 for level in ['field','subfield183']:
  samples=[np.load(selected_dir/f'size{n}_{level}.npz')['observed'] for n in [128,256,512]]
  assert all(set(a).issubset(b) for sm,lg in zip(samples[:-1],samples[1:]) for rep in range(50) for a,b in zip(sm[rep],lg[rep]))
 nested=selected_dir/'nested26.npz'
 if not nested.exists():
  keys=panels['subfield217'];parents=np.array([field[groups[k][0]] for k in keys]);qs=np.array([[np.sum(period[groups[k][:256]]==p) for p in PERIODS] for k in keys]);reals=[];randoms=[];chosen=[]
  for outer in range(50):
   pick=np.array([rng(f'centres/nested/subfield/{outer}/{f}').choice(np.flatnonzero(parents==f)) for f in FIELDS]);chosen.append([int(keys[i][1]) for i in pick])
   for inner in range(10):
    ids=np.stack([selected(groups[keys[i]],period,qs[i],f'centres/nested/articles/{outer}/{inner}/{keys[i][1]}') for i in pick]).astype(np.int32)
    rand=shuffled(ids,period,f'centres/nested/random/{outer}/{inner}');reals.append(ids);randoms.append(rand)
    records.append({'design':'nested26','repeat':outer*10+inner,'outer':outer,'inner':inner,'seed_label':f'centres/nested/articles/{outer}/{inner}/SUBFIELD/PERIOD','random_seed_label':f'centres/nested/random/{outer}/{inner}/PERIOD','real_sha256':ids_sha(ids),'random_sha256':ids_sha(rand)})
  np.savez(nested,observed=np.stack(reals),random=np.stack(randoms),chosen_subfields=np.array(chosen))
 # On a restart, preserve the complete records generated at first preparation.
 if records and not (selected_dir/'records.csv').exists():save_csv(selected_dir/'records.csv',records)
 write_json(selected_dir/'designs.json',{n:{**s,'quotas':s['quotas'].tolist()} for n,s in specs.items()})
 return sorted(selected_dir.glob('*.npz'))

def scores(arrays):
 ck=cka_matrix(cosine_grams(arrays));return np.array([ck[i,j] for i,j in PAIRS])

def main():
 folder=freeze('centres',['sos_closure/centres.py','sos_analysis/native_data.py','sos_analysis/reader.py','sos_analysis/geometry.py','sos_followup/pilot_statistics.py','sos_deep/subfield_controls.py'],['data/robustness_v2/centroid_scales/audit.json',BASE['catalog']])
 with run_lock(folder):
  data=NativeData(ROOT,max_bytes=2*1024**3);paths=prepare(folder,data)
  for model in MODELS:
   target=folder/'models'/model;target.mkdir(parents=True,exist_ok=True)
   if committed(target):continue
   start=time.monotonic();raw=data.get(model+'/'+POOLS[model],slice(None))
   for p in paths:
    dest=target/p.name
    if dest.exists() and dest.with_suffix('.sha.json').exists():assert file_sha(dest)==json.loads(dest.with_suffix('.sha.json').read_text())['sha256'];continue
    source=np.load(p);arrays={}
    for typ in ['observed','random']:
     arr=source[typ];values=[]
     for ids in arr:
      g,n=ids.shape;x=normalize_rows(raw[ids.ravel()]);values.append(x.reshape(g,n,-1).mean(1))
     arrays[typ]=np.stack(values)
    np.savez(dest,**arrays);write_json(dest.with_suffix('.sha.json'),{'sha256':file_sha(dest),'selection_sha256':file_sha(p)})
   commit(target,seconds=time.monotonic()-start)
   print(f'CENTRES {model}: {time.monotonic()-start:.1f}s',flush=True)
  pair_rows=[];rep_rows=[];loo=[]
  for p in paths:
   cubes=[np.load(folder/'models'/m/p.name) for m in MODELS]
   for typ in ['observed','random']:
    for rep in range(cubes[0][typ].shape[0]):
     arrays=[c[typ][rep] for c in cubes];values=scores(arrays)
     info={'design':p.stem,'grouping':typ,'repeat':rep,'centres':len(arrays[0]),'articles_per_centre':int(np.load(p)[typ].shape[-1])}
     rep_rows.append({**info,**stats(values)})
     pair_rows.extend({**info,'model_a':MODELS[i],'model_b':MODELS[j],'cka':float(v)} for (i,j),v in zip(PAIRS,values))
     if p.stem=='repeat256_field' and typ=='observed':
      for index,f in enumerate(FIELDS):
       result=scores([np.delete(a,index,axis=0) for a in arrays]);loo.extend({'selection':rep,'omitted_field':f,'model_a':MODELS[i],'model_b':MODELS[j],'full':float(v),'without':float(w),'change':float(w-v)} for (i,j),v,w in zip(PAIRS,values,result))
   print('CENTRE SCORES',p.stem,flush=True)
  original=[np.load(OLD/(m+'_centroids.npz'))['matched_field'] for m in MODELS];values=scores(original)
  for index,f in enumerate(FIELDS):
   result=scores([np.delete(a,index,axis=0) for a in original]);loo.extend({'selection':-1,'omitted_field':f,'model_a':MODELS[i],'model_b':MODELS[j],'full':float(v),'without':float(w),'change':float(w-v)} for (i,j),v,w in zip(PAIRS,values,result))
  save_csv(folder/'model_pairs.csv',pair_rows);save_csv(folder/'repetitions.csv',rep_rows);save_csv(folder/'leave_one_field_out.csv',loo)
  finish(folder,designs=len(paths),model_pair_rows=len(pair_rows),repetition_rows=len(rep_rows),leave_one_out_rows=len(loo))
if __name__=='__main__':main()
