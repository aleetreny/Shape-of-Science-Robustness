"""Bounded SPECTER2/SciNCL sensitivity probe; historical sample, not final results."""
import collections
import gc
import hashlib
import json
import os
from pathlib import Path
import time

os.environ.setdefault('HF_HUB_DISABLE_IMPLICIT_TOKEN','1')
os.environ.setdefault('TOKENIZERS_PARALLELISM','false')
import numpy as np
import pyarrow.dataset as ds
import pyarrow.parquet as pq
import torch
from transformers import AutoTokenizer,AutoModel

OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[1]
SOURCE=Path('/Users/alejandrotreny/Workspace/Mapping-Science')
SEED=20260916
# These diagnostic tolerances are fixed before reading cross-model results.
CRITERIA={'max_abs_median_change_1024_to_2048':0.02,'max_empirical_95_range_at_2048':0.04,'note':'Screening tolerance, not a journal requirement or universal power calculation.'}
(OUT/'sample_size_probe_criteria.json').write_text(json.dumps(CRITERIA,indent=2))
cases={('27',2000):[],('27',2020):[],('34',2000):[],('34',2020):[]}
rng=np.random.default_rng(SEED); available=collections.Counter()
for batch in pq.ParquetFile(SOURCE/'data/processed/works_text_2000_2024_400py.parquet').iter_batches(batch_size=65536,columns=['work_id','title','abstract','field_id','publication_year']):
    field=np.array(batch.column('field_id').to_pylist()); year=np.array(batch.column('publication_year').to_pylist())
    for case in cases:
        idx=np.flatnonzero((field==case[0]) & (year>=case[1]) & (year<=case[1]+4))
        available[str(case)]+=len(idx)
        if len(idx):
            priority=rng.random(len(idx)); keep=np.argsort(priority)[:4096]
            selected=batch.take(idx[keep]).to_pylist()
            cases[case].extend((float(priority[k]),r) for k,r in zip(keep,selected))
            cases[case]=sorted(cases[case],key=lambda x:x[0])[:4096]
rows=[]; boundaries=[]
for case, selected in cases.items():
    start=len(rows); rows.extend(r for _,r in selected);boundaries.append((case,start,len(rows)))
    assert len(selected)>=2048
ids=[r['work_id'] for r in rows]; locations={}
index=ds.dataset(SOURCE/'data/processed/embedding_index.parquet').to_table(columns=['work_id','embedding_shard_file','embedding_row_in_shard'],filter=ds.field('work_id').isin(ids)).to_pylist()
for r in index: locations[r['work_id']]=(r['embedding_shard_file'],r['embedding_row_in_shard'])
assert len(locations)==len(rows)
specter=np.empty((len(rows),768),dtype=np.float32); byshard=collections.defaultdict(list)
for i,r in enumerate(rows):
    shard,row=locations[r['work_id']];byshard[shard].append((i,row))
for shard, positions in byshard.items():
    a=np.load(SOURCE/'embeddings/specter2_v1_2000_2024_400py'/shard,mmap_mode='r')
    ii, jj=zip(*positions);specter[list(ii)]=a[list(jj)]
revision=json.loads((OUT/'benchmark_model_revisions.json').read_text())[0]['revision']
tokenizer=AutoTokenizer.from_pretrained('malteos/scincl',revision=revision,cache_dir=ROOT/'.benchmark-models',local_files_only=True)
model=AutoModel.from_pretrained('malteos/scincl',revision=revision,cache_dir=ROOT/'.benchmark-models',local_files_only=True,dtype=torch.float32,attn_implementation='eager').eval().to('mps')
torch.set_num_threads(8);vectors=[];t=time.perf_counter(); checkpoints=[]
with torch.inference_mode():
    for start in range(0,len(rows),16):
        texts=[r['title']+tokenizer.sep_token+r['abstract'] for r in rows[start:start+16]]
        inputs=tokenizer(texts,padding=True,truncation=True,max_length=512,return_tensors='pt')
        inputs={k:v.to('mps') for k,v in inputs.items()}
        vectors.append(model(**inputs).last_hidden_state[:,0,:].cpu().numpy())
        if (start+16)%2048==0:
            elapsed=time.perf_counter()-t;checkpoints.append(dict(n=start+16,seconds=elapsed));print('Encoded',start+16,'/',len(rows),'papers;',round(elapsed,1),'seconds',flush=True)
