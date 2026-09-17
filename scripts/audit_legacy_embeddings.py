"""Locate and validate existing vectors for exact text matches, without copying vectors."""
from collections import defaultdict
import json
from pathlib import Path
import sqlite3

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

ROOT=Path(__file__).resolve().parents[1]
OLD=Path('/Users/alejandrotreny/Workspace/Mapping-Science')
SHARDS=OLD/'embeddings/specter2_v1_2000_2024_400py'
OUT=ROOT/'research/corpus_audit_2026-09-15'
db=sqlite3.connect((ROOT/'data/corpus_audit/audit.sqlite').resolve().as_uri()+'?mode=ro',uri=True)
assert db.execute('SELECT count(*) FROM selected').fetchone()[0]==500000
targets={wid:dict(work_id=wid,selection_order=order,cohort=cohort,text_sha256=text_sha)
         for wid,order,cohort,text_sha in db.execute('SELECT work_id,selection_order,cohort,text_sha FROM selected WHERE legacy_text=1')}
db.close()
index=pq.ParquetFile(OLD/'data/processed/embedding_index.parquet')
columns=['work_id','embedding_shard_file','embedding_row_in_shard','metadata_shard_file','embedding_dim','embedding_dtype']
groups=defaultdict(list);found=set()
for batch in index.iter_batches(batch_size=20000,columns=columns):
    for row in batch.to_pylist():
        if row['work_id'] in targets:
            assert row['work_id'] not in found
            found.add(row['work_id']);groups[row['embedding_shard_file']].append(row)
assert found==set(targets),'Some exact legacy text matches have no indexed vector'
output=[];min_norm=float('inf');max_norm=0
for name,rows in sorted(groups.items()):
    matrix=np.load(SHARDS/name,mmap_mode='r')
    metadata=pq.read_table(SHARDS/rows[0]['metadata_shard_file'],columns=['work_id']).column(0).to_pylist()
    assert len(metadata)==matrix.shape[0]
    positions=[r['embedding_row_in_shard'] for r in rows]
    assert min(positions)>=0 and max(positions)<matrix.shape[0]
    for row in rows:
        assert metadata[row['embedding_row_in_shard']]==row['work_id']
        assert row['embedding_dim']==matrix.shape[1]==768
        assert row['embedding_dtype']==str(matrix.dtype)=='float16'
    values=np.asarray(matrix[positions],dtype=np.float32)
    assert np.isfinite(values).all()
    norms=np.linalg.norm(values,axis=1);assert (norms>0).all()
    min_norm=min(min_norm,float(norms.min()));max_norm=max(max_norm,float(norms.max()))
    for row in rows:
        output.append({**targets[row['work_id']],
                       'embedding_shard_path':str(SHARDS/name),
                       'embedding_row_in_shard':row['embedding_row_in_shard'],
                       'embedding_dim':768,'embedding_dtype':'float16',
                       'numerically_valid':True,'approved_for_final_experiments':False})
    del matrix,values
output.sort(key=lambda r:r['selection_order'])
pq.write_table(pa.Table.from_pylist(output),OUT/'legacy_embedding_candidates.parquet',compression='zstd')
summary=dict(exact_text_matches=len(targets),indexed_vectors=len(output),shards_checked=len(groups),
             all_matching_vectors_finite_nonzero=True,all_metadata_row_ids_match=True,
             norm_min=min_norm,norm_max=max_norm,
             readiness='Candidates only: exact model/tokenizer/adapter revisions and original input processing remain to be resolved. Additional cleaning may remove some IDs. No vectors recomputed or copied.')
(OUT/'legacy_embedding_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
