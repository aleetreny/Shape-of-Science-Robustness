"""Package presentation sources and compile the extracted copy without corpus files."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import shutil
import subprocess
import zipfile

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    source = ROOT / 'manuscript_es'
    package = ROOT / 'output/manuscript_source_es.zip'
    allowed = {'.tex', '.bib', '.md', '.sh', '.json', '.tiff', '.svg',
               '.pdf', '.png', '.py', '.csv'}
    files = sorted(p for p in source.rglob('*')
                   if p.is_file() and '__pycache__' not in p.parts)
    assert all(p.suffix in allowed for p in files)
    assert not any(p.is_symlink() for p in files)
    with zipfile.ZipFile(package, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(source).as_posix(), (2026, 9, 18, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100755 if path.suffix == '.sh' else 0o100644) << 16
            archive.writestr(info, path.read_bytes())

    extracted = ROOT / 'tmp/pdfs/spanish_portable_source'
    build = ROOT / 'tmp/pdfs/spanish_portable_build'
    if extracted.exists():
        shutil.rmtree(extracted)
    extracted.mkdir(parents=True)
    build.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(package) as archive:
        assert archive.testzip() is None
        archive.extractall(extracted)
    for path in files:
        assert sha(path) == sha(extracted / path.relative_to(source))

    compiler = ROOT / 'data/manuscript_layout_v1/toolchain/tectonic'
    environment = dict(os.environ, SOURCE_DATE_EPOCH='1789732800')
    documents = {}
    for name in ('main', 'supplement'):
        result = subprocess.run(
            [str(compiler), '--keep-logs', '--outdir', str(build), f'{name}.tex'],
            cwd=extracted, env=environment, text=True, capture_output=True, check=True,
        )
        (build / f'{name}_compile.txt').write_text(result.stdout + result.stderr)
        actual = PdfReader(build / f'{name}.pdf')
        expected = PdfReader(ROOT / 'output/pdf/es' / f'{name}.pdf')
        actual_text = [p.extract_text() for p in actual.pages]
        expected_text = [p.extract_text() for p in expected.pages]
        assert actual_text == expected_text, name
        assert sha(build / f'{name}.pdf') == sha(ROOT / 'output/pdf/es' / f'{name}.pdf'), name
        documents[name] = {'pages': len(actual.pages), 'identical_extracted_text': True,
                           'sha256': sha(build / f'{name}.pdf')}

    evidence = {'created_at': datetime.now(timezone.utc).isoformat(),
                'package': str(package.relative_to(ROOT)), 'files': len(files),
                'bytes': package.stat().st_size, 'sha256': sha(package),
                'zip_integrity': True, 'extracted_files_match': True,
                'compiled_from_extracted_sources': True, 'documents': documents,
                'overleaf_upload_or_remote_compile': False}
    (EVIDENCE / 'portable_source_audit.json').write_text(json.dumps(evidence, indent=2) + '\n')
    print(json.dumps(evidence, indent=2))


if __name__ == '__main__':
    run()
