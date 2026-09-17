"""Full-corpus comparisons within Subfields; small groups remain in coverage."""
import csv
import itertools
import json
from pathlib import Path
import platform
import importlib.metadata

import numpy as np
import pyarrow.parquet as pq

from sos_analysis.native_data import NativeData
from sos_analysis.geometry import shape_scores, rsa_scores
from sos_analysis.neighbors import exact_neighbors, independent_neighbors, shared_counts
from sos_embed.storage import file_sha, write_json, utcnow, run_lock

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'config/subfields_native_v1.json'
D=json.loads(CONFIG.read_text())
OUT=ROOT/D['output']
MODELS=list(D['poolings'])
NAMES=[m+'/'+D['poolings'][m] for m in MODELS]
PAIRS=list(itertools.combinations(range(len(MODELS)),2))


def csv_write(path,rows):
    if not rows:raise ValueError('Empty output table')
    with Path(path).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def run_group(subfield, ids, get_vectors, output, *, names=None, seed=None):
    names=NAMES if names is None else names
    models=[n.split('/')[0] for n in names]
    pairs=list(itertools.combinations(range(len(names)),2))
    ids=np.asarray(ids,dtype=np.int64)
    assert len(set(ids))==len(ids) and len(ids)>0
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    if (output/'commit.json').exists():
        old=json.loads((output/'commit.json').read_text())
        assert old['rows']==len(ids) and np.array_equal(np.load(output/'row_indices.npy'),ids)
        for n,h in old['files'].items():assert file_sha(output/n)==h,n
        return old
    arrays=[get_vectors(name,ids) for name in names]
    for x in arrays:
        assert len(x)==len(ids) and np.isfinite(x).all() and (np.linalg.norm(x,axis=1)>0).all()
    np.save(output/'row_indices.npy',ids,allow_pickle=False)
    unavailable=None
    shapes=[]
    if len(ids)>=D['minimum_shape_rows']:
        try:
            raw=shape_scores(arrays,names,procrustes=True)
        except ValueError as exc:
            if 'Degenerate unbiased self-HSIC' not in str(exc):raise
            raw=[];unavailable='degenerate_self_similarity'
        if raw:
            rsa=rsa_scores(get_vectors,ids,names,count=D['rsa_pairs'],seed=seed or D['seed']+int(subfield))
            shapes=[{'subfield_id':str(subfield),'status':'computed',**r,
                     'rsa_spearman':rsa[r['model_a'],r['model_b']]} for r in raw]
    else:unavailable='fewer_than_four_rows'
    if not shapes:
        shapes=[{'subfield_id':str(subfield),'status':unavailable,'model_a':a,'model_b':b,'n':len(ids),
                 'cka_debiased':None,'cka_biased':None,'procrustes_similarity':None,
                 'procrustes_angle_degrees':None,'rsa_spearman':None}
                for a,b in itertools.combinations(names,2)]
    csv_write(output/'shape.csv',shapes)
    allowed=[k for k in D['knn_k'] if k<len(ids)]
    nn=[];verified=0
    if allowed:
        maximum=max(allowed)
        queries=np.unique(np.linspace(0,len(ids)-1,min(10,len(ids)),dtype=int))
        for name,x in zip(names,arrays):
            neighbors,_=exact_neighbors(x,ids,k=maximum)
            proof=independent_neighbors(x,ids,x[queries],ids[queries],k=maximum)
            assert np.array_equal(neighbors[queries],proof),(subfield,name)
            nn.append(neighbors);verified+=len(queries)
        nn=np.stack(nn)
        np.save(output/'neighbors.npy',nn,allow_pickle=False)
    records=[]
    for k in D['knn_k']:
        counts=np.stack([shared_counts(nn[i],nn[j],k) for i,j in pairs],axis=1) if k in allowed else None
        if counts is not None:np.save(output/f'shared_counts_k{k}.npy',counts,allow_pickle=False)
        for column,(i,j) in enumerate(pairs):
            overlap=float(counts[:,column].mean()/k) if counts is not None else None
            chance=k/(len(ids)-1) if len(ids)>1 else None
            status=('trivial_all_other_papers' if chance==1 else 'computed') if counts is not None else 'too_few_candidates'
            records.append({'subfield_id':str(subfield),'model_a':models[i],'model_b':models[j],
                            'rows':len(ids),'k':k,'status':status,
                            'mean_overlap':overlap,'chance_expected':chance if counts is not None else None,
                            'chance_adjusted':(overlap-chance)/(1-chance) if counts is not None and chance<1 else None})
    csv_write(output/'neighbors.csv',records)
    commit={'subfield_id':str(subfield),'rows':len(ids),'completed_at':utcnow(),
            'shape_status':shapes[0]['status'],'neighbors_available_k':allowed,
            'independent_neighbor_queries':verified,'pair_order':[[models[i],models[j]] for i,j in pairs],
            'files':{p.name:file_sha(p) for p in sorted(output.iterdir()) if p.is_file() and p.name!='commit.json'}}
    write_json(output/'commit.json',commit)
    print('SUBFIELD',subfield,len(ids),'complete',flush=True)
    return commit


