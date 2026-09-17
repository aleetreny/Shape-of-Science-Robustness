"""Post-result atlas: deterministic examples, matched candidates, no encoder inference."""
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from scipy.stats import rankdata

from sos_deep.artifacts import ROOT, freeze, finish, read_csv, save_csv, verify_audit
from sos_embed.storage import file_sha, write_json, run_lock

CONFIG = 'config/case_atlas_v1.json'
DESIGN = json.loads((ROOT / CONFIG).read_text())
BASE = json.loads((ROOT / 'config/analysis_v1.json').read_text())
MODELS = list(BASE['poolings'])
PAIRS = list(itertools.combinations(range(10), 2))
KS = np.array([10, 25, 50])
PARENT = ROOT / 'data/robustness_v2'
OUT = ROOT / DESIGN['output']


def anchor_counts(neighbors, queries):
    """Count only edges whose endpoints are always eligible; shape G,Q,Q,K."""
    repeats, groups, nq, nk = neighbors.shape
    assert queries.shape == (groups, nq) and nk >= max(KS)
    result = np.zeros((groups, nq, nq, len(KS)), np.uint8)
    for g in range(groups):
        assert np.all(np.diff(queries[g]) > 0)
        positions = np.searchsorted(queries[g], neighbors[:, g])
        eligible = positions < nq
        eligible &= queries[g][np.minimum(positions, nq - 1)] == neighbors[:, g]
        for ki, k in enumerate(KS):
            rep, source, rank = np.nonzero(eligible[:, :, :k])
            target = positions[rep, source, rank]
            np.add.at(result[g, :, :, ki], (source, target), 1)
    assert result.max() <= repeats
    assert not np.any(result[:, np.arange(nq), np.arange(nq)])
    return result


def choose_examples(rows, high_key, low_key, eligible_key='illustration_eligible'):
    selected = []
    occupied = set()
    fields, subfields = Counter(), set()
    for tail, metric, sign in [('higher', high_key, -1), ('lower', low_key, 1)]:
        chosen = 0
        for row in sorted(rows, key=lambda r: (sign * r[metric], r['row_index'])):
            if (not row[eligible_key] or row['row_index'] in occupied or
                    row['subfield_id'] in subfields or fields[row['field_id']] >= 2):
                continue
            selected.append(dict(row, tail=tail))
            occupied.add(row['row_index'])
            subfields.add(row['subfield_id'])
            fields[row['field_id']] += 1
            chosen += 1
            if chosen == 6:
                break
        assert chosen == 6
    return selected


def rank_centers(centers, ids):
    x = np.asarray(centers, dtype=np.float64)
    x /= np.linalg.norm(x, axis=1, keepdims=True)
    scores = x @ x.T
    scores[np.diag_indices(len(x))] = -np.inf
    order = np.lexsort((np.broadcast_to(ids, scores.shape), -scores), axis=1)
    ranks = np.empty_like(order)
    np.put_along_axis(ranks, order, np.arange(len(x))[None, :] + 1, axis=1)
    assert np.all(ranks.diagonal() == len(x))
    return ranks


def subfields(names):
    folder = PARENT / 'subfield_controls'
    groups = defaultdict(list)
    for r in read_csv(folder / 'neighbors.csv'):
        if r['level'] == 'subfield' and r['selection'] in ('128', '256', '512'):
            groups[r['selection'], r['recipe'], int(r['k']), r['group']].append(float(r['mean_overlap']))
    assert all(len(v) == 45 for v in groups.values())
    values = {k: float(np.mean(v)) for k, v in groups.items()}
    common = sorted({k[3] for k in groups if k[:3] == ('512', 'mean', 25)}, key=int)
    assert len(common) == 183
    panels = {}
    rows = []
    for size, recipe, k in itertools.product(('128', '256', '512'), ('mean', 'cls', 'sep'), KS):
        v = [values[size, recipe, int(k), sf] for sf in common]
        panels[size, recipe, int(k)] = rankdata(v, method='average') / len(v)
        for i, sf in enumerate(common):
            rows.append({'subfield_id': sf, 'name': names[sf], 'candidates': int(size),
                         'recipe': recipe, 'k': int(k), 'agreement': v[i],
                         'within_panel_percentile': float(panels[size, recipe, int(k)][i])})
    save_csv(OUT / 'subfield_sensitivity_panels.csv', rows)
    shape = defaultdict(list)
    for r in read_csv(folder / 'shape.csv'):
        if r['level'] == 'subfield' and r['selection'] == '256' and r['recipe'] == 'mean':
            shape[r['group']].append(float(r['cka_debiased']))
    alerts = Counter(r['subfield_id'] for r in read_csv(folder / 'selection_stability.csv')
                     if r['passes_operational_screen'] == 'False')
    summary = []
    for sf in sorted(shape, key=int):
        ranks = [float(p[common.index(sf)]) for p in panels.values()] if sf in common else []
        summary.append({'subfield_id': sf, 'name': names[sf], 'agreement_k25': values['256', 'mean', 25, sf],
                        'cka': float(np.mean(shape[sf])), 'candidate_size': 256,
                        'sensitivity_panels': len(ranks), 'worst_percentile': min(ranks) if ranks else None,
                        'best_percentile': max(ranks) if ranks else None, 'shape_pair_alerts': alerts[sf]})
    assert len(summary) == 217
    save_csv(OUT / 'subfields.csv', summary)
    common_rows = [r for r in summary if r['sensitivity_panels'] == 27]
    high = sorted(common_rows, key=lambda r: (-r['worst_percentile'], int(r['subfield_id'])))[:6]
    low = sorted(common_rows, key=lambda r: (r['best_percentile'], int(r['subfield_id'])))[:6]
    examples = [dict(r, tail=t) for t, rr in [('higher', high), ('lower', low)] for r in rr]
    save_csv(OUT / 'subfield_examples.csv', examples)
    return examples


