"""Re-run the language detector on every final text and report retained flags."""
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import sys

import fasttext
import pyarrow as pa
import pyarrow.parquet as pq

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.expand_content_checks import content_signature


def main():
    data=ROOT/'data/corpus_clean_v1';reports=ROOT/'research/cleaning_2026-09-15'
    manifest=json.loads((data/'embedding_manifest.json').read_text())
    assert manifest['status']=='prepared_and_verified'
    policy=json.loads((ROOT/'config/cleaning_v1.json').read_text())
    model=fasttext.load_model(str(ROOT/'data/audit_models/lid.176.bin'))
    totals=Counter();cells=defaultdict(Counter);dups=defaultdict(list);abstract_groups=defaultdict(list)
    flagged=[];n=0;lang_mismatches=0;segment_mismatches=0;content_signatures=0
    cols=['work_id','row_index','title','abstract','text_sha256','cohort','field_id','period_start','publication_year',
          'abstract_detected_language','abstract_language_score','language_segments_json',
          'language_ambiguous','possible_mixed_language','content_review_flag','possible_notice','possible_access_message',
          'abstract_50_79','abstract_over_2000','normalized_text_group','doi']
    for batch in pq.ParquetFile(data/'corpus.parquet').iter_batches(batch_size=5000,columns=cols):
        rows=batch.to_pylist();texts=[' '.join(r['abstract'].split()) for r in rows]
        labels,scores=model.predict(texts,k=1)
        parts=[];part_rows=[]
        for r,text,lab,score in zip(rows,texts,labels,scores):
            label=lab[0].removeprefix('__label__')
            if label!=r['abstract_detected_language'] or abs(float(score[0])-r['abstract_language_score'])>1e-6:lang_mismatches+=1
            if label!='en':
                parts.extend([text[len(text)*i//3:len(text)*(i+1)//3] for i in range(3)]);part_rows.append(r)
        if parts:
            part_labels,part_scores=model.predict(parts,k=1)
            for i,r in enumerate(part_rows):
                expected=json.loads(r['language_segments_json'])
                for j in range(3):
                    if expected[j]['language']!=part_labels[i*3+j][0].removeprefix('__label__') or abs(expected[j]['score']-float(part_scores[i*3+j][0]))>1e-6:segment_mismatches+=1
        for r in rows:
            key=(r['field_id'],r['period_start'],r['cohort'])
            cells[key]['n']+=1
            flags=[]
            for flag in ('language_ambiguous','possible_mixed_language','content_review_flag','possible_notice','possible_access_message','abstract_50_79','abstract_over_2000'):
                totals[flag]+=int(r[flag]);cells[key][flag]+=int(r[flag])
                if r[flag]:flags.append(flag)
            totals['abstract_top_label_non_en']+=int(r['abstract_detected_language']!='en')
            content_signatures+=int(content_signature(r['abstract']) is not None)
            dups[r['normalized_text_group']].append(r['work_id'])
            abstract_groups[hashlib.sha256(r['abstract'].encode()).hexdigest()].append(r['work_id'])
            if flags:flagged.append((r['work_id'],r['row_index'],r['cohort'],r['field_id'],r['period_start'],';'.join(flags)))
        n+=len(rows);print(f'Idioma verificado de nuevo: {n:,}.',flush=True)
    assert n==500000 and lang_mismatches==0 and segment_mismatches==0
    assert content_signatures==0,'Known webpage/notice signature survives final selection'
    with (reports/'retained_quality_flags.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['work_id','row_index','cohort','field_id','period_start','flags']);w.writerows(flagged)
    flag_names=['n','language_ambiguous','possible_mixed_language','content_review_flag','possible_notice','possible_access_message','abstract_50_79','abstract_over_2000']
    with (reports/'quality_by_field_period.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['field_id','period_start','cohort',*flag_names]);w.writerows([*key,*[val[k] for k in flag_names]] for key,val in sorted(cells.items()))
    for name,groups in [('normalized_text',dups),('abstract',abstract_groups)]:
        with (reports/f'retained_duplicate_{name}_groups.csv').open('w',newline='') as f:
            w=csv.writer(f);w.writerow(['sha256','n','work_ids']);w.writerows((key,len(ids),','.join(ids)) for key,ids in sorted(groups.items()) if len(ids)>1)
    result=dict(status='passed',rows=n,language_prediction_mismatches=lang_mismatches,segment_prediction_mismatches=segment_mismatches,
                known_content_signatures_remaining=content_signatures,retained_flags=dict(totals),
                normalized_duplicate_groups=sum(len(ids)>1 for ids in dups.values()),
                abstract_duplicate_groups=sum(len(ids)>1 for ids in abstract_groups.values()),
                limitation='Verifies detector execution and removal of known errors, not ground-truth language or exhaustive metadata quality.')
    (reports/'quality_recheck.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
