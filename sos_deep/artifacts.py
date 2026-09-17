"""Versioned evidence helpers for the expanded closure; never touch parent data."""
import csv
import json
import platform
import importlib.metadata
from pathlib import Path
from sos_embed.storage import file_sha, write_json, utcnow

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with Path(path).open() as f:
        return list(csv.DictReader(f))


def save_csv(path, rows):
    rows = list(rows)
    if not rows:
        raise ValueError('Empty evidence table: ' + str(path))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.partial.csv')
    with temp.open('w') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    temp.replace(path)


def verify_audit(folder):
    folder = Path(folder)
    audit = json.loads((folder / 'audit.json').read_text())
    assert audit['all_complete'], folder
    for name, digest in audit['files'].items():
        assert file_sha(folder / name) == digest, (folder, name)
    return audit


def freeze(output, sources, parents, design):
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    source_files = {n: file_sha(ROOT / n) for n in sources}
    parent_files = {n: file_sha(ROOT / n) for n in parents}
    manifest = {'source_files': source_files, 'parent_files': parent_files, 'design': design,
                'environment': {'python': platform.python_version(), 'packages':
                    {p: importlib.metadata.version(p) for p in ['numpy', 'scipy', 'pyarrow']}}}
    path = output / 'manifest.json'
    if path.exists():
        assert json.loads(path.read_text()) == manifest, 'Changed frozen run: ' + str(output)
    else:
        write_json(path, manifest)
    for name, digest in source_files.items():
        target = output / 'source_snapshot' / name; target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            assert file_sha(target) == digest, target
        else:
            target.write_bytes((ROOT / name).read_bytes())
    return manifest


def finish(output, **checks):
    output = Path(output)
    write_json(output / 'audit.json', {'all_complete': True, 'completed_at': utcnow(), **checks,
        'files': {str(p.relative_to(output)): file_sha(p) for p in sorted(output.iterdir())
                  if p.is_file() and p.suffix in ['.csv', '.parquet', '.json', '.npy']
                  and p.name not in ['audit.json', 'progress.json']}})