elapsed=time.perf_counter()-t;scincl=np.concatenate(vectors)
np.save(OUT/'sample_size_scincl_vectors.npy',scincl);np.save(OUT/'sample_size_specter_vectors.npy',specter)
del model;gc.collect();torch.mps.empty_cache()

def hsic_u(x,y):
    n=x.shape[0];dx=(x*x).sum(1);dy=(y*y).sum(1)
    ksum=x@x.sum(0)-dx;lsum=y@y.sum(0)-dy
    offdiag_trace=(x.T@y).square().sum()-(dx*dy).sum()
    return (offdiag_trace+ksum.sum()*lsum.sum()/((n-1)*(n-2))-2*(ksum*lsum).sum()/(n-2))/(n*(n-3))
def cka(x,y):return (hsic_u(x,y)/(hsic_u(x,x)*hsic_u(y,y)).sqrt()).item()
# Verify finite-sample correction against its explicit off-diagonal Gram formula.
cpu_x=torch.tensor(specter[:32],dtype=torch.float64);cpu_y=torch.tensor(scincl[:32],dtype=torch.float64)
k=cpu_x@cpu_x.T;l=cpu_y@cpu_y.T;k.fill_diagonal_(0);l.fill_diagonal_(0);n=len(k)
direct=((k*l).sum()+k.sum()*l.sum()/((n-1)*(n-2))-2*(k.sum(0)*l.sum(0)).sum()/(n-2))/(n*(n-3))
assert torch.allclose(direct,hsic_u(cpu_x,cpu_y),rtol=1e-8,atol=1e-8)
results=[]
for case,start,end in boundaries:
    x=torch.tensor(specter[start:end],device='mps');y=torch.tensor(scincl[start:end],device='mps')
    x=torch.nn.functional.normalize(x,dim=1);y=torch.nn.functional.normalize(y,dim=1)
    cpu=cka(x[:32].cpu().double(),y[:32].cpu().double());gpu=cka(x[:32],y[:32]);assert abs(cpu-gpu)<1e-3
    sampling=[]; rg=np.random.default_rng(SEED+start)
    for size in [256,512,1024,2048]:
        scores=[]
        for repeat in range(20):
            sel=torch.tensor(rg.choice(len(x),size,replace=False),device='mps');scores.append(cka(x[sel],y[sel]))
        sampling.append(dict(n=size,median=float(np.median(scores)),p025=float(np.quantile(scores,.025)),p975=float(np.quantile(scores,.975)),values=scores))
    result=dict(field_id=case[0],period_start=case[1],pool_size=end-start,full_pool_cka=cka(x,y),samples=sampling,passes_screen=bool(abs(sampling[-1]['median']-sampling[-2]['median'])<=.02 and sampling[-1]['p975']-sampling[-1]['p025']<=.04))
    results.append(result);print('Size probe',case,'pool',end-start,'pass',result['passes_screen'],flush=True)
report=dict(criteria=CRITERIA,source='Historical TFM corpus with its existing subfield-year selection; not the future probability sample.',models=['legacy SPECTER2','malteos/scincl@'+revision],seed=SEED,n_encoded=len(rows),encoding_seconds=elapsed,papers_per_second=len(rows)/elapsed,encoding_checkpoints=checkpoints,source_cell_counts=available,selected_ids=ids,input_ids_sha256=hashlib.sha256('\n'.join(ids).encode()).hexdigest(),results=results,note='Empirical resampling ranges are conditional on these finite pilot pools, not population confidence intervals. Four extreme Field-period cases and one model pair cannot certify all future comparisons.')
(OUT/'sample_size_probe.json').write_text(json.dumps(report,indent=2))
print('DONE: total encoding',round(elapsed,1),'seconds',flush=True)
