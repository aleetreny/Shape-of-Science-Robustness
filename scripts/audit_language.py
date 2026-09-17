"""Flag possible metadata language errors; never exclude or translate corpus records."""
import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import fcntl
import hashlib
import json
from pathlib import Path
import sqlite3
import time

import fasttext

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/corpus_500k'
CACHE=ROOT/'data/corpus_audit'
REPORTS=ROOT/'research/corpus_audit_2026-09-15'


def summary(db,finished):
    count=db.execute('SELECT count(*) FROM predictions').fetchone()[0]
    languages=dict(db.execute('SELECT abstract_language,count(*) FROM predictions GROUP BY 1 ORDER BY count(*) DESC'))
    confident=dict(db.execute('SELECT abstract_language,count(*) FROM predictions WHERE abstract_score>=0.9 GROUP BY 1 ORDER BY count(*) DESC'))
    row=db.execute("SELECT sum(abstract_language!='en'),sum(abstract_language!='en' AND abstract_score>=.8),sum(abstract_language!='en' AND abstract_score>=.9),sum(abstract_language='en' AND abstract_score<.8) FROM predictions").fetchone()
    report=dict(updated_at=datetime.now(timezone.utc).isoformat(),status='complete' if finished else 'in_progress',
                rows=count,model='fastText lid.176.bin',all_top_labels=languages,top_labels_score_at_least_09=confident,
                non_english_top_label=row[0],non_english_score_at_least_08=row[1],non_english_score_at_least_09=row[2],
                english_score_below_08=row[3],notes='Diagnostic scores are not calibrated error probabilities. Mixed-language and low-score cases need a defined rule. No rows removed; thresholds 0.8/0.9 shown for comparison, not approved exclusion rules.')
    tmp=REPORTS/'language_summary.json.tmp';tmp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');tmp.replace(REPORTS/'language_summary.json')
    with (REPORTS/'language_by_field_period.csv').open('w',newline='') as handle:
        writer=csv.writer(handle);writer.writerow(['field_id','period_start','cohort','n','non_en_top_label','non_en_score_ge_09'])
        writer.writerows(db.execute("SELECT field_id,period_start,cohort,count(*),sum(abstract_language!='en'),sum(abstract_language!='en' AND abstract_score>=.9) FROM predictions GROUP BY 1,2,3 ORDER BY 1,2,3"))
    with (REPORTS/'language_review_candidates.csv').open('w',newline='') as handle:
        writer=csv.writer(handle);writer.writerow(['work_id','selection_order','cohort','field_id','period_start','title_language','title_score','abstract_language','abstract_score','text_sha256'])
        writer.writerows(db.execute("SELECT work_id,selection_order,cohort,field_id,period_start,title_language,title_score,abstract_language,abstract_score,text_sha FROM predictions WHERE abstract_language!='en' OR abstract_score<.8 ORDER BY selection_order"))
    return report


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--watch',action='store_true');args=parser.parse_args()
    CACHE.mkdir(parents=True,exist_ok=True);REPORTS.mkdir(parents=True,exist_ok=True)
    with (CACHE/'language.lock').open('a+') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:print('Language audit already active.');return
        db=sqlite3.connect(CACHE/'language.sqlite')
        db.execute('''CREATE TABLE IF NOT EXISTS predictions(work_id TEXT PRIMARY KEY,selection_order INTEGER UNIQUE,
            cohort TEXT,field_id INTEGER,period_start INTEGER,title_language TEXT,title_score REAL,
            abstract_language TEXT,abstract_score REAL,text_sha TEXT)''')
        db.execute('CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT)')
        source=sqlite3.connect((DATA/'state.sqlite').resolve().as_uri()+'?mode=ro',uri=True)
        source.execute('PRAGMA query_only=ON')
        model_path=ROOT/'data/audit_models/lid.176.bin'
        with model_path.open('rb') as handle:model_sha=hashlib.file_digest(handle,'sha256').hexdigest()
        identity=json.dumps({'model_sha':model_sha,'script_sha':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                             'created_at':source.execute("SELECT value FROM meta WHERE key='created_at'").fetchone()[0]},sort_keys=True)
        old=db.execute("SELECT value FROM meta WHERE key='identity'").fetchone()
        assert old is None or old[0]==identity,'Source/model/script changed; do not mix audit predictions'
        with db:db.execute('INSERT OR REPLACE INTO meta VALUES(?,?)',('identity',identity))
        model=fasttext.load_model(str(model_path))
        last=db.execute('SELECT COALESCE(max(selection_order),0) FROM predictions').fetchone()[0]
        try:
            while True:
                while True:
                    batch=source.execute('SELECT record_json FROM works WHERE selection_order>? ORDER BY selection_order LIMIT 5000',(last,)).fetchall()
                    if not batch:break
                    records=[json.loads(row[0]) for row in batch]
                    title_labels,title_scores=model.predict([' '.join(r['title'].split()) for r in records],k=1)
                    abstract_labels,abstract_scores=model.predict([' '.join(r['abstract'].split()) for r in records],k=1)
                    rows=[]
                    for r,tl,ts,al,ass in zip(records,title_labels,title_scores,abstract_labels,abstract_scores):
                        rows.append((r['work_id'],r['selection_order'],r['cohort'],r['field_id'],r['period_start'],tl[0].replace('__label__',''),float(ts[0]),al[0].replace('__label__',''),float(ass[0]),r['text_sha256']))
                    with db:db.executemany('INSERT INTO predictions VALUES(?,?,?,?,?,?,?,?,?,?)',rows)
                    last=records[-1]['selection_order']
                    print(f'Idioma comprobado en {last:,} resúmenes.',flush=True)
                finished=source.execute("SELECT 1 FROM meta WHERE key='complete'").fetchone() is not None
                if finished and last!=500000:continue
                result=summary(db,finished)
                print(f"Comprobados {last:,}; posible idioma distinto de inglés: {result['non_english_top_label']:,}.",flush=True)
                if finished or not args.watch:break
                time.sleep(30)
        finally:source.close();db.close()


if __name__=='__main__':main()
