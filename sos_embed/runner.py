"""Bounded-memory runs, fixed identities and no implicit change of scientific policy."""
import hashlib
import heapq
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import torch

from .models import Encoder, snapshot_path
from .storage import IDENTITY, Store, file_sha, object_sha, run_lock, utcnow, write_json

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config/embeddings_v1.json'
CACHE = ROOT / '.benchmark-models'
ASSETS = ROOT / 'data/embedding_assets_v1.json'
PILOT = ROOT / 'data/embedding_pilot_v1'
FULL = ROOT / 'data/embeddings_v1'
CONTROL = ROOT / 'data/embedding_control_pilot_v1'
INPUT = ROOT / 'data/corpus_clean_v1/embedding_input.parquet'
META_COLUMNS = IDENTITY + ['cohort', 'field_id', 'publication_year', 'period_start']


def config():
    return json.loads(CONFIG.read_text())


def check_scope(cfg, scope):
    if scope not in ('pilot', 'full', 'control'):
        raise ValueError('Unknown run scope')
    if scope == 'full' and not cfg['production_input_policy_approved']:
        raise ValueError('Production input policy has not been resolved; technical pilot is available')


def verify_input(path, manifest):
    if file_sha(path) != manifest['input_sha256']:
        raise ValueError('Frozen input checksum changed')


def corpus_check():
    result = subprocess.run([str(ROOT / 'prepare.sh'), 'preflight'], cwd=ROOT,
                            capture_output=True, text=True, check=True)
    if json.loads(result.stdout)['status'] != 'ready_for_model_configuration':
        raise ValueError('Corpus is not ready')
    m = json.loads((INPUT.parent / 'embedding_manifest.json').read_text())
    return {'rows': m['rows'], 'input_sha256': m['embedding_input_sha256'],
            'source_manifest_sha256': file_sha(INPUT.parent / 'embedding_manifest.json')}


def assets_for(spec):
    return [spec] + ([spec['adapter']] if 'adapter' in spec else [])


def download_assets():
    env = dict(os.environ, HF_HUB_DISABLE_IMPLICIT_TOKEN='1', HF_HUB_DISABLE_PROGRESS_BARS='1')
    for m in config()['models']:
        for a in assets_for(m):
            print(f"Preparando {a['repo_id']}", flush=True)
            subprocess.run([str(Path(sys.executable).parent / 'hf'), 'download', a['repo_id'],
                            *a['files'], '--revision', a['revision'], '--cache-dir', str(CACHE),
                            '--max-workers', '2', '--quiet'], env=env, check=True)
    return freeze_assets()


def freeze_assets():
    from huggingface_hub import HfApi
    records = {}
    for m in config()['models']:
        for a in assets_for(m):
            info = HfApi(token=False).model_info(a['repo_id'], revision=a['revision'], files_metadata=True)
            if info.sha != a['revision']:
                raise ValueError('Unexpected upstream revision')
            remote = {s.rfilename: s for s in info.siblings}
            files = {}
            for name in a['files']:
                p = snapshot_path(CACHE, a) / name
                digest = file_sha(p)
                sibling = remote[name]
                if sibling.lfs:
                    upstream = sibling.lfs['sha256']
                    if digest != upstream:
                        raise ValueError(f'Weight checksum differs from publisher: {a["repo_id"]}/{name}')
                else:
                    h = hashlib.sha1(f'blob {p.stat().st_size}\0'.encode() + p.read_bytes()).hexdigest()
                    upstream = sibling.blob_id
                    if h != upstream:
                        raise ValueError(f'File differs from publisher: {a["repo_id"]}/{name}')
                files[name] = {'sha256': digest, 'bytes': p.stat().st_size, 'upstream_oid': upstream}
            records[a['repo_id']] = {'revision': a['revision'], 'files': files}
    if ASSETS.exists() and json.loads(ASSETS.read_text()) != records:
        raise ValueError('Asset lock changed; inspect before replacing it')
    write_json(ASSETS, records)
    return {'asset_repositories': len(records), 'sha256': file_sha(ASSETS)}