def papers_and_edges(meta):
    folder = PARENT / 'paired_neighbor_scales'
    axes = json.loads((folder / 'axes.json').read_text())
    assert axes['pairs'] == [[MODELS[a], MODELS[b]] for a, b in PAIRS]
    q = np.load(folder / 'query_ids.npy')
    candidates = np.load(folder / 'candidate_ids.npy', mmap_mode='r')
    counts = np.load(folder / 'shared_counts.npy', mmap_mode='r')[:, :, 0]
    assert q.shape == (217, 50) and counts.shape == (10, 217, 50, 45, 3)
    nn = []
    edge_counts = np.empty((217, 50, 50, 10, 3), np.uint8)
    parent_hashes = {}
    for mi, m in enumerate(MODELS):
        commit = json.loads((folder / 'models' / m / 'commit.json').read_text())
        p = folder / 'models' / m / 'neighbors.npy'
        assert file_sha(p) == commit['neighbors_sha256']
        parent_hashes[str(p.relative_to(ROOT))] = commit['neighbors_sha256']
        neighbors = np.load(p, mmap_mode='r')[:, :, 0]
        nn.append(neighbors)
        for rep in range(10):
            for gi in range(217):
                assert set(q[gi]) <= set(candidates[rep, gi, 0])
        edge_counts[:, :, :, mi] = anchor_counts(neighbors, q)
        print('ATLAS edges', m, flush=True)
    np.save(OUT / 'anchored_edge_counts.npy', edge_counts, allow_pickle=False)
    write_json(OUT / 'edge_axes.json', {'axes': ['subfield', 'query_source', 'query_target', 'model', 'k'],
        'subfields': axes['subfields'], 'query_ids': q.tolist(), 'models': MODELS, 'ks': KS.tolist(),
        'denominator': 10, 'all_endpoints_eligible_every_repeat': True, 'diagonal': 'excluded'})
    values = counts.mean(axis=3) / KS
    omit = {m: {m} for m in MODELS}
    omit.update({f'family_{key}': set(v) for key, v in BASE['family_sensitivity'].items()})
    omit['family_biomedical'] = {'biobert', 'pubmedbert'}
    omissions = np.stack([counts[:, :, :, [not ({MODELS[a], MODELS[b]} & removed) for a, b in PAIRS], 1].mean(3) / 25
                          for removed in omit.values()], axis=-1)
    rows = []
    bad_flags = list(dict.fromkeys(BASE['quality_sensitivity_flags'] + ['duplicate_doi', 'duplicate_text']))
    for gi in range(217):
        for qi, idx in enumerate(q[gi]):
            r = {k: meta[k][int(idx)].as_py() for k in ('row_index', 'work_id', 'field_id', 'field_display_name',
                                                       'subfield_id', 'subfield_display_name', 'publication_year')}
            r['illustration_eligible'] = not any(meta[f][int(idx)].as_py() for f in bad_flags)
            for ki, k in enumerate(KS):
                v = values[:, gi, qi, ki]
                r.update({f'k{k}_mean': float(v.mean()), f'k{k}_min': float(v.min()), f'k{k}_max': float(v.max())})
            r['k25_omission_min'] = float(omissions[:, gi, qi].min())
            r['k25_omission_max'] = float(omissions[:, gi, qi].max())
            r['gi'], r['qi'] = gi, qi
            rows.append(r)
    examples = choose_examples(rows, 'k25_min', 'k25_max')
    pq.write_table(pa.Table.from_pylist(rows), OUT / 'papers.parquet', compression='zstd')
    native = pq.read_table(PARENT / 'regions_native/paper_agreement.parquet').take(pa.array([r['row_index'] for r in examples]))
    for i, r in enumerate(examples):
        for c in native.column_names:
            if c.startswith(('subfield_k25', 'field_period_k25')) or c.endswith('_candidates'):
                r['native_' + c] = native[c][i].as_py()
    save_csv(OUT / 'paper_examples.csv', examples)
    # Long-form edge table contains all eligible directed edges, not just selected stories.
    gi, si, ti = np.where(np.broadcast_to(~np.eye(50, dtype=bool), (217, 50, 50)))
    v = edge_counts[gi, si, ti, :, 1].astype(np.float64) / 10
    columns = {'source_row': q[gi, si], 'target_row': q[gi, ti], 'subfield_id': np.array(axes['subfields'])[gi],
               'mean_support': v.mean(1), 'min_model_support': v.min(1), 'max_model_support': v.max(1),
               'model_spread': np.ptp(v, axis=1)}
    columns.update({m + '_support': v[:, i] for i, m in enumerate(MODELS)})
    pq.write_table(pa.table(columns), OUT / 'article_relations_k25.parquet', compression='zstd')
    selected_edges, pair_rows, checks = [], [], 0
    for r in examples:
        g, s = r['gi'], r['qi']
        options = []
        for t, target in enumerate(q[g]):
            if t == s:
                continue
            support = edge_counts[g, s, t, :, 1].astype(float) / 10
            e = {'source_row': r['row_index'], 'target_row': int(target), 'subfield_id': r['subfield_id'],
                 'mean_support': float(support.mean()), 'min_model_support': float(support.min()),
                 'max_model_support': float(support.max()), 'model_spread': float(np.ptp(support)),
                 **{m + '_support': float(support[i]) for i, m in enumerate(MODELS)}}
            options.append(e)
        for kind, key in [('recurrent', lambda e: (-e['mean_support'], e['target_row'])),
                          ('encoder_dependent', lambda e: (-e['model_spread'], -e['mean_support'], e['target_row']))]:
            selected_edges.append(dict(min(options, key=key), relation=kind, source_tail=r['tail']))
        for pi, (a, b) in enumerate(PAIRS):
            vv = counts[:, g, s, pi, 1].astype(float) / 25
            pair_rows.append({'row_index': r['row_index'], 'model_a': MODELS[a], 'model_b': MODELS[b],
                              'mean': float(vv.mean()), 'min': float(vv.min()), 'max': float(vv.max())})
        # Independent Python-set reconstruction: all repetitions, pairs and k for each illustrated source.
        for rep in range(10):
            for ki, k in enumerate(KS):
                sets = [set(n[rep, g, s, :k].tolist()) for n in nn]
                for pi, (a, b) in enumerate(PAIRS):
                    assert len(sets[a] & sets[b]) == counts[rep, g, s, pi, ki]
                    checks += 1
        for t, target in enumerate(q[g]):
            for mi in range(10):
                for ki, k in enumerate(KS):
                    direct = sum(int(target) in set(nn[mi][rep, g, s, :k].tolist()) for rep in range(10))
                    assert direct == int(edge_counts[g, s, t, mi, ki])
                    checks += 1
    save_csv(OUT / 'article_relation_examples.csv', selected_edges)
    save_csv(OUT / 'paper_example_pairs.csv', pair_rows)
    # Titles/abstracts inspected only after deterministic rankings are finalized.
    ids = sorted({r['row_index'] for r in examples} | {r['target_row'] for r in selected_edges})
    text = pq.read_table(ROOT / 'data/corpus_clean_v1/embedding_input.parquet', columns=['row_index', 'work_id', 'title', 'abstract']).take(pa.array(ids))
    details = {int(r['row_index']): r for r in text.to_pylist()}
    for idx in ids:
        details[idx]['doi'] = meta['doi'][idx].as_py()
        details[idx]['subfield'] = meta['subfield_display_name'][idx].as_py()
    write_json(OUT / 'case_texts_local.json', details)
    write_json(OUT / 'selected_cases.json', {'papers': examples, 'relations': selected_edges})
    return {'queries': len(rows), 'eligible_illustration_queries': sum(r['illustration_eligible'] for r in rows),
            'directed_article_relations': len(gi), 'independent_reconstructions': checks,
            'parent_neighbor_hashes': parent_hashes}, examples


