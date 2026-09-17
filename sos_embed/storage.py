"""A shard is committed only after all its files are written and checksummed."""
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import tempfile

import numpy as np
import pyarrow.parquet as pq

IDENTITY = ['row_index', 'work_id', 'text_sha256']


def file_sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def object_sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def sync_dir(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.' + path.name, dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(obj, f, indent=2, sort_keys=True)
            f.write('\n')
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
        sync_dir(path.parent)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


@contextmanager
def run_lock(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    with (path / '.run.lock').open('a+') as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError('An embedding process is already running for this output') from None
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def validate_vectors(vectors, rows, dimension, poolings):
    if set(vectors) != set(poolings):
        raise ValueError('Wrong pooling outputs')
    for name, a in vectors.items():
        if a.shape != (rows, dimension) or a.dtype != np.float32:
            raise ValueError(f'Wrong shape/dtype: {name}')
        if not np.isfinite(a).all() or not (np.linalg.norm(a, axis=1) > 0).all():
            raise ValueError(f'Invalid or zero vector: {name}')


class Store:
    def __init__(self, path, manifest):
        self.path, self.manifest = Path(path), manifest
        self.path.mkdir(parents=True, exist_ok=True)
        (self.path / 'shards').mkdir(exist_ok=True)
        p = self.path / 'manifest.json'
        if p.exists():
            if json.loads(p.read_text()) != manifest:
                raise ValueError('Run manifest/configuration changed; use a separate output')
        else:
            if any((self.path / 'shards').iterdir()):
                raise ValueError('Shards exist without their manifest')
            write_json(p, manifest)

    def commit(self, start, rows, vectors, stats):
        end = start + len(rows)
        if not 0 <= start < end <= self.manifest['rows']:
            raise ValueError('Invalid shard range')
        validate_vectors(vectors, len(rows), self.manifest['dimension'], self.manifest['poolings'])
        target = self.path / 'shards' / f'{start:09d}-{end:09d}'
        if target.exists():
            raise FileExistsError(target)
        temp = Path(tempfile.mkdtemp(prefix='.partial-', dir=target.parent))
        files = {}
        # Interrupted .partial directories are never interpreted as finished work.
        pq.write_table(rows, temp / 'rows.parquet', compression='zstd')
        for name, a in vectors.items():
            with (temp / f'{name}.npy').open('wb') as f:
                np.save(f, a, allow_pickle=False)
                f.flush()
                os.fsync(f.fileno())
        for p in temp.iterdir():
            with p.open('rb') as f:
                os.fsync(f.fileno())
            files[p.name] = file_sha(p)
        write_json(temp / 'commit.json', {'start': start, 'end': end, 'files': files,
                   'stats': stats, 'committed_at': utcnow(), 'manifest_sha256': object_sha(self.manifest)})
        sync_dir(temp)
        os.rename(temp, target)
        sync_dir(target.parent)

    def scan(self, expected_rows=None):
        count, seconds, truncated = 0, 0.0, 0
        paths = []
        for p in sorted((self.path / 'shards').iterdir()):
            if p.name.startswith('.'):
                continue
            c = json.loads((p / 'commit.json').read_text())
            if c['start'] != count or not count < c['end'] <= self.manifest['rows']:
                raise ValueError('Shard gap/order/range violation')
            if p.name != f"{count:09d}-{c['end']:09d}" or c['manifest_sha256'] != object_sha(self.manifest):
                raise ValueError('Shard manifest/range mismatch')
            required = {'rows.parquet', *(x + '.npy' for x in self.manifest['poolings'])}
            if set(c['files']) != required:
                raise ValueError('Wrong shard files')
            for name, digest in c['files'].items():
                if not (p / name).is_file() or file_sha(p / name) != digest:
                    raise ValueError(f'Shard checksum mismatch: {p / name}')
            rows = pq.read_table(p / 'rows.parquet', columns=IDENTITY)
            n = c['end'] - count
            if len(rows) != n:
                raise ValueError('Shard row count mismatch')
            if expected_rows is not None and not rows.equals(expected_rows.slice(count, n).select(IDENTITY)):
                raise ValueError('Shard identity does not match expected papers/texts/order')
            vectors = {key: np.load(p / (key + '.npy'), mmap_mode='r', allow_pickle=False)
                       for key in self.manifest['poolings']}
            validate_vectors(vectors, n, self.manifest['dimension'], self.manifest['poolings'])
            count += n
            seconds += c['stats'].get('seconds', 0)
            truncated += c['stats'].get('truncated_rows', 0)
            paths.append(p.name)
        return {'rows': count, 'target': self.manifest['rows'], 'complete': count == self.manifest['rows'],
                'shards': len(paths), 'seconds': seconds, 'truncated_rows': truncated}
