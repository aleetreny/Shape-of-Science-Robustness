"""Pre-real-data tests: mathematical identities and failure modes."""
import argparse
import csv
import json
import time
from pathlib import Path
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.sparse.csgraph import minimum_spanning_tree, connected_components
from .metrics import measure, unit, spectrum, gaussian_reference


def run(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    rng=np.random.default_rng(20260918)
    z=rng.normal(size=(1000,32))
    # Ambient coordinate = common direction; tangent coordinates carry shapes.
    def cone(a, shift=20):return np.column_stack([np.full(len(a),shift),a])
    label=np.repeat([-1,1],500)
    two=z.copy();two[:,0]=.3*z[:,0]+6*label
    elongated=z.copy();elongated[:,0]*=6
    outliers=z.copy();outliers[:10]*=30
    low=z.copy();low[:,4:]*=.01
    four=z.copy(); labs=np.tile(np.arange(4),250); four[:,0]=.3*z[:,0]+8*(labs%2-.5);four[:,1]=.3*z[:,1]+8*(labs//2-.5)
    bridges=two.copy();bridges[:100,0]=np.linspace(-6,6,100)
    clouds={'one_round':cone(z),'one_narrow':cone(z,50),'one_wide':cone(z,8),
            'one_elongated':cone(elongated),'low_rank':cone(low),
            'two_separated':cone(two),'four_separated':cone(four),
            'two_with_bridges':cone(bridges),'one_with_outliers':cone(outliers)}
    rows=[];start=time.monotonic()
    for name,x in clouds.items():
        r=measure(x);rows.append({'cloud':name,**r})
    a=measure(clouds['one_round'])
    q,_=np.linalg.qr(rng.normal(size=(33,33)))
    b=measure(clouds['one_round']@q)
    scalar=measure(clouds['one_round']*17)
    keys=['angle_p50','pr','erank','connect_ratio90_50','gap_25','hub_gini25']
    rotation=max(abs(a[k]-b[k]) for k in keys)
    scaling=max(abs(a[k]-scalar[k]) for k in keys)
    assert rotation<1e-7 and scaling<1e-7,(rotation,scaling)
    x=unit(clouds['one_round'][:100])
    eig=np.linalg.svd(x-x.mean(0),compute_uv=False)**2
    sp=spectrum(x)
    assert abs(sp['pr']-eig.sum()**2/np.dot(eig,eig))<1e-9
    dist=squareform(pdist(x)); tree=minimum_spanning_tree(dist).toarray()
    levels=sorted(set(tree[tree>0]))
    r90=next(t for t in levels if np.bincount(connected_components((dist<=t).astype(int),directed=False)[1]).max()>=90)
    ref=measure(x)
    assert abs(ref['connect_r90']-r90/np.median(pdist(x)))<1e-10
    # Translation invariance belongs to Euclidean covariance/graph geometry,
    # not angular geometry measured after per-row L2 normalization.
    c=measure(z,normalize=False);d=measure(z+20,normalize=False)
    assert max(abs(c[k]-d[k]) for k in ['pr','erank','gap_25','connect_ratio90_50'])<1e-7
    # Test dimension ceiling/sample-size effect, without calling it true ID.
    size_rows=[]
    for ambient in [32,384,768]:
        base=rng.normal(size=(4000,ambient))
        for n in [250,500,1000,2000,4000]:
            size_rows.append({'ambient':ambient,'n':n,**spectrum(unit(base[:n]))})
    # Gaussian reference: two mixtures versus single ellipsoid, repeated seeds.
    null=[]
    for name in ['one_round','one_elongated','two_separated','four_separated','one_with_outliers']:
        for rep in range(3):
            y=gaussian_reference(clouds[name],540+rep)
            null.append({'cloud':name,'repeat':rep,**measure(y)})
    for name,records in [('clouds',rows),('sample_size',size_rows),('references',null)]:
        with (out/(name+'.csv')).open('w') as f:
            w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    summary={'all_checks_passed':True,'rotation_max_error':rotation,'positive_scaling_max_error':scaling,
             'independent_svd_pr_verified':True,'independent_mst_components_verified':True,
             'seconds':time.monotonic()-start,'clouds':len(rows),'reference_clouds':len(null)}
    (out/'audit.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)
    print(json.dumps([{k:r[k] for k in ['cloud','angle_p50','pr','gap_25','union_giant_25','mutual_giant_25','connect_ratio90_50','mst_max_median']} for r in rows],indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();run(a.out)
