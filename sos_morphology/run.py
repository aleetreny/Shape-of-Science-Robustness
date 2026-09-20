"""Bounded, resumable morphology pilot on verified existing representations."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import time
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from sos_embed.storage import Store, file_sha, write_json, utcnow, run_lock
from sos_analysis.native_data import NativeData, load_control
from sos_deep.artifacts import freeze
from .metrics import measure, spectrum, unit, gaussian_reference

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/'config/morphology_pilot_v1.json'
D=json.loads(DESIGN.read_text())
OUT=ROOT/D['output']
INPUTS=ROOT/'data/robustness_v2/inputs'


def seed(text):
    return int.from_bytes(hashlib.sha256((D['seed']+'/'+text).encode()).digest()[:8],'little')


def ids_sha(ids):
    return hashlib.sha256(np.asarray(ids,dtype='<i8').tobytes()).hexdigest()


def select(ids, periods, per_period, label):
    return np.sort(np.concatenate([np.random.default_rng(seed(label+'/'+str(p))).permutation(ids[periods==p])[:per_period] for p in D['periods']]))


def prepare(data):
    manifest=json.loads((INPUTS/'input_manifest.json').read_text())
    path=INPUTS/'native_input.parquet'
    assert file_sha(path)==manifest['files']['native_input.parquet']
    meta=data.metadata
    selected=pq.read_table(path,columns=['row_index','work_id','text_sha256','field_id','period_start'])
    ids=selected['row_index'].to_numpy()
    native=meta.take(pa.array(ids))
    for col in ['row_index','work_id','text_sha256','field_id','period_start']:
        assert selected[col].equals(native[col]),col
    fields=meta['field_id'].to_numpy();periods=meta['period_start'].to_numpy()
    flags=np.any(np.stack([meta[c].to_numpy(zero_copy_only=False) for c in D['controls']['quality_flags']]),axis=0)
    selections={};quality=[]
    for f in D['fields']:
        all_ids=np.flatnonzero(fields==f)
        primary=ids[fields[ids]==f]
        assert len(primary)==2000 and all(np.sum(periods[primary]==p)==400 for p in D['periods'])
        selections[f'primary_{f}']=primary
        for rep in range(D['stability']['within_52k_repeats']):
            selections[f'half_{f}_{rep}']=select(primary,periods[primary],200,f'half/{f}/{rep}')
        half=selections[f'half_{f}_0']
        selections[f'small_{f}']=select(half,periods[half],100,f'small/{f}')
        extra=np.setdiff1d(all_ids,primary)
        selections[f'large_{f}']=np.sort(np.concatenate([primary,select(extra,periods[extra],400,f'large/{f}')]))
        for rep in range(D['stability']['external_corpus_repeats']):
            selections[f'external_{f}_{rep}']=select(all_ids,periods[all_ids],400,f'external/{f}/{rep}')
        eligible=primary[~flags[primary]]
        keep=half[~flags[half]]
        add=[]
        for p in D['periods']:
            need=200-np.sum(periods[keep]==p)
            candidates=np.setdiff1d(eligible[periods[eligible]==p],keep)
            assert len(candidates)>=need
            add.extend(np.random.default_rng(seed(f'quality/{f}/{p}')).permutation(candidates)[:need])
        selections[f'quality_{f}']=np.sort(np.concatenate([keep,np.asarray(add,dtype=np.int64)]))
        quality.append({'field_id':f,'flagged_in_primary':int(flags[primary].sum()),'replaced_in_half':len(half)-len(keep)})
        for p in D['periods']:
            cell=primary[periods[primary]==p]
            selections[f'period_{f}_{p}']=cell
            if p in [2000,2020]:
                for rep in range(D['temporal']['endpoint_repeats']):
                    selections[f'period_half_{f}_{p}_{rep}']=np.sort(np.random.default_rng(seed(f'endpoint/{f}/{p}/{rep}')).choice(cell,200,replace=False))
    # Exactly 2,000, with 15/16 per cell; this is a calibrated mixture reference.
    cells=[(f,p) for f in D['fields'] for p in D['periods']]
    extra_cells=set(np.random.default_rng(seed('global')).choice(130,50,replace=False))
    global_ids=[]
    for i,(f,p) in enumerate(cells):
        rows=ids[(fields[ids]==f)&(periods[ids]==p)]
        global_ids.extend(np.random.default_rng(seed(f'global/{f}/{p}')).choice(rows,15+int(i in extra_cells),replace=False))
    selections['global']=np.sort(global_ids)
    selections['all_primary']=ids
    path=OUT/'selections.npz'
    if path.exists():
        with np.load(path,allow_pickle=False) as old:
            assert set(old.files)==set(selections)
            assert all(np.array_equal(old[k],v) for k,v in selections.items())
    else:np.savez_compressed(path,**selections)
    write_json(OUT/'selection_audit.json',{'verified_at':utcnow(),'arrays':len(selections),
        'unique_primary':len(set(ids)),'primary_per_field':2000,'primary_per_period':400,
        'paired_across_models':True,'selection_sha256':file_sha(path),'quality':quality,
        'all_selection_hashes':{k:ids_sha(v) for k,v in selections.items()}})
    return selections


def load_input(model, condition, pool):
    folder=INPUTS/condition/model
    manifest=json.loads((folder/'manifest.json').read_text())
    inp=INPUTS/(('native' if condition=='title_abstract' else condition)+'_input.parquet')
    assert manifest['input_sha256']==file_sha(inp)
    expected=pq.read_table(inp,columns=['row_index','work_id','text_sha256'])
    assert manifest['condition']==condition and manifest['model']['key']==model
    assert Store(folder,manifest).scan(expected)['complete']
    arr=np.concatenate([np.load(s/(pool+'.npy'),allow_pickle=False) for s in sorted((folder/'shards').glob('[0-9]*'))])
    assert len(arr)==len(expected)
    return expected['row_index'].to_numpy(),arr,file_sha(folder/'manifest.json')


def record(rows, model, kind, field, ids, x, *, rep=0, period=0, full=True, **extra):
    ids=np.asarray(ids);order=np.argsort(ids,kind='stable');ids=ids[order];x=x[order]
    assert len(set(ids))==len(ids)
    rows.append({'model':model,'kind':kind,'field_id':int(field),'period':int(period),
        'repeat':int(rep),'selection_sha256':ids_sha(ids),**extra,**measure(x,full=full)})


def save_part(stage,model,rows,provenance):
    path=OUT/'parts'/(stage+'__'+model+'.json');path.parent.mkdir(exist_ok=True)
    write_json(path,{'model':model,'stage':stage,'rows':rows,'provenance':provenance})
    write_json(path.with_suffix('.sha.json'),{'sha256':file_sha(path),'completed_at':utcnow()})


def completed(stage,model):
    path=OUT/'parts'/(stage+'__'+model+'.json')
    if not path.exists():return False
    assert file_sha(path)==json.loads(path.with_suffix('.sha.json').read_text())['sha256']
    return True


def native_stage(data,sel,model,pool):
    if completed('native',model):return
    rows=[];name=model+'/'+pool
    getter=lambda ids:data.get(name,ids)
    for f in D['fields']:
        ids=sel[f'primary_{f}'];record(rows,model,'primary',f,ids,getter(ids))
        for rep in range(20):
            ids=sel[f'half_{f}_{rep}'];record(rows,model,'half',f,ids,getter(ids),rep=rep,full=rep==0)
        for rep in range(5):
            ids=sel[f'external_{f}_{rep}'];record(rows,model,'external',f,ids,getter(ids),rep=rep,full=rep==0)
        for size,tag in [(500,'small'),(4000,'large')]:
            ids=sel[f'{tag}_{f}'];record(rows,model,'size',f,ids,getter(ids))
        print(f'native {model} Field {f} complete',flush=True)
    ids=sel['global'];record(rows,model,'global',0,ids,getter(ids))
    save_part('native',model,rows,{'catalog':data.reader.catalog['models'][model]['manifest_sha256'],'pooling':pool})


def temporal_stage(data,sel,model,pool):
    if completed('temporal',model):return
    rows=[]
    for f in D['fields']:
        for p in D['periods']:
            ids=sel[f'period_{f}_{p}'];record(rows,model,'period',f,ids,data.get(model+'/'+pool,ids),period=p)
        for p in [2000,2020]:
            for rep in range(10):
                ids=sel[f'period_half_{f}_{p}_{rep}'];record(rows,model,'period_half',f,ids,data.get(model+'/'+pool,ids),rep=rep,period=p,full=False)
    save_part('temporal',model,rows,{'pooling':pool})


def controls_stage(data,sel,model,pool):
    if completed('controls',model):return
    rows=[];provenance={};name=model+'/'+pool
    periods=data.metadata['period_start'].to_numpy()
    global_center=unit(data.get(name,sel['all_primary'])).mean(axis=0)
    for f in D['fields']:
        ids=sel[f'half_{f}_0'];x=data.get(name,ids)
        record(rows,model,'global_centered',f,ids,unit(x)-global_center)
        qi=sel[f'quality_{f}'];record(rows,model,'quality',f,qi,data.get(name,qi))
        xu=unit(x);radii=np.linalg.norm(xu-xu.mean(0),axis=1)
        trim=[];rand=[]
        for p in D['periods']:
            positions=np.flatnonzero(periods[ids]==p)
            trim.extend(positions[np.argsort(radii[positions],kind='stable')[:190]])
            rand.extend(np.random.default_rng(seed(f'trim/{f}/{p}')).choice(positions,190,replace=False))
        for kind,inds in [('trim_extreme',trim),('trim_random',rand)]:
            inds=np.asarray(inds);record(rows,model,kind,f,ids[inds],x[inds])
        for rep in range(3):
            ref=gaussian_reference(x,seed(f'gaussian/{model}/{f}/{rep}'))
            record(rows,model,'gaussian',f,ids,ref,rep=rep,full=rep==0)
    for condition in ['title','abstract']:
        allids,arr,digest=load_input(model,condition,pool);provenance[condition]=digest
        for f in D['fields']:
            ids=sel[f'half_{f}_0'];pos=np.searchsorted(allids,ids);assert np.array_equal(allids[pos],ids)
            record(rows,model,condition,f,ids,arr[pos])
    if model in D['controls']['word_bert_models']:
        for recipe in ['cls','sep']:
            for f in D['fields']:
                ids=sel[f'half_{f}_0'];record(rows,model,'pool_'+recipe,f,ids,data.get(model+'/'+recipe,ids))
    identity,arr=load_control(ROOT,D['controls']['common_directory'],model,pool)
    allids=identity['row_index'].to_numpy()
    original=data.metadata.take(pa.array(allids))
    assert identity['work_id'].equals(original['work_id'])
    common_source=pq.read_table(ROOT/D['controls']['common_directory']/'input.parquet',columns=['source_text_sha256'])
    assert common_source['source_text_sha256'].equals(original['text_sha256'])
    provenance['common']=file_sha(ROOT/D['controls']['common_directory']/model/'manifest.json')
    fs=original['field_id'].to_numpy()
    for f in D['fields']:
        pos=np.flatnonzero(fs==f);ids=allids[pos];assert len(ids)==2000
        record(rows,model,'common',f,ids,arr[pos])
        record(rows,model,'common_native',f,ids,data.get(name,ids))
    if model=='minilm':
        identity,arr=load_control(ROOT,D['controls']['minilm512_directory'],model,pool)
        assert np.array_equal(identity['row_index'].to_numpy(),np.arange(500000))
        provenance['minilm512']=file_sha(ROOT/D['controls']['minilm512_directory']/model/'manifest.json')
        for f in D['fields']:
            ids=sel[f'primary_{f}'];record(rows,model,'minilm512',f,ids,arr[ids])
    save_part('controls',model,rows,provenance)


def audit():
    rows=[];files={};counts={}
    for stage in ['native','temporal','controls']:
        for model in D['models']:
            assert completed(stage,model),(stage,model)
            path=OUT/'parts'/(stage+'__'+model+'.json')
            part=json.loads(path.read_text());rows.extend(part['rows'])
            files[str(path.relative_to(OUT))]=file_sha(path)
            counts[stage+'/'+model]=len(part['rows'])
    keys=sorted(set().union(*(r.keys() for r in rows)))
    table=pa.Table.from_pylist([{k:r.get(k) for k in keys} for r in rows])
    pq.write_table(table,OUT/'metrics.parquet',compression='zstd')
    for row in rows:
        assert row['n']>=200
        assert 1-1e-8 <= row['pr'] <= min(row['dimension'],row['n']-1)+1e-6
        assert 0<=row['gap_25']<=2
        assert 0<=row['angle_p50']<=180
        assert row['union_giant_25']>=row['mutual_giant_25']
        if 'gap_residual_25' in row:assert row['gap_residual_25']<1e-6
    for name in ['metrics.parquet','manifest.json','selections.npz','selection_audit.json']:
        files[name]=file_sha(OUT/name)
    write_json(OUT/'audit.json',{'all_complete':True,'completed_at':utcnow(),'rows':len(rows),'counts':counts,
        'files':files,'finite_metrics':True,'parents_read_only':True,'new_inference':False})
    print('MORPHOLOGY PILOT COMPLETE',len(rows),'metric sets',flush=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('--stage',choices=['prepare','native','temporal','controls','all','audit'],default='all');a=p.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    with run_lock(OUT):
        sources=['sos_morphology/metrics.py','sos_morphology/run.py','sos_morphology/synthetic.py','sos_morphology/__init__.py',
                 'config/morphology_pilot_v1.json','MORPHOLOGY_PROTOCOL.md','sos_analysis/native_data.py','sos_analysis/reader.py',
                 'sos_embed/storage.py','sos_deep/artifacts.py']
        parents=['config/input52_v1.json','data/robustness_v2/inputs/input_manifest.json',
                 'research/embedding_final_audit_2026-09-17/catalog.json','data/robustness_v2/final_audit/audit.json']
        freeze(OUT,sources,parents,D)
        if a.stage=='audit':audit();return
        data=NativeData(ROOT,max_bytes=6*1024**3)
        sel=prepare(data)
        if a.stage=='prepare':print('PREPARED',len(sel),'selections');return
        start=time.monotonic()
        for model,pool in D['models'].items():
            for stage,fn in [('native',native_stage),('temporal',temporal_stage),('controls',controls_stage)]:
                if a.stage in ['all',stage]:
                    fn(data,sel,model,pool)
                    write_json(OUT/'progress.json',{'state':'running','model':model,'stage':stage,'updated_at':utcnow(),'elapsed_s':time.monotonic()-start})
                    print(model,stage,'finished',round(time.monotonic()-start,1),'seconds',flush=True)
        if a.stage=='all':audit();write_json(OUT/'progress.json',{'state':'complete','updated_at':utcnow(),'elapsed_s':time.monotonic()-start})


if __name__=='__main__':main()
