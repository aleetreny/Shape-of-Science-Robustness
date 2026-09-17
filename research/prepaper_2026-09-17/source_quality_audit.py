"""Read-only source and residual-quality audit, triggered by fixed atlas examples.
The narrow generic-title rule is a post-result diagnostic, not a new corpus filter.
"""
import gzip
import hashlib
import json
import re
import sqlite3
from collections import Counter
from pathlib import Path
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/prepaper_v1/source_quality'
OUT.mkdir(parents=True, exist_ok=True)
GENERIC = re.compile(r'^(?:announcements?|editorials?|book reviews?|news|corrections?|erratum|errata|corrigendum|contents|table of contents|preface|foreword|index|author index|subject index|conference calendar)$')


def main():
    corpus = pq.read_table(ROOT / 'data/corpus_clean_v1/corpus.parquet')
    meta = pq.read_table(ROOT / 'data/analysis_ready_v1/metadata.parquet')
    assert corpus['work_id'].to_pylist() == meta['work_id'].to_pylist()
    assert corpus['text_sha256'].to_pylist() == meta['text_sha256'].to_pylist()
    mismatch = []
    for i, raw in enumerate(corpus['primary_topic_json'].to_pylist()):
        topic = json.loads(raw)
        field = int(topic['field']['id'].rsplit('/', 1)[-1])
        subfield = topic['subfield']['id'].rsplit('/', 1)[-1]
        if field != meta['field_id'][i].as_py() or subfield != meta['subfield_id'][i].as_py():
            mismatch.append(i)
    assert not mismatch
    texts = json.loads((ROOT / 'data/prepaper_v1/case_atlas/case_texts_local.json').read_text())
    db = sqlite3.connect((ROOT / 'data/corpus_clean_v1/state.sqlite').as_uri() + '?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    source_records = []
    for idx in sorted(map(int, texts)):
        r = corpus.slice(idx, 1).to_pylist()[0]
        page = db.execute('SELECT * FROM pages WHERE block_id=? AND page=?', (r['source_block'], r['source_page'])).fetchone()
        path = ROOT / 'data/corpus_clean_v1' / page['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == page['sha256']
        with gzip.open(path, 'rt') as f:
            envelope = json.load(f)
        source = envelope['response']['results'][r['source_page_index']]
        assert source['id'].rsplit('/', 1)[-1] == r['work_id']
        assert source['title'] == r['title']
        assert source['primary_topic'] == json.loads(r['primary_topic_json'])
        inv = source['abstract_inverted_index']
        words = sorted((position, word) for word, positions in inv.items() for position in positions)
        assert ' '.join(word for position, word in words) == r['abstract']
        source_records.append({'row_index': idx, 'work_id': r['work_id'], 'title': r['title'],
            'source_page': page['path'], 'source_sha256': page['sha256'], 'source_type': source['type'],
            'source_is_paratext': source['is_paratext'], 'source_primary_topic': source['primary_topic'],
            'exact_text_and_labels_match_source': True})
    db.close()
    (OUT / 'illustration_source_checks.json').write_text(json.dumps(source_records, ensure_ascii=False, indent=2))
    flags = np.array([bool(GENERIC.fullmatch(re.sub(r'[^\w\s]', '', t.casefold()).strip())) for t in corpus['title'].to_pylist()])
    existing = np.zeros(len(corpus), dtype=bool)
    design = json.loads((ROOT / 'config/analysis_v1.json').read_text())
    for name in design['quality_sensitivity_flags'] + ['duplicate_doi', 'duplicate_text']:
        existing |= meta[name].to_numpy().astype(bool)
    columns = ['row_index', 'work_id', 'title', 'field_id', 'subfield_id', 'cohort', 'possible_notice']
    flagged = corpus.select(columns).filter(pa.array(flags))
    pq.write_table(flagged, OUT / 'generic_title_candidates.parquet', compression='zstd')
    queries = np.load(ROOT / 'data/robustness_v2/paired_neighbor_scales/query_ids.npy')
    counts = np.load(ROOT / 'data/robustness_v2/paired_neighbor_scales/shared_counts.npy', mmap_mode='r')
    v = counts[:, :, 0, :, :, 1].mean(axis=(0, 3)) / 25
    keep = ~flags[queries]
    # Query-only control. Same original candidates; no claim that the candidate pool is cleaned.
    group_means = [float(v[g, keep[g]].mean()) for g in range(len(queries)) if keep[g].any()]
    summary = {'all_corpus_rows': len(corpus), 'all_work_ids_and_text_hashes_match_metadata': True,
        'all_primary_field_subfield_labels_match_corpus_source_json': True,
        'illustrated_records_verified_against_raw_response': len(source_records),
        'generic_title_rule': GENERIC.pattern, 'generic_title_records': int(flags.sum()),
        'additional_beyond_existing_strict_flags': int((flags & ~existing).sum()),
        'generic_title_count_by_title': dict(Counter(flagged['title'].to_pylist())),
        'fixed_queries_flagged': int(flags[queries].sum()), 'fixed_query_count': queries.size,
        'equal_subfield_k25_before': float(v.mean()), 'equal_subfield_k25_excluding_generic_queries': float(np.mean(group_means)),
        'scope_limit': 'Posthoc narrow generic-title diagnostic. Candidates unchanged. Does not estimate semantic label error prevalence or validate all abstracts.',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
