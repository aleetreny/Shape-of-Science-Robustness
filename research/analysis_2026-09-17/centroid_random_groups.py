"""Diagnostic random groups with fixed group and period sizes, on the paired 52k.

This follow-up tests a limitation of centroid aggregation; no p-values.
"""
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
import numpy as np
import pyarrow.parquet as pq
from scipy.stats import spearmanr
from sos_embed.storage import file_sha,object_sha,run_lock,utcnow,write_json
from sos_analysis.geometry import prepare
from sos_analysis.native_data import NativeData,load_control

OUT=ROOT/'data/analysis_v1/centroid_random_groups'


def run():
    files=['research/analysis_2026-09-17/centroid_random_groups.py','sos_analysis/geometry.py',
           'sos_analysis/native_data.py','sos_analysis/reader.py','config/analysis_v1.json']
    manifest={'files':{name:file_sha(ROOT/name) for name in files},'repeats':20,
      'seed_prefix':'sos-centroid-random-groups-v1','role':'diagnostic follow-up after native centroid inspection; no p-values',
      'input_sha256':file_sha(ROOT/'data/analysis_v1/controls/common_text_52k/input.parquet')}
    if (OUT/'manifest.json').exists() and json.loads((OUT/'manifest.json').read_text())!=manifest:raise ValueError('Changed diagnostic')
    for name in files:
        target=OUT/'source_snapshot'/name;target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():shutil.copyfile(ROOT/name,target)
    write_json(OUT/'manifest.json',manifest)
    data=NativeData(ROOT,max_bytes=2*1024**3);models=list(data.design['poolings'])
    input_table=pq.read_table(ROOT/'data/analysis_v1/controls/common_text_52k/input.parquet',columns=['row_index','work_id','text_sha256'])
    ids=input_table['row_index'].to_numpy();meta=data.metadata.take(ids)
    fields=meta['field_id'].to_numpy();periods=meta['period_start'].to_numpy()
    real=np.asarray([np.flatnonzero(fields==field) for field in sorted(np.unique(fields))])
    groups=[];seeds=[]
    for rep in range(20):
        pieces=[]
        for period in sorted(np.unique(periods)):
            label=f'sos-centroid-random-groups-v1/{rep}/{period}'
            seed=int.from_bytes(hashlib.sha256(label.encode()).digest()[:8],'little')
            positions=np.flatnonzero(periods==period)
            pieces.append(np.random.default_rng(seed).permutation(positions).reshape(26,400))
            seeds.append({'repeat':rep,'period_start':int(period),'seed':seed})
        groups.append(np.concatenate(pieces,axis=1))
    distances={};edges=np.triu_indices(26,1)
    for model,pool in data.design['poolings'].items():
        native=prepare(data.get(f'{model}/{pool}',ids))
        identity,array=load_control(ROOT,'data/analysis_v1/controls/common_text_52k',model,pool)
        if not identity.equals(input_table):raise ValueError('Wrong common input identity')
        common=prepare(array)
        for condition,values in [('native_paired',native),('common_paired',common)]:
            for rep,selection in [(-1,real),*enumerate(groups)]:
                centers=prepare(values[selection].mean(1))
                distances[condition,rep,model]=(1-centers@centers.T)[edges]
        del native,common,array
        print('Referencia de grupos aleatorios:',model,flush=True)
    scores=[]
    for condition in ('native_paired','common_paired'):
        for rep in range(-1,20):
            for a,b in itertools.combinations(models,2):
                value=spearmanr(distances[condition,rep,a],distances[condition,rep,b]).statistic
                scores.append({'condition':condition,'repeat':rep,'groups':'real' if rep==-1 else 'random',
                               'model_a':a,'model_b':b,'centroid_edge_spearman':float(value)})
    result={'scores':scores,'seeds':seeds,'manifest_sha256':object_sha(manifest),'completed_at':utcnow(),
      'interpretation':'20 shared permutations, 26 groups, each 2000 papers with exactly 400 per period; diagnostic distributions only'}
    write_json(OUT/'results.json',result)
    write_json(OUT/'results.sha.json',{'sha256':file_sha(OUT/'results.json')})
    write_json(OUT/'progress.json',{'state':'complete','updated_at':utcnow()})


if __name__=='__main__':
    with run_lock(OUT):run()
