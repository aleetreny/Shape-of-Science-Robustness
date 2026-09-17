"""Freeze aligned text inputs and diagnostic flags without running embeddings."""
from collections import Counter
import csv
import hashlib
import json
import os
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from sos_download.store import utcnow, write_json
from .quality import reasons_for, normalized, digest
from .runner import readonly


def file_sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()


def export_prepared(runner, reports):
    root = runner.store.root
    reports = Path(reports);reports.mkdir(parents=True,exist_ok=True)
    q = runner.quality
    db = runner.store.db
    source = readonly(runner.source/'state.sqlite')
    old = {r[0]:r[1] for r in source.execute('SELECT work_id,cohort FROM works')}
    selected = {r[0]:r[1] for r in db.execute('SELECT work_id,cohort FROM works')}
    origins = dict(db.execute('SELECT block_id,origin FROM origins'))
    extra_types = [('row_index',pa.int64()),('source_origin',pa.string()),('title_detected_language',pa.string()),
                   ('abstract_detected_language',pa.string()),('abstract_language_score',pa.float64()),
                   ('language_ambiguous',pa.bool_()),('possible_mixed_language',pa.bool_()),
                   ('possible_notice',pa.bool_()),('possible_access_message',pa.bool_()),
                   ('abstract_over_2000',pa.bool_()),('language_segments_json',pa.string()),
                   ('normalized_text_group',pa.string()),('content_review_flag',pa.bool_()),('content_review_note',pa.string())]
    original_schema = pq.ParquetFile(runner.source/'corpus.parquet').schema_arrow
    schema = pa.schema(list(original_schema)+[pa.field(name,t) for name,t in extra_types])
    input_names = ['row_index','work_id','title','abstract','text_sha256','cohort','field_id','period_start',
                   'publication_year','language_ambiguous','possible_mixed_language','abstract_50_79',
                   'duplicate_doi','duplicate_text','normalized_text_group','possible_notice','possible_access_message',
                   'content_review_flag','content_review_note']
    input_schema = pa.schema([schema.field(name) for name in input_names])
    main_temp = root/'corpus.parquet.tmp'
    input_temp = root/'embedding_input.parquet.tmp'
    doi_dups = {r[0] for r in db.execute('SELECT doi FROM works WHERE doi IS NOT NULL GROUP BY doi HAVING count(*)>1')}
    text_dups = {r[0] for r in db.execute('SELECT text_sha256 FROM works GROUP BY text_sha256 HAVING count(*)>1')}
    stats = Counter();ids_sha = hashlib.sha256();texts_sha = hashlib.sha256();rows = 0
    norm_groups = Counter()
    with pq.ParquetWriter(main_temp,schema,compression='zstd') as writer, pq.ParquetWriter(input_temp,input_schema,compression='zstd') as inputs:
        cursor = db.execute('SELECT record_json FROM works ORDER BY selection_order')
        while batch := cursor.fetchmany(5000):
            records = []
            for row in batch:
                r = json.loads(row[0]);sha = r['text_sha256']
                diagnosis = json.loads(q.db.execute('SELECT diagnosis FROM quality WHERE text_sha256=?',(sha,)).fetchone()[0])
                if reasons_for(r,diagnosis,q.policy):
                    raise ValueError('A selected record violates the fixed quality rules')
                r.update(row_index=rows,source_origin=origins[r['source_block']],
                         title_detected_language=diagnosis['title_language'],abstract_detected_language=diagnosis['abstract_language'],
                         abstract_language_score=diagnosis['abstract_score'],language_segments_json=json.dumps(diagnosis['segments']),
                         normalized_text_group=digest(normalized(r['title']).casefold()+'\n\n'+normalized(r['abstract']).casefold()),
                         duplicate_doi=r['doi'] in doi_dups,duplicate_text=sha in text_dups)
                review=q.policy.get('reviewed_records',{}).get(r['work_id'])
                r['content_review_flag']=bool(review and review['action']=='keep_flagged')
                r['content_review_note']=review['reason'] if r['content_review_flag'] else None
                stats['content_review_flag']+=int(r['content_review_flag'])
                for key in ('language_ambiguous','possible_mixed_language','possible_notice','possible_access_message','abstract_over_2000'):
                    r[key] = diagnosis[key]
                    stats[key] += int(r[key])
                stats['abstract_50_79'] += int(r['abstract_50_79'])
                stats['source_'+r['source_origin']] += 1
                stats['legacy_text_match'] += int(r['legacy_text_match'])
                stats['old_id_retained'] += int(r['work_id'] in old)
                stats['old_extra_moved_to_base'] += int(old.get(r['work_id'])=='extra' and r['cohort']=='base')
                norm_groups[r['normalized_text_group']] += 1
                ids_sha.update((r['work_id']+'\n').encode())
                texts_sha.update((r['work_id']+'\t'+sha+'\n').encode())
                records.append(r);rows += 1
            table = pa.Table.from_pylist(records,schema=schema)
            writer.write_table(table);inputs.write_table(table.select(input_names))
            print(f'Entrada común preparada: {rows:,}.',flush=True)
    for temp,dest in ((main_temp,root/'corpus.parquet'),(input_temp,root/'embedding_input.parquet')):
        with temp.open('rb') as handle:os.fsync(handle.fileno())
        os.replace(temp,dest)
    removed_reasons = Counter();removed = 0
    with (reports/'original_records_not_selected.csv').open('w',newline='') as f:
        out = csv.writer(f);out.writerow(['work_id','original_cohort','field_id','period_start','reason','text_sha256'])
        for row in source.execute('SELECT record_json FROM works ORDER BY selection_order'):
            r = json.loads(row[0])
            if r['work_id'] in selected:continue
            diagnosis = json.loads(q.db.execute('SELECT diagnosis FROM quality WHERE text_sha256=?',(r['text_sha256'],)).fetchone()[0])
            reasons = reasons_for(r,diagnosis,q.policy)
            if not reasons:reasons = ['not_reselected_after_clean_base_and_reallocation']
            removed += 1;removed_reasons.update(reasons)
            out.writerow([r['work_id'],r['cohort'],r['field_id'],r['period_start'],';'.join(reasons),r['text_sha256']])
    source.close()
    with (reports/'quality_exclusions.csv').open('w',newline='') as f:
        out = csv.writer(f);out.writerow(['source_block','candidate_rank','work_id','text_sha256','reasons'])
        out.writerows(db.execute("SELECT block_id,candidate_rank,work_id,text_sha256,reasons FROM decisions WHERE outcome='rejected_quality' ORDER BY block_id,candidate_rank"))
    with (reports/'field_period_counts.csv').open('w',newline='') as f:
        out = csv.writer(f);out.writerow(['field_id','period_start','base','extra','total'])
        out.writerows(db.execute("SELECT field_id,period_start,sum(cohort='base'),sum(cohort='extra'),count(*) FROM works GROUP BY 1,2 ORDER BY 1,2"))
    with (reports/'field_year_counts.csv').open('w',newline='') as f:
        out = csv.writer(f);out.writerow(['field_id','publication_year','cohort','n'])
        out.writerows(db.execute("SELECT field_id,json_extract(record_json,'$.publication_year'),cohort,count(*) FROM works GROUP BY 1,2,3 ORDER BY 1,2,3"))
    with (reports/'field_summary.csv').open('w',newline='') as f:
        out = csv.writer(f);out.writerow(['field_id','field_name','base','extra','total'])
        out.writerows(db.execute("SELECT field_id,json_extract(record_json,'$.field_display_name'),sum(cohort='base'),sum(cohort='extra'),count(*) FROM works GROUP BY 1 ORDER BY 1"))
    manifest = dict(status='exported_pending_independent_verification',created_at=utcnow(),rows=rows,
                    counts=runner.store.counts(),policy_path='config/cleaning_v1.json',policy_sha256=file_sha(q.policy_path),
                    source_original_sha256=json.loads((runner.source/'validation.json').read_text())['parquet_sha256'],
                    corpus_sha256=file_sha(root/'corpus.parquet'),embedding_input_sha256=file_sha(root/'embedding_input.parquet'),
                    ordered_work_ids_sha256=ids_sha.hexdigest(),ordered_ids_text_hashes_sha256=texts_sha.hexdigest(),
                    text_hash_definition='SHA256(title + two newline characters + abstract), exact UTF-8 strings',
                    ordering='row_index from 0 to rows-1; selection_order=row_index+1; base before extra',
                    raw_original_root=str(runner.source),raw_references='Original gzip pages are relative symlinks; retain original data directory.',
                    model_runs_started=False,model_specific_formatting_and_versions='pending',
                    stats=dict(stats),original_records_not_reselected=removed,original_removal_reason_counts=dict(removed_reasons),
                    additional_api_pages=db.execute("SELECT count(*) FROM pages p JOIN origins o ON o.block_id=p.block_id WHERE o.origin='additional'").fetchone()[0],
                    duplicates=dict(doi_groups=len(doi_dups),exact_text_groups=len(text_dups),
                                    normalized_text_groups=sum(v>1 for v in norm_groups.values()),
                                    normalized_text_excess=sum(v-1 for v in norm_groups.values() if v>1)),
                    limitations=['Language classification is imperfect; ambiguous and mixed-language records are retained and flagged.',
                                 'Distinct OpenAlex IDs with matching DOI/text remain marked, not merged; unique study counts are not claimed.',
                                 'Title/abstract retained verbatim. No translation, generated replacement or model-specific truncation.',
                                 'No guarantee that all metadata/abstract errors have been detected.'])
    write_json(root/'embedding_manifest.json',manifest)
    write_json(reports/'preparation_summary.json',manifest)
    write_json(root/'validation.json',{**json.loads((root/'validation.json').read_text()),
                                     'parquet_sha256':manifest['corpus_sha256'],
                                     'status':'exported_pending_independent_verification'})
    return manifest
