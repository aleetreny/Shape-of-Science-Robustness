import csv, hashlib, json, platform, importlib.metadata
from pathlib import Path
import numpy as np
from sos_embed.storage import file_sha, write_json, utcnow
from sos_deep.artifacts import save_csv
ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'config/robustness_closure_v1.json'
D=json.loads(CONFIG.read_text());OUT=ROOT/D['output'];REPORT=ROOT/D['reports']
MODELS=D['models'];BASE=json.loads((ROOT/'config/analysis_v1.json').read_text());POOLS=BASE['poolings']
PAIRS=[(i,j) for i in range(10) for j in range(i+1,10)]
PERIODS=D['periods'];FIELDS=D['fields']
def seed(label): return int.from_bytes(hashlib.sha256((D['seed']+'/'+label).encode()).digest()[:8],'little')
def rng(label): return np.random.default_rng(seed(label))
def ids_sha(ids): return hashlib.sha256(np.asarray(ids,dtype='<i8').tobytes()).hexdigest()
def read_csv(path):
 with Path(path).open() as f:return list(csv.DictReader(f))
def freeze(branch,sources,parents=()):
 folder=OUT/branch;folder.mkdir(parents=True,exist_ok=True)
 src=['config/robustness_closure_v1.json','ROBUSTNESS_CLOSURE_PROTOCOL.md','sos_closure/__init__.py','sos_closure/common.py',*sources]
 parent=['research/robustness_closure_2026-09-20/phase0_audit.json',*parents]
 m={'source_files':{n:file_sha(ROOT/n) for n in src},'parent_files':{n:file_sha(ROOT/n) for n in parent},'environment':{'python':platform.python_version(),'packages':{p:importlib.metadata.version(p) for p in ['numpy','scipy','pyarrow']}},'configuration':D,'seed_rule':'first 8 SHA256 bytes little endian of seed/label'}
 p=folder/'manifest.json'
 if p.exists():assert json.loads(p.read_text())==m,('Frozen branch changed',branch)
 else:write_json(p,m)
 for n in src:
  dest=folder/'source_snapshot'/n;dest.parent.mkdir(parents=True,exist_ok=True)
  if dest.exists():assert file_sha(dest)==m['source_files'][n]
  else:dest.write_bytes((ROOT/n).read_bytes())
 return folder

def committed(folder):
 p=folder/'commit.json'
 if not p.exists():return False
 c=json.loads(p.read_text())
 for n,h in c['files'].items():assert file_sha(folder/n)==h,(folder,n)
 return True

def commit(folder,**extra):
 write_json(folder/'commit.json',{'completed_at':utcnow(),**extra,'files':{p.name:file_sha(p) for p in sorted(folder.iterdir()) if p.is_file() and p.name!='commit.json'}})

def finish(folder,**extra):
 write_json(folder/'audit.json',{'all_complete':True,'completed_at':utcnow(),**extra,'files':{str(p.relative_to(folder)):file_sha(p) for p in sorted(folder.rglob('*')) if p.is_file() and 'source_snapshot' not in p.parts and p.name not in ['audit.json','progress.json'] and not p.name.endswith('.lock')}})

def stats(values):
 x=np.asarray(values,float);assert np.isfinite(x).all() and x.size
 return {'n':int(x.size),'mean':float(x.mean()),'median':float(np.median(x)),'p025':float(np.quantile(x,.025)),'p975':float(np.quantile(x,.975)),'min':float(x.min()),'max':float(x.max())}

def selected(ids,periods,counts,label):
 out=np.concatenate([rng(label+'/'+str(p)).permutation(np.sort(ids[periods[ids]==p]))[:int(n)] for p,n in zip(PERIODS,counts)])
 assert len(out)==sum(counts) and len(np.unique(out))==len(out)
 assert all(np.sum(periods[out]==p)==n for p,n in zip(PERIODS,counts))
 return np.sort(out)
