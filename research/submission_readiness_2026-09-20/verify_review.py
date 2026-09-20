"""Verify this review's deliverables and preservation of prior scientific artifacts."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

editorial = json.loads((HERE / 'editorial_baseline.json').read_text())
for item in editorial:
    assert sha(ROOT / item['path']) == item['sha256'], item['path']
protected = json.loads((ROOT / 'research/first_reader_review_2026-09-20/protected_manifest.json').read_text())
for name, expected in protected.items():
    assert sha(ROOT / name) == expected, name

documents = [ROOT / 'NOVELTY_AND_REPRODUCIBILITY.md', HERE / 'README.md',
             HERE / 'SOURCES.md', HERE / 'RELEASE_SPEC.md',
             HERE / 'MANUSCRIPT_POSITIONING_DRAFT.md', HERE / 'replication_demo/README.md']
links = []
for document in documents:
    text = document.read_text()
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if '://' not in link and not link.startswith('#'):
            path = document.parent / link.split('#')[0]
            assert path.exists(), (document, link)
            links.append(str(path.relative_to(ROOT)))

with tempfile.TemporaryDirectory(prefix='sos-repro-review-') as temp:
    with zipfile.ZipFile(HERE / 'replication_demo.zip') as archive:
        names = archive.namelist()
        assert len(names) == 5
        assert all(name.startswith('replication_demo/') and '..' not in name for name in names)
        archive.extractall(temp)
    run = subprocess.run([sys.executable, '-I', '-S', 'reproduce.py'],
                         cwd=Path(temp) / 'replication_demo', text=True,
                         capture_output=True, check=True)

summary = json.loads((HERE / 'inventory_summary.json').read_text())
demo = json.loads((HERE / 'demo_portability_audit.json').read_text())
assert sha(HERE / 'replication_demo.zip') == demo['archive_sha256']
assert summary['public']['head'] == '44c941019ecc34417641929ada97da79bf12fe58'
assert not summary['public']['tree_truncated']
assert not summary['public']['license']
result = {
    'review_complete': True,
    'scope': 'Novelty positioning and public reproducibility investigation, not a full data release.',
    'editorial_files_unchanged': len(editorial),
    'prior_protected_files_unchanged': len(protected),
    'local_document_links_checked': len(links),
    'demo_zip_files': len(names), 'demo_verified_from_isolated_extract': True,
    'demo_stdout': run.stdout,
    'manuscript_changes': False, 'scientific_recalculation': False,
    'public_deposit_created': False, 'license_selected': False,
    'full_public_reproduction_verified': False,
    'qss_direct_access': 'HTTP 403; official indexed page used with explicit age caveat',
    'pending': ['author review of positioning', 'complete release packaging and rights decisions',
                'full isolated reproduction', 'authorised persistent public deposit', 'submission'],
    'documents': {str(p.relative_to(ROOT)): sha(p) for p in documents},
}
(HERE / 'closure_audit.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['documents','pending']}, indent=2))