def verify_assets(spec):
    records = json.loads(ASSETS.read_text())
    result = {}
    for a in assets_for(spec):
        record = records[a['repo_id']]
        if record['revision'] != a['revision'] or set(record['files']) != set(a['files']):
            raise ValueError('Asset lock differs from model specification')
        for name, entry in record['files'].items():
            if file_sha(snapshot_path(CACHE, a) / name) != entry['sha256']:
                raise ValueError(f'Local model file changed: {a["repo_id"]}/{name}')
        result[a['repo_id']] = record
    return result


def environment():
    names = ('torch', 'transformers', 'adapters', 'huggingface-hub', 'numpy', 'pyarrow',
             'tokenizers', 'safetensors')
    return {'python': platform.python_version(), 'system': platform.platform(),
            'packages': {p: importlib.metadata.version(p) for p in names}}


def source_files():
    paths = sorted((ROOT / 'sos_embed').glob('*.py')) + [ROOT / 'embed.sh', ROOT / 'requirements-embeddings.txt',
                    ROOT / 'research/feasibility_2026-09-14/requirements-benchmark.txt']
    return {str(p.relative_to(ROOT)): file_sha(p) for p in paths}


def snapshot_sources(output, fingerprints):
    for name,digest in fingerprints.items():
        dest=output/'source_snapshot'/name
        if dest.exists():
            if file_sha(dest)!=digest:
                raise ValueError('Source snapshot differs; do not mix program versions')
        else:
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/name,dest)
        if file_sha(dest)!=digest:
            raise ValueError('Source changed while snapshotting')


def prepare_pilot():
    source = corpus_check()
    selection = {'source': source, 'method': 'ten lowest SHA256(seed + work_id) per Field/period',
                 'seed': 'embedding-technical-pilot-v1', 'per_cell': 10, 'purpose': 'technical_only'}
    PILOT.mkdir(parents=True, exist_ok=True)
    if (PILOT / 'input_manifest.json').exists():
        saved = json.loads((PILOT / 'input_manifest.json').read_text())
        if saved['selection'] != selection:
            raise ValueError('Pilot selection changed')
        verify_input(PILOT / 'input.parquet', saved)
        return saved
    heaps = {}
    for batch in pq.ParquetFile(INPUT).iter_batches(batch_size=2048):
        for r in batch.to_pylist():
            key = (r['field_id'], r['period_start'])
            h = int(hashlib.sha256((selection['seed'] + r['work_id']).encode()).hexdigest(), 16)
            heap = heaps.setdefault(key, [])
            entry = (-h, r['row_index'], r)
            if len(heap) < 10:
                heapq.heappush(heap, entry)
            elif entry > heap[0]:
                heapq.heapreplace(heap, entry)
    if len(heaps) != 130 or any(len(h) != 10 for h in heaps.values()):
        raise ValueError('Incomplete Field/period coverage in pilot')
    rows = sorted((item[2] for h in heaps.values() for item in h), key=lambda r: r['row_index'])
    table = pa.Table.from_pylist(rows, schema=pq.read_schema(INPUT))
    temp = PILOT / '.input.parquet.partial'
    pq.write_table(table, temp, compression='zstd')
    os.replace(temp, PILOT / 'input.parquet')
    saved = {'selection': selection, 'rows': len(rows), 'input_sha256': file_sha(PILOT / 'input.parquet')}
    write_json(PILOT / 'input_manifest.json', saved)
    return saved


def input_for(scope):
    if scope == 'control':
        manifest = prepare_control()
        return CONTROL / 'input.parquet', manifest, CONTROL
    if scope == 'pilot':
        manifest = prepare_pilot()
        return PILOT / 'input.parquet', manifest, PILOT
    return INPUT, corpus_check(), FULL


