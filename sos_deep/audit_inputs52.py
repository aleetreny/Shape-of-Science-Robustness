"""Independent text/identity/token audit of finished input pilot stores; no inference."""
import argparse,hashlib,json,struct
from pathlib import Path
import numpy as np
import pyarrow.parquet as pq
from transformers import AutoTokenizer
from sos_embed.runner import CACHE,config,verify_assets
from sos_embed.models import snapshot_path,format_text
from sos_embed.storage import Store,file_sha,write_json,utcnow
from sos_analysis.extra_embeddings import NativeBlocks
from sos_deep.inputs52 import PriorRows

ROOT=Path(__file__).resolve().parents[1];INP=ROOT/'data/robustness_v2/inputs';OUT=ROOT/'research/robustness_2026-09-17/input_audit'


def audit(model,condition):
    folder=INP/condition/model['key'];p=folder/'manifest.json'
    if not p.exists():return False
    manifest=json.loads(p.read_text());meta_path=INP/(('native' if condition=='title_abstract' else condition)+'_input.parquet')
    expected=pq.read_table(meta_path);check=Store(folder,manifest).scan(expected)
    if not check['complete']:return False
    OUT.mkdir(parents=True,exist_ok=True);target=OUT/(model['key']+'_'+condition+'.json')
    if target.exists():
        old=json.loads(target.read_text())
        assert old['manifest_sha256']==file_sha(p) and old['input_sha256']==file_sha(meta_path)
        # Store.scan above verifies vectors on every pass, even if token audit already saved.
        return True
    verify_assets(model)
    source=manifest['source_files']
    for name,sha in source.items():
        assert file_sha(ROOT/name)==sha and file_sha(INP/'source_snapshot'/name)==sha,name
    original=pq.read_table(INP/'native_input.parquet').to_pylist();rows=expected.to_pylist()
    tokenizer=AutoTokenizer.from_pretrained(snapshot_path(CACHE,model),local_files_only=True,trust_remote_code=False,use_fast=True)
    saved=[];native=NativeBlocks(model['key']) if condition=='title_abstract' else None
    prior=PriorRows(model['key'],condition) if condition!='title_abstract' else None
    if prior:assert manifest['pilot26k_manifest_sha256']==prior.manifest_sha256
    exact=0;prior_exact=0;fresh=0;truncated=0;tokens_total=0;lost_total=0
    for shard in sorted((folder/'shards').glob('[0-9]*')):
        meta=pq.read_table(shard/'rows.parquet').to_pylist();offset=len(saved)
        batch=rows[offset:offset+len(meta)];orig=original[offset:offset+len(meta)]
        texts=[format_text(r['title'],r['abstract'],model['text_format'],tokenizer.sep_token) if condition=='title_abstract' else r[condition] for r in batch]
        ids=tokenizer(texts,truncation=True,max_length=model['max_length'],padding=False,return_token_type_ids=False)['input_ids']
        full=tokenizer(texts,truncation=False,padding=False,return_token_type_ids=False,verbose=False)['input_ids']
        arrays={pool:np.load(shard/(pool+'.npy'),allow_pickle=False) for pool in model['poolings']}
        for j,(r,o,m,txt,tok,orig_tokens) in enumerate(zip(batch,orig,meta,texts,ids,full)):
            assert r['row_index']==o['row_index']==m['row_index'] and r['work_id']==o['work_id']==m['work_id']
            source_sha=hashlib.sha256((o['title']+'\n\n'+o['abstract']).encode()).hexdigest();assert source_sha==o['text_sha256']
            if condition!='title_abstract':
                assert r['source_text_sha256']==m['source_text_sha256']==source_sha
                assert r['text_sha256']==m['text_sha256']==hashlib.sha256(r[condition].encode()).hexdigest()
                assert r['title']==o['title'] and r['abstract']==o['abstract']
            assert m['formatted_text_sha256']==hashlib.sha256(txt.encode()).hexdigest()
            assert m['token_ids_sha256']==hashlib.sha256(struct.pack('<'+'I'*len(tok),*tok)).hexdigest()
            assert m['tokens_used']==len(tok) and m['tokens_original']==len(orig_tokens)
            assert m['truncated']==(len(orig_tokens)>model['max_length'])
            truncated+=m['truncated'];tokens_total+=len(orig_tokens);lost_total+=len(orig_tokens)-len(tok)
            if native:
                old,vec=native.row(r['row_index'])
                assert all(old[k]==m[k] for k in ['row_index','work_id','text_sha256','token_ids_sha256'])
                for pool in arrays:assert np.array_equal(arrays[pool][j],vec[pool]),(model['key'],pool,r['row_index'])
                exact+=1
                assert m['reuse_origin']=='native500k'
            else:
                previous=prior.row(r['row_index'])
                if previous is None:
                    assert m['reuse_origin']=='new_inference'
                    fresh+=1
                else:
                    old,vec=previous
                    assert m['reuse_origin']=='pilot26k'
                    assert all(old[k]==m[k] for k in ['row_index','work_id','text_sha256','source_text_sha256','token_ids_sha256'])
                    for pool in arrays:assert np.array_equal(arrays[pool][j],vec[pool]),(model['key'],pool,r['row_index'])
                    prior_exact+=1
        saved.extend(meta)
    assert len(saved)==52000
    if condition=='title_abstract':assert exact==52000 and fresh==prior_exact==0
    else:assert prior_exact==fresh==26000 and exact==0
    write_json(target,{'all_pass':True,'completed_at':utcnow(),'model':model['key'],'condition':condition,'rows':len(saved),
        'manifest_sha256':file_sha(p),'input_sha256':file_sha(meta_path),'native_exact_reuse':exact,'pilot26k_exact_reuse':prior_exact,'new_inference_rows':fresh,'truncated_rows':int(truncated),
        'original_tokens':tokens_total,'lost_tokens':lost_total,'token_sequences_checked':len(saved),
        'source_identity_text_order_checked':True,'all_saved_poolings_checked':True,'auditor_sha256':file_sha(__file__)})
    print('AUDIT',model['key'],condition,'PASS',flush=True)
    return True


def main():
    p=argparse.ArgumentParser();p.add_argument('--require-complete',action='store_true');a=p.parse_args()
    complete=0
    for model in config()['models']:
        for condition in ['title_abstract','title','abstract']:complete+=audit(model,condition)
    if a.require_complete and complete!=30:raise ValueError(f'Only {complete}/30 finished audits')
    write_json(OUT/'audit_summary.json',{'all_complete':complete==30,'complete_conditions':complete,'target':30,'updated_at':utcnow()})
    print('AUDITS COMPLETE',complete,'/30',flush=True)
if __name__=='__main__':main()
