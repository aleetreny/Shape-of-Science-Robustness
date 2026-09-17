"""Refresh old-vector pointers for the final clean IDs. Never approve or copy vectors."""
from collections import defaultdict
import json
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

ROOT=Path(__file__).resolve().parents[1]
OLD=Path('/Users/alejandrotreny/Workspace/Mapping-Science')
OUT=ROOT/'research/cleaning_2026-09-15'
manifest=json.loads((ROOT/'data/corpus_clean_v1/embedding_manifest.json').read_text())
assert manifest['status']=='prepared_and_verified'
targets={}
for batch in pq.ParquetFile(ROOT/'data/corpus_clean_v1/corpus.parquet').iter_batches(columns=['work_id','row_index','text_sha256','legacy_text_match']):
    for r in batch.to_pylist():
        if r['legacy_text_match']:targets[r['work_id']]=r
found=set();groups=defaultdict(list)
for batch in pq.ParquetFile(OLD/'data/processed/embedding_index.parquet').iter_batches(columns=['work_id','embedding_shard_file','embedding_row_in_shard','metadata_shard_file','embedding_dim','embedding_dtype']):
    for r in batch.to_pylist():
        if r['work_id'] in targets:
            assert r['work_id'] not in found
            found.add(r['work_id']);groups[r['embedding_shard_file']].append(r)
assert found==set(targets)
output=[];shards=OLD/'embeddings/specter2_v1_2000_2024_400py'
for name,rows in sorted(groups.items()):
    matrix=np.load(shards/name,mmap_mode='r')
    meta=pq.read_table(shards/rows[0]['metadata_shard_file'],columns=['work_id']).column(0).to_pylist()
    assert matrix.shape[0]==len(meta) and matrix.shape[1]==768 and str(matrix.dtype)=='float16'
    positions=[r['embedding_row_in_shard'] for r in rows]
    assert all(meta[p]==r['work_id'] for p,r in zip(positions,rows))
    values=np.asarray(matrix[positions],dtype=np.float32)
    assert np.isfinite(values).all() and (np.linalg.norm(values,axis=1)>0).all()
    for r in rows:
        t=targets[r['work_id']]
        output.append(dict(work_id=r['work_id'],row_index=t['row_index'],text_sha256=t['text_sha256'],
                           embedding_shard_path=str(shards/name),embedding_row_in_shard=r['embedding_row_in_shard'],
                           embedding_dim=768,embedding_dtype='float16',numerically_valid=True,approved_for_final_experiments=False))
output.sort(key=lambda r:r['row_index'])
pq.write_table(pa.Table.from_pylist(output),OUT/'legacy_embedding_candidates.parquet',compression='zstd')
result=dict(exact_text_candidates=len(targets),vectors_located_and_checked=len(output),shards=len(groups),
            approved_for_final_experiments=False,reason='Exact model/tokenizer/adapter revisions remain unresolved. No vectors copied or computed.')
(OUT/'legacy_embedding_summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
