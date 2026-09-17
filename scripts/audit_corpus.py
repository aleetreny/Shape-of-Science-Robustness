"""Read-only audit of finished download blocks, independent reports outside the downloader.

Runs incrementally; --watch waits for more blocks until the final Parquet exists.
Never instantiates the downloader Store or changes its database/configuration/modules.
"""
import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import fcntl
import gzip
import hashlib
import json
from pathlib import Path
import random
import re
import sqlite3
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from sos_download.records import normalize_work

DATA = ROOT/'data/corpus_500k'
CACHE = ROOT/'data/corpus_audit'
REPORTS = ROOT/'research/corpus_audit_2026-09-15'
NOTICE = re.compile(r'^(?:retracted|withdrawn|retraction|erratum|corrigendum|editorial|expression of concern)\b|^(?:correction|author correction|publisher correction)\s*(?:to\b|:)', re.I)
WORDS = re.compile(r'\b\w+\b')


def now(): return datetime.now(timezone.utc).isoformat()
def canonical(value): return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
def sha(value): return hashlib.sha256(value.encode()).hexdigest()


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name+'.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
    temp.replace(path)


def readonly(path):
    db = sqlite3.connect(path.resolve().as_uri()+'?mode=ro',uri=True,timeout=30)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA query_only=ON')
    return db


def allocation(counts, slots, exhausted=()):
    """Independent implementation: find a common floor, then break ties by cell ID."""
    available = {k:v for k,v in counts.items() if k not in exhausted}
    result = {k:0 for k in counts}
    if not slots: return result
    if not available: raise AssertionError('No available cells for remaining supplement')
    low,high = min(available.values()),max(available.values())+slots
    while low < high:
        mid=(low+high+1)//2
        if sum(max(0,mid-n) for n in available.values()) <= slots:low=mid
        else:high=mid-1
    for key,value in available.items():result[key]=max(0,low-value)
    remaining=slots-sum(result.values())
    for key in sorted(k for k in available if available[k]+result[k]==low)[:remaining]:
        result[key]+=1
    assert sum(result.values())==slots
    return result


