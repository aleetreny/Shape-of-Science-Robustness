"""Predeclared shape statistics; float64 moments, no NxN full-corpus matrix."""
import itertools
import numpy as np
from scipy.stats import rankdata


def normalize_rows(x):
    x = np.asarray(x, dtype=np.float64)
    norms = np.linalg.norm(x, axis=1)
    if not np.isfinite(x).all() or np.any(norms == 0):
        raise ValueError("Invalid input vector")
    return x / norms[:, None]


def prepare(x, normalize=True):
    return normalize_rows(x) if normalize else np.asarray(x, dtype=np.float64)


def centered_moments(arrays):
    n = len(arrays[0])
    if n < 4 or any(len(x) != n for x in arrays):
        raise ValueError("Need >=4 aligned rows")
    centered = [x - x.mean(axis=0) for x in arrays]
    joined = np.concatenate(centered, axis=1)
    norms = np.column_stack([np.einsum("ij,ij->i", x, x) for x in centered])
    return joined.T @ joined, norms.T @ norms, norms.sum(axis=0)


def streamed_moments(get_block, ids, names, dimensions, *, normalize=True, chunk=4096):
    """Two passes; get_block(name, global_ids) returns corresponding raw rows."""
    n = len(ids)
    offsets = np.cumsum([0] + dimensions)
    means = [np.zeros(d, dtype=np.float64) for d in dimensions]
    for start in range(0, n, chunk):
        chosen = ids[start:start + chunk]
        for i, name in enumerate(names):
            means[i] += prepare(get_block(name, chosen), normalize).sum(axis=0)
    means = [s / n for s in means]
    gram = np.zeros((offsets[-1], offsets[-1]), dtype=np.float64)
    norm_products = np.zeros((len(names), len(names)), dtype=np.float64)
    norm_sums = np.zeros(len(names), dtype=np.float64)
    for start in range(0, n, chunk):
        chosen = ids[start:start + chunk]
        blocks = [prepare(get_block(name, chosen), normalize) - mean
                  for name, mean in zip(names, means)]
        joined = np.concatenate(blocks, axis=1)
        gram += joined.T @ joined
        norms = np.column_stack([np.einsum("ij,ij->i", b, b) for b in blocks])
        norm_products += norms.T @ norms
        norm_sums += norms.sum(axis=0)
    return gram, norm_products, norm_sums


def scores_from_moments(moments, n, dimensions, names, *, procrustes=True):
    gram, norm_products, sums = moments
    offsets = np.cumsum([0] + dimensions)
    blocks = [slice(offsets[i], offsets[i+1]) for i in range(len(names))]
    cross_sq = np.empty((len(names), len(names)))
    for i in range(len(names)):
        for j in range(i, len(names)):
            c = gram[blocks[i], blocks[j]]
            cross_sq[i, j] = cross_sq[j, i] = np.einsum("ij,ij->", c, c)
    # Equivalent to unbiased HSIC on zero-diagonal Gram matrices. Common factor
    # 1/[n(n-3)] cancels in CKA. Centered feature formula avoids NxN allocation.
    corrected = cross_sq - n / (n - 2) * norm_products + np.outer(sums, sums) / ((n - 1) * (n - 2))
    if n < 4 or np.any(np.diag(corrected) <= 0):
        raise ValueError("Degenerate unbiased self-HSIC")
    result = []
    for i, j in itertools.combinations(range(len(names)), 2):
        unbiased = corrected[i, j] / np.sqrt(corrected[i, i] * corrected[j, j])
        biased = cross_sq[i, j] / np.sqrt(cross_sq[i, i] * cross_sq[j, j])
        row = {"model_a": names[i], "model_b": names[j], "n": n,
               "cka_debiased": float(unbiased), "cka_biased": float(biased)}
        if procrustes:
            similarity = np.linalg.svd(gram[blocks[i], blocks[j]], compute_uv=False).sum() / np.sqrt(sums[i] * sums[j])
            if not -1e-10 <= similarity <= 1 + 1e-8:
                raise ValueError("Invalid Procrustes similarity")
            similarity = np.clip(similarity, 0, 1)
            row.update(procrustes_similarity=float(similarity),
                       procrustes_angle_degrees=float(np.degrees(np.arccos(similarity))))
        result.append(row)
    return result


def shape_scores(arrays, names=None, *, normalize=True, procrustes=True):
    arrays = [prepare(x, normalize) for x in arrays]
    names = names or [str(i) for i in range(len(arrays))]
    return scores_from_moments(centered_moments(arrays), len(arrays[0]),
                               [x.shape[1] for x in arrays], names, procrustes=procrustes)


def sample_pairs(n, count, seed):
    """Uniform pairs without replacement; symmetric duplicates removed."""
    count = min(count, n * (n - 1) // 2)
    rng = np.random.default_rng(seed)
    codes = np.array([], dtype=np.int64)
    while len(codes) < count:
        a, b = rng.integers(0, n, size=(2, max(256, (count - len(codes)) * 2)))
        keep = a != b
        low, high = np.minimum(a[keep], b[keep]), np.maximum(a[keep], b[keep])
        new = np.unique(low * n + high)
        # Sorting itself must not favor low-ID pairs; randomize before truncation.
        codes = np.union1d(codes, new)
        if len(codes) >= count:
            codes = rng.choice(codes, count, replace=False)
    return codes // n, codes % n


def rsa_scores(get_block, ids, names, *, count=20000, seed=20260917, chunk=2048):
    a, b = sample_pairs(len(ids), count, seed)
    columns = []
    for name in names:
        distances = np.empty(len(a))
        for start in range(0, len(a), chunk):
            x = normalize_rows(get_block(name, ids[a[start:start + chunk]]))
            y = normalize_rows(get_block(name, ids[b[start:start + chunk]]))
            distances[start:start + len(x)] = 1 - np.einsum("ij,ij->i", x, y)
        rank = rankdata(distances, method="average")
        rank -= rank.mean()
        norm = np.linalg.norm(rank)
        if norm == 0:
            raise ValueError("Constant pair distances")
        columns.append(rank / norm)
    correlations = np.asarray(columns) @ np.asarray(columns).T
    return {(names[i], names[j]): float(correlations[i, j])
            for i, j in itertools.combinations(range(len(names)), 2)}
