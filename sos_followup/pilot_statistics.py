"""Paired, dimension-invariant statistics for a fixed small input pilot."""
import numpy as np
from scipy.stats import rankdata
from sos_analysis.geometry import normalize_rows, sample_pairs


def cosine_grams(arrays):
    return np.stack([x@x.T for x in map(normalize_rows,arrays)])


def u_center(grams):
    g=np.asarray(grams,dtype=np.float64).copy()
    if g.ndim!=3 or g.shape[1]!=g.shape[2] or g.shape[1]<4:raise ValueError('Need square kernels with >=4 rows')
    if not np.isfinite(g).all():raise ValueError('Nonfinite kernel')
    n=g.shape[1];i=np.arange(n);g[:,i,i]=0
    sums=g.sum(axis=2);total=sums.sum(axis=1)
    g-=sums[:,:,None]/(n-2);g-=sums[:,None,:]/(n-2);g+=total[:,None,None]/((n-1)*(n-2))
    g[:,i,i]=0
    return g


def cka_matrix(grams):
    g=u_center(grams).reshape(len(grams),-1)
    norms=np.linalg.norm(g,axis=1)
    if (norms<1e-14).any():raise ValueError('Degenerate kernel')
    g/=norms[:,None]
    result=g@g.T
    if not np.allclose(np.diag(result),1,atol=1e-10):raise ValueError('CKA self check')
    return result


def rsa_matrix(grams,seed,count=20000):
    a,b=sample_pairs(grams.shape[1],count,seed)
    ranks=np.array([rankdata(1-g[a,b],method='average') for g in grams])
    ranks-=ranks.mean(axis=1,keepdims=True)
    norms=np.linalg.norm(ranks,axis=1,keepdims=True)
    if (norms==0).any():raise ValueError('Constant distances')
    ranks/=norms
    return ranks@ranks.T


def effect_rows(matrix,names,models):
    """Same-paper, same-scale contrasts, anchored on the habitual full input."""
    at={name:i for i,name in enumerate(names)};conditions=['title','abstract','title_abstract'];rows=[]
    for m in models:
        base=at[(m,'title_abstract')]
        model_change=float(np.mean([1-matrix[base,at[(b,'title_abstract')]] for b in models if b!=m]))
        for condition in ['title','abstract']:
            input_change=float(1-matrix[base,at[(m,condition)]])
            rows.append({'model':m,'input_condition':condition,'model_change_at_full':model_change,
                         'input_change_from_full':input_change,'model_minus_input':model_change-input_change})
    all_model=np.mean([1-matrix[at[(a,c)],at[(b,c)]] for c in conditions for i,a in enumerate(models) for b in models[i+1:]])
    all_input=np.mean([1-matrix[at[(m,a)],at[(m,b)]] for m in models for i,a in enumerate(conditions) for b in conditions[i+1:]])
    return rows,{'model_change_all_inputs':float(all_model),'input_change_all_transitions':float(all_input),'model_minus_input':float(all_model-all_input)}
