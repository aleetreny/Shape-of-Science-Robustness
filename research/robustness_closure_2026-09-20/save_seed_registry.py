from pathlib import Path
import sys,json,csv
import numpy as np
sys.path.insert(0,str(Path('.').resolve()))
from sos_closure.common import seed,OUT,MODELS,FIELDS,PERIODS
rows={}
def add(branch,label):rows[branch,label]={'branch':branch,'label':label,'uint64_seed':seed(label)}
designs=json.loads((OUT/'centres/selections/designs.json').read_text())
for name,d in designs.items():
 for rep in range(d['repeats']):
  for level,group in d['keys']:
   for p in PERIODS:add('centres',f"centres/{d['family']}/{level}/{group}/{rep}/{p}")
  for p in PERIODS:add('centres',f'centres/random/{name}/{rep}/{p}')
chosen=np.load(OUT/'centres/selections/nested26.npz')['chosen_subfields']
for outer in range(50):
 for f in FIELDS:add('centres',f'centres/nested/subfield/{outer}/{f}')
 for inner in range(10):
  for sf in chosen[outer]:
   for p in PERIODS:add('centres',f'centres/nested/articles/{outer}/{inner}/{sf}/{p}')
  for p in PERIODS:add('centres',f'centres/nested/random/{outer}/{inner}/{p}')
for f in FIELDS:
 for rep in range(50):
  for p in PERIODS:add('headline',f'headline/{f}/{rep}/{p}')
 for p in PERIODS:
  add('quality',f'quality/queries/{f}/{p}')
  sel=np.load(OUT/'quality/selections'/f'{f}_{p}.npz')
  for n in [1024,2048]:
   if f'original_{n}' in sel:add('quality',f'quality/candidates/{f}/{p}/{n}')
  add('quality',f'quality/input/queries/{f}/{p}');add('quality',f'quality/input/candidates/{f}/{p}')
add('technical','technical/synthetic')
o=Path('research/robustness_closure_2026-09-20/random_seeds.csv')
with o.open('w') as f:
 w=csv.DictWriter(f,fieldnames=['branch','label','uint64_seed']);w.writeheader();w.writerows(rows.values())
print('Recorded actual numeric seeds:',len(rows))
