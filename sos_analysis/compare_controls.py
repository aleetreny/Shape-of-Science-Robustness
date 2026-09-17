"""Paired scientific length controls, always using identical source paper IDs."""
import argparse
import hashlib
import importlib.metadata
import itertools
import json
from pathlib import Path
import shutil
import time

import numpy as np

from sos_embed.storage import Store, file_sha, object_sha, run_lock, utcnow, write_json
from .geometry import shape_scores, rsa_scores, prepare
from .native_data import NativeData, load_control
from .neighbors import exact_neighbors, shared_counts

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/analysis_v1/robustness_controls'
COMMON = 'data/analysis_v1/controls/common_text_52k'


def seed(label):
    return int.from_bytes(hashlib.sha256(('sos-control-v1/' + label).encode()).digest()[:8], 'little')


def freeze():
    files = ['sos_analysis/compare_controls.py','sos_analysis/geometry.py','sos_analysis/neighbors.py',
             'sos_analysis/native_data.py','sos_analysis/reader.py','config/analysis_v1.json','config/neighbors_v1.json']
    manifest = {'files': {name: file_sha(ROOT/name) for name in files},
                'packages': {p: importlib.metadata.version(p) for p in ('numpy','scipy','pyarrow')}}
    path = OUT / 'manifest.json'
    if path.exists():
        if json.loads(path.read_text()) != manifest:
            raise ValueError('Control comparison changed; use new version')
    else:
        for name in files:
            target = OUT / 'source_snapshot' / name
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/name,target)
        write_json(path,manifest)
    return manifest


def done(path, manifest):
    if not path.exists():
        return False
    if json.loads(path.read_text())['manifest_sha256'] != object_sha(manifest):
        raise ValueError('Different control analysis')
    if file_sha(path) != json.loads(path.with_suffix('.sha.json').read_text())['sha256']:
        raise ValueError('Control result changed')
    return True


def save(path, manifest, result):
    write_json(path, {**result, 'manifest_sha256': object_sha(manifest), 'completed_at': utcnow()})
    write_json(path.with_suffix('.sha.json'), {'sha256': file_sha(path)})


def minilm(data, manifest):
    expected, extended = load_control(ROOT, 'data/analysis_v1/controls/minilm_512', 'minilm', 'mean')
    if not expected.equals(data.metadata.select(['row_index','work_id','text_sha256'])):
        raise ValueError('MiniLM length comparison identity mismatch')
    names = [f'{m}/{p}' for m,p in data.design['poolings'].items()]
    variant = 'minilm_512/mean'
    models = list(data.design['poolings'])
    for field,period in data.cells():
        for model in models:
            if not (ROOT/'data/analysis_v1/neighbors/local'/f'{field}_{period}'/model/'commit.json').exists():
                raise ValueError('Complete native neighbors before the length comparison')
    for (field,period),ids in data.cells().items():
        path = OUT / 'minilm512' / f'{field}_{period}.json'
        if done(path,manifest):
            continue
        started=time.monotonic()
        arrays=[data.get(n,ids) for n in names]+[extended[ids]]
        all_names=names+[variant]
        scores=[r for r in shape_scores(arrays,all_names) if variant in (r['model_a'],r['model_b'])]
        original=data.get('minilm/mean',ids)
        old_knn,_=exact_neighbors(original,ids,k=max(data.design['knn_k']))
        new_knn,_=exact_neighbors(extended[ids],ids,k=max(data.design['knn_k']))
        changes=[]
        # Compare every existing native model with the same MiniLM variant on the
        # same candidate set. Never replace the original principal result.
        for model in models:
            folder=ROOT/'data/analysis_v1/neighbors/local'/f'{field}_{period}'/model
            if (folder/'commit.json').exists():
                commit=json.loads((folder/'commit.json').read_text())
                for name,digest in commit['files'].items():
                    if file_sha(folder/name)!=digest: raise ValueError('Changed neighbor input')
                np.testing.assert_array_equal(np.load(folder/'query_row_index.npy'),ids)
                reference=np.load(folder/'neighbors.npy',mmap_mode='r')
                for k in data.design['knn_k']:
                    before=shared_counts(old_knn,reference,k)/k
                    after=shared_counts(new_knn,reference,k)/k
                    changes.append({'other_model':model,'k':k,'native_overlap':float(before.mean()),
                                    'extended_overlap':float(after.mean()),'delta_overlap':float((after-before).mean())})
        preservation={str(k):float((shared_counts(old_knn,new_knn,k)/k).mean()) for k in data.design['knn_k']}
        save(path,manifest,{'field_id':field,'period_start':period,'n':len(ids),'scores':scores,
                          'minilm_neighbor_preservation':preservation,'comparison_with_others':changes,
                          'seconds':time.monotonic()-started})
        print('Control MiniLM 512:',field,period,flush=True)


