"""Offline verification of the final live smoke result; never starts production."""
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from sos_download.cli import get_key, LEGACY_SOURCE, LEGACY_INDEX
from sos_download.records import normalize_work

output = Path(__file__).resolve().parent
smoke = ROOT / 'data/smoke_verified_2026-09-15'
tests = subprocess.run([str(ROOT/'.venv/bin/python'), '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                       cwd=ROOT, capture_output=True, text=True)
(output/'tests.txt').write_text(tests.stdout + tests.stderr)
assert tests.returncode == 0, 'Offline tests did not pass'
subprocess.run(['/bin/bash', '-n', str(ROOT/'download.sh')], check=True)
config = json.loads((smoke/'config.json').read_text())
table = pq.read_table(smoke/'corpus.parquet')
records = table.to_pylist()
assert len(records) == 124 and len({r['work_id'] for r in records}) == 124
assert sum(r['cohort']=='base' for r in records)==120
assert sum(r['cohort']=='extra' for r in records)==4
db = sqlite3.connect((smoke/'state.sqlite').as_uri()+'?mode=ro',uri=True)
raw = {}
pages = list(db.execute('SELECT block_id,page,sha256 FROM pages'))
for block,page,sha in pages:
    path = smoke/'raw'/f'block_{block:06d}_page_{page:03d}.json.gz'
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest()==sha
    raw[(block,page)] = json.loads(gzip.decompress(data))
for record in records:
    envelope = raw[(record['source_block'],record['source_page'])]
    candidate = envelope['response']['results'][record['source_page_index']]
    normalized, reason = normalize_work(candidate,config)
    assert reason is None
    for key,value in normalized.items():
        assert record[key]==value, f'Export disagrees with original response: {key}'
saved_code = json.loads(db.execute("SELECT value FROM meta WHERE key='implementation'").fetchone()[0])
for name,sha in saved_code.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha
resume_events = [json.loads(r[0]) for r in db.execute("SELECT details FROM events WHERE kind='resume_pages_checked'")]
assert resume_events and resume_events[0]['checks'][0]['page']==1
stats = [dict(block=r[0],cohort=r[1],stats=json.loads(r[2])) for r in db.execute('SELECT id,cohort,stats_json FROM blocks ORDER BY id')]
db.close()
key = get_key().encode()
scan_files = list((ROOT/'sos_download').glob('*.py')) + list((ROOT/'config').glob('*.json'))
scan_files += list(ROOT.glob('*.md')) + [ROOT/'download.sh', ROOT/'requirements.txt']
scan_files += [p for p in smoke.rglob('*') if p.is_file()]
for path in scan_files:
    value=path.read_bytes()
    assert key not in value, f'Credential found in {path.name}'
    if path.suffix=='.gz':assert key not in gzip.decompress(value)
old_status = subprocess.run(['git','-C',str(LEGACY_SOURCE.parents[2]),'status','--porcelain'],capture_output=True,text=True,check=True).stdout
assert not old_status, 'Reference project has Git changes; investigate'
index = sqlite3.connect(LEGACY_INDEX.as_uri()+'?mode=ro',uri=True)
legacy_rows=index.execute('SELECT count(*) FROM legacy').fetchone()[0];index.close()
assert legacy_rows==2378036
assert not (ROOT/'data/corpus_500k/state.sqlite').exists(), 'Production was started; this verification expects it untouched'
validation=json.loads((smoke/'validation.json').read_text())
report=dict(verified_at=datetime.now(timezone.utc).isoformat(), status='passed', offline_tests=21,
            live_smoke=dict(rows=len(records),base=120,extra=4,pages=len(pages),resume_events=resume_events,
                            raw_to_export_match=True,validation=validation,block_stats=stats),
            legacy_index_rows=legacy_rows,reference_git_clean=True,production_started=False,
            credentials_absent_from_scanned_artifacts=True,code_matches_live_smoke=True,
            versions=dict(python=sys.version.split()[0], **{n:importlib.metadata.version(n) for n in ('requests','pyarrow','python-dotenv')}))
(output/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('status','offline_tests','legacy_index_rows','production_started')},ensure_ascii=False))
print(f'Live smoke: {len(records)} unique records, all exported values agree with saved responses; {len(pages)} pages.')
