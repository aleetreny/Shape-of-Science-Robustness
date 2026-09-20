"""Independent real-data identities; does not recompute parent experiments."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from scipy.sparse.csgraph import minimum_spanning_tree, connected_components
from scipy.spatial.distance import pdist, squareform
from sos_embed.storage import write_json, file_sha, utcnow
from .run import load_input, ROOT, OUT, D
from .metrics import measure, unit
import pyarrow.parquet as pq


def main():
    metadata=pq.read_table(ROOT/'data/analysis_ready_v1/metadata.parquet',columns=['field_id'])['field_id'].to_numpy()
    results=[];full=[]
    for model in ['specter','bert','minilm']:
        ids,arr,manifest=load_input(model,'title_abstract',D['models'][model])
        for field in [11,27]:
            positions=np.flatnonzero(metadata[ids]==field)[:128]
            x=unit(arr[positions]);n=len(x);actual=measure(x)
            gram=x@x.T;np.fill_diagonal(gram,1.)
            upper=gram[np.triu_indices(n,1)]
            angle=float(np.median(np.arccos(np.clip(upper,-1,1)))*180/np.pi)
            singular=np.linalg.svd(x-x.mean(0),compute_uv=False)
            eigen=singular**2
            pr=float(eigen.sum()**2/np.dot(eigen,eigen))
            erank=float(np.exp(-np.dot(eigen[eigen>0]/eigen.sum(),np.log(eigen[eigen>0]/eigen.sum()))))
            cosine=1-gram;np.fill_diagonal(cosine,np.inf)
            neighbors=np.argsort(cosine,axis=1,kind='stable')[:,:25]
            adjacency=np.zeros((n,n));adjacency[np.arange(n)[:,None],neighbors]=1
            adjacency=np.maximum(adjacency,adjacency.T)
            degrees=adjacency.sum(1)
            lap=np.eye(n)-adjacency/np.sqrt(degrees[:,None]*degrees[None,:])
            gap=float(np.linalg.eigvalsh(lap)[1])
            distances=squareform(pdist(x));mst=minimum_spanning_tree(distances).toarray()
            links=np.sort(mst[mst>0]);assert len(links)==n-1
            radius=next(t for t in links if np.bincount(connected_components((distances<=t).astype(int),directed=False)[1]).max()>=.9*n)
            rr=radius/np.median(pdist(x))
            reference={'angle_p50':angle,'pr':pr,'erank':erank,'gap_25':gap,'connect_r90':float(rr)}
            errors={k:abs(v-actual[k]) for k,v in reference.items()}
            assert max(errors.values())<1e-8,errors
            padded=measure(np.column_stack([x,np.zeros((n,128))]),full=False)
            padding_error=max(abs(actual[k]-padded[k]) for k in ['pr','angle_p50','gap_25'])
            assert padding_error<1e-8,padding_error
            # Average pair cosine is algebraically redundant with the centroid;
            # this identity is a numeric check, not a second semantic validation.
            mean_cos=1-(n*np.dot(x.mean(0),x.mean(0))-1)/(n-1)
            assert abs(actual['mean_cosine_distance']-mean_cos)<1e-10
            results.append({'model':model,'field_id':field,'n':n,'max_errors':errors,
                            'padding_error':padding_error,'input_manifest_sha256':manifest})
        positions=np.flatnonzero(metadata[ids]==11);x=unit(arr[positions]);assert len(x)==2000
        part=json.loads((OUT/'parts'/('native__'+model+'.json')).read_text())
        row=next(r for r in part['rows'] if r['field_id']==11 and r['kind']=='primary')
        singular=np.linalg.svd(x-x.mean(0),compute_uv=False);eigen=singular**2
        pr=float(eigen.sum()**2/np.dot(eigen,eigen))
        gram=x@x.T;v=gram[np.triu_indices(len(x),1)]
        angle=float(np.median(np.arccos(np.clip(v,-1,1)))*180/np.pi)
        errors={'pr':abs(pr-row['pr']),'angle_p50':abs(angle-row['angle_p50'])}
        assert max(errors.values())<1e-8,errors
        full.append({'model':model,'field_id':11,'n':2000,'errors':errors})
    rejected=0
    for bad in [np.zeros((128,4)),np.ones((128,4)),np.full((128,4),np.nan)]:
        try:measure(bad)
        except ValueError:rejected+=1
    assert rejected==3
    manifest=json.loads((OUT/'manifest.json').read_text())
    for name,digest in manifest['source_files'].items():
        assert file_sha(ROOT/name)==digest
        assert file_sha(OUT/'source_snapshot'/name)==digest
    for name,digest in manifest['parent_files'].items():assert file_sha(ROOT/name)==digest
    report={'all_complete':True,'completed_at':utcnow(),'real_128_checks':results,'real_2000_checks':full,
            'invalid_inputs_rejected':rejected,'frozen_sources_and_parents_unchanged':True,
            'source_sha256':file_sha(Path(__file__))}
    write_json(OUT/'independent_audit.json',report)
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
