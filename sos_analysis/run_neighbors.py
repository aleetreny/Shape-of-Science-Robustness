"""Native exact neighbors and article-level overlap, with verified checkpoints."""
import argparse
import hashlib
import importlib.metadata
import itertools
import json
import os
from pathlib import Path
import shutil
import time

import numpy as np

from sos_embed.storage import file_sha, object_sha, run_lock, utcnow, write_json
from .native_data import NativeData
from .neighbors import exact_neighbors, independent_neighbors, shared_counts

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/analysis_v1/neighbors"


def save_array(path, array):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name('.' + path.name + '.partial')
    with temporary.open('wb') as f:
        np.save(f, array, allow_pickle=False)
        f.flush(); os.fsync(f.fileno())
    os.replace(temporary, path)


def freeze():
    files = ["config/analysis_v1.json", "config/neighbors_v1.json", "requirements-analysis.txt",
             "sos_analysis/neighbors.py", "sos_analysis/run_neighbors.py",
             "sos_analysis/native_data.py", "sos_analysis/reader.py"]
    manifest = {"files": {f: file_sha(ROOT / f) for f in files},
                "packages": {p: importlib.metadata.version(p) for p in ('numpy','pyarrow')}}
    path = OUT / 'manifest.json'
    if path.exists():
        if json.loads(path.read_text()) != manifest:
            raise ValueError('Neighbor implementation changed; use new version')
    else:
        for name in files:
            target = OUT / 'source_snapshot' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        write_json(path, manifest)
    return manifest


def verified(folder, manifest):
    path = folder / 'commit.json'
    if not path.exists():
        return False
    record = json.loads(path.read_text())
    if record['manifest_sha256'] != object_sha(manifest):
        raise ValueError('Neighbor manifest mismatch')
    for name, digest in record['files'].items():
        if file_sha(folder / name) != digest:
            raise ValueError('Neighbor output changed')
    return True


def commit(folder, manifest, stats):
    files = [p for p in folder.iterdir() if p.name != 'commit.json' and not p.name.startswith('.')]
    write_json(folder / 'commit.json', {'manifest_sha256': object_sha(manifest),
               'files': {p.name: file_sha(p) for p in files}, 'stats': stats, 'completed_at': utcnow()})


def anchors(data, per_cell=100):
    works = data.metadata['work_id'].to_pylist()
    ranks = [hashlib.sha256(('sos-v1-global-neighbors/' + w).encode()).digest() for w in works]
    return np.asarray(sorted(i for ids in data.cells().values()
                             for i in sorted(ids, key=lambda i: ranks[i])[:per_cell]), dtype=np.int64)


def local_search(data, manifest, settings):
    cells = data.cells()
    names = [f'{m}/{p}' for m, p in data.design['poolings'].items()]
    for name in names:
        model = name.split('/')[0]
        write_json(OUT / 'progress.json', {'stage': 'local_search', 'model': name, 'state': 'running', 'updated_at': utcnow()})
        raw = data.get(name, slice(None))
        for (field, period), ids in cells.items():
            folder = OUT / 'local' / f'{field}_{period}' / model
            if verified(folder, manifest):
                continue
            started = time.monotonic()
            x = raw[ids]
            neighbors, stats = exact_neighbors(x, ids, k=max(data.design['knn_k']),
                         batch_size=settings['query_batch_local'], decimals=settings['score_decimals_for_ties'])
            # Deterministic equally spaced anchors, independent full sort and cosine.
            chosen = np.unique(np.linspace(0, len(ids)-1, 10, dtype=int))
            check = independent_neighbors(x, ids, x[chosen], ids[chosen],
                        k=neighbors.shape[1], decimals=settings['score_decimals_for_ties'])
            np.testing.assert_array_equal(neighbors[chosen], check)
            save_array(folder / 'query_row_index.npy', ids)
            save_array(folder / 'neighbors.npy', neighbors)
            stats.update(seconds=time.monotonic()-started, independent_queries=len(chosen), validation='exact_match')
            commit(folder, manifest, stats)
            print(f'Vecinos {model}: {field}/{period}, n={len(ids):,}, {stats["seconds"]:.1f}s', flush=True)
        del raw


