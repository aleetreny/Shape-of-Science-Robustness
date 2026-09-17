"""Supplemental content flags discovered during inspection; no corpus changes.

These rules locate candidates for a future agreed cleaning protocol, not exclusions.
Exact repeated boilerplate families are recorded as observed evidence. Generic
access-message patterns and placeholder-looking titles can have false positives.
"""
import csv
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from collections import Counter
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1]
REPORTS=ROOT/'research/corpus_audit_2026-09-15'
KNOWN_PREFIXES={
    'doi_error_text':'This DOI is not currently attached to any metadata records.',
    'journal_description_ijcse':'International Journal of Computer Sciences and Engineering (A UGC Approved',
    'library_description_americanae':'Americanae nace como un proyecto conjunto',
    'catalog_description_kansas':'Published as: Kansas Farmer, Vol.',
    'journal_description_cad':'Computer-Aided Design and Applications is an international journal',
    'journal_description_asian_chemistry':'Asian Journal of Chemistry, a Multidisciplinary Chemistry Journal',
}
ACCESS=re.compile(r'\b(?:access denied|enable javascript|verify (?:that )?you are (?:a )?human|checking your browser|cookies are disabled)\b',re.I)
NO_TITLE={'not available','untitled','unknown','no title','[no title found]','[no title]','contents'}


def main():
    source=sqlite3.connect((ROOT/'data/corpus_500k/state.sqlite').resolve().as_uri()+'?mode=ro',uri=True)
    source.execute('PRAGMA query_only=ON')
    cutoff=source.execute('SELECT max(selection_order) FROM works').fetchone()[0]
    counts=Counter();by_cell=Counter();examples={};flagged=0;last=0
    with (REPORTS/'content_review_candidates.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['work_id','selection_order','cohort','field_id','period_start','title','flags','text_sha256'])
        while True:
            batch=source.execute('SELECT record_json FROM works WHERE selection_order>? AND selection_order<=? ORDER BY selection_order LIMIT 10000',(last,cutoff)).fetchall()
            if not batch:break
            for row in batch:
                r=json.loads(row[0]);abstract=r['abstract'].strip();flags=[]
                for label,prefix in KNOWN_PREFIXES.items():
                    if abstract.startswith(prefix):flags.append(label)
                if ACCESS.search(abstract):flags.append('possible_access_message')
                if r['title'].strip().casefold() in NO_TITLE:flags.append('possible_placeholder_title')
                if flags:
                    flagged+=1;counts.update(flags)
                    writer.writerow([r[k] for k in ('work_id','selection_order','cohort','field_id','period_start','title')]+[';'.join(flags),r['text_sha256']])
                    for flag in flags:
                        by_cell[(r['field_id'],r['period_start'],r['cohort'],flag)]+=1
                        if len(examples.setdefault(flag,[]))<3:
                            examples[flag].append(dict(work_id=r['work_id'],title=r['title'],abstract_start=abstract[:600]))
                last=r['selection_order']
    source.close()
    with (REPORTS/'content_flags_by_cell.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['field_id','period_start','cohort','flag','n'])
        writer.writerows([*key,value] for key,value in sorted(by_cell.items()))
    summary=dict(at=datetime.now(timezone.utc).isoformat(),checked_rows=cutoff,flagged_rows=flagged,counts=dict(counts),
                 examples=examples,observed_prefixes=KNOWN_PREFIXES,
                 script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 warning='Exploratory flags, not approved exclusion rules. They do not prove absence of other bad abstracts. Generic access/title flags require review; do not discard all repeated abstracts automatically.')
    (REPORTS/'content_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(checked_rows=cutoff,flagged_rows=flagged,counts=dict(counts)),ensure_ascii=False))


if __name__=='__main__':main()