def common(data, manifest):
    names=[f'{m}/{p}' for m,p in data.design['poolings'].items()]
    models=list(data.design['poolings'])
    common_vectors={};expected=None;control_manifests={}
    for model,pool in data.design['poolings'].items():
        identity,array=load_control(ROOT,COMMON,model,pool)
        if expected is not None and not identity.equals(expected):
            raise ValueError('Common models use different IDs/texts')
        expected=identity;common_vectors[f'{model}/{pool}']=array
        control_manifests[model]=file_sha(ROOT/COMMON/model/'manifest.json')
    source_ids=expected['row_index'].to_numpy()
    source=data.metadata.take(source_ids)
    import pyarrow.parquet as pq
    common_source=pq.read_table(ROOT/COMMON/'input.parquet',columns=['source_text_sha256'])
    if common_source['source_text_sha256'].to_pylist()!=source['text_sha256'].to_pylist():
        raise ValueError('Common source text differs from the frozen corpus')
    if source['work_id'].to_pylist()!=expected['work_id'].to_pylist():
        raise ValueError('Common IDs do not match source corpus')
    fields=source['field_id'].to_numpy();periods=source['period_start'].to_numpy()
    # Capture scientific input provenance once in the result directory.
    write_json(OUT/'common_input_provenance.json',{'control_manifests':control_manifests,
               'input_manifest_sha256':file_sha(ROOT/COMMON/'input_manifest.json'),
               'source_indices_sha256':hashlib.sha256(source_ids.astype('<i8').tobytes()).hexdigest()})
    for field in np.unique(fields):
        path=OUT/'common_fields'/f'{field}.json'
        if done(path,manifest):continue
        positions=np.flatnonzero(fields==field);ids=source_ids[positions]
        if len(ids)!=2000:raise ValueError('Expected 2000 matched papers per Field')
        native=[data.get(name,ids) for name in names]
        common_arrays=[common_vectors[name][positions] for name in names]
        before=shape_scores(native,names);after=shape_scores(common_arrays,names)
        get_native=lambda name,i:data.get(name,ids[i])
        get_common=lambda name,i:common_vectors[name][positions[i]]
        rsa_before=rsa_scores(get_native,np.arange(len(ids)),names,seed=seed(f'rsa/{field}'))
        rsa_after=rsa_scores(get_common,np.arange(len(ids)),names,seed=seed(f'rsa/{field}'))
        for table,values in ((before,rsa_before),(after,rsa_after)):
            for r in table:r['rsa_spearman']=values[r['model_a'],r['model_b']]
        own=[]
        for name,x,y in zip(names,native,common_arrays):
            own.append({'model':name,**shape_scores([x,y],['native','common'])[0]})
        # Nested sample-size check on exactly the paired common/native texts.
        samples=[]
        for rep in range(20):
            chosen=np.sort(np.random.default_rng(seed(f'stability/{field}/{rep}')).choice(2000,1000,replace=False))
            for label,arrays in (('native',native),('common',common_arrays)):
                for r in shape_scores([a[chosen] for a in arrays],names,procrustes=False):
                    samples.append({**r,'repeat':rep,'text':label})
        save(path,manifest,{'field_id':int(field),'n':2000,'period_weight':'equal; 400 from each period',
             'native_scores':before,'common_scores':after,'same_model_native_common':own,
             'subsamples_n1000':samples,'indices_sha256':hashlib.sha256(ids.astype('<i8').tobytes()).hexdigest()})
        print('Texto común, forma:',int(field),flush=True)
    # Paired neighbor controls use each cell's same 400 candidates in both text conditions.
    for (field,period),_ in data.cells().items():
        path=OUT/'common_neighbors'/f'{field}_{period}.json'
        if done(path,manifest):continue
        pos=np.flatnonzero((fields==field)&(periods==period));ids=source_ids[pos]
        native={};controlled={}
        for name in names:
            native[name],_=exact_neighbors(data.get(name,ids),ids,k=50)
            controlled[name],_=exact_neighbors(common_vectors[name][pos],ids,k=50)
        rows=[]
        for a,b in itertools.combinations(names,2):
            for k in data.design['knn_k']:
                old=shared_counts(native[a],native[b],k)/k
                new=shared_counts(controlled[a],controlled[b],k)/k
                chance=k/(len(ids)-1)
                rows.append({'model_a':a,'model_b':b,'k':k,'native_overlap':float(old.mean()),
                    'common_overlap':float(new.mean()),'delta_overlap':float((new-old).mean()),
                    'native_adjusted':float(((old-chance)/(1-chance)).mean()),
                    'common_adjusted':float(((new-chance)/(1-chance)).mean())})
        save(path,manifest,{'field_id':field,'period_start':period,'n':len(ids),'scores':rows,
             'interpretation':'same 400 candidates per condition; not directly comparable to full-cell overlap'})
        print('Texto común, vecinos:',field,period,flush=True)


