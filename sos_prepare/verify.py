"""Read-only replay and full-table checks before declaring text preparation ready."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import random

import pyarrow.parquet as pq

from sos_download.records import normalize_work, text_hash
from sos_download.store import utcnow, write_json
from .export import file_sha
from .quality import reasons_for, normalized, digest


def independent_allocation(counts, total):
    lo,hi = min(counts.values()),max(counts.values())+total
    while lo<hi:
        level=(lo+hi+1)//2
        if sum(max(0,level-n) for n in counts.values())<=total:lo=level
        else:hi=level-1
    out={cell:max(0,lo-n) for cell,n in counts.items()}
    rest=total-sum(out.values())
    for cell in sorted(c for c,n in counts.items() if n+out[c]==lo)[:rest]:out[cell]+=1
    assert sum(out.values())==total
    return out


def verify(runner, reports):
    root=runner.store.root;db=runner.store.db;q=runner.quality
    config=runner.config;reports=Path(reports)
    if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok':
        raise ValueError('Preparation database integrity check failed')
    # Exhaustion would require a separately verified redistribution path.
    assert not db.execute('SELECT 1 FROM allocations WHERE exhausted=1').fetchone(), 'Review exhausted cells before certifying'
    expected_source_sha=json.loads((runner.source/'validation.json').read_text())['parquet_sha256']
    assert file_sha(runner.source/'corpus.parquet')==expected_source_sha,'Original corpus changed'
    seen=set();base_cells={(f,p):0 for f in config['field_ids'] for p in config['period_starts']}
    extra_cells=Counter();targets=None;counts=Counter();total=0;page_checks=0;candidate_checks=0
    records=db.execute('SELECT record_json FROM works ORDER BY selection_order')
    blocks=db.execute('SELECT b.* FROM processed_blocks p JOIN blocks b ON b.id=p.block_id ORDER BY p.sequence').fetchall()
    for block in blocks:
        cohort=block['cohort'];cell=(block['field_id'],block['period_start'])
        if cohort=='extra':
            assert counts['base']==config['base_target'],'Complement precedes full clean base'
            if targets is None:targets=independent_allocation(base_cells,config['extra_target'])
            remaining=targets[cell]-extra_cells[cell]
        else:
            assert counts['extra']==0
            remaining=config['base_target']-counts['base']
        assert remaining>0
        candidates=[];sample_ids=set()
        pages=db.execute('SELECT * FROM pages WHERE block_id=? ORDER BY page',(block['id'],)).fetchall()
        assert len(pages)==block['n_pages']
        for p in pages:
            path=root/p['path'];raw_bytes=path.read_bytes()
            assert hashlib.sha256(raw_bytes).hexdigest()==p['sha256']
            envelope=json.loads(gzip.decompress(raw_bytes));params=envelope['parameters']
            assert params==runner.params(block,p['page'])
            assert envelope['retrieved_at']==p['retrieved_at']
            assert len(envelope['response']['results'])==p['n_records']
            assert envelope['response']['meta']['count']==block['sample_result_count']
            for i,raw in enumerate(envelope['response']['results']):
                assert raw['id'] not in sample_ids;sample_ids.add(raw['id'])
                candidates.append((raw,p['page'],i,envelope['retrieved_at']))
            page_checks+=1
        random.Random(block['seed']).shuffle(candidates)
        decisions=db.execute('SELECT * FROM decisions WHERE block_id=? ORDER BY candidate_rank',(block['id'],)).fetchall()
        accepted=0;examined=0;stats=Counter(candidates=len(candidates),accepted=0)
        for rank,(raw,page,index,retrieved) in enumerate(candidates):
            if accepted>=remaining:break
            r,reason=normalize_work(raw,config)
            why=[reason] if reason else []
            outcome='rejected_original_filter' if reason else None
            wid=raw['id'].rsplit('/',1)[-1]
            sha=None if r is None else r['text_sha256']
            if r:
                d=json.loads(q.db.execute('SELECT diagnosis FROM quality WHERE text_sha256=?',(sha,)).fetchone()[0])
                why=reasons_for(r,d,q.policy)
                if why:outcome='rejected_quality'
                elif wid in seen:outcome,why='duplicate_work_id',['already_selected']
                else:
                    outcome='accepted';accepted+=1;total+=1;counts[cohort]+=1;seen.add(wid)
                    if cohort=='base':base_cells[(r['field_id'],r['period_start'])]+=1
                    else:
                        assert (r['field_id'],r['period_start'])==cell
                        extra_cells[cell]+=1
                    expected=json.loads(next(records)[0])
                    assert all(expected[k]==v for k,v in r.items()),f'Original record mismatch {wid}'
                    assert expected['selection_order']==total and expected['cohort']==cohort
                    assert (expected['source_block'],expected['source_page'],expected['source_page_index'],expected['source_seed'],expected['retrieved_at'])==(block['id'],page,index,block['seed'],retrieved)
                    assert (expected['legacy_id_present'],expected['legacy_text_match'])==runner.legacy.lookup(wid,sha)
            saved=decisions[rank]
            assert (saved['candidate_rank'],saved['work_id'],saved['text_sha256'],saved['outcome'],json.loads(saved['reasons']))==(rank,wid,sha,outcome,why)
            stats[outcome]+=1;examined+=1;candidate_checks+=1
        assert len(decisions)==examined
        stats['not_examined_after_target']=len(candidates)-examined
        assert dict(stats)==json.loads(block['stats_json'])
        print(f'Selección reproducida: {total:,}.',flush=True)
    assert next(records,None) is None
    assert counts==dict(base=config['base_target'],extra=config['extra_target'])
    if targets is None:targets=independent_allocation(base_cells,config['extra_target'])
    assert all(extra_cells[cell]==n for cell,n in targets.items())
    assert len(seen)==total
    corpus=pq.ParquetFile(root/'corpus.parquet');inputs=pq.ParquetFile(root/'embedding_input.parquet')
    assert corpus.metadata.num_rows==inputs.metadata.num_rows==total
    doi_dups={r[0] for r in db.execute('SELECT doi FROM works WHERE doi IS NOT NULL GROUP BY doi HAVING count(*)>1')}
    text_dups={r[0] for r in db.execute('SELECT text_sha256 FROM works GROUP BY text_sha256 HAVING count(*)>1')}
    raw_records=db.execute('SELECT record_json FROM works ORDER BY selection_order')
    position=0;ids_sha=hashlib.sha256();texts_sha=hashlib.sha256()
    for batch,input_batch in zip(corpus.iter_batches(batch_size=5000),inputs.iter_batches(batch_size=5000),strict=True):
        for r,inp in zip(batch.to_pylist(),input_batch.to_pylist(),strict=True):
            expected=json.loads(next(raw_records)[0])
            assert all(r[k]==v for k,v in expected.items())
            assert r['row_index']==position and r['selection_order']==position+1
            assert r['text_sha256']==text_hash(r['title'],r['abstract'])
            assert r['normalized_text_group']==digest(normalized(r['title']).casefold()+'\n\n'+normalized(r['abstract']).casefold())
            assert r['duplicate_doi']==(r['doi'] in doi_dups) and r['duplicate_text']==(r['text_sha256'] in text_dups)
            d=json.loads(q.db.execute('SELECT diagnosis FROM quality WHERE text_sha256=?',(r['text_sha256'],)).fetchone()[0])
            assert not reasons_for(r,d,q.policy)
            for key in ('language_ambiguous','possible_mixed_language','possible_notice','possible_access_message','abstract_over_2000'):
                assert r[key]==d[key]
            assert r['abstract_detected_language']==d['abstract_language'] and r['abstract_language_score']==d['abstract_score']
            assert r['title_detected_language']==d['title_language'] and json.loads(r['language_segments_json'])==d['segments']
            review=q.policy.get('reviewed_records',{}).get(r['work_id'])
            assert r['content_review_flag']==bool(review and review['action']=='keep_flagged')
            assert r['content_review_note']==(review['reason'] if r['content_review_flag'] else None)
            assert all(r[k]==v for k,v in inp.items())
            ids_sha.update((r['work_id']+'\n').encode());texts_sha.update((r['work_id']+'\t'+r['text_sha256']+'\n').encode())
            position+=1
    assert position==total and next(raw_records,None) is None
    manifest=json.loads((root/'embedding_manifest.json').read_text())
    assert manifest['ordered_work_ids_sha256']==ids_sha.hexdigest()
    assert manifest['ordered_ids_text_hashes_sha256']==texts_sha.hexdigest()
    assert manifest['corpus_sha256']==file_sha(root/'corpus.parquet')
    assert manifest['embedding_input_sha256']==file_sha(root/'embedding_input.parquet')
    identity=runner.store.get_meta('preparation_identity')
    repo=Path(__file__).resolve().parents[1]
    assert all(file_sha(repo/name)==sha for name,sha in identity['source_hashes'].items())
    result=dict(status='passed',completed_at=utcnow(),rows=total,counts=dict(counts),pages_verified=page_checks,
                candidates_replayed=candidate_checks,fields=len(config['field_ids']),field_period_cells=len(base_cells),
                minimum_cell=min(base_cells[c]+extra_cells[c] for c in base_cells),
                original_corpus_unchanged=True,additional_api_pages=manifest['additional_api_pages'],
                checks=['full_random_selection_replay','every_candidate_decision_replayed','every_selected_record_against_raw_response',
                        'independent_supplement_allocation','all_legacy_flags','all_parquet_rows','all_input_rows_and_order',
                        'all_quality_flags_and_exclusion_rules','frozen_input_hashes','database_integrity','original_corpus_hash'],
                model_runs_started=False)
    manifest['status']='prepared_and_verified'
    write_json(root/'embedding_manifest.json',manifest)
    write_json(reports/'preparation_summary.json',manifest)
    write_json(reports/'final_validation.json',result)
    write_json(root/'validation.json',{**result,'parquet_sha256':manifest['corpus_sha256']})
    runner.store.set_meta('clean_complete',result)
    runner.status('corpus limpio preparado y verificado',validation=result)
    print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
    return result


def preflight(root):
    root=Path(root)
    manifest=json.loads((root/'embedding_manifest.json').read_text())
    assert manifest['status']=='prepared_and_verified','Independent verification is unfinished'
    assert file_sha(root/'corpus.parquet')==manifest['corpus_sha256'],'Corpus changed'
    assert file_sha(root/'embedding_input.parquet')==manifest['embedding_input_sha256'],'Input changed'
    rows=pq.ParquetFile(root/'embedding_input.parquet').metadata.num_rows
    assert rows==manifest['rows']==500000
    return dict(status='ready_for_model_configuration',rows=rows,counts=manifest['counts'],
                input=str((root/'embedding_input.parquet').resolve()),
                message='Datos preparados. Antes de calcular: fijar modelos, versiones y formato de entrada de cada modelo.',
                models_started=False)