def prepare_control():
    from transformers import AutoTokenizer
    from .common_text import common_fragment
    pilot = prepare_pilot()
    specs = config()['models']
    selection = {'source_pilot_sha256': pilot['input_sha256'],
                 'model_input_rules_sha256': object_sha([{k:m[k] for k in
                     ('repo_id','revision','text_format','max_length')} for m in specs]),
                 'method': 'common original title/abstract prefix ending at whitespace boundaries',
                 'purpose': 'technical control; final scientific control sample size remains open'}
    CONTROL.mkdir(parents=True, exist_ok=True)
    if (CONTROL / 'input_manifest.json').exists():
        saved = json.loads((CONTROL / 'input_manifest.json').read_text())
        if saved['selection'] != selection:
            raise ValueError('Common control configuration changed')
        verify_input(CONTROL / 'input.parquet', saved)
        return saved
    pairs = [(m, AutoTokenizer.from_pretrained(snapshot_path(CACHE,m), local_files_only=True,
                                               trust_remote_code=False, use_fast=True)) for m in specs]
    rows = pq.read_table(PILOT / 'input.parquet').to_pylist()
    changed = title_changed = 0
    for i,r in enumerate(rows):
        title, abstract = common_fragment(r['title'], r['abstract'], pairs)
        r['source_text_sha256'] = r['text_sha256']
        changed += (title,abstract) != (r['title'],r['abstract'])
        title_changed += title != r['title']
        r['title'], r['abstract'] = title, abstract
        r['text_sha256'] = hashlib.sha256((title+'\n\n'+abstract).encode()).hexdigest()
        if (i+1) % 250 == 0:
            print(f'Fragmento común: {i+1}/{len(rows)}', flush=True)
    temp = CONTROL / '.input.parquet.partial'
    pq.write_table(pa.Table.from_pylist(rows), temp, compression='zstd')
    os.replace(temp, CONTROL / 'input.parquet')
    saved = {'selection': selection, 'rows': len(rows), 'input_sha256': file_sha(CONTROL/'input.parquet'),
             'changed_rows': changed, 'titles_shortened': title_changed}
    write_json(CONTROL / 'input_manifest.json', saved)
    return saved


