"""Independent streaming audit of control identities, truncation and exact reuse."""
import argparse
from collections import OrderedDict
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import numpy as np
import pyarrow.parquet as pq
from sos_embed.storage import Store,file_sha,object_sha,utcnow,write_json


def audit(model,kind):
    group=ROOT/'data/analysis_v1/controls'/('minilm_512' if kind=='minilm512' else 'common_text_52k')
    folder=group/model
    manifest=json.loads((folder/'manifest.json').read_text())
    source=ROOT/'data/corpus_clean_v1/embedding_input.parquet' if kind=='minilm512' else group/'input.parquet'
    if file_sha(source)!=manifest['input_sha256']:raise ValueError('Changed input')
    expected=pq.read_table(source,columns=['row_index','work_id','text_sha256'])
    verified=Store(folder,manifest).scan(expected)
    if not verified['complete']:raise ValueError('Incomplete control')
    for name,digest in manifest['source_files'].items():
        if file_sha(ROOT/name)!=digest or file_sha(group/'source_snapshot'/name)!=digest:
            raise ValueError('Changed control source or snapshot')
    native_folder=ROOT/'data/embeddings_v1'/model
    native_manifest=json.loads((native_folder/'manifest.json').read_text())
    if file_sha(native_folder/'manifest.json')!=manifest['native_manifest_sha256']:raise ValueError('Wrong native parent')
    cache=OrderedDict()
    def original(chunk):
        if chunk not in cache:
            start=chunk*1024;end=min(start+1024,500000)
            native=native_folder/'shards'/f'{start:09d}-{end:09d}'
            record=json.loads((native/'commit.json').read_text())
            if record['manifest_sha256']!=object_sha(native_manifest):raise ValueError('Wrong native shard')
            # Hash the same source material that the reuse comparison relies on.
            for name in ['rows.parquet']+[p+'.npy' for p in manifest['poolings']]:
                if file_sha(native/name)!=record['files'][name]:raise ValueError('Changed original reused input')
            cache[chunk]=(pq.read_table(native/'rows.parquet').to_pylist(),
                          {p:np.load(native/(p+'.npy'),mmap_mode='r') for p in manifest['poolings']})
            while len(cache)>16:cache.popitem(last=False)
        cache.move_to_end(chunk)
        return cache[chunk]
    reused=actual_truncated=declared_reused=rows=0
    for shard in sorted((folder/'shards').glob('[0-9]*')):
        records=pq.read_table(shard/'rows.parquet').to_pylist()
        vectors={p:np.load(shard/(p+'.npy'),mmap_mode='r') for p in manifest['poolings']}
        declared_reused+=json.loads((shard/'commit.json').read_text())['stats']['reused_rows']
        for i,row in enumerate(records):
            old_rows,old_vectors=original(row['row_index']//1024)
            j=row['row_index']%1024;old=old_rows[j]
            if old['work_id']!=row['work_id'] or old['text_sha256']!=row.get('source_text_sha256',row['text_sha256']):
                raise ValueError('Changed paper identity/source text')
            same=(row['text_sha256']==old['text_sha256']) and (kind=='common' or not old['truncated'])
            if same:
                for pool in vectors:
                    if not np.array_equal(vectors[pool][i],old_vectors[pool][j]):raise ValueError('Reuse is not bit-identical')
                if row['token_ids_sha256']!=old['token_ids_sha256']:raise ValueError('Changed reused tokens')
                reused+=1
            if not 0<row['tokens_used']<=manifest['model']['max_length']:raise ValueError('Token count outside limit')
            actual_truncated+=bool(row['truncated']);rows+=1
    if reused!=declared_reused or actual_truncated!=verified['truncated_rows']:raise ValueError('Declared statistics differ from rows')
    if kind=='common' and (actual_truncated!=0 or reused!=26857):raise ValueError('Common-text coverage/reuse differs')
    result={'model':model,'control':kind,'rows':rows,'reused_rows_checked_bit_exact':reused,
       'recomputed_rows':rows-reused,'truncated_rows_from_metadata':actual_truncated,
       'manifest_sha256':object_sha(manifest),'input_sha256':manifest['input_sha256'],
       'file_and_identity_validation':verified,'source_files_current_and_snapshot_match':True,'audited_at':utcnow()}
    destination=ROOT/'research/analysis_2026-09-17/extra_output_audit'/f'{kind}_{model}.json'
    write_json(destination,result)
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('scope',choices=['minilm512','common','all']);args=parser.parse_args()
    if args.scope in ('minilm512','all'):audit('minilm','minilm512')
    if args.scope in ('common','all'):
        for model in json.loads((ROOT/'config/analysis_v1.json').read_text())['poolings']:audit(model,'common')
