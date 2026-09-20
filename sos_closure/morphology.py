"""Complete the saved morphology selections, without graphs or new embeddings."""
import argparse,time
import numpy as np
import pyarrow as pa, pyarrow.parquet as pq
from scipy.spatial.distance import pdist
from sos_analysis.native_data import NativeData
from sos_morphology.metrics import unit,spectrum
from sos_embed.storage import run_lock
from .common import *
CONDITIONS=[('primary',0)]+[('half',r) for r in range(20)]+[('external',r) for r in range(5)]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--models',nargs='*');args=ap.parse_args()
 folder=freeze('morphology',['sos_closure/morphology.py','sos_morphology/metrics.py','sos_analysis/native_data.py','sos_analysis/reader.py'],['data/morphology_pilot_v1/audit.json','data/morphology_pilot_v1/metrics.parquet','data/morphology_pilot_v1/selections.npz',BASE['catalog']])
 with run_lock(folder):
  data=NativeData(ROOT,max_bytes=2*1024**3);sel=np.load(ROOT/'data/morphology_pilot_v1/selections.npz');old=pq.read_table(ROOT/'data/morphology_pilot_v1/metrics.parquet').to_pylist()
  index={(r['model'],r['kind'],r['field_id'],r['repeat']):r for r in old if r['kind'] in ['primary','half','external','global_centered']}
  for model in args.models or MODELS:
   sub=folder/model;sub.mkdir(exist_ok=True)
   if committed(sub):continue
   t=time.monotonic();raw=data.get(model+'/'+POOLS[model],slice(None));global_mean=unit(raw[sel['all_primary']]).mean(0);np.save(sub/'global_mean.npy',global_mean)
   rows=[];maxpr=0.;maxalt=0.;maxcenter=0.
   for f in FIELDS:
    part=sub/f'{f}.json'
    if part.exists():
     saved=json.loads(part.read_text());assert file_sha(part)==json.loads(part.with_suffix('.sha.json').read_text())['sha256'];rows+=saved['rows'];maxpr=max(maxpr,saved['pr_error']);maxalt=max(maxalt,saved['alternative_error']);maxcenter=max(maxcenter,saved['center_error']);continue
    fr=[];pe=ae=ce=0.
    for kind,rep in CONDITIONS:
     key=f'{kind}_{f}'+(f'_{rep}' if kind!='primary' else '');ids=sel[key];x=unit(raw[ids]);ref=index[model,kind,f,rep];assert ids_sha(ids)==ref['selection_sha256']
     original=spectrum(x,full=True);pe=max(pe,abs(original['pr']-ref['pr']))
     for k in ['erank','d80']:
      if ref.get(k) is not None:ae=max(ae,abs(original[k]-ref[k]))
     centered=unit(x-global_mean);sp=spectrum(centered,full=False)
     median_chord=float(np.quantile(pdist(centered,metric='euclidean'),.5));angle=float(2*np.arcsin(np.clip(median_chord/2,0,1))*180/np.pi)
     if kind=='half' and rep==0:
      cr=index[model,'global_centered',f,0];ce=max(ce,abs(angle-cr['angle_p50']),abs(sp['pr']-cr['pr']))
     info={'model':model,'field_id':f,'kind':kind,'repeat':rep,'n':len(ids),'selection_sha256':ids_sha(ids)}
     fr.append({**info,'representation':'original','angle_p50':ref['angle_p50'],'pr':original['pr'],'erank':original['erank'],'d80':original['d80']})
     fr.append({**info,'representation':'global_centered','angle_p50':angle,'pr':sp['pr'],'erank':None,'d80':None})
    assert pe<1e-8 and ae<1e-8 and ce<1e-8,(model,f,pe,ae,ce)
    write_json(part,{'rows':fr,'pr_error':pe,'alternative_error':ae,'center_error':ce});write_json(part.with_suffix('.sha.json'),{'sha256':file_sha(part)})
    rows+=fr;maxpr=max(maxpr,pe);maxalt=max(maxalt,ae);maxcenter=max(maxcenter,ce)
    print(f'MORPHOLOGY {model} Field {f}: {time.monotonic()-t:.1f}s',flush=True)
   pq.write_table(pa.Table.from_pylist(rows),sub/'metrics.parquet');commit(sub,rows=len(rows),pr_max_error=maxpr,alternative_max_error=maxalt,old_center_max_error=maxcenter,seconds=time.monotonic()-t)
  if all(committed(folder/m) for m in MODELS):
   tables=[pq.read_table(folder/m/'metrics.parquet') for m in MODELS];table=pa.concat_tables(tables);assert len(table)==13520
   pq.write_table(table,folder/'metrics.parquet');finish(folder,rows=len(table),conditions=26,models=10,fields=26)
if __name__=='__main__':main()