def global_search(data, manifest, settings):
    ids = anchors(data, data.design['knn_global_anchors_per_cell'])
    ref_ids = np.flatnonzero(data.metadata['cohort'].to_numpy() == 'base')
    for model, pool in data.design['poolings'].items():
        folder = OUT / 'global' / model
        if verified(folder, manifest):
            continue
        started = time.monotonic()
        write_json(OUT / 'progress.json', {'stage': 'global_search', 'model': model, 'state': 'running', 'updated_at': utcnow()})
        raw = data.get(f'{model}/{pool}', slice(None))
        neighbors, stats = exact_neighbors(raw[ref_ids], ref_ids, queries=raw[ids], query_ids=ids,
                        k=max(data.design['knn_k']), batch_size=settings['query_batch_global'],
                        decimals=settings['score_decimals_for_ties'])
        chosen = np.unique(np.linspace(0, len(ids)-1, 26, dtype=int))
        check = independent_neighbors(raw[ref_ids], ref_ids, raw[ids[chosen]], ids[chosen],
                      k=neighbors.shape[1], decimals=settings['score_decimals_for_ties'])
        np.testing.assert_array_equal(neighbors[chosen], check)
        save_array(folder / 'query_row_index.npy', ids)
        save_array(folder / 'neighbors.npy', neighbors)
        stats.update(seconds=time.monotonic()-started, independent_queries=len(chosen), validation='exact_match')
        commit(folder, manifest, stats)
        print(f'Vecinos globales {model}: {len(ids):,} consultas, {stats["seconds"]:.1f}s', flush=True)
        del raw


def summarize_group(data, manifest, scope, label, ids, folders, available):
    folder = OUT / 'overlap' / scope / label
    if verified(folder, manifest):
        return
    models = list(data.design['poolings'])
    arrays = {}
    for m, source in zip(models, folders):
        if not verified(source, manifest):
            raise ValueError('Unverified neighbor input')
        np.testing.assert_array_equal(np.load(source / 'query_row_index.npy'), ids)
        arrays[m] = np.load(source / 'neighbors.npy', mmap_mode='r')
    pairs = list(itertools.combinations(models, 2))
    ks = data.design['knn_k']
    counts = np.empty((len(ids), len(pairs), len(ks)), dtype=np.uint8)
    records = []
    for pi, (a, b) in enumerate(pairs):
        for ki, k in enumerate(ks):
            shared = shared_counts(arrays[a], arrays[b], k)
            counts[:,pi,ki] = shared
            fractions = shared.astype(np.float64) / k
            chance = k / np.asarray(available)
            adjusted = (fractions-chance)/(1-chance)
            records.append({'model_a': a, 'model_b': b, 'k': k, 'queries': len(ids),
                            'mean_overlap': float(fractions.mean()), 'median_overlap': float(np.median(fractions)),
                            'mean_chance_adjusted_overlap': float(adjusted.mean()),
                            'q05_overlap': float(np.quantile(fractions,.05)), 'q95_overlap': float(np.quantile(fractions,.95))})
    save_array(folder / 'query_row_index.npy', ids)
    save_array(folder / 'shared_counts.npy', counts)
    write_json(folder / 'summary.json', {'scope': scope, 'label': label, 'pairs': pairs, 'ks': ks,
               'rows': len(ids), 'scores': records, 'counts_axes': ['article','model_pair','k'],
               'interpretation': 'query distributions; no independence assumption across papers or model pairs'})
    commit(folder, manifest, {'rows': len(ids)})


def overlap(data, manifest):
    models = list(data.design['poolings'])
    for (field, period), ids in data.cells().items():
        label = f'{field}_{period}'
        folders = [OUT / 'local' / label / m for m in models]
        summarize_group(data, manifest, 'local', label, ids, folders, len(ids)-1)
        print('Coincidencia de vecinos:', label, flush=True)
    ids = anchors(data, data.design['knn_global_anchors_per_cell'])
    cohorts = data.metadata['cohort'].to_numpy()[ids]
    available = 400000 - (cohorts == 'base')
    summarize_group(data, manifest, 'global', 'anchors', ids,
                    [OUT / 'global' / m for m in models], available)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['local','global','overlap','all'])
    args = parser.parse_args()
    with run_lock(OUT):
        manifest = freeze()
        data = NativeData(ROOT, max_bytes=2 * 1024**3)
        settings = json.loads((ROOT / 'config/neighbors_v1.json').read_text())
        if args.stage in ('local','all'):
            local_search(data, manifest, settings)
        if args.stage in ('global','all'):
            global_search(data, manifest, settings)
        if args.stage in ('overlap','all'):
            overlap(data, manifest)
        write_json(OUT / 'progress.json', {'state': 'requested_stages_complete', 'requested': args.stage, 'updated_at': utcnow()})


if __name__ == '__main__':
    main()
