import hashlib,json,struct,time
from pathlib import Path
import numpy as np
import pyarrow.parquet as pq
import torch
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from sos_followup.input_embeddings import LiteralEncoder, condition_text, OUT, prepare
from sos_analysis.extra_embeddings import NativeBlocks
from sos_embed.runner import CACHE,config,verify_assets
from sos_embed.storage import write_json,utcnow
ROOT=Path.cwd()
prepare();rows=pq.read_table(OUT/'native_input.parquet').slice(0,4).to_pylist()
results=[];torch.set_num_threads(8)
for spec in config()['models']:
    verify_assets(spec);enc=LiteralEncoder(spec,CACHE,'mps');native=NativeBlocks(spec['key'])
    same,audit,stats=enc.encode(rows)
    expected={p:np.stack([native.row(r['row_index'])[1][p] for r in rows]) for p in spec['poolings']}
    errors={p:float(np.max(np.abs(same[p]-expected[p]))) for p in same}
    for p in same:
        assert np.allclose(same[p],expected[p],rtol=1e-4,atol=1e-3),(spec['key'],p,errors)
    cases=[]
    for condition in ['title','abstract']:
        arrays,records,st=enc.encode_literal(rows,condition)
        for r,rec in zip(rows,records):
            txt=r[condition]
            ids=enc.tokenizer(txt,truncation=True,max_length=spec['max_length'],return_token_type_ids=False)['input_ids']
            assert rec['formatted_text_sha256']==hashlib.sha256(txt.encode()).hexdigest()
            assert rec['token_ids_sha256']==hashlib.sha256(struct.pack('<'+'I'*len(ids),*ids)).hexdigest()
        # Separate one-row inference must match the same literal condition in a padded batch.
        one,_,_=enc.encode_literal(rows[:1],condition,1)
        for p in arrays:assert np.allclose(one[p][0],arrays[p][0],rtol=1e-4,atol=1e-3)
        cases.append({'condition':condition,'seconds':st['seconds'],'tokens':[r['tokens_used'] for r in records]})
    results.append({'model':spec['key'],'native_max_absolute_errors':errors,'literal_conditions':cases,'passed':True})
    print(spec['key'],errors,flush=True)
    del enc;torch.mps.empty_cache()
write_json(ROOT/'research/checklist_2026-09-17/input_preflight.json',{'at':utcnow(),'rows':4,'all_models_pass':True,'models':results})
print('ALL PREFLIGHT CHECKS PASSED',flush=True)
