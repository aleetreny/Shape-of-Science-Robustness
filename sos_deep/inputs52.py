"""Nested 52k inputs: preserve all old representations, infer only added rows."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import torch

from sos_embed.runner import (CACHE, INPUT, META_COLUMNS, config, environment,
                              source_files, snapshot_sources, verify_assets)
from sos_embed.storage import Store, file_sha, run_lock, utcnow, write_json
from sos_analysis.extra_embeddings import NativeBlocks
from sos_followup.input_embeddings import LiteralEncoder, condition_text

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / 'config/input52_v1.json'
OUT = ROOT / 'data/robustness_v2/inputs'
OLD = ROOT / 'data/checklist_v1/inputs'
AUDIT_COLUMNS = ['tokens_original', 'tokens_used', 'truncated',
                 'formatted_text_sha256', 'token_ids_sha256',
                 'last_content_character', 'formatted_characters']


def sources():
    names = ['sos_deep/inputs52.py', 'sos_followup/input_embeddings.py',
             'sos_analysis/extra_embeddings.py', 'config/input52_v1.json',
             'config/embeddings_v1.json']
    return {**source_files(), **{n: file_sha(ROOT/n) for n in names}}


def prepare():
    design = json.loads(DESIGN.read_text())
    definition = {'source_sha256': file_sha(INPUT), 'design_sha256': file_sha(DESIGN),
                  'seed': design['seed'], 'per_cell': design['per_cell'], 'rows': design['rows'],
                  'parent_selection_sha256': file_sha(OLD/'input_manifest.json')}
    with run_lock(OUT):
        path = OUT/'input_manifest.json'
        if path.exists():
            result = json.loads(path.read_text())
            assert result['definition'] == definition
            for name, digest in result['files'].items():
                assert file_sha(OUT/name) == digest, name
            return result
        parent = json.loads((OLD/'input_manifest.json').read_text())
        assert parent['definition']['source_sha256'] == definition['source_sha256']
        assert parent['definition']['seed'] == design['seed']
        old = pq.read_table(OLD/'native_input.parquet')
        assert file_sha(OLD/'native_input.parquet') == parent['files']['native_input.parquet']
        old_ids = set(old['row_index'].to_pylist())
        table = pq.read_table(INPUT)
        cells = {}
        for row in table.select(META_COLUMNS).to_pylist():
            rank = hashlib.sha256((design['seed']+row['work_id']).encode()).digest()
            cells.setdefault((row['field_id'], row['period_start']), []).append((rank, row['row_index']))
        assert len(cells) == 130 and min(map(len, cells.values())) >= design['per_cell']
        expected_old = {i for values in cells.values() for _, i in sorted(values)[:parent['definition']['per_cell']]}
        assert expected_old == old_ids, 'Parent selection does not reproduce'
        ids = sorted(i for values in cells.values() for _, i in sorted(values)[:design['per_cell']])
        assert len(ids) == len(set(ids)) == design['rows'] and old_ids.issubset(ids)
        selected = table.take(pa.array(ids))
        pq.write_table(selected, OUT/'native_input.parquet', compression='zstd')
        for condition in ['title', 'abstract']:
            rows = selected.to_pylist()
            for row in rows:
                row['source_text_sha256'] = row['text_sha256']
                row['text_sha256'] = hashlib.sha256(condition_text(row, condition).encode()).hexdigest()
                row['input_condition'] = condition
            pq.write_table(pa.Table.from_pylist(rows), OUT/(condition+'_input.parquet'), compression='zstd')
        result = {'definition': definition, 'completed_at': utcnow(),
                  'nested_old_rows': len(old_ids), 'added_rows': len(ids)-len(old_ids),
                  'cells': [{'field_id': f, 'period_start': p, 'available': len(v),
                             'selected': design['per_cell'], 'old_preserved': sum(i in old_ids for _, i in sorted(v)[:design['per_cell']])}
                            for (f, p), v in sorted(cells.items())],
                  'files': {n: file_sha(OUT/n) for n in ['native_input.parquet', 'title_input.parquet', 'abstract_input.parquet']}}
        assert all(c['old_preserved'] == 200 for c in result['cells'])
        write_json(path, result)
        return result


class PriorRows:
    """Load and verify one old single-input condition, indexed by global row ID."""
    def __init__(self, model, condition):
        self.folder = OLD/condition/model
        path = self.folder/'manifest.json'
        self.manifest = json.loads(path.read_text())
        expected = pq.read_table(OLD/(condition+'_input.parquet'), columns=META_COLUMNS)
        assert Store(self.folder, self.manifest).scan(expected)['complete']
        assert self.manifest['input_sha256'] == file_sha(OLD/(condition+'_input.parquet'))
        assert self.manifest['model']['key'] == model and self.manifest['condition'] == condition
        self.manifest_sha256 = file_sha(path)
        tables = []
        vectors = {p: [] for p in self.manifest['poolings']}
        for shard in sorted((self.folder/'shards').glob('[0-9]*')):
            tables.append(pq.read_table(shard/'rows.parquet'))
            for p in vectors:
                vectors[p].append(np.load(shard/(p+'.npy'), allow_pickle=False))
        self.rows = pa.concat_tables(tables).to_pylist()
        self.vectors = {p: np.concatenate(v) for p, v in vectors.items()}
        self.positions = {r['row_index']: i for i, r in enumerate(self.rows)}
        assert len(self.positions) == len(self.rows) == 26000

    def row(self, global_index):
        pos = self.positions.get(global_index)
        if pos is None:
            return None
        return self.rows[pos], {p: v[pos] for p, v in self.vectors.items()}


def assemble_literal(rows, condition, prior, encoder):
    """Keep bitwise parents and insert new inference at the correct shared IDs."""
    start = time.monotonic()
    saved = [prior.row(r['row_index']) for r in rows]
    new_positions = [i for i, old in enumerate(saved) if old is None]
    poolings = prior.manifest['poolings']
    dimension = prior.manifest['dimension']
    vectors = {p: np.empty((len(rows), dimension), dtype=np.float32) for p in poolings}
    audits = [None]*len(rows)
    for i, old in enumerate(saved):
        if old is None:
            continue
        meta, vec = old
        assert all(meta[k] == rows[i][k] for k in ['row_index', 'work_id', 'text_sha256', 'source_text_sha256'])
        for p in poolings:
            vectors[p][i] = vec[p]
        audits[i] = {k: meta[k] for k in AUDIT_COLUMNS}
        audits[i]['reuse_origin'] = 'pilot26k'
    if new_positions:
        fresh, details, _ = encoder.encode_literal([rows[i] for i in new_positions], condition)
        assert set(fresh) == set(poolings) and len(details) == len(new_positions)
        for p in poolings:
            assert fresh[p].shape == (len(new_positions), dimension)
            vectors[p][new_positions] = fresh[p]
        for i, detail in zip(new_positions, details):
            audits[i] = {**detail, 'reuse_origin': 'new_inference'}
    assert all(a is not None for a in audits)
    return vectors, audits, {'seconds': time.monotonic()-start, 'rows': len(rows),
                           'reused_rows': len(rows)-len(new_positions), 'new_rows': len(new_positions),
                           'truncated_rows': sum(a['truncated'] for a in audits)}


def run_model(key, max_shards=None, only_condition=None):
    prepare()
    design = json.loads(DESIGN.read_text())
    spec = next(m for m in config()['models'] if m['key'] == key)
    native = NativeBlocks(key)
    assets = verify_assets(spec)
    torch.set_num_threads(8)
    torch.manual_seed(20260917)
    encoder = None
    with run_lock(OUT/'locks'/key):
        for condition in ['title_abstract', 'title', 'abstract']:
            if only_condition and condition != only_condition:
                continue
            path = OUT/(('native' if condition == 'title_abstract' else condition)+'_input.parquet')
            prior = PriorRows(key, condition) if condition != 'title_abstract' else None
            expected = pq.read_table(path, columns=META_COLUMNS)
            manifest = {'schema_version': 2, 'scope': 'nested_input52', 'model': spec,
                        'condition': condition, 'rows': design['rows'], 'dimension': spec['dimension'],
                        'poolings': spec['poolings'], 'input_sha256': file_sha(path),
                        'selection_manifest_sha256': file_sha(OUT/'input_manifest.json'),
                        'native_manifest_sha256': native.model['manifest_sha256'],
                        'pilot26k_manifest_sha256': prior.manifest_sha256 if prior else None,
                        'source_files': sources(), 'environment': environment(), 'asset_records': assets,
                        'dtype': 'float32', 'device': 'mps', 'batch_size': 16,
                        'shard_size': 1024, 'postprocessing': 'none', 'seed': 20260917}
            folder = OUT/condition/key
            snapshot_sources(OUT, manifest['source_files'])
            store = Store(folder, manifest)
            state = store.scan(expected)
            if state['complete']:
                print(condition, key, 'already complete', flush=True)
                continue
            completed = 0
            offset = 0
            for batch in pq.ParquetFile(path).iter_batches(batch_size=1024):
                end = offset+batch.num_rows
                if end <= state['rows']:
                    offset = end
                    continue
                if offset < state['rows']:
                    raise ValueError('Partial shard boundary')
                table = pa.Table.from_batches([batch])
                rows = table.to_pylist()
                start = time.monotonic()
                if condition == 'title_abstract':
                    vectors = {p: [] for p in spec['poolings']}
                    audits = []
                    for row in rows:
                        original, vec = native.row(row['row_index'])
                        assert all(original[k] == row[k] for k in ['row_index', 'work_id', 'text_sha256'])
                        for p in vectors:
                            vectors[p].append(vec[p].copy())
                        audits.append({**{k: original[k] for k in AUDIT_COLUMNS}, 'reuse_origin': 'native500k'})
                    vectors = {p: np.stack(v) for p, v in vectors.items()}
                    stats = {'seconds': time.monotonic()-start, 'rows': len(rows), 'reused_rows': len(rows),
                             'new_rows': 0, 'truncated_rows': sum(a['truncated'] for a in audits)}
                else:
                    if encoder is None:
                        encoder = LiteralEncoder(spec, CACHE, 'mps')
                    vectors, audits, stats = assemble_literal(rows, condition, prior, encoder)
                meta = table.select(META_COLUMNS)
                if 'source_text_sha256' in table.column_names:
                    meta = meta.append_column('source_text_sha256', table['source_text_sha256'])
                for k in audits[0]:
                    meta = meta.append_column(k, pa.array([a[k] for a in audits]))
                store.commit(offset, meta, vectors, stats)
                write_json(folder/'progress.json', {'state': 'running', 'rows': end, 'target': design['rows'],
                                                     'updated_at': utcnow(), 'last_shard': stats})
                print(f'{key}/{condition}: {end:,}/{design["rows"]:,}; reused {stats["reused_rows"]}, new {stats["new_rows"]}', flush=True)
                offset = end
                completed += 1
                if max_shards and completed >= max_shards:
                    break
            result = {**store.scan(expected), 'updated_at': utcnow()}
            write_json(folder/'validation.json', result)
            write_json(folder/'progress.json', {**result, 'state': 'complete' if result['complete'] else 'paused'})
            if not result['complete']:
                return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'model', 'all'])
    parser.add_argument('--model')
    parser.add_argument('--max-shards', type=int)
    parser.add_argument('--condition', choices=['title_abstract', 'title', 'abstract'])
    args = parser.parse_args()
    if args.action == 'prepare':
        result = prepare()
        print(json.dumps({k: result[k] for k in ['definition', 'nested_old_rows', 'added_rows']}), flush=True)
    elif args.action == 'model':
        run_model(args.model, args.max_shards, args.condition)
    else:
        prepare()
        with run_lock(OUT/'queue'):
            for spec in config()['models']:
                subprocess.run([sys.executable, '-m', 'sos_deep.inputs52', 'model', '--model', spec['key']], cwd=ROOT, check=True)
        print('ALL 52K INPUT CONDITIONS COMPLETE', flush=True)


if __name__ == '__main__':
    main()
