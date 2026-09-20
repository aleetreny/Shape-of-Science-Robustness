"""Read and verify the already completed 52,000-paper input experiment."""
import numpy as np
from sos_deep.input_analysis52 import verified_inputs,INPUTS
from .common import *
def load_inputs(alternatives=False):
 meta,primary,parents=verified_inputs()
 arrays={(m,POOLS[m],c):x for (m,c),x in primary.items()}
 if alternatives:
  for m in D['word_models']:
   for c in ['title_abstract','title']:
    # verified_inputs already checks each complete store, including its saved poolings.
    for pool in ['cls','sep']:
     arr=np.concatenate([np.load(s/(pool+'.npy'),allow_pickle=False) for s in sorted((INPUTS/c/m/'shards').glob('[0-9]*'))]);assert len(arr)==len(meta)
     arrays[m,pool,c]=arr
 return meta,arrays,parents