def main():
    with run_lock(OUT):
        source_names=['sos_deep/subfields_native.py','config/subfields_native_v1.json',
                      'sos_analysis/native_data.py','sos_analysis/reader.py','sos_analysis/geometry.py',
                      'sos_analysis/neighbors.py','sos_embed/storage.py','requirements-analysis.txt']
        sources={p:file_sha(ROOT/p) for p in source_names}
        manifest={'design_sha256':file_sha(CONFIG),'source_files':sources,
                  'metadata_sha256':file_sha(ROOT/D['metadata']),
                  'catalog_sha256':file_sha(ROOT/D['catalog']),
                  'representations':NAMES,'environment':{'python':platform.python_version(),
                     'packages':{p:importlib.metadata.version(p) for p in ['numpy','scipy','pyarrow']}}}
        assert manifest['catalog_sha256']==D['catalog_sha256']
        path=OUT/'manifest.json'
        if path.exists():assert json.loads(path.read_text())==manifest,'Use a new version after changes'
        else:write_json(path,manifest)
        for p,h in sources.items():
            target=OUT/'source_snapshot'/p;target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists():assert file_sha(target)==h
            else:target.write_bytes((ROOT/p).read_bytes())
        corpus=NativeData(ROOT,max_bytes=16*1024**3)
        metadata=corpus.metadata
        groups={}
        for row in metadata.to_pylist():groups.setdefault(str(row['subfield_id']),[]).append(row['row_index'])
        commits=[]
        for group,ids in sorted(groups.items()):
            commits.append(run_group(group,ids,corpus.get,OUT/'groups'/group))
            write_json(OUT/'progress.json',{'state':'running','last_subfield':group,'groups_complete':len(commits),
                                           'target_groups':len(groups),'updated_at':utcnow()})
        counts={}
        for name in ['shape','neighbors']:
            rows=[]
            for group in sorted(groups):
                with (OUT/'groups'/group/(name+'.csv')).open() as f:rows.extend(csv.DictReader(f))
            csv_write(OUT/(name+'.csv'),rows);counts[name]=len(rows)
        assert sum(c['rows'] for c in commits)==500000 and len(commits)==252
        assert counts=={'shape':len(groups)*45,'neighbors':len(groups)*45*3}
        coverage=[]
        for c in commits:
            coverage.append({k:c[k] for k in ['subfield_id','rows','shape_status','neighbors_available_k']})
        write_json(OUT/'coverage.json',coverage)
        write_json(OUT/'audit.json',{'all_complete':True,'completed_at':utcnow(),'groups':len(commits),
                    'papers_covered':sum(c['rows'] for c in commits),'counts':counts,
                    'independent_neighbor_queries':sum(c['independent_neighbor_queries'] for c in commits),
                    'small_groups_preserved':True,'source_metadata_verified':True,
                    'files':{p.name:file_sha(p) for p in [OUT/'shape.csv',OUT/'neighbors.csv',OUT/'coverage.json']}})
        write_json(OUT/'progress.json',{'state':'complete','updated_at':utcnow()})
        print('ALL NATIVE SUBFIELD COMPARISONS COMPLETE',flush=True)


if __name__=='__main__':main()
