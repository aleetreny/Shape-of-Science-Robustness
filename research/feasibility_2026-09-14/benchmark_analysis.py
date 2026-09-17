"""Memory/time feasibility of exact query neighbors on 500k real legacy vectors."""
import json
from pathlib import Path
import time
import numpy as np
import torch

OUT=Path(__file__).resolve().parent
SOURCE=Path('/Users/alejandrotreny/Workspace/Mapping-Science/embeddings/specter2_v1_2000_2024_400py/analysis/main_embeddings.float16.npy')
torch.set_num_threads(8)
data=np.load(SOURCE,mmap_mode='r')
t=time.perf_counter()
reference=torch.tensor(np.asarray(data[:500000],dtype=np.float32),device='mps')
reference=torch.nn.functional.normalize(reference,dim=1)
torch.mps.synchronize(); load_seconds=time.perf_counter()-t
ids=np.random.default_rng(20260917).choice(len(reference),256,replace=False)
queries=reference[torch.tensor(ids,device='mps')]
torch.topk(queries[:8]@reference.T,21,dim=1);torch.mps.synchronize()
t=time.perf_counter();checksum=0;max_driver=0
for start in range(0,len(queries),32):
    scores=queries[start:start+32]@reference.T
    neighbors=torch.topk(scores,21,dim=1).indices
    checksum+=int(neighbors[:,1:].sum().item())
    max_driver=max(max_driver,torch.mps.driver_allocated_memory())
torch.mps.synchronize(); seconds=time.perf_counter()-t
report=dict(reference_rows=len(reference),query_rows=len(queries),dimensions=768,dtype='float32',device='mps',query_batch=32,topk=21,load_seconds=load_seconds,search_seconds=seconds,queries_per_second=len(queries)/seconds,estimated_10000_queries_seconds=10000*seconds/len(queries),observed_max_mps_driver_allocated_gib=max_driver/2**30,checksum=checksum,note='Timing only, first 500k legacy analysis rows; not a representative scientific sample. 21 retrieved to accommodate self; no neighbor-overlap conclusion is reported. Extrapolation is not a sustained whole-study runtime.')
(OUT/'analysis_benchmark.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
