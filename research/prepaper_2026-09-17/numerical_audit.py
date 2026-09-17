"""Independent Gram-formula and full-sort checks on real saved vectors, read-only."""
import csv
import hashlib
import itertools
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from sos_analysis.native_data import NativeData
from sos_deep.artifacts import verify_audit


def ucenter(x):
    gram = x @ x.T
    np.fill_diagonal(gram, 0)
    n = len(x)
    sums = gram.sum(0)
    centered = gram - (sums[:, None] + sums[None, :]) / (n - 2) + sums.sum() / ((n - 1) * (n - 2))
    np.fill_diagonal(centered, 0)
    return centered


def main():
    base = ROOT / 'data/robustness_v2'
    audit_manifest = json.loads((base / 'final_audit/manifest.json').read_text())
    verification = []
    for parent, expected in audit_manifest['parent_files'].items():
        p = ROOT / parent
        assert hashlib.sha256(p.read_bytes()).hexdigest() == expected
        audit = verify_audit(p.parent)
        manifest = json.loads((p.parent / 'manifest.json').read_text())
        for source, digest in manifest['source_files'].items():
            assert hashlib.sha256((ROOT / source).read_bytes()).hexdigest() == digest
            assert hashlib.sha256((p.parent / 'source_snapshot' / source).read_bytes()).hexdigest() == digest
        verification.append({'component': p.parent.name, 'files': len(audit['files']), 'sources': len(manifest['source_files'])})
    data = NativeData(ROOT, max_bytes=2 * 1024**3)
    names = {'specter': 'cls', 'bert': 'mean', 'minilm': 'mean'}
    groups = ['2214', '2602']
    shapes = {g: {} for g in groups}
    folder = base / 'paired_neighbor_scales'
    axes = json.loads((folder / 'axes.json').read_text())
    queries = np.load(folder / 'query_ids.npy')
    candidates = np.load(folder / 'candidate_ids.npy', mmap_mode='r')
    neighbor_checks = 0
    for m, pool in names.items():
        vectors = data.get(m + '/' + pool, slice(None))
        for g in groups:
            selected = np.load(base / 'subfield_controls/groups/subfield' / g / '128/row_indices.npy')
            x = vectors[selected].astype(float)
            x /= np.linalg.norm(x, axis=1, keepdims=True)
            shapes[g][m] = ucenter(x)
            gi = axes['subfields'].index(g)
            ids = candidates[0, gi, 0]
            ref = vectors[ids].astype(float)
            ref /= np.linalg.norm(ref, axis=1, keepdims=True)
            saved = np.load(folder / 'models' / m / 'neighbors.npy', mmap_mode='r')[0, gi, 0]
            for qi, q in enumerate(queries[gi]):
                v = vectors[q].astype(float)
                v /= np.linalg.norm(v)
                cosine = np.round(np.sum(ref * v[None, :], axis=1), 12)
                order = sorted((i for i, idx in enumerate(ids) if idx != q), key=lambda i: (-cosine[i], ids[i]))[:50]
                assert np.array_equal(ids[order], saved[qi]), (m, g, q)
                neighbor_checks += 1
        print('Verified raw vectors and full neighbor sorting', m, flush=True)
        del vectors
    formula_checks = []
    for g in groups:
        with (base / 'subfield_controls/groups/subfield' / g / '128/shape.csv').open() as f:
            saved = {(r['model_a'], r['model_b']): float(r['cka_debiased']) for r in csv.DictReader(f) if r['recipe'] == 'mean'}
        for a, b in itertools.combinations(names, 2):
            x, y = shapes[g][a], shapes[g][b]
            score = float(np.sum(x * y) / np.sqrt(np.sum(x * x) * np.sum(y * y)))
            delta = abs(score - saved[a, b])
            assert delta < 1e-10, (g, a, b, delta)
            formula_checks.append({'subfield': g, 'model_a': a, 'model_b': b, 'cka': score, 'absolute_error': delta})
    report = {'all_complete': True, 'components': verification, 'real_gram_formula_checks': formula_checks,
        'real_full_sort_neighbor_queries': neighbor_checks, 'checks_per_query': 50,
        'scope': 'All 15 current component seals/sources; independent real-vector spot-check of 3 models and 2 Subfields. Not a semantic validation.',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT / 'research/prepaper_2026-09-17/numerical_audit.json').write_text(json.dumps(report, indent=2))
    print('PASS', neighbor_checks, 'queries', len(formula_checks), 'independent shape scores')


if __name__ == '__main__':
    main()