def group_relations(names):
    folder = PARENT / 'centroid_scales'
    labels = json.loads((folder / 'group_labels.json').read_text())
    ids = np.array(labels['matched_subfields'], dtype=int)
    ni = [labels['native_subfields'].index(str(s)) for s in ids]
    rank, native_rank = [], []
    for m in MODELS:
        p = folder / (m + '_centroids.npz')
        assert file_sha(p) == json.loads((folder / (m + '_centroids.commit.json')).read_text())['sha256']
        with np.load(p) as data:
            rank.append(rank_centers(data['matched_subfield'], ids))
            native_rank.append(rank_centers(data['native_subfield'][ni], ids))
    rank, native_rank = np.array(rank), np.array(native_rank)
    records = []
    for a, b in itertools.combinations(range(len(ids)), 2):
        mutual = np.maximum(rank[:, a, b], rank[:, b, a])
        native = np.maximum(native_rank[:, a, b], native_rank[:, b, a])
        records.append({'subfield_a': int(ids[a]), 'name_a': names[str(ids[a])],
            'subfield_b': int(ids[b]), 'name_b': names[str(ids[b])],
            'mutual_top5_models': int((mutual <= 5).sum()), 'native_mutual_top5_models': int((native <= 5).sum()),
            'best_mutual_rank': int(mutual.min()), 'worst_mutual_rank': int(mutual.max()),
            'mutual_rank_range': int(np.ptp(mutual)), 'mean_mutual_rank': float(mutual.mean()),
            **{m + '_mutual_rank': int(mutual[i]) for i, m in enumerate(MODELS)}})
    pq.write_table(pa.Table.from_pylist(records), OUT / 'subfield_relations.parquet', compression='zstd')
    # A readable deterministic display. Full table is authoritative; titles did not affect the order.
    high = sorted(records, key=lambda r: (-r['mutual_top5_models'], -r['native_mutual_top5_models'],
                r['worst_mutual_rank'], r['subfield_a'], r['subfield_b']))[:8]
    low = sorted(records, key=lambda r: (-r['mutual_rank_range'], r['subfield_a'], r['subfield_b']))[:8]
    save_csv(OUT / 'subfield_relation_examples.csv', [dict(r, tail=t) for t, rr in [('recurrent', high), ('encoder_dependent', low)] for r in rr])
    # Direct rowwise ordering verifies rank meaning on every model and every center.
    for mi, m in enumerate(MODELS):
        with np.load(folder / (m + '_centroids.npz')) as d:
            x = d['matched_subfield'].astype(float)
            x /= np.linalg.norm(x, axis=1, keepdims=True)
            for a in range(len(ids)):
                ordered = sorted((b for b in range(len(ids)) if b != a), key=lambda b: (-float(x[a] @ x[b]), ids[b]))
                assert np.array_equal(rank[mi, a, ordered], np.arange(1, len(ids)))
    return {'subfield_center_pairs': len(records), 'independent_center_orderings': len(ids) * len(MODELS),
            'center_recipe_sensitivity': 'not available; primary-recipe example only'}


