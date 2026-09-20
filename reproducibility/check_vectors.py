"""Recompute fixed checks for all four main figures directly from deposited ZIPs.

This is a bounded portability check, not a rerun of every experimental condition.
No original checkout, historical source program or plaintext abstract is read.
"""
import argparse, csv, hashlib, io, itertools, json, time, zipfile
from pathlib import Path
import numpy as np
import pyarrow.parquet as pq
from scipy.linalg import eigvalsh
from scipy.spatial.distance import pdist

# Fixed before inspecting this reproduction. Discrete IDs/counts must be exact.
TOL=1e-8
MODELS=['specter','specter2','scincl','scibert','bert','mpnet','minilm','pubmedbert','biobert','simcse']
WORD={'scibert','bert','pubmedbert','biobert'}
POOLS={m:('cls' if m in {'specter','specter2','scincl','simcse'} else 'mean') for m in MODELS}
PAIRS=list(itertools.combinations(range(10),2))

class Archives:
    def __init__(self,path):
        self.files={};self.zips={}
        manifest=json.loads((path/'DATA_MANIFEST.json').read_text())
        for a in manifest['archives']:
            self.zips[a['archive']]=zipfile.ZipFile(path/a['archive'])
            for f in a['files']:
                assert f['path'] not in self.files
                self.files[f['path']]=(a['archive'],f)
    def read(self,path):
        archive,info=self.files[path];b=self.zips[archive].read(path)
        assert len(b)==info['bytes'] and hashlib.sha256(b).hexdigest()==info['sha256'],path
        return b
    def array(self,path):return np.load(io.BytesIO(self.read(path)),allow_pickle=False)
    def table(self,path):return pq.read_table(io.BytesIO(self.read(path)))
    def csv(self,path):return list(csv.DictReader(io.StringIO(self.read(path).decode())))
    def matrix(self,prefix,pool,expected_ids):
        names=sorted(n for n in self.files if n.startswith(prefix+'/shards/') and n.endswith('/'+pool+'.npy'))
        assert names,prefix
        result=None;offset=0
        for name in names:
            x=self.array(name)
            rows=self.table(name.rsplit('/',1)[0]+'/rows.parquet')['row_index'].to_numpy()
            assert np.array_equal(rows,expected_ids[offset:offset+len(x)]),name
            if result is None:result=np.empty((len(expected_ids),x.shape[1]),dtype=x.dtype)
            result[offset:offset+len(x)]=x;offset+=len(x)
        assert offset==len(expected_ids)
        return result

def unit(x):
    x=np.asarray(x,dtype=np.float64);return x/np.linalg.norm(x,axis=1,keepdims=True)
def close(a,b,label):
    error=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    assert error<TOL,(label,error)
    return error
def nearest(x,ids,query_positions=None):
    y=unit(x);positions=np.arange(len(ids)) if query_positions is None else query_positions
    scores=y[positions]@y.T;scores[np.arange(len(positions)),positions]=-np.inf
    return np.stack([ids[np.lexsort((ids,-row))[:50]] for row in scores])