def run_model(key, scope='pilot', device='mps', max_shards=None):
    cfg = config()
    check_scope(cfg, scope)
    spec = next(m for m in cfg['models'] if m['key'] == key)
    path, input_manifest, output = input_for(scope)
    verify_input(path, input_manifest)
    asset_records = verify_assets(spec)
    if device == 'mps' and not torch.backends.mps.is_available():
        raise ValueError('MPS is unavailable; no silent CPU fallback')
    torch.set_num_threads(8)
    torch.manual_seed(20260915)
    np.random.seed(20260915)
    batch_size, shard_size = 16, 1024
    manifest = {'schema_version': 1, 'scope': scope, 'model': spec, 'dimension': spec['dimension'],
                'poolings': spec['poolings'], 'rows': input_manifest['rows'],
                'input_sha256': input_manifest['input_sha256'], 'input_manifest': input_manifest,
                'asset_records': asset_records, 'source_files': source_files(), 'environment': environment(),
                'device': device, 'dtype': 'float32', 'attention': 'eager', 'batch_size': batch_size,
                'shard_size': shard_size, 'text_policy': 'common_fragment' if scope=='control' else cfg['input_policy'], 'postprocessing': 'none',
                'seed': 20260915, 'cpu_threads': 8}
    with run_lock(output):
        snapshot_sources(output,manifest['source_files'])
        store = Store(output / key, manifest)
        expected = pq.read_table(path, columns=IDENTITY)
        current = store.scan(expected)
        if current['complete']:
            print(json.dumps({'model': key, **current}), flush=True)
            return current
        remaining_bytes = (input_manifest['rows'] - current['rows']) * spec['dimension'] * 4 * len(spec['poolings'])
        if shutil.disk_usage(output).free < remaining_bytes + 2 * 1024**3:
            raise ValueError('Insufficient disk space for this model and safety margin')
        encoder = Encoder(spec, CACHE, device)
        write_json(store.path / 'loading_info.json', encoder.loading_info)
        # Warm-up excluded from throughput; no scientific scores are evaluated.
        warm = next(pq.ParquetFile(path).iter_batches(batch_size=8, columns=['title','abstract'])).to_pylist()
        encoder.encode(warm, batch_size=8)
        offset, committed = 0, 0
        for batch in pq.ParquetFile(path).iter_batches(batch_size=shard_size):
            end = offset + batch.num_rows
            if end <= current['rows']:
                offset = end
                continue
            if offset < current['rows']:
                raise ValueError('Resume does not match fixed shard boundaries')
            rows = pa.Table.from_batches([batch])
            vectors, audit, stats = encoder.encode(rows.select(['title','abstract']).to_pylist(), batch_size)
            metadata = rows.select(META_COLUMNS)
            if 'source_text_sha256' in rows.column_names:
                metadata = metadata.append_column('source_text_sha256',rows['source_text_sha256'])
            if scope == 'control' and any(a['truncated'] for a in audit):
                raise ValueError('Common fragment unexpectedly truncated by a model')
            for name in audit[0]:
                metadata = metadata.append_column(name, pa.array([r[name] for r in audit]))
            store.commit(offset, metadata, vectors, stats)
            offset, committed = end, committed + 1
            print(f"{key}: {end:,}/{input_manifest['rows']:,} — {stats['rows']/stats['seconds']:.1f} artículos/s", flush=True)
            write_json(store.path / 'progress.json', {'rows': end, 'target': input_manifest['rows'],
                       'updated_at': utcnow(), 'last_shard': stats, 'state': 'running'})
            if max_shards is not None and committed >= max_shards:
                break
        result = store.scan(expected)
        result.update({'model': key, 'updated_at': utcnow(), 'manifest_sha256': object_sha(manifest)})
        write_json(store.path / 'validation.json', result)
        write_json(store.path / 'progress.json', {**result, 'state': 'complete' if result['complete'] else 'paused'})
        print(json.dumps(result), flush=True)
        return result


def run_all(scope, device='mps'):
    check_scope(config(), scope)
    _, _, output = input_for(scope)
    # Release each model's GPU memory by giving it a separate process.
    with run_lock(output / 'queue'):
        for spec in config()['models']:
            subprocess.run([sys.executable, '-m', 'sos_embed.cli', 'model', spec['key'],
                            '--scope', scope, '--device', device], cwd=ROOT, check=True)
    return status(scope, verify=True)


def status(scope='pilot', verify=False):
    output = {'pilot':PILOT,'full':FULL,'control':CONTROL}[scope]
    path = output / 'input.parquet' if scope != 'full' else INPUT
    expected = pq.read_table(path, columns=IDENTITY) if verify and path.exists() else None
    reports = []
    for m in config()['models']:
        root = output / m['key']
        if not (root / 'manifest.json').exists():
            reports.append({'model': m['key'], 'state': 'not_started', 'rows': 0})
            continue
        manifest = json.loads((root / 'manifest.json').read_text())
        if verify:
            verify_input(path, manifest)
            r = Store(root, manifest).scan(expected)
            r['state'] = 'verified_complete' if r['complete'] else 'verified_partial'
        else:
            p = root / 'progress.json'
            r = json.loads(p.read_text()) if p.exists() else {'rows': 0, 'state': 'initializing'}
            # A saved "running" state is a last checkpoint, not evidence a process is alive.
            r['state_is_last_checkpoint'] = True
        reports.append({'model': m['key'], **r})
    return {'scope': scope, 'verified': verify, 'models': reports}
