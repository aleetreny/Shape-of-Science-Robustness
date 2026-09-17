"""Measure real inference on MPS, not a final scientific comparison."""
import gc
import hashlib
import json
import os
from pathlib import Path
import resource
import time

os.environ.setdefault('HF_HUB_DISABLE_IMPLICIT_TOKEN','1')
os.environ.setdefault('TOKENIZERS_PARALLELISM','false')
import numpy as np
import torch
import transformers
from transformers import AutoModel, AutoTokenizer

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
rows=json.loads((OUT/'local_benchmark_texts.json').read_text())
records=json.loads((OUT/'benchmark_model_revisions.json').read_text())
torch.set_num_threads(8)
assert torch.backends.mps.is_available()
all_results=[]
for record in records:
    model_id=record['model']; limit=512 if model_id=='malteos/scincl' else 384
    tokenizer=AutoTokenizer.from_pretrained(model_id,revision=record['revision'],cache_dir=ROOT/'.benchmark-models',local_files_only=True)
    model=AutoModel.from_pretrained(model_id,revision=record['revision'],cache_dir=ROOT/'.benchmark-models',local_files_only=True,torch_dtype=torch.float32,attn_implementation='eager').eval().to('mps')
    texts=[r['title']+tokenizer.sep_token+r['abstract'] if model_id=='malteos/scincl' else r['title']+'\n\n'+r['abstract'] for r in rows]
    lengths=[len(x) for x in tokenizer(texts,add_special_tokens=True,truncation=False)['input_ids']]
    def encode(texts,batch_size,padding=True):
        result=[]; padded=0
        with torch.inference_mode():
            for i in range(0,len(texts),batch_size):
                inputs=tokenizer(texts[i:i+batch_size],padding=padding,truncation=True,max_length=limit,return_tensors='pt')
                padded+=inputs['input_ids'].numel()
                inputs={k:v.to('mps') for k,v in inputs.items()}
                hidden=model(**inputs).last_hidden_state
                if model_id=='malteos/scincl':
                    vector=hidden[:,0,:]
                else:
                    mask=inputs['attention_mask'].unsqueeze(-1)
                    vector=(hidden*mask).sum(1)/mask.sum(1).clamp(min=1)
                result.append(vector.cpu().numpy())
        torch.mps.synchronize()
        return np.concatenate(result),padded
    encode(texts[:16],8)
    trials=[]
    for batch in [8,16,32]:
        start=time.perf_counter(); _,pad=encode(texts[:128],batch);seconds=time.perf_counter()-start
        trial=dict(n=128,batch_size=batch,seconds=seconds,papers_per_second=128/seconds,padded_tokens=pad)
        trials.append(trial);print(model_id,'batch',batch,'papers/s',round(trial['papers_per_second'],2),flush=True)
    best=max(trials,key=lambda x:x['papers_per_second'])['batch_size']
    start=time.perf_counter();vectors,padded=encode(texts,best);seconds=time.perf_counter()-start
    assert vectors.shape==(len(rows),768) and np.isfinite(vectors).all()
    np.save(OUT/(model_id.rsplit('/',1)[-1]+'_vectors.npy'),vectors)
    result=dict(model=model_id,revision=record['revision'],device='mps',dtype='float32',attention='eager',max_length=limit,n=len(rows),batch_size=best,seconds=seconds,papers_per_second=len(rows)/seconds,padded_tokens=padded,token_lengths_percentiles=np.percentile(lengths,[0,25,50,75,90,95,100]).tolist(),truncated_fraction=float(np.mean(np.array(lengths)>limit)),process_peak_rss_gib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**30,mps_driver_allocated_gib=torch.mps.driver_allocated_memory()/2**30,mps_current_allocated_gib=torch.mps.current_allocated_memory()/2**30,batch_trials=trials)
    all_results.append(result)
    report=dict(torch=torch.__version__,transformers=transformers.__version__,numpy=np.__version__,input_ids_sha256=hashlib.sha256('\n'.join(r['work_id'] for r in rows).encode()).hexdigest(),results=all_results,note='Short warm benchmark on local historical sample; no claim about sustained thermals, different future encoders, or scientific convergence.')
    (OUT/'embedding_benchmark.json').write_text(json.dumps(report,indent=2))
    print('COMPLETE',model_id,round(seconds,2),'seconds for',len(rows),'papers',flush=True)
    del model,tokenizer;gc.collect();torch.mps.empty_cache()