def main():
    with run_lock(OUT):
        for d in ['paired_neighbor_scales', 'subfield_controls', 'centroid_scales', 'regions_native']:
            verify_audit(PARENT / d)
        parents = [f'data/robustness_v2/{d}/audit.json' for d in ['paired_neighbor_scales', 'subfield_controls', 'centroid_scales', 'regions_native']]
        parents += ['data/analysis_ready_v1/metadata.parquet', 'data/corpus_clean_v1/embedding_input.parquet']
        freeze(OUT, ['sos_review/case_atlas.py', CONFIG, 'CASE_ATLAS_PROTOCOL.md', 'config/analysis_v1.json',
                     'sos_deep/artifacts.py', 'sos_embed/storage.py'], parents, DESIGN)
        meta = pq.read_table(ROOT / 'data/analysis_ready_v1/metadata.parquet')
        names = dict(zip(meta['subfield_id'].to_pylist(), meta['subfield_display_name'].to_pylist()))
        names = {str(k): v for k, v in names.items()}
        sf = subfields(names)
        evidence, papers = papers_and_edges(meta)
        evidence.update(group_relations(names))
        evidence.update({'subfield_examples': len(sf), 'paper_examples': len(papers),
                         'exploratory': True, 'no_new_encoder_inference': True})
        write_json(OUT / 'summary.json', evidence)
        finish(OUT, **evidence)
        print(json.dumps(evidence, indent=2))


if __name__ == '__main__':
    main()
