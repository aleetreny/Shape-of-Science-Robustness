"""Exact cosine neighbors in float64, with an explicit numerical tie rule."""
import numpy as np


def unit(x):
    x = np.asarray(x, dtype=np.float64)
    norms = np.linalg.norm(x, axis=1)
    if not np.isfinite(x).all() or (norms == 0).any():
        raise ValueError("Invalid neighbor input")
    return x / norms[:, None]


def exact_neighbors(reference, reference_ids, *, queries=None, query_ids=None,
                    k=50, batch_size=128, decimals=12):
    reference_ids = np.asarray(reference_ids, dtype=np.int64)
    r = unit(reference)
    if queries is None:
        q, query_ids = r, reference_ids
    else:
        q, query_ids = unit(queries), np.asarray(query_ids, dtype=np.int64)
    if len(np.unique(reference_ids)) != len(r) or k < 1:
        raise ValueError("References must have unique IDs and k must be positive")
    lookup = {int(value): i for i, value in enumerate(reference_ids)}
    self_positions = np.asarray([lookup.get(int(i), -1) for i in query_ids])
    if (len(r) - (self_positions >= 0) < k).any():
        raise ValueError("Too few nonself candidates")
    output = np.empty((len(q), k), dtype=np.int32)
    tie_rows = 0
    for start in range(0, len(q), batch_size):
        end = min(start + batch_size, len(q))
        scores = np.round(q[start:end] @ r.T, decimals=decimals)
        positions = self_positions[start:end]
        present = np.flatnonzero(positions >= 0)
        scores[present, positions[present]] = -np.inf
        take = min(k + 1, len(r))
        candidates = np.argpartition(scores, -take, axis=1)[:, -take:]
        values = np.take_along_axis(scores, candidates, axis=1)
        order = np.lexsort((reference_ids[candidates], -values), axis=1)
        candidates = np.take_along_axis(candidates, order, axis=1)
        values = np.take_along_axis(values, order, axis=1)
        best = reference_ids[candidates[:, :k]].copy()
        if take > k:
            for i in np.flatnonzero(values[:, k-1] == values[:, k]):
                tied = np.flatnonzero(scores[i] >= values[i, k-1])
                order_all = np.lexsort((reference_ids[tied], -scores[i, tied]))
                best[i] = reference_ids[tied[order_all[:k]]]
                tie_rows += 1
        if (best == query_ids[start:end, None]).any():
            raise ValueError("Self appeared among neighbors")
        output[start:end] = best
    return output, {"queries": len(q), "references": len(r), "k": k,
                    "boundary_tie_queries_at_max_k": tie_rows, "decimals": decimals,
                    "dtype": "float64", "algorithm": "exact blocked dot products"}


def independent_neighbors(reference, reference_ids, queries, query_ids, k=50, decimals=12):
    """Full sorting with direct elementwise cosine, independent of partition/BLAS."""
    reference = np.asarray(reference, dtype=np.float64)
    ids = np.asarray(reference_ids)
    ref_norms = np.linalg.norm(reference, axis=1)
    result = []
    for raw, query_id in zip(queries, query_ids):
        query = np.asarray(raw, dtype=np.float64)
        values = np.einsum("ij,j->i", reference, query) / (ref_norms * np.linalg.norm(query))
        values = np.round(values, decimals=decimals)
        values[ids == query_id] = -np.inf
        result.append(ids[np.lexsort((ids, -values))[:k]])
    return np.asarray(result, dtype=np.int32)


def shared_counts(a, b, k, batch_size=512):
    if a.shape[0] != b.shape[0] or k > min(a.shape[1], b.shape[1]):
        raise ValueError("Mismatched neighbor rows or k")
    counts = np.empty(len(a), dtype=np.uint8)
    for start in range(0, len(a), batch_size):
        aa, bb = a[start:start+batch_size, :k], b[start:start+batch_size, :k]
        counts[start:start+len(aa)] = (aa[:, :, None] == bb[:, None, :]).any(axis=2).sum(axis=1)
    return counts
