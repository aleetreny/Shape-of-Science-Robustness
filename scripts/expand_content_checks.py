"""Inspect all saved candidates for specific webpage signatures before selection.

This extends exact-text exclusions using clear source-page/notice structures.
A bare occurrence of 'advertisement' or 'abstract' is deliberately insufficient.
Original pages are opened in read-only mode and never rewritten.
"""
from collections import Counter
import csv
import gzip
import json
from pathlib import Path
import sqlite3
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from sos_download.records import normalize_work
from sos_prepare.quality import digest,normalized,content_signature




def main():
    config=json.loads((ROOT/'config/corpus.json').read_text())
    path=ROOT/'config/cleaning_v1.json';policy=json.loads(path.read_text())
    source=ROOT/'data/corpus_500k'
    db=sqlite3.connect((source/'state.sqlite').as_uri()+'?mode=ro',uri=True)
    counts=Counter();matches={};pages=0
    for (name,) in db.execute('SELECT path FROM pages ORDER BY block_id,page'):
        with gzip.open(source/name,'rt') as f:envelope=json.load(f)
        for raw in envelope['response']['results']:
            r,reason=normalize_work(raw,config)
            if reason:continue
            signature=content_signature(r['abstract'])
            if signature:
                sha=digest(normalized(r['abstract']))
                matches[(r['work_id'],r['text_sha256'])]=(r,signature,sha)
                if sha not in policy['boilerplate_abstracts']:
                    policy['boilerplate_abstracts'][sha]=dict(reason=signature,example_id=r['work_id'],abstract=r['abstract'],
                        evidence='Specific source-page or explicit notice structure verified with scripts/expand_content_checks.py across all stored candidate pages; not a keyword-only rule.')
        pages+=1
        if pages%500==0:print('Páginas comprobadas para contenido impropio:',pages,flush=True)
    db.close()
    out=ROOT/'research/cleaning_2026-09-15/content_signature_matches.csv'
    with out.open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['work_id','text_sha256','abstract_sha256','reason'])
        for (wid,text_sha),(r,reason,sha) in sorted(matches.items()):
            writer.writerow([wid,text_sha,sha,reason]);counts[reason]+=1
    path.write_text(json.dumps(policy,ensure_ascii=False,indent=2)+'\n')
    report=dict(pages_checked=pages,matched_distinct_id_text_pairs=len(matches),counts=dict(counts),
                final_exact_abstract_exclusions=len(policy['boilerplate_abstracts']),
                note='This expands a known-error catalogue before final selection. It is not proof of exhaustive content quality.')
    (out.parent/'content_signature_summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
