"""Small, serial API timing/quality probe. Never prints or persists credentials."""
import collections
import datetime
import json
import os
from pathlib import Path
import re
import statistics
import time

import pyarrow.parquet as pq
import requests
from dotenv import dotenv_values

OUT = Path(__file__).resolve().parent
SOURCE = Path('/Users/alejandrotreny/Workspace/Mapping-Science')
KEY = os.environ.get('OPENALEX_API_KEY') or dotenv_values(SOURCE / '.env').get('OPENALEX_API_KEY')
FILTER = 'publication_year:2000-2024,type:article|review|conference-paper,language:en,has_abstract:true,is_retracted:false,is_paratext:false,primary_topic.field.id:!null'
session = requests.Session()
calls = []

def get(label, params):
    start = time.perf_counter()
    response = session.get('https://api.openalex.org/works', params={**params, 'api_key': KEY}, timeout=45)
    elapsed = time.perf_counter() - start
    if response.status_code != 200:
        raise RuntimeError(f'{label}: HTTP {response.status_code}')
    data = response.json()
    record = dict(label=label, parameters=params, seconds=elapsed, bytes=len(response.content), count=data['meta']['count'], retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    calls.append(record)
    time.sleep(0.2)
    return data

def abstract(index):
    if not isinstance(index, dict) or not index:
        return None
    pos = {}
    for word, indexes in index.items():
        if not isinstance(word, str) or not isinstance(indexes, list):
            return None
        for i in indexes:
            if not isinstance(i, int) or i < 0 or i in pos:
                return None
            pos[i] = word
    if not pos or len(pos) != max(pos) + 1:
        return None
    return ' '.join(pos[i] for i in range(len(pos)))

fields = get('fields', dict(corpus='core', filter=FILTER, group_by='primary_topic.field.id', per_page=100))
assert len(fields['group_by']) == 26
(OUT / 'proposed_population_fields.json').write_text(json.dumps(fields, ensure_ascii=False, indent=2))
field_years = []
for g in fields['group_by']:
    fid = g['key'].rsplit('/', 1)[-1]
    result = get('years_'+fid, dict(corpus='core', filter=FILTER.replace('primary_topic.field.id:!null','primary_topic.field.id:'+fid), group_by='publication_year', per_page=100))
    assert sum(v['count'] for v in result['group_by']) == g['count']
    field_years.extend(dict(field_id=fid, field_name=g['key_display_name'], year=int(v['key']), candidates=v['count']) for v in result['group_by'])
(OUT / 'proposed_population_field_years.json').write_text(json.dumps(field_years, ensure_ascii=False, indent=2))

raw = []
select = 'id,doi,title,abstract_inverted_index,publication_year,type,language,primary_topic,is_retracted,is_paratext'
for label, fid, page in [('global_1',None,1),('global_2',None,2),('global_3',None,3),('global_4',None,4),('veterinary','34',1),('arts','12',1),('computer_science','17',1)]:
    flt = FILTER if fid is None else FILTER.replace('primary_topic.field.id:!null','primary_topic.field.id:'+fid)
    result = get(label, dict(corpus='core',filter=flt,sample=400 if fid is None else 100,seed=20260914,per_page=100,page=page,select=select))
    assert len(result['results']) == 100
    raw.extend(dict(probe_group='global' if fid is None else label, work=r) for r in result['results'])
    print(label, round(calls[-1]['seconds'],2), 'seconds',flush=True)
(OUT / 'openalex_probe_raw.json').write_text(json.dumps(raw, ensure_ascii=False))
local_ids = set(pq.read_table(SOURCE/'data/processed/works_text_2000_2024_400py.parquet',columns=['work_id']).column(0).to_pylist())
quality = collections.defaultdict(collections.Counter)
for item in raw:
    r = item['work']; q=quality[item['probe_group']]; q['total']+=1
    text=abstract(r.get('abstract_inverted_index')); title=r.get('title') or ''
    n=len(re.findall(r'\b\w+\b', text or '')); nt=len(re.findall(r'\b\w+\b', title))
    q['abstract_reconstructable']+=int(text is not None)
    q['nonempty_title_abstract']+=int(bool(title.strip()) and bool(text))
    q['title_ge1_abstract_ge50']+=int(nt>=1 and n>=50)
    q['title_ge1_abstract_ge80']+=int(nt>=1 and n>=80)
    q['old_title_ge5_abstract_ge80']+=int(nt>=5 and n>=80)
    q['existing_local_id']+=int(r['id'].rsplit('/',1)[-1] in local_ids)
timing=[r['seconds'] for r in calls if r['label'] not in ['fields'] and not r['label'].startswith('years_')]
report=dict(filter=FILTER,corpus='core',calls=calls,quality=quality,pages_median_seconds=statistics.median(timing),pages_range_seconds=[min(timing),max(timing)],note='400 global random candidates plus 100 in each of three areas; exploratory acceptance rates, not population guarantees')
encoded=json.dumps(report,ensure_ascii=False,indent=2)
assert not KEY or KEY not in encoded
(OUT / 'openalex_probe_summary.json').write_text(encoded)
print(json.dumps({k:report[k] for k in ['quality','pages_median_seconds','pages_range_seconds']},indent=2),flush=True)
