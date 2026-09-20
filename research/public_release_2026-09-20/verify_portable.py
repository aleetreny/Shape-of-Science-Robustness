"""Package the reviewed sources and reproduce all four PDF files from extraction."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import tempfile
import zipfile

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
compiler = ROOT / 'data/manuscript_layout_v1/toolchain/tectonic'
environment = dict(os.environ, SOURCE_DATE_EPOCH='1789732800')
allowed = {'.tex', '.bib', '.md', '.sh', '.json', '.tiff', '.svg', '.pdf', '.png', '.py', '.csv'}
report = {'created_at': datetime.now(timezone.utc).isoformat(), 'packages': {}}

for lang, folder, package_name, pdf_dir in [
    ('en', 'manuscript', 'manuscript_source.zip', 'output/pdf'),
    ('es', 'manuscript_es', 'manuscript_source_es.zip', 'output/pdf/es'),
]:
    source = ROOT / folder
    package = ROOT / 'output' / package_name
    files = sorted(p for p in source.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    assert all(p.suffix in allowed and not p.is_symlink() for p in files)
    with zipfile.ZipFile(package, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(source).as_posix(), (2026, 9, 20, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100755 if path.suffix == '.sh' else 0o100644) << 16
            archive.writestr(info, path.read_bytes())
    temp = Path(tempfile.mkdtemp(prefix=f'public_release_portable_{lang}_', dir=ROOT/'tmp/pdfs'))
    extracted, build = temp/'source', temp/'build'
    extracted.mkdir(); build.mkdir()
    with zipfile.ZipFile(package) as archive:
        assert archive.testzip() is None
        archive.extractall(extracted)
    for path in files:
        assert sha(path) == sha(extracted / path.relative_to(source))
    documents = {}
    for document in ['main', 'supplement']:
        result = subprocess.run([str(compiler), '--keep-logs', '--outdir', str(build), f'{document}.tex'],
                                cwd=extracted, env=environment, text=True, capture_output=True, check=True)
        (HERE/f'portable_{lang}_{document}.log').write_text(result.stdout+result.stderr)
        actual, expected = build/f'{document}.pdf', ROOT/pdf_dir/f'{document}.pdf'
        assert sha(actual) == sha(expected), (lang, document, 'PDF differs from extracted source')
        documents[document] = {'path': str(expected.relative_to(ROOT)), 'sha256': sha(actual),
                               'pages': len(PdfReader(actual).pages), 'byte_identical': True}
    report['packages'][lang] = {'path': str(package.relative_to(ROOT)), 'sha256': sha(package),
                                'files': len(files), 'source_hashes': {str(p.relative_to(source)): sha(p) for p in files},
                                'documents': documents, 'extracted_directory': str(extracted)}
    print(f'{lang}: {len(files)} files; both PDFs reproduced exactly.', flush=True)
report['exclusions'] = 'Corpus, embeddings, model weights, API keys and full texts of third parties are not packaged.'
report['limit'] = 'This reproduces manuscript presentation, not the scientific calculations or a remote Overleaf upload.'
(HERE/'portable_source_audit.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n')
