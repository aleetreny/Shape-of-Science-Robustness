"""Post-completion audit and catalog. Reads frozen sources; never runs a model."""
from collections import Counter, defaultdict
import csv
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DERIVED=ROOT/'data/analysis_ready_v1'
IDENTITY=['row_index','work_id','text_sha256']
JOIN=IDENTITY+['cohort','field_id','publication_year','period_start']
QUALITY=['language_ambiguous','possible_mixed_language','abstract_50_79','abstract_over_2000',
         'duplicate_doi','duplicate_text','normalized_text_group','possible_notice',
         'possible_access_message','content_review_flag','content_review_note']


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()


def objsha(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name('.'+path.name+'.partial')
    temporary.write_text(json.dumps(data,indent=2)+'\n')
    os.replace(temporary,path)


def write_csv(name,rows):
    with (HERE/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def relative(path):return str(path.relative_to(ROOT))


def main():
    # Advisory lock survives an interrupted shell and excludes overlapping audits.
    lock=(HERE/'.audit.lock').open('a+')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    save(HERE/'audit_state.json',{'state':'running','pid':os.getpid(),'started_at':datetime.datetime.now(datetime.UTC).isoformat()})
    config=json.loads((ROOT/'config/embeddings_v1.json').read_text())
    source=ROOT/'data/corpus_clean_v1'
    source_manifest=json.loads((source/'embedding_manifest.json').read_text())
    assert sha(source/'corpus.parquet')==source_manifest['corpus_sha256']
    assert sha(source/'embedding_input.parquet')==source_manifest['embedding_input_sha256']
    for scope in ('full','pilot','control'):
        check=json.loads((HERE/(scope+'_verification.json')).read_text())
        assert check['verified'] and len(check['models'])==10
        assert all(m['complete'] and m['rows']==(500000 if scope=='full' else 1300) for m in check['models'])
    full_check={m['model']:m for m in json.loads((HERE/'full_verification.json').read_text())['models']}
    current_env=json.loads((HERE/'model_preflight.json').read_text())['environment']
    assets=json.loads((ROOT/'data/embedding_assets_v1.json').read_text())
    assert assets==json.loads((ROOT/'research/embedding_setup_2026-09-15/assets_manifest.json').read_text())
    columns=JOIN+['field_display_name','subfield_id','subfield_display_name','doi','type','abstract_word_count','title_word_count']+QUALITY
    metadata=pq.read_table(source/'corpus.parquet',columns=columns)
    frozen=pq.read_table(source/'embedding_input.parquet',columns=JOIN)
    assert metadata.select(JOIN).equals(frozen)
    assert len(metadata)==500000 and pc.count_distinct(metadata['work_id']).as_py()==500000
    np.testing.assert_array_equal(metadata['row_index'].to_numpy(),np.arange(500000))
    cohorts=Counter(metadata['cohort'].to_pylist());assert cohorts=={'base':400000,'extra':100000}
    fields=dict(zip(metadata['field_id'].to_pylist(),metadata['field_display_name'].to_pylist()))
    cells=Counter(zip(metadata['field_id'].to_pylist(),metadata['period_start'].to_pylist()))
    assert len(fields)==26 and len(cells)==130
    DERIVED.mkdir(exist_ok=True)
    meta_path=DERIVED/'metadata.parquet'
    # Small derived index only; no abstracts or vectors are copied.
    if meta_path.exists():assert pq.read_table(meta_path).equals(metadata)
    else:pq.write_table(metadata,meta_path,compression='zstd')
    catalog={'schema_version':1,'status':'verified','rows':500000,
             'source_input_sha256':source_manifest['embedding_input_sha256'],
             'source_corpus_sha256':source_manifest['corpus_sha256'],
             'metadata_path':relative(meta_path),'metadata_sha256':sha(meta_path),
             'cohort_counts':dict(cohorts),'normalization':'none','models':{}}
    totals=[];by_cell=[];by_field=[];shard_inventory=[];all_full_text=np.ones(500000,dtype=bool)
    environments=[];bytes_total=0;partial_paths=[]
    for spec in config['models']:
        key=spec['key'];root=ROOT/'data/embeddings_v1'/key
        manifest=json.loads((root/'manifest.json').read_text());environments.append(manifest['environment'])
        assert manifest['model']==spec and manifest['environment']==current_env
        assert manifest['input_sha256']==source_manifest['embedding_input_sha256']
        assert manifest['postprocessing']=='none' and manifest['dtype']=='float32' and manifest['scope']=='full'
        assert manifest['rows']==500000 and manifest['dimension']==spec['dimension']
        for repo,record in manifest['asset_records'].items():assert assets[repo]==record
        for name,digest in manifest['source_files'].items():
            assert sha(ROOT/name)==digest
            assert sha(ROOT/'data/embeddings_v1/source_snapshot'/name)==digest
        validation=json.loads((root/'validation.json').read_text())
        assert validation['complete'] and validation['manifest_sha256']==objsha(manifest)
        entry={'name':spec['name'],'dimension':spec['dimension'],'poolings':spec['poolings'],
               'repo_id':spec['repo_id'],'revision':spec['revision'],'adapter':spec.get('adapter'),
               'max_length':spec['max_length'],'text_format':spec['text_format'],
               'manifest_path':relative(root/'manifest.json'),'manifest_sha256':sha(root/'manifest.json'),
               'shards':[]}
        groups=defaultdict(Counter);offset=0;token_sums=Counter();this_bytes=0
        for folder in sorted((root/'shards').iterdir()):
            if folder.name.startswith('.'):
                partial_paths.append(relative(folder));continue
            commit_path=folder/'commit.json';commit=json.loads(commit_path.read_text())
            assert commit['start']==offset and commit['manifest_sha256']==objsha(manifest)
            rows_path=folder/'rows.parquet';assert sha(rows_path)==commit['files']['rows.parquet']
            table=pq.read_table(rows_path);end=offset+len(table);assert end==commit['end']
            assert table.select(JOIN).equals(frozen.slice(offset,len(table)))
            original=table['tokens_original'].to_numpy();used=table['tokens_used'].to_numpy();trunc=table['truncated'].to_numpy()
            np.testing.assert_array_equal(used,np.minimum(original,spec['max_length']))
            np.testing.assert_array_equal(trunc,original>spec['max_length'])
            last=table['last_content_character'].to_numpy();chars=table['formatted_characters'].to_numpy()
            assert np.all((last>=0)&(last<=chars))
            all_full_text[offset:end]&=~trunc
            token_sums.update({'rows':len(table),'truncated':int(trunc.sum()),'tokens_original':int(original.sum()),'tokens_used':int(used.sum())})
            for fid,period,cohort,t in zip(table['field_id'].to_pylist(),table['period_start'].to_pylist(),table['cohort'].to_pylist(),trunc):
                g=groups[(fid,period,cohort)];g['rows']+=1;g['truncated']+=int(t)
            item={'start':offset,'end':end,'rows_path':relative(rows_path),'rows_sha256':commit['files']['rows.parquet'],
                  'commit_path':relative(commit_path),'commit_sha256':sha(commit_path),'vectors':{}}
            for pool in spec['poolings']:
                path=folder/(pool+'.npy')
                item['vectors'][pool]={'path':relative(path),'sha256':commit['files'][pool+'.npy']}
                this_bytes+=path.stat().st_size
            entry['shards'].append(item)
            shard_inventory.append({'model':key,'start':offset,'end':end,'rows':len(table),'directory':relative(folder),
                                    'rows_sha256':commit['files']['rows.parquet'],'commit_sha256':sha(commit_path)})
            offset=end
        assert offset==500000 and token_sums['truncated']==full_check[key]['truncated_rows']
        assert len(entry['shards'])==489
        for (fid,period,cohort),g in sorted(groups.items()):
            by_cell.append({'model':key,'field_id':fid,'field':fields[fid],'period_start':period,'cohort':cohort,
                            'rows':g['rows'],'truncated':g['truncated'],'truncated_percent':100*g['truncated']/g['rows']})
        for fid in sorted(fields):
            g=sum((v for (f,p,c),v in groups.items() if f==fid),Counter())
            by_field.append({'model':key,'field_id':fid,'field':fields[fid],**g,'truncated_percent':100*g['truncated']/g['rows']})
        base=sum((v for (f,p,c),v in groups.items() if c=='base'),Counter())
        extra=sum((v for (f,p,c),v in groups.items() if c=='extra'),Counter())
        totals.append({'model':key,'name':spec['name'],**token_sums,'truncated_percent':100*token_sums['truncated']/500000,
                       'base_truncated':base['truncated'],'base_truncated_percent':100*base['truncated']/400000,
                       'extra_truncated':extra['truncated'],'extra_truncated_percent':100*extra['truncated']/100000,
                       'vector_files':len(entry['shards'])*len(spec['poolings']),'vector_file_bytes':this_bytes,
                       'inference_hours':full_check[key]['seconds']/3600})
        catalog['models'][key]=entry;bytes_total+=this_bytes
        print('Auditado',key,'500000 filas; variantes',','.join(spec['poolings']),flush=True)
    write_csv('truncation_by_model.csv',totals)
    write_csv('truncation_by_field_period_cohort.csv',by_cell)
    write_csv('truncation_by_field.csv',by_field)
    write_csv('shard_inventory.csv',shard_inventory)
    save(HERE/'catalog.json',catalog)
    # The technical common-text sample has distinct text hashes, but the same source paper IDs.
    native=pq.read_table(ROOT/'data/embedding_pilot_v1/input.parquet')
    common=pq.read_table(ROOT/'data/embedding_control_pilot_v1/input.parquet')
    assert native.select(['row_index','work_id']).equals(common.select(['row_index','work_id']))
    assert native['text_sha256'].to_pylist()==common['source_text_sha256'].to_pylist()
    unchanged=np.array(native['text_sha256'])==np.array(common['text_sha256'])
    max_diffs={}
    for m in config['models']:
        for pool in m['poolings']:
            arrays=[]
            for scope in ('embedding_pilot_v1','embedding_control_pilot_v1'):
                paths=sorted((ROOT/'data'/scope/m['key']/'shards').glob('[0-9]*/'+pool+'.npy'))
                arrays.append(np.concatenate([np.load(p,allow_pickle=False) for p in paths]))
            np.testing.assert_allclose(arrays[0][unchanged],arrays[1][unchanged],atol=0.0002,rtol=0.0001)
            max_diffs[m['key']+'/'+pool]=float(np.max(np.abs(arrays[0][unchanged]-arrays[1][unchanged])))
    control_check=json.loads((HERE/'control_verification.json').read_text())
    assert all(m['truncated_rows']==0 for m in control_check['models'])
    all_fulltext_cells=[]
    for fid,period in sorted(cells):
        mask=(metadata['field_id'].to_numpy()==fid)&(metadata['period_start'].to_numpy()==period)
        all_fulltext_cells.append({'field_id':fid,'field':fields[fid],'period_start':period,'rows':int(mask.sum()),
                                  'full_text_in_all_models':int((mask&all_full_text).sum())})
    write_csv('full_text_coverage_by_field_period.csv',all_fulltext_cells)
    report={'status':'verified','completed_at':datetime.datetime.now(datetime.UTC).isoformat(),
            'models':10,'rows_per_model':500000,'variants':18,'shards_per_model':489,'shard_directories':len(shard_inventory),
            'vector_files':sum(r['vector_files'] for r in totals),'vector_file_bytes':bytes_total,
            'metadata_bytes':meta_path.stat().st_size,'metadata_sha256':sha(meta_path),'catalog_sha256':sha(HERE/'catalog.json'),
            'cohort_counts':dict(cohorts),'fields':26,'field_period_cells':130,'minimum_cell':min(cells.values()),
            'all_models_read_full_text_rows':int(all_full_text.sum()),'partial_directories_excluded':partial_paths,
            'source_corpus_sha256':source_manifest['corpus_sha256'],'source_input_sha256':source_manifest['embedding_input_sha256'],
            'source_environment_matches':True,'saved_and_current_asset_locks_match':True,
            'control_sample_rows':len(common),'unchanged_control_text_rows':int(unchanged.sum()),
            'control_vector_max_abs_differences':max_diffs,'truncation':totals,
            'new_scientific_analyses_started':False,'source_or_embedding_files_modified':False}
    save(HERE/'audit_summary.json',report)
    save(HERE/'audit_state.json',{'state':'complete','pid':os.getpid(),'completed_at':report['completed_at']})
    print('AUDITORIA COMPLETA',report['models'],'modelos',report['vector_files'],'archivos de vectores',flush=True)


if __name__=='__main__':main()