def overlap(a,b,k):return np.mean([len(set(x[:k]).intersection(y[:k]))/k for x,y in zip(a,b)])
def cka(x,y):
    def centered(z):
        z=unit(z);g=z@z.T;n=len(g);np.fill_diagonal(g,0);s=g.sum(0);g=g-s[:,None]/(n-2)-s[None,:]/(n-2)+s.sum()/((n-1)*(n-2));np.fill_diagonal(g,0);return g
    a,b=centered(x),centered(y);return np.sum(a*b)/np.sqrt(np.sum(a*a)*np.sum(b*b))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    started=time.monotonic();data=Archives(args.directory);errors=[]
    geom=data.array('data/morphology_pilot_v1/selections.npz')
    metrics=data.table('data/robustness_closure_v1/morphology/metrics.parquet').to_pylist()
    expected={(r['model'],r['kind'],r['repeat'],r['field_id'],r['representation']):r for r in metrics}
    designs=['repeat256_field','repeat256_subfield217'];selections={d:data.array('data/robustness_closure_v1/centres/selections/'+d+'.npz') for d in designs};centres={}
    candidates=data.array('data/robustness_v2/paired_neighbor_scales/candidate_ids.npy')[0,0]
    queries=data.array('data/robustness_v2/paired_neighbor_scales/query_ids.npy')[0]
    shared=data.array('data/robustness_v2/paired_neighbor_scales/shared_counts.npy')[0,0]
    neighbors={};geometry_cases=0
    metadata=data.table('data/analysis_ready_v1/metadata.parquet')
    global_ids=metadata['row_index'].to_numpy();assert np.array_equal(global_ids,np.arange(500000))
    for model in MODELS:
        raw=data.matrix('data/embeddings_v1/'+model,POOLS[model],global_ids)
        for design in designs:
            saved=data.array('data/robustness_closure_v1/centres/models/'+model+'/'+design+'.npz')
            for grouping in ['observed','random']:
                ids=selections[design][grouping][0];g,n=ids.shape
                actual=unit(raw[ids.ravel()]).reshape(g,n,-1).mean(1)
                errors.append(close(actual,saved[grouping][0],('centres',model,design,grouping)));centres[model,design,grouping]=actual
        global_mean=unit(raw[geom['all_primary']]).mean(0)
        for kind,key in [('primary','primary_11'),('half','half_11_0'),('external','external_11_0')]:
            x=unit(raw[geom[key]])
            for representation,y in [('original',x),('global_centered',unit(x-global_mean))]:
                ref=expected[model,kind,0,11,representation]
                angle=float(2*np.arcsin(np.clip(np.median(pdist(y))/2,0,1))*180/np.pi)
                z=y-y.mean(0);cov=z.T@z/(len(y)-1);pr=np.trace(cov)**2/np.sum(cov*cov)
                errors.append(close([angle,pr],[ref['angle_p50'],ref['pr']],('geometry',model,kind,representation)));geometry_cases+=1
                if representation=='original':
                    vals=np.maximum(eigvalsh(cov),0)[::-1];p=vals/vals.sum();p0=p[p>0];erank=np.exp(-np.dot(p0,np.log(p0)));d80=int(np.searchsorted(np.cumsum(p),.8)+1)
                    errors.append(close(erank,ref['erank'],('entropy',model,kind)));assert d80==ref['d80']
        for scope in range(2):
            ids=candidates[scope];position=np.array([np.flatnonzero(ids==q)[0] for q in queries]);neighbors[model,scope]=nearest(raw[ids],ids,position)
        del raw
        print('Native vectors checked:',model,flush=True)
    rows=data.csv('data/robustness_closure_v1/centres/model_pairs.csv');cka_checks=0
    for r in rows:
        if int(r['repeat'])==0 and r['design'] in designs:
            actual=cka(centres[r['model_a'],r['design'],r['grouping']],centres[r['model_b'],r['design'],r['grouping']]);errors.append(close(actual,float(r['cka']),'CKA'));cka_checks+=1
    scope_counts=0
    for scope in range(2):
        for pi,(i,j) in enumerate(PAIRS):
            for ki,k in enumerate([10,25,50]):
                actual=[len(set(a[:k]).intersection(b[:k])) for a,b in zip(neighbors[MODELS[i],scope],neighbors[MODELS[j],scope])]
                assert np.array_equal(actual,shared[scope,:,pi,ki]),('scope',scope,pi,k);scope_counts+=len(actual)
    input_ids=data.table('public_metadata/robustness_v2/inputs/native_input.parquet')['row_index'].to_numpy()
    chosen=data.array('data/robustness_closure_v1/headline/fields/11/selected_global_ids.npy')[0]
    positions=np.searchsorted(input_ids,chosen);assert np.array_equal(input_ids[positions],chosen)
    nn={}
    for model in MODELS:
        for condition in ['title_abstract','title']:
            for pool in (['mean','cls','sep'] if model in WORD else [POOLS[model]]):
                raw=data.matrix('data/robustness_v2/inputs/'+condition+'/'+model,pool,input_ids)
                nn[model,condition,pool]=nearest(raw[positions],chosen);del raw
        print('Text vectors checked:',model,flush=True)
    reference=data.csv('data/robustness_closure_v1/headline/fields/11/field_repetitions.csv');headline_checks=0
    for recipe,ks in [('mean',[10,25,50]),('cls',[25]),('sep',[25])]:
        pool=lambda m:recipe if m in WORD else POOLS[m]
        for k in ks:
            a=[1-overlap(nn[MODELS[i],'title_abstract',pool(MODELS[i])],nn[MODELS[j],'title_abstract',pool(MODELS[j])],k) for i,j in PAIRS]
            b=[1-overlap(nn[m,'title_abstract',pool(m)],nn[m,'title',pool(m)],k) for m in MODELS]
            r=next(r for r in reference if int(r['repeat'])==0 and r['recipe']==recipe and int(r['k'])==k)
            errors.append(close([np.mean(a),np.mean(b),np.mean(b)-np.mean(a)],[float(r[x]) for x in ['model_change','title_only_change','title_minus_model']],('headline',recipe,k)));headline_checks+=1
    result={'all_checks_passed':True,'seconds':time.monotonic()-started,'absolute_tolerance_fixed_before_run':TOL,'max_absolute_error':max(errors),'models':10,'centroid_arrays':40,'cka_pair_values':cka_checks,'geometry_cases':geometry_cases,'exact_neighbor_intersection_counts':scope_counts,'headline_recipe_k_combinations':headline_checks,'conditions_checked':{'centres':'repeat 0, 26 Fields and 217 Subfields, observed and random','geometry':'Field 11: primary, half 0, external 0; both representations','search_scope':'Subfield 1100, repeat 0, both scopes, 50 queries, all pairs and k','input':'Field 11, repeat 0, 1000 candidates, all 36 representations'},'limit':'bounded calculation checks for all four figures; not all conditions, inference or every supplementary analysis'}
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