def pooling(data, manifest):
    for model in ('scibert','bert','pubmedbert','biobert'):
        names=[f'{model}/{p}' for p in ('mean','cls','sep')]
        # This isolates recipe changes within one model, using existing vectors.
        for (field,period),ids in data.cells().items():
            path=OUT/'pooling'/model/f'{field}_{period}.json'
            if done(path,manifest):continue
            scores=shape_scores([data.get(name,ids) for name in names],names)
            save(path,manifest,{'model':model,'field_id':field,'period_start':period,'n':len(ids),'scores':scores})
        print('Control de receta:',model,flush=True)


def balanced_neighbors(data, manifest):
    """Separate fixed-size candidate control; do not redefine the full analysis."""
    works = data.metadata['work_id'].to_pylist()
    ranks = [hashlib.sha256(('sos-v1-equal-neighbors/' + w).encode()).digest() for w in works]
    cells = data.cells()
    selected = {cell: np.asarray(sorted(sorted(ids, key=lambda i: ranks[i])[:2048]), dtype=np.int64)
                for cell, ids in cells.items()}
    joined_ids = np.concatenate(list(selected.values()))
    variants = dict(data.design['poolings'])
    names = [f'{m}/{p}' for m,p in variants.items()]
    names += [f'{m}/{p}' for m in ('scibert','bert','pubmedbert','biobert') for p in ('cls','sep')]
    neighbors = {}
    for name in names:
        folder = OUT/'equal2048_neighbors'/'arrays'/name
        check = folder/'validation.json'
        if done(check, manifest):
            record = json.loads(check.read_text())
            if file_sha(folder/'neighbors.npy') != record['neighbors_sha256']:
                raise ValueError('Changed equal-size neighbor control')
        else:
            raw = data.get(name, slice(None))
            result = []
            for cell,ids in selected.items():
                result.append(exact_neighbors(raw[ids], ids, k=50)[0])
            folder.mkdir(parents=True,exist_ok=True)
            with (folder/'neighbors.npy.tmp').open('wb') as stream:
                np.save(stream,np.concatenate(result))
            (folder/'neighbors.npy.tmp').replace(folder/'neighbors.npy')
            save(check,manifest,{'model':name,'rows':len(joined_ids),'candidates_per_cell':2048,
                'indices_sha256':hashlib.sha256(joined_ids.astype('<i8').tobytes()).hexdigest(),
                'neighbors_sha256':file_sha(folder/'neighbors.npy')})
            del raw, result
        neighbors[name] = np.load(folder/'neighbors.npy',mmap_mode='r')
        print('Vecinos con 2.048 candidatos:',name,flush=True)
    for ci,((field,period),ids) in enumerate(selected.items()):
        path = OUT/'equal2048_neighbors'/'summary'/f'{field}_{period}.json'
        if done(path,manifest):continue
        block = slice(ci*2048,(ci+1)*2048)
        rows = []
        for recipe in ('mean','cls','sep'):
            use = {m:f'{m}/{recipe if m in ("scibert","bert","pubmedbert","biobert") else p}'
                   for m,p in variants.items()}
            for a,b in itertools.combinations(use,2):
                for k in data.design['knn_k']:
                    values = shared_counts(neighbors[use[a]][block],neighbors[use[b]][block],k)/k
                    chance = k/2047
                    rows.append({'model_a':a,'model_b':b,'recipe':recipe,'k':k,
                        'mean_overlap':float(values.mean()),
                        'mean_chance_adjusted_overlap':float(((values-chance)/(1-chance)).mean())})
        save(path,manifest,{'field_id':field,'period_start':period,'n':2048,'scores':rows,
            'indices':ids.tolist(),'interpretation':'identical fixed-size candidate set; recipe and density sensitivity'})


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['minilm','common','pooling','balanced-neighbors','all']);args=parser.parse_args()
    with run_lock(OUT):
        manifest=freeze();data=NativeData(ROOT,max_bytes=(5 if args.stage=='pooling' else 16)*1024**3)
        write_json(OUT/'progress.json',{'state':'running','stage':args.stage,'updated_at':utcnow()})
        if args.stage in ('pooling','all'):pooling(data,manifest)
        if args.stage in ('minilm','all'):minilm(data,manifest)
        if args.stage in ('common','all'):common(data,manifest)
        if args.stage in ('balanced-neighbors','all'):balanced_neighbors(data,manifest)
        write_json(OUT/'progress.json',{'state':'requested_stages_complete','stage':args.stage,'updated_at':utcnow()})


if __name__=='__main__':main()
