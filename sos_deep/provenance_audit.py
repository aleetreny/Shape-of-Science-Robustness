"""Read-only verification of frozen OpenAlex responses, corpus and ten native models."""
import json
import sqlite3
from pathlib import Path
from sos_deep.artifacts import ROOT,save_csv,freeze,finish
from sos_embed.storage import file_sha,write_json,run_lock

OUT=ROOT/'data/robustness_v2/provenance'


def main():
    with run_lock(OUT):
        freeze(OUT,['sos_deep/provenance_audit.py','sos_deep/artifacts.py'],
            ['data/corpus_clean_v1/embedding_manifest.json','data/corpus_clean_v1/source_snapshot_manifest.json',
             'research/embedding_final_audit_2026-09-17/catalog.json','config/embeddings_v1.json'],
            {'purpose':'Read-only raw response, corpus, saved source and native vector verification',
             'snapshot_warning':'Collected API responses over time, not a global simultaneous OpenAlex snapshot'})
        rows=[];seen={};counts={}
        for base in ['data/corpus_500k','data/corpus_clean_v1']:
            conn=sqlite3.connect((ROOT/base/'state.sqlite').as_uri()+'?mode=ro',uri=True)
            pages=conn.execute('SELECT block_id,page,path,sha256,n_records,retrieved_at FROM pages ORDER BY block_id,page').fetchall()
            for block,page,rel,digest,n,time in pages:
                path=ROOT/base/rel;actual=path.resolve()
                if actual not in seen:seen[actual]=file_sha(path)
                assert seen[actual]==digest,(base,rel)
                rows.append({'collection':base,'block':block,'page':page,'path':str(path.relative_to(ROOT)),
                    'sha256':digest,'records':n,'retrieved_at':time,'is_symlink':path.is_symlink()})
            counts[base]={'pages':len(pages),'first_retrieved_at':min(p[-1] for p in pages),
                          'last_retrieved_at':max(p[-1] for p in pages)}
            conn.close()
        assert counts['data/corpus_500k']['pages']==6138 and counts['data/corpus_clean_v1']['pages']==6139
        save_csv(OUT/'openalex_response_inventory.csv',rows)
        manifest=json.loads((ROOT/'data/corpus_clean_v1/embedding_manifest.json').read_text())
        for name,key in [('corpus.parquet','corpus_sha256'),('embedding_input.parquet','embedding_input_sha256')]:
            assert file_sha(ROOT/'data/corpus_clean_v1'/name)==manifest[key]
        original=json.loads((ROOT/'data/corpus_500k/validation.json').read_text())
        assert file_sha(ROOT/'data/corpus_500k/corpus.parquet')==original['parquet_sha256']
        prep=json.loads((ROOT/'data/corpus_clean_v1/source_snapshot_manifest.json').read_text())
        for name,digest in prep.items():assert file_sha(ROOT/'data/corpus_clean_v1/source_snapshot'/name)==digest,name
        catalog=json.loads((ROOT/'research/embedding_final_audit_2026-09-17/catalog.json').read_text())
        vector_files=0;asset_files=0;vectors_bytes=0;model_rows=[];commits=0;hashed_assets={}
        for key,m in catalog['models'].items():
            mp=ROOT/m['manifest_path'];assert file_sha(mp)==m['manifest_sha256']
            mf=json.loads(mp.read_text())
            assert mf['input_sha256']==manifest['embedding_input_sha256']
            for name,digest in mf['source_files'].items():
                assert file_sha(ROOT/'data/embeddings_v1/source_snapshot'/name)==digest
                assert file_sha(ROOT/name)==digest,name
            for repo,record in mf['asset_records'].items():
                folder=ROOT/'.benchmark-models'/('models--'+repo.replace('/','--'))/'snapshots'/record['revision']
                for name,info in record['files'].items():
                    path=folder/name;actual=path.resolve()
                    if actual not in hashed_assets:hashed_assets[actual]=file_sha(path)
                    assert hashed_assets[actual]==info['sha256'],(key,name)
                    asset_files+=1
            cursor=0
            for shard in m['shards']:
                assert shard['start']==cursor;cursor=shard['end']
                for pathkey,hashkey in [('commit_path','commit_sha256'),('rows_path','rows_sha256')]:
                    assert file_sha(ROOT/shard[pathkey])==shard[hashkey]
                commits+=1
                for pool,v in shard['vectors'].items():
                    path=ROOT/v['path'];assert file_sha(path)==v['sha256'],(key,pool,shard['start'])
                    vector_files+=1;vectors_bytes+=path.stat().st_size
            assert cursor==500000
            model_rows.append({'model':key,'repo_id':m['repo_id'],'revision':m['revision'],
                'adapter':json.dumps(m['adapter'],sort_keys=True),'max_length':m['max_length'],
                'dimension':m['dimension'],'poolings':'|'.join(m['poolings']),
                'manifest_path':m['manifest_path'],'manifest_sha256':m['manifest_sha256'],
                'rows':cursor,'shards':len(m['shards'])})
            print('PROVENANCE',key,'verified',flush=True)
        save_csv(OUT/'model_versions.csv',model_rows)
        write_json(OUT/'summary.json',{'raw_responses':counts,'unique_raw_files':len(seen),
            'original_source_unchanged':True,'clean_corpus_unchanged':True,
            'native_models':len(model_rows),'native_commits':commits,'native_vector_files':vector_files,
            'native_vector_bytes':vectors_bytes,'asset_records_checked':asset_files,
            'saved_source_hashes_verified':True,'current_embedding_source_matches_frozen':True,
            'openalex_scope':'Frozen downloaded pages, not the full OpenAlex database or a simultaneous snapshot'})
        finish(OUT,originals_unchanged=True,raw_responses_verified=True,native_vectors_verified=True,
               model_weights_and_versions_verified=True)
        print('RAW DATA AND MODEL PROVENANCE COMPLETE',flush=True)


if __name__=='__main__':main()
