"""Describe repeated and short source texts without altering the paired pilot."""
import csv
import json
from collections import Counter
from pathlib import Path
import numpy as np
import pyarrow.parquet as pq
from sos_embed.storage import file_sha,write_json,utcnow

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'data/checklist_v1/inputs/native_input.parquet'
OUT=ROOT/'data/checklist_v1/text_profile'


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    rows=pq.read_table(INPUT,columns=['field_id','title','abstract']).to_pylist()
    assert len(rows)==26000
    results=[];summary={}
    for condition in ['title','abstract','title_abstract']:
        values={}
        for r in rows:
            text=r[condition] if condition!='title_abstract' else r['title']+'\n\n'+r['abstract']
            values.setdefault(r['field_id'],[]).append(text)
        for field,texts in sorted(values.items()):
            assert len(texts)==1000
            exact=Counter(texts);norm=Counter(' '.join(t.casefold().split()) for t in texts)
            words=np.array([len(t.split()) for t in texts]);chars=np.array(list(map(len,texts)))
            results.append({'field_id':field,'condition':condition,'rows':len(texts),
                'rows_in_exact_repeated_groups':sum(v for v in exact.values() if v>1),
                'exact_repeated_groups':sum(v>1 for v in exact.values()),
                'rows_in_normalized_repeated_groups':sum(v for v in norm.values() if v>1),
                'maximum_exact_repetitions':max(exact.values()),'fewer_than_four_words':int((words<4).sum()),
                'mean_whitespace_words':float(words.mean()),'median_whitespace_words':float(np.median(words)),
                'mean_characters':float(chars.mean())})
        chosen=[r for r in results if r['condition']==condition]
        summary[condition]={k:sum(r[k] for r in chosen) for k in ['rows','rows_in_exact_repeated_groups','exact_repeated_groups','rows_in_normalized_repeated_groups','fewer_than_four_words']}
        summary[condition]['maximum_exact_repetitions']=max(r['maximum_exact_repetitions'] for r in chosen)
    with (OUT/'source_text_profile.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
    write_json(OUT/'summary.json',summary)
    (OUT/'source_snapshot.py').write_bytes(Path(__file__).read_bytes())
    write_json(OUT/'audit.json',{'all_complete':True,'created_at':utcnow(),'input_sha256':file_sha(INPUT),
        'source_sha256':file_sha(__file__),'rows':26000,'counts_scope':'repetitions within Field across the five periods; same scope as pilot comparison',
        'normalization':'casefold and whitespace collapse only; no linguistic tokenization',
        'files':{p.name:file_sha(p) for p in sorted(OUT.glob('*.csv'))}})
    print('SOURCE TEXT PROFILE COMPLETE',flush=True)


if __name__=='__main__':main()
