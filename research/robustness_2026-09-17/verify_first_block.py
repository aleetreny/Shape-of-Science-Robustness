from pathlib import Path
import hashlib,json,struct,sys
import numpy as np
import pyarrow.parquet as pq
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root))
from sos_deep.inputs52 import PriorRows,LiteralEncoder,OUT
from sos_embed.runner import config,CACHE
from sos_embed.storage import Store,file_sha
spec=next(m for m in config()['models'] if m['key']=='minilm')
folder=OUT/'title/minilm';manifest=json.loads((folder/'manifest.json').read_text())
expected=pq.read_table(OUT/'title_input.parquet')
scan=Store(folder,manifest).scan(expected)
assert scan['rows']==1024 and not scan['complete']
shard=next((folder/'shards').glob('[0-9]*'))
rows=pq.read_table(shard/'rows.parquet').to_pylist()
texts=expected.slice(0,1024).to_pylist()
vectors=np.load(shard/'mean.npy');prior=PriorRows('minilm','title')
encoder=LiteralEncoder(spec,CACHE,'mps')
reused=0;new=[]
for i,(row,source) in enumerate(zip(rows,texts)):
 assert all(row[k]==source[k] for k in ['row_index','work_id','text_sha256','source_text_sha256'])
 assert row['formatted_text_sha256']==hashlib.sha256(source['title'].encode()).hexdigest()
 token_ids=encoder.tokenizer(source['title'],truncation=True,max_length=spec['max_length'])['input_ids']
 assert row['token_ids_sha256']==hashlib.sha256(struct.pack('<'+'I'*len(token_ids),*token_ids)).hexdigest()
 old=prior.row(row['row_index'])
 if old:
  assert row['reuse_origin']=='pilot26k' and np.array_equal(vectors[i],old[1]['mean'])
  reused+=1
 else:new.append(i);assert row['reuse_origin']=='new_inference'
errors=[]
for i in new[:4]:
 x,_,_=encoder.encode_literal([texts[i]],'title',1)
 error=float(np.max(np.abs(x['mean'][0]-vectors[i])))
 assert np.allclose(x['mean'][0],vectors[i],rtol=1e-4,atol=2e-5),error
 errors.append(error)
proof={'all_pass':True,'rows_checked':len(rows),'reused_rows_exact':reused,'new_rows':len(new),
       'tokens_checked':len(rows),'individually_reencoded_new_rows':4,'maximum_batch_absolute_error':max(errors),
       'manifest_sha256':file_sha(folder/'manifest.json'),'script_sha256':file_sha(__file__)}
(root/'research/robustness_2026-09-17/input52_preflight.json').write_text(json.dumps(proof,indent=2)+'\n')
checkpoint={str(p.relative_to(root)):file_sha(p) for p in shard.iterdir() if p.is_file()}
(root/'research/robustness_2026-09-17/input52_resume_checkpoint.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
print(json.dumps(proof,indent=2))
