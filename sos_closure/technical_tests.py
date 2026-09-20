import numpy as np
from sos_analysis.neighbors import exact_neighbors,independent_neighbors,shared_counts
from sos_followup.pilot_statistics import cka_matrix,cosine_grams
from sos_analysis.geometry import shape_scores
from .fast_neighbors import full_ranks,restrict,overlaps
from .common import *
def main():
 r=rng('technical/synthetic');ids=np.arange(97,dtype=np.int32)*7;x=r.normal(size=(97,24));x[4]=x[3];y=r.normal(size=(97,17))
 selections=np.stack([np.sort(r.choice(97,70,replace=False)) for _ in range(3)])
 a=restrict(full_ranks(x,ids),selections,ids);b=restrict(full_ranks(y,ids),selections,ids)
 for rep,s in enumerate(selections):
  ex,_=exact_neighbors(x[s],ids[s],k=50);ind=independent_neighbors(x[s],ids[s],x[s],ids[s],k=50)
  assert np.array_equal(a[rep],ex) and np.array_equal(a[rep],ind)
  got=overlaps(np.stack([a[rep],b[rep]]),[(0,1)])[0]
  target=[float(shared_counts(a[rep],b[rep],k).mean()/k) for k in [10,25,50]]
  np.testing.assert_allclose(got,target,rtol=0,atol=1e-15)
 ck=cka_matrix(cosine_grams([x,y]))[0,1];other=shape_scores([x,y],procrustes=False)[0]['cka_debiased'];assert abs(ck-other)<1e-12
 out=OUT/'technical';out.mkdir(exist_ok=True)
 write_json(out/'tests.json',{'passed':True,'restricted_exact_searches':3,'independent_queries':210,'k':[10,25,50],'duplicate_vector_ties':True,'cross_formula_error':abs(ck-other),'kernel_sha256':file_sha(ROOT/'sos_closure/kernels.c'),'wrapper_sha256':file_sha(ROOT/'sos_closure/fast_neighbors.py')})
 print('Exact restriction, overlap sets, ties and corrected CKA: PASS')
if __name__=='__main__':main()
