"""Independent audit of the technical outputs; never starts a full model run."""
import hashlib
import json
from pathlib import Path
import re

import numpy as np
import pyarrow.parquet as pq

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()


cfg=json.loads((ROOT/'config/embeddings_v1.json').read_text())
assert len(cfg['models'])==10
assert len({m['key'] for m in cfg['models']})==10
assert cfg['production_input_policy_approved'] is True
original_manifest=json.loads((ROOT/'data/corpus_clean_v1/embedding_manifest.json').read_text())
assert sha(ROOT/'data/corpus_clean_v1/embedding_input.parquet')==original_manifest['embedding_input_sha256']
assert sha(ROOT/'data/corpus_clean_v1/corpus.parquet')==original_manifest['corpus_sha256']
pilot_root=ROOT/'data/embedding_pilot_v1'
control_root=ROOT/'data/embedding_control_pilot_v1'
source=pq.read_table(pilot_root/'input.parquet').to_pylist()
common=pq.read_table(control_root/'input.parquet').to_pylist()
assert len(source)==len(common)==1300
assert len({r['work_id'] for r in source})==1300
assert len({(r['field_id'],r['period_start']) for r in source})==130
same=[]
for a,b in zip(source,common):
    assert a['row_index']==b['row_index'] and a['work_id']==b['work_id']
    assert b['source_text_sha256']==a['text_sha256']
    assert a['title'].startswith(b['title']) and a['abstract'].startswith(b['abstract'])
    for r in (a,b):
        assert hashlib.sha256((r['title']+'\n\n'+r['abstract']).encode()).hexdigest()==r['text_sha256']
    same.append(a['text_sha256']==b['text_sha256'])
same=np.array(same)
report=[]
identity=['row_index','work_id','text_sha256']
for m in cfg['models']:
    assert re.fullmatch('[a-f0-9]{40}',m['revision'])
    saved_vectors={}
    model_report={'model':m['key'],'name':m['name'],'revision':m['revision'],'dimension':m['dimension'],'poolings':m['poolings']}
    for scope,root,expected in [('native',pilot_root,source),('common',control_root,common)]:
        folder=root/m['key'];manifest=json.loads((folder/'manifest.json').read_text())
        assert manifest['model']==m
        assert sha(root/'input.parquet')==manifest['input_sha256']
        for name,digest in manifest['source_files'].items():
            assert sha(ROOT/name)==digest
            assert sha(root/'source_snapshot'/name)==digest
        rows=[];vecs={p:[] for p in m['poolings']};seconds=0.;rss=[];gpu=[];total_bytes=0
        for shard in sorted((folder/'shards').glob('[0-9]*')):
            c=json.loads((shard/'commit.json').read_text())
            assert c['start']==len(rows)
            for name,digest in c['files'].items():
                assert sha(shard/name)==digest
                total_bytes+=(shard/name).stat().st_size
            part=pq.read_table(shard/'rows.parquet').to_pylist();rows.extend(part)
            assert c['end']==len(rows)
            for p in vecs:
                a=np.load(shard/(p+'.npy'),allow_pickle=False)
                assert a.shape==(len(part),m['dimension']) and a.dtype==np.float32
                assert np.isfinite(a).all() and np.all(np.linalg.norm(a,axis=1)>0)
                vecs[p].append(a)
            seconds+=c['stats']['seconds'];rss.append(c['stats']['process_peak_rss_gib'])
            gpu.append(c['stats']['mps_driver_allocated_gib_at_shard_end'])
        assert len(rows)==1300
        for r,e in zip(rows,expected):
            assert all(r[k]==e[k] for k in identity)
            assert r['tokens_used']<=m['max_length']
            separator='[SEP]' if m['text_format']=='sep' else '\n\n'
            formatted=e['title']+separator+e['abstract']
            assert r['formatted_text_sha256']==hashlib.sha256(formatted.encode()).hexdigest()
        if scope=='common':assert not any(r['truncated'] for r in rows)
        saved_vectors[scope]={p:np.concatenate(v) for p,v in vecs.items()}
        model_report[scope]={'rows':len(rows),'seconds':seconds,'papers_per_second':len(rows)/seconds,
                            'truncated':sum(r['truncated'] for r in rows),'output_bytes':total_bytes,
                            'max_process_peak_rss_gib':max(rss),'max_driver_gib_at_shard_end':max(gpu)}
    # Unchanged source fragments must still identify the same vectors across two distinct runs.
    diffs={}
    for p in m['poolings']:
        a=saved_vectors['native'][p][same];b=saved_vectors['common'][p][same]
        np.testing.assert_allclose(a,b,atol=0.0002,rtol=0.0001)
        diffs[p]=float(np.max(np.abs(a-b)))
    model_report['unchanged_fragment_max_abs_difference']=diffs
    model_report['full_500k_hours_extrapolated']=model_report['native']['seconds']/1300*500000/3600
    report.append(model_report)
before=json.loads((HERE/'before_resume_hashes.json').read_text())
assert all(sha(ROOT/p)==h for p,h in before.items())
assert not list((ROOT/'data/embeddings_v1').glob('*/shards/[0-9]*'))
result={'status':'verified','models':report,'source_input_sha256':original_manifest['embedding_input_sha256'],
        'native_pilot_rows_per_model':1300,'control_pilot_rows_per_model':1300,
        'identical_fragment_rows_compared':int(same.sum()),'first_shard_unchanged_after_resume':True,
        'full_calculation_started':False,'full_vectors_bytes':sum(m['dimension']*len(m['poolings'])*4*500000 for m in cfg['models']),
        'full_total_hours_extrapolated':sum(r['full_500k_hours_extrapolated'] for r in report),
        'limitation':'Short balanced technical sample; extrapolated times are not a sustained full-corpus benchmark.'}
(HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='models'},indent=2))