class Auditor:
    def __init__(self):
        CACHE.mkdir(parents=True,exist_ok=True);REPORTS.mkdir(parents=True,exist_ok=True)
        self.source=readonly(DATA/'state.sqlite')
        self.config=json.loads(self.source.execute("SELECT value FROM meta WHERE key='config'").fetchone()[0])
        assert self.config==json.loads((ROOT/'config/corpus.json').read_text())
        expected=json.loads(self.source.execute("SELECT value FROM meta WHERE key='implementation'").fetchone()[0])
        assert all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==value for name,value in expected.items())
        self.legacy=readonly(ROOT/'data/cache/legacy_index.sqlite')
        self.db=sqlite3.connect(CACHE/'audit.sqlite');self.db.row_factory=sqlite3.Row
        self.db.executescript('''
            CREATE TABLE IF NOT EXISTS audited_blocks(id INTEGER PRIMARY KEY,fingerprint TEXT NOT NULL,report TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS selected(work_id TEXT PRIMARY KEY,selection_order INTEGER UNIQUE,
                cohort TEXT,field_id INTEGER,period_start INTEGER,year INTEGER,subfield_id TEXT,topic_id TEXT,
                doi TEXT,text_sha TEXT,normalized_text_sha TEXT,abstract_sha TEXT,record_sha TEXT,
                title TEXT,abstract_words INTEGER,title_words INTEGER,legacy_id INTEGER,legacy_text INTEGER,
                flags TEXT);
            CREATE INDEX IF NOT EXISTS cohort_idx ON selected(cohort);
            CREATE INDEX IF NOT EXISTS field_idx ON selected(field_id,period_start);
            CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT);
        ''')
        identity=canonical(dict(config=self.config,created_at=json.loads(self.source.execute("SELECT value FROM meta WHERE key='created_at'").fetchone()[0])))
        old=self.db.execute("SELECT value FROM meta WHERE key='source_identity'").fetchone()
        assert not old or old[0]==identity,'Audit cache belongs to another download'
        code_sha=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        old_code=self.db.execute("SELECT value FROM meta WHERE key='audit_code_sha'").fetchone()
        assert not old_code or old_code[0]==code_sha,'Audit implementation changed; use a fresh audit cache'
        with self.db:
            self.db.execute('INSERT OR REPLACE INTO meta VALUES(?,?)',('source_identity',identity))
            self.db.execute('INSERT OR REPLACE INTO meta VALUES(?,?)',('audit_code_sha',code_sha))
        self.seen={r[0] for r in self.db.execute('SELECT work_id FROM selected')}
        self.counts=Counter(dict(self.db.execute('SELECT cohort,count(*) FROM selected GROUP BY cohort')))
        self.cells={(f,p):0 for f in self.config['field_ids'] for p in self.config['period_starts']}
        for row in self.db.execute('SELECT field_id,period_start,count(*) FROM selected GROUP BY 1,2'):
            self.cells[(row[0],row[1])]=row[2]
        self.exhausted=set()
        for row in self.db.execute('SELECT report FROM audited_blocks'):
            report=json.loads(row[0])
            if report['exhausted']:self.exhausted.add(tuple(report['cell']))

    def close(self):
        self.source.close();self.db.close();self.legacy.close()

    def audit_block(self, block):
        bid=block['id']
        pages=self.source.execute('SELECT * FROM pages WHERE block_id=? ORDER BY page',(bid,)).fetchall()
        selected=[json.loads(r[0]) for r in self.source.execute('SELECT record_json FROM works WHERE block_id=? ORDER BY selection_order',(bid,)).fetchall()]
        assert len(pages)==block['n_pages']
        assert [p['page'] for p in pages]==list(range(1,block['n_pages']+1))
        candidates=[];raw_ids=set();rejections=Counter();by_cell={};file_hashes=[]
        first_at=last_at=None
        for page in pages:
            path=DATA/page['path'];compressed=path.read_bytes()
            assert hashlib.sha256(compressed).hexdigest()==page['sha256'],f'Page integrity: {path.name}'
            file_hashes.append(page['sha256'])
            envelope=json.loads(gzip.decompress(compressed))
            params=envelope['parameters'];response=envelope['response']
            assert not any(k.lower() in ('api_key','authorization') for k in params)
            year0,year1=(2000,2024) if block['cohort']=='base' else (block['period_start'],block['period_start']+4)
            field='!null' if block['cohort']=='base' else str(block['field_id'])
            expected_filter=f'publication_year:{year0}-{year1},type:article|review|conference-paper,language:en,has_abstract:true,is_retracted:false,is_paratext:false,primary_topic.field.id:{field}'
            assert params['corpus']=='core' and params['filter']==expected_filter
            assert params['seed']==block['seed'] and params['sample']==block['sample_size']
            assert params['page']==page['page'] and params['per_page']==self.config['per_page']
            assert 'sort' not in params
            assert response['meta']['count']==block['sample_result_count']
            expected_n=max(0,min(params['per_page'],min(block['sample_size'],response['meta']['count'])-(page['page']-1)*params['per_page']))
            assert len(response['results'])==expected_n==page['n_records']
            assert envelope['retrieved_at']==page['retrieved_at']
            first_at=first_at or envelope['retrieved_at'];last_at=envelope['retrieved_at']
            for index,raw in enumerate(response['results']):
                assert raw['id'] not in raw_ids,'Duplicate ID inside a sample block'
                raw_ids.add(raw['id'])
                normalized,reason=normalize_work(raw,self.config)
                field_entity=(raw.get('primary_topic') or {}).get('field') or {}
                fid=str(field_entity.get('id','')).rsplit('/',1)[-1]
                year=raw.get('publication_year')
                cell_key=f'{fid}:{2000+(year-2000)//5*5}' if isinstance(year,int) else 'unknown'
                entry=by_cell.setdefault(cell_key,dict(candidates=0,valid=0,rejections={}))
                entry['candidates']+=1
                if reason:
                    rejections[reason]+=1;entry['rejections'][reason]=entry['rejections'].get(reason,0)+1
                else:entry['valid']+=1
                candidates.append((raw,normalized,reason,page['page'],index,envelope['retrieved_at']))
        assert len(candidates)==min(block['sample_size'],block['sample_result_count'])
        random.Random(block['seed']).shuffle(candidates)
        cell=None if block['cohort']=='base' else (block['field_id'],block['period_start'])
        remaining=self.config['base_target']-self.counts['base'] if cell is None else allocation(self.cells,self.config['extra_target']-self.counts['extra'],self.exhausted)[cell]
        expected=[];stats=Counter(candidates=len(candidates),accepted=0)
        for raw,normal,reason,page,index,date in candidates:
            if len(expected)>=remaining:break
            if reason:stats['rejected_'+reason]+=1;continue
            if normal['work_id'] in self.seen:stats['duplicate_work_id']+=1;continue
            if cell:assert (normal['field_id'],normal['period_start'])==cell
            expected.append((raw,normal,page,index,date));stats['accepted']+=1
        stats['not_examined_after_target']=len(candidates)-sum(v for k,v in stats.items() if k!='candidates')
        assert dict(stats)==json.loads(block['stats_json']),f'Block {bid}: replay statistics disagree'
        assert [r['work_id'] for r in selected]==[r[1]['work_id'] for r in expected],f'Block {bid}: selected order disagrees'
        rows=[]
        for stored,(raw,normal,page,index,date) in zip(selected,expected):
            assert all(stored[k]==v for k,v in normal.items()),f'Block {bid}: stored metadata/text disagree with API'
            assert stored['selection_order']==len(self.seen)+len(rows)+1
            assert (stored['source_block'],stored['source_page'],stored['source_page_index'],stored['source_seed'],stored['retrieved_at'])==(bid,page,index,block['seed'],date)
            # Direct checks against the original API record, independent of stored flags.
            assert raw['language']=='en' and raw['type'] in ('article','review','conference-paper')
            assert raw['is_retracted'] is False and raw['is_paratext'] is False
            assert stored['title'].strip() and stored['abstract_word_count']>=50
            assert len(WORDS.findall(stored['abstract']))==stored['abstract_word_count']
            assert stored['text_sha256']==sha(stored['title']+'\n\n'+stored['abstract'])
            assert 2000<=stored['publication_year']<=2024 and stored['field_id'] in range(11,37)
            assert stored['period_start']==2000+(stored['publication_year']-2000)//5*5
            old=self.legacy.execute('SELECT text_sha256 FROM legacy WHERE work_id=?',(stored['work_id'],)).fetchone()
            assert stored['legacy_id_present']==bool(old)
            assert stored['legacy_text_match']==bool(old and old[0]==stored['text_sha256'])
            flags=[]
            if stored['abstract_word_count']<80:flags.append('abstract_50_79')
            if NOTICE.search(stored['title'].strip()):flags.append('possible_notice_title')
            if stored['abstract_word_count']>2000:flags.append('abstract_over_2000_words')
            letters=[c for c in stored['abstract'] if c.isalpha()]
            if letters and sum(ord(c)>127 for c in letters)/len(letters)>.3:flags.append('many_non_ascii_letters')
            rows.append((stored['work_id'],stored['selection_order'],stored['cohort'],stored['field_id'],stored['period_start'],stored['publication_year'],stored['subfield_id'],stored['primary_topic_id'],stored['doi'],stored['text_sha256'],sha(' '.join((stored['title']+' '+stored['abstract']).lower().split())),sha(' '.join(stored['abstract'].lower().split())),sha(canonical(stored)),stored['title'],stored['abstract_word_count'],stored['title_word_count'],stored['legacy_id_present'],stored['legacy_text_match'],json.dumps(flags)))
        exhausted=bool(cell and len(candidates)<block['sample_size'] and len(rows)<remaining)
        summary=dict(id=bid,cohort=block['cohort'],cell=cell,candidates=len(candidates),selected=len(rows),
                     first_retrieved_at=first_at,last_retrieved_at=last_at,cleaning_rejections=dict(rejections),
                     candidate_cells=by_cell,selected_replayed=True,pages=len(pages),page_hashes_sha256=sha('\n'.join(file_hashes)),
                     exhausted=exhausted,audited_at=now())
        fingerprint=sha(canonical(dict(block=dict(block),pages=[dict(p) for p in pages])))
        with self.db:
            self.db.executemany('INSERT INTO selected VALUES('+','.join('?'*19)+')',rows)
            self.db.execute('INSERT INTO audited_blocks VALUES(?,?,?)',(bid,fingerprint,canonical(summary)))
        for stored in selected:
            self.seen.add(stored['work_id']);self.counts[stored['cohort']]+=1
            self.cells[(stored['field_id'],stored['period_start'])]+=1
        if exhausted:self.exhausted.add(cell)
        print(f"Auditado bloque {bid}: {len(rows):,} trabajos; total comprobado {len(self.seen):,}.",flush=True)
        save_json(CACHE/'progress.json',dict(updated_at=now(),phase='auditing',audited_records=len(self.seen),last_block=bid))

    def run_pass(self):
        blocks=self.source.execute("SELECT * FROM blocks WHERE status='applied' ORDER BY id").fetchall()
        done={r[0] for r in self.db.execute('SELECT id FROM audited_blocks')}
        for block in blocks:
            if block['id'] not in done:self.audit_block(block)
        return self.source.execute("SELECT value FROM meta WHERE key='complete'").fetchone() is not None

    def summaries(self):
        def csv_query(name,headers,query):
            with (REPORTS/name).open('w',newline='') as f:
                writer=csv.writer(f);writer.writerow(headers);writer.writerows(self.db.execute(query))
        csv_query('field_period_counts.csv',['field_id','period_start','cohort','n','abstract_50_79','legacy_id','legacy_text'],
                  'SELECT field_id,period_start,cohort,count(*),sum(abstract_words<80),sum(legacy_id),sum(legacy_text) FROM selected GROUP BY 1,2,3 ORDER BY 1,2,3')
        csv_query('field_year_counts.csv',['field_id','year','cohort','n'],
                  'SELECT field_id,year,cohort,count(*) FROM selected GROUP BY 1,2,3 ORDER BY 1,2,3')
        csv_query('reusable_text_ids.csv',['work_id','selection_order','cohort','text_sha256'],
                  'SELECT work_id,selection_order,cohort,text_sha FROM selected WHERE legacy_text=1 ORDER BY selection_order')
        csv_query('quality_flags.csv',['work_id','cohort','field_id','year','title','abstract_words','flags'],
                  "SELECT work_id,cohort,field_id,year,title,abstract_words,flags FROM selected WHERE flags!='[]' ORDER BY selection_order")
        duplicates={}
        for label,column in [('doi','doi'),('exact_text','text_sha'),('normalized_text','normalized_text_sha'),('abstract','abstract_sha')]:
            groups=self.db.execute(f'SELECT {column},count(*) n,group_concat(work_id) FROM selected WHERE {column} IS NOT NULL GROUP BY {column} HAVING n>1').fetchall()
            with (REPORTS/f'duplicate_{label}_groups.csv').open('w',newline='') as f:
                writer=csv.writer(f);writer.writerow([column,'n','work_ids']);writer.writerows(groups)
            duplicates[label]=dict(groups=len(groups),records=sum(r[1] for r in groups),excess=sum(r[1]-1 for r in groups))
        flags=Counter();lengths=Counter()
        for row in self.db.execute('SELECT flags,abstract_words FROM selected'):
            flags.update(json.loads(row[0]));lengths[row[1]]+=1
        def quantile(fraction):
            position=max(1,round(len(self.seen)*fraction));cumulative=0
            for length,count in sorted(lengths.items()):
                cumulative+=count
                if cumulative>=position:return length
        basic=dict(audited_at=now(),audited_rows=len(self.seen),counts=dict(self.counts),duplicates=duplicates,
                   quality_flags=dict(flags),abstract_words=dict(min=min(lengths),median=quantile(.5),p95=quantile(.95),p99=quantile(.99),max=max(lengths)),
                   coverage=dict(fields=self.db.execute('SELECT count(distinct field_id) FROM selected').fetchone()[0],
                                 field_period_cells=sum(v>0 for v in self.cells.values()),
                                 subfields=self.db.execute('SELECT count(distinct subfield_id) FROM selected').fetchone()[0],
                                 topics=self.db.execute('SELECT count(distinct topic_id) FROM selected').fetchone()[0]),
                   legacy=dict(self.db.execute('SELECT \'id_matches\',sum(legacy_id) FROM selected UNION ALL SELECT \'exact_text_matches\',sum(legacy_text) FROM selected')))
        save_json(REPORTS/'summary.json',basic)
        return basic

    def final_check(self):
        import pyarrow.parquet as pq
        assert self.counts=={'base':400000,'extra':100000}
        assert self.source.execute('PRAGMA quick_check').fetchone()[0]=='ok'
        assert self.source.execute("SELECT count(*) FROM blocks WHERE status!='applied'").fetchone()[0]==0
        assert self.source.execute('SELECT count(*),count(distinct work_id) FROM works').fetchone()[0]==500000
        base_cells={(f,p):0 for f,p in self.cells}
        for r in self.db.execute("SELECT field_id,period_start,count(*) FROM selected WHERE cohort='base' GROUP BY 1,2"):
            base_cells[(r[0],r[1])]=r[2]
        if not self.exhausted:
            supplements=allocation(base_cells,100000)
            for cell in self.cells:assert self.cells[cell]==base_cells[cell]+supplements[cell]
        manifest_hash=hashlib.sha256();ids_hash=hashlib.sha256();seen=0
        doi_dups={r[0] for r in self.db.execute('SELECT doi FROM selected WHERE doi IS NOT NULL GROUP BY doi HAVING count(*)>1')}
        text_dups={r[0] for r in self.db.execute('SELECT text_sha FROM selected GROUP BY text_sha HAVING count(*)>1')}
        for batch in pq.ParquetFile(DATA/'corpus.parquet').iter_batches(batch_size=10000):
            for row in batch.to_pylist():
                seen+=1;assert row['selection_order']==seen
                assert row.pop('duplicate_doi')==(row['doi'] in doi_dups)
                assert row.pop('duplicate_text')==(row['text_sha256'] in text_dups)
                expected=self.db.execute('SELECT record_sha FROM selected WHERE work_id=?',(row['work_id'],)).fetchone()
                assert expected and expected[0]==sha(canonical(row)),'Final Parquet differs from API-validated record'
                ids_hash.update((row['work_id']+'\n').encode())
                manifest_hash.update((row['work_id']+'\t'+row['text_sha256']+'\n').encode())
            print(f'Tabla final comparada: {seen:,}/500,000.',flush=True)
        assert seen==500000
        with (DATA/'corpus.parquet').open('rb') as f:parquet_sha=hashlib.file_digest(f,'sha256').hexdigest()
        extractor_validation=json.loads((DATA/'validation.json').read_text())
        assert parquet_sha==extractor_validation['parquet_sha256']
        audit=self.summaries()
        audit.update(status='passed',completed_at=now(),parquet_sha256=parquet_sha,
                     ordered_ids_sha256=ids_hash.hexdigest(),ordered_ids_texts_sha256=manifest_hash.hexdigest(),
                     checks=['all_page_checksums','all_selected_rows_against_original_api','full_seeded_selection_replay',
                             'all_cleaning_statistics_replayed','all_legacy_flags_checked','independent_supplement_allocation',
                             'exact_cohort_sizes','all_parquet_rows_and_duplicate_flags','parquet_file_hash','sqlite_integrity'],
                     exhausted_cells=sorted(self.exhausted))
        save_json(REPORTS/'final_validation.json',audit)
        save_json(CACHE/'progress.json',dict(updated_at=now(),phase='complete',audited_records=500000))
        save_json(REPORTS/'corpus_manifest.json',dict(frozen_at=now(),corpus_path=str(DATA/'corpus.parquet'),rows=500000,
                  parquet_sha256=parquet_sha,ordered_ids_sha256=ids_hash.hexdigest(),
                  ordered_ids_texts_sha256=manifest_hash.hexdigest(),row_order='selection_order ascending',
                  cohorts={'base':400000,'extra':100000},input_text_decision='Pending: preserve title and abstract separately; do not choose model formatting here',
                  config=self.config))
        print('Auditoría completa: 500.000 trabajos, selección y tabla final comprobados.',flush=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--watch',action='store_true');args=parser.parse_args()
    CACHE.mkdir(parents=True,exist_ok=True)
    with (CACHE/'audit.lock').open('a+') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            print('Ya hay una auditoría trabajando.');return
        auditor=Auditor()
        try:
            while True:
                finished=auditor.run_pass()
                if finished:
                    auditor.run_pass();auditor.final_check();return
                auditor.summaries()
                if not args.watch:return
                print(f'Seguimiento activo: {len(auditor.seen):,} trabajos auditados. Esperando nuevos bloques.',flush=True)
                time.sleep(30)
        except Exception as error:
            save_json(CACHE/'error.json',dict(at=now(),type=type(error).__name__,message=str(error)))
            raise
        finally:auditor.close()


if __name__=='__main__':main()
