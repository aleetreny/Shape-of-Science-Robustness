"""Explicit descriptive properties of a point cloud, never semantic validity.

Input rows are unit vectors unless normalize=False is explicitly requested for
synthetic geometric tests. No projection is used for distances or graphs.
"""
import numpy as np
from scipy.linalg import eigvalsh
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage
from scipy.sparse import csr_matrix, diags
from scipy.sparse.csgraph import connected_components
from scipy.sparse.linalg import eigsh


def unit(x):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim != 2 or len(x) < 4 or not np.isfinite(x).all():
        raise ValueError('Expected at least four finite vectors')
    norms = np.linalg.norm(x, axis=1)
    if np.any(norms < 1e-12):
        raise ValueError('Zero vector')
    return x / norms[:, None]


def spectrum(x, full=True):
    c = x - x.mean(axis=0)
    cov = (c.T @ c) / (len(c)-1)
    trace = float(np.trace(cov))
    denom = float(np.sum(cov*cov))
    if trace <= 1e-14 or denom <= 1e-28:
        raise ValueError('Collapsed point cloud')
    out = {'pr': trace*trace/denom, 'variance_trace': trace}
    if full:
        values = np.maximum(eigvalsh(cov, check_finite=False), 0)[::-1]
        prob = values / values.sum()
        positive = prob[prob > 0]
        out.update(erank=float(np.exp(-np.dot(positive, np.log(positive)))),
                   d80=int(np.searchsorted(np.cumsum(prob), .8)+1),
                   pc1_share=float(prob[0]))
    return out


def gini(values):
    values = np.sort(np.asarray(values, dtype=float))
    n = len(values)
    return float(2*np.dot(np.arange(1,n+1),values)/(n*values.sum())-(n+1)/n)


def graph_stats(neighbors, distances, k, weighted=False):
    n = len(neighbors)
    rows = np.repeat(np.arange(n), k)
    cols = neighbors[:, :k].ravel()
    if weighted:
        # Local-scale affinity, as in Zelnik-Manor & Perona; support is union kNN.
        sig = np.maximum(distances[np.arange(n), neighbors[:, k-1]], 1e-12)
        vals = np.exp(-distances[rows, cols]**2 / (sig[rows]*sig[cols]))
    else:
        vals = np.ones(n*k)
    directed = csr_matrix((vals, (rows, cols)), shape=(n,n))
    union = directed.maximum(directed.T)
    mutual = directed.minimum(directed.T)
    nc, labs = connected_components(union, directed=False)
    ncm, labm = connected_components(mutual, directed=False)
    out = {f'union_components_{k}': int(nc),
           f'union_giant_{k}': float(np.bincount(labs).max()/n),
           f'mutual_components_{k}': int(ncm),
           f'mutual_giant_{k}': float(np.bincount(labm).max()/n)}
    if nc > 1:
        gap, residual = 0., 0.
    else:
        deg = np.asarray(union.sum(axis=1)).ravel()
        inv = diags(1/np.sqrt(deg))
        lap = diags(np.ones(n)) - inv @ union @ inv
        vals, vec = eigsh(lap, k=2, which='SM', tol=1e-8,
                          v0=np.random.default_rng(734).normal(size=n), maxiter=20000)
        order = np.argsort(vals); vals=vals[order]; vec=vec[:,order]
        gap = float(max(vals[1],0))
        residual = float(np.max(np.linalg.norm(lap@vec-vec*vals, axis=0)))
        if residual > 1e-6:
            raise ValueError(f'Inaccurate eigenpair: {residual}')
    out[f'gap_{k}'] = gap
    out[f'gap_residual_{k}'] = residual
    if weighted:
        return {f'weighted_{key}': value for key, value in out.items() if key.startswith('gap')}
    return out


def connectivity_profile(condensed, n):
    # Single linkage is the component filtration of the complete distance graph.
    # Link heights equal the sorted MST edges (including exact zero distances).
    tree = linkage(condensed, method='single', optimal_ordering=False)
    largest = np.maximum.accumulate(tree[:,3])
    heights = tree[:,2]
    qs = {q: float(heights[np.flatnonzero(largest >= q*n)[0]]) for q in [.5,.9,.95,.99,1.]}
    scale = max(float(np.median(condensed)), 1e-12)
    out = {'connect_r50':qs[.5]/scale, 'connect_r90':qs[.9]/scale,
           'connect_r95':qs[.95]/scale, 'connect_r99':qs[.99]/scale,
           'connect_r100':qs[1.]/scale,
           'connect_ratio90_50':qs[.9]/max(qs[.5],1e-12),
           'connect_ratio95_50':qs[.95]/max(qs[.5],1e-12),
           'mst_max_median':float(heights[-1]/max(np.median(heights),1e-12))}
    return out


def measure(x, *, full=True, normalize=True):
    x = unit(x) if normalize else np.asarray(x, dtype=np.float64)
    n,d=x.shape
    if not np.isfinite(x).all() or n < 55:
        raise ValueError('Invalid cloud or fewer than 55 rows')
    condensed = pdist(x, metric='euclidean')
    quant = np.quantile(condensed, [.1,.5,.9])
    out = {'n':n,'dimension':d, **spectrum(x,full),
           'pair_chord_p10':float(quant[0]), 'pair_chord_p50':float(quant[1]),
           'pair_chord_p90':float(quant[2]),
           'zero_distance_pairs':int(np.sum(condensed < 1e-10)),
           **connectivity_profile(condensed,n)}
    if normalize:
        angles = 2*np.arcsin(np.clip(quant/2,0,1))*180/np.pi
        out.update(angle_p10=float(angles[0]),angle_p50=float(angles[1]),angle_p90=float(angles[2]),
                   mean_cosine_distance=float(np.mean(condensed**2)/2))
        center = x.mean(axis=0); center /= max(np.linalg.norm(center),1e-12)
        out['center_angle_p50'] = float(np.median(np.arccos(np.clip(x@center,-1,1)))*180/np.pi)
    distances = squareform(condensed)
    np.fill_diagonal(distances,np.inf)
    # Exact ties broken by the input order; callers sort global row IDs first.
    neighbors = np.argsort(distances,axis=1,kind='stable')[:, :50]
    for k in ([10,25,50] if full else [25]):
        out.update(graph_stats(neighbors, distances, k))
    if full:
        out.update(graph_stats(neighbors,distances,25,weighted=True))
    counts=np.bincount(neighbors[:,:25].ravel(),minlength=n)
    out['hub_gini25']=gini(counts)
    out['knn25_median_chord']=float(np.median(distances[np.arange(n),neighbors[:,24]]))
    return out


def gaussian_reference(x, seed):
    """Single Gaussian with original unit-cloud mean/covariance in expectation.

    Reprojection to the sphere changes those moments. Output diagnostics must
    assess that mismatch; this reference is not a calibrated hypothesis test.
    """
    x=unit(x); mean=x.mean(axis=0); c=x-mean
    values,vectors=np.linalg.eigh(c.T@c/(len(c)-1))
    rng=np.random.default_rng(seed)
    y=(rng.normal(size=x.shape)*np.sqrt(np.maximum(values,0)))@vectors.T+mean
    return y
