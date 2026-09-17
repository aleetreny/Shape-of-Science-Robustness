"""Follow-up sensitivity of Field-centroid relations; no new embeddings.

Declared after inspecting the native centroid result, before these controls.
This is a transparently labelled robustness follow-up, not preregistration.
"""
import hashlib
import itertools
import json
from pathlib import Path
import shutil

import numpy as np
from scipy.stats import spearmanr
from sos_embed.storage import file_sha,object_sha,run_lock,utcnow,write_json
from .geometry import prepare
from .native_data import NativeData,load_control
from .run_shape import strict_quality

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/analysis_v1/macro_controls'
WORD=('scibert','bert','pubmedbert','biobert')


def distances(centres):
    values=prepare(np.asarray(centres))
    return (1-values@values.T)[np.triu_indices(len(values),1)]


def compare(all_distances,models):
    return [{'model_a':a,'model_b':b,
             'centroid_edge_spearman':float(spearmanr(all_distances[a],all_distances[b]).statistic)}
            for a,b in itertools.combinations(models,2)]


def run():
    files=['sos_analysis/macro_controls.py','sos_analysis/geometry.py','sos_analysis/native_data.py',
           'sos_analysis/run_shape.py','sos_analysis/reader.py','config/analysis_v1.json']
    manifest={'files':{name:file_sha(ROOT/name) for name in files},
              'role':'Follow-up centroid robustness; declared after the native result',
              'common_text_field_pooled':'2000 per Field; five periods equally represented',
              'common_input_sha256':file_sha(ROOT/'data/analysis_v1/controls/common_text_52k/input.parquet'),
              'common_manifests_sha256':{m:file_sha(ROOT/'data/analysis_v1/controls/common_text_52k'/m/'manifest.json')
                  for m in json.loads((ROOT/'config/analysis_v1.json').read_text())['poolings']},
              'native_parent_manifest_sha256':file_sha(ROOT/'data/analysis_v1/shape/manifest.json')}
    path=OUT/'manifest.json'
    if path.exists() and json.loads(path.read_text())!=manifest:raise ValueError('Macro control changed')
    for name in files:
        target=OUT/'source_snapshot'/name;target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists() and file_sha(target)!=manifest['files'][name]:raise ValueError('Snapshot mismatch')
        if not target.exists():shutil.copyfile(ROOT/name,target)
    write_json(path,manifest)
    write_json(OUT/'progress.json',{'state':'running','updated_at':utcnow()})
    data=NativeData(ROOT,max_bytes=2*1024**3);models=list(data.design['poolings'])
    cells=data.cells();fields=sorted({f for f,p in cells});periods=sorted({p for f,p in cells})
    quality=strict_quality(data);centres={};common_centres={};native_paired_centres={}
    identity_reference=None
    for model,pool in data.design['poolings'].items():
        for recipe in (('mean','cls','sep') if model in WORD else (pool,)):
            name=f'{model}/{recipe}';raw=data.get(name,slice(None));centres[name]={}
            for cell,ids in cells.items():centres[name][cell]=prepare(raw[ids]).mean(0)
            if recipe==pool:
                centres[name+'/quality']={cell:prepare(raw[ids[quality[ids]]]).mean(0) for cell,ids in cells.items()}
                centres[name+'/raw']={cell:raw[ids].astype(np.float64).mean(0) for cell,ids in cells.items()}
        native=data.get(f'{model}/{pool}',slice(None))
        identity,common=load_control(ROOT,'data/analysis_v1/controls/common_text_52k',model,pool)
        if identity_reference is not None and not identity.equals(identity_reference):raise ValueError('Different common IDs/texts')
        identity_reference=identity
        source_ids=identity['row_index'].to_numpy();source=data.metadata.take(source_ids)
        if source['work_id'].to_pylist()!=identity['work_id'].to_pylist():raise ValueError('Wrong common source IDs')
        common_centres[model]={};native_paired_centres[model]={}
        for field in fields:
            positions=np.flatnonzero(source['field_id'].to_numpy()==field)
            if len(positions)!=2000:raise ValueError('Expected 2000 common papers per field')
            common_centres[model][field]=prepare(common[positions]).mean(0)
            native_paired_centres[model][field]=prepare(native[source_ids[positions]]).mean(0)
        del native,common,raw
        print('Controles de relaciones entre áreas:',model,flush=True)
    scores=[];edges=[]
    for stage in ('mean','cls','sep','quality','raw'):
        names={model:f'{model}/{stage if stage in ("cls","sep") and model in WORD else pool}'+
               (('/'+stage) if stage in ('quality','raw') else '') for model,pool in data.design['poolings'].items()}
        for period in periods:
            by_model={m:distances([centres[names[m]][field,period] for field in fields]) for m in models}
            scores.extend({'stage':stage,'period_start':period,**r} for r in compare(by_model,models))
            for m in models:
                edges.extend({'stage':stage,'period_start':period,'model':m,'field_a':a,'field_b':b,'cosine_distance':float(d)}
                             for (a,b),d in zip(itertools.combinations(fields,2),by_model[m]))
    original=json.loads((ROOT/'data/analysis_v1/shape/centroids/relations.json').read_text())
    reference={(r['period_start'],r['model_a'].split('/')[0],r['model_b'].split('/')[0]):r['centroid_edge_spearman'] for r in original['scores']}
    for r in scores:
        if r['stage']=='mean' and not np.isclose(r['centroid_edge_spearman'],reference[r['period_start'],r['model_a'],r['model_b']],atol=1e-12,rtol=0):
            raise ValueError('Native centroid reconstruction differs')
    for label,values in [('native_paired',native_paired_centres),('common_paired',common_centres)]:
        by_model={m:distances([values[m][f] for f in fields]) for m in models}
        scores.extend({'stage':label,'period_start':'pooled_equal_five_periods',**r} for r in compare(by_model,models))
        for m in models:
            edges.extend({'stage':label,'period_start':'pooled_equal_five_periods','model':m,'field_a':a,'field_b':b,'cosine_distance':float(d)}
                         for (a,b),d in zip(itertools.combinations(fields,2),by_model[m]))
    result={'scores':scores,'edges':edges,'manifest_sha256':object_sha(manifest),'completed_at':utcnow(),
        'native_reconstruction_matches':True,'common_source_indices_sha256':hashlib.sha256(source_ids.astype('<i8').tobytes()).hexdigest(),
        'interpretation':'Native controls compare 325 relations per period. Paired text control pools 2000 papers per Field equally over time.'}
    destination=OUT/'relations.json';write_json(destination,result)
    write_json(destination.with_suffix('.sha.json'),{'sha256':file_sha(destination)})
    write_json(OUT/'progress.json',{'state':'complete','updated_at':utcnow()})


if __name__=='__main__':
    with run_lock(OUT):run()
