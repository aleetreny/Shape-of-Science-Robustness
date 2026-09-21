"""Verify the exact compact draft; --publish archives the authorized release."""
import argparse, hashlib, importlib.util, json, time, urllib.error, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
RECORD=22876602; BASE='https://zenodo.org'; API=f'{BASE}/api/deposit/depositions/{RECORD}'
spec=importlib.util.spec_from_file_location('private_upload',ROOT/'scripts/zenodo_upload.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); token=m.load_token()
def request(url, *, auth=True, method='GET', payload=None):
    assert url.startswith(BASE+'/api/')
    headers={'Accept':'application/json','User-Agent':'ShapeOfScienceReproduction/1.1'}
    if auth:headers['Authorization']='Bearer '+token
    body=None if payload is None else json.dumps(payload).encode()
    if body is not None:headers['Content-Type']='application/json'
    with urllib.request.urlopen(urllib.request.Request(url,data=body,headers=headers,method=method),timeout=60) as r:
        return json.load(r)
def check_files(files, public=False):
    found={f['key'] if public else f['filename']:f for f in files}
    assert set(found)==set(expected),'Remote file set differs'
    for name,wanted in expected.items():
        actual=found[name]
        assert actual.get('size',actual.get('filesize'))==wanted['bytes'],(name,'size')
        assert actual['checksum'].removeprefix('md5:')==wanted['md5'],(name,'checksum')
    return {'files_verified':len(found),'bytes':sum(e['bytes'] for e in expected.values())}
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--publish',action='store_true');args=parser.parse_args()
folder=ROOT/'output/compact_release';manifest=json.loads((folder/'release-manifest.json').read_text())
entries=manifest['files']+[{'name':'release-manifest.json','bytes':(folder/'release-manifest.json').stat().st_size,'sha256':hashlib.sha256((folder/'release-manifest.json').read_bytes()).hexdigest()}]
expected={}
for e in entries:
    data=(folder/e['name']).read_bytes()
    assert len(data)==e['bytes'] and hashlib.sha256(data).hexdigest()==e['sha256']
    expected[e['name']]={**e,'md5':hashlib.md5(data).hexdigest()}
draft=request(API);assert draft['id']==RECORD
if len(draft['files'])!=len(expected):
    print(json.dumps({'record':RECORD,'uploaded':len(draft['files']),'expected':len(expected),'submitted':draft['submitted']}))
    raise SystemExit(1 if args.publish else 0)
counts=check_files(draft['files'])
metadata=json.loads((HERE/'metadata.json').read_text())['metadata']
for key in ['title','upload_type','version','publication_date','access_right','license','description','creators']:
    assert draft['metadata'][key]==metadata[key],key
assert draft['metadata'].get('prereserve_doi',{}).get('doi',draft['metadata'].get('doi'))==f'10.5281/zenodo.{RECORD}'
if not args.publish:
    print(json.dumps({'record':RECORD,**counts,'submitted':draft['submitted'],'ready':True}));raise SystemExit()
# The clean Linux run is an additional portability check before final publication.
linux=json.loads((HERE/'linux_reproduction/verification.json').read_text())
assert linux['all_checks_passed'] is True and linux['closure_csv_rows']==106445 and linux['local_neighbor_score_checks']==17550
if not draft['submitted']:
    assert draft['state']=='unsubmitted'
    try:
        result=request(API+'/actions/publish',method='POST',payload={})
    except (TimeoutError,urllib.error.URLError):
        # A publication response can be lost. Read its state; never blindly repeat POST.
        result=request(API)
    assert result['submitted'] is True,'Publication not confirmed; inspect draft state before another attempt'
public=request(f'{BASE}/api/records/{RECORD}?verify={time.time_ns()}',auth=False)
assert int(public['id'])==RECORD
counts=check_files(public['files'],public=True)
assert public['doi']==f'10.5281/zenodo.{RECORD}'
assert public['metadata']['title']==metadata['title'] and public['metadata']['version']=='1.1.0'
receipt={'published':True,'record':RECORD,'doi':public['doi'],'url':f'{BASE}/records/{RECORD}',**counts,'files':expected,'metadata':public['metadata'],'checked_at_unix':time.time()}
(HERE/'public_verification.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in {'files','metadata'}},indent=2))
