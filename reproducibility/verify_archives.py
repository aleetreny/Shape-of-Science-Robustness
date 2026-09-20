"""Verify downloaded archive checksums, optionally every uncompressed member."""
import argparse, hashlib, json, zipfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def digest(stream):
    h=hashlib.sha256()
    for block in iter(lambda:stream.read(8*1024**2),b''):h.update(block)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);ap.add_argument('--full',action='store_true');ap.add_argument('--output',type=Path);args=ap.parse_args()
    manifest=json.loads((args.directory/'DATA_MANIFEST.json').read_text())
    def check(record):
        p=args.directory/record['archive']
        assert p.stat().st_size==record['archive_bytes'],p.name
        with p.open('rb') as f:assert digest(f)==record['archive_sha256'],p.name
        if args.full:
            with zipfile.ZipFile(p) as z:
                inner=json.loads(z.read('ARCHIVE_MANIFEST.json'))
                assert inner==record['files']
                assert len(z.namelist())==len(set(z.namelist()))==len(inner)+1
                for item in inner:
                    name=item['path'];assert not name.startswith('/') and '..' not in Path(name).parts
                    assert z.getinfo(name).file_size==item['bytes']
                    with z.open(name) as f:assert digest(f)==item['sha256'],name
        print(p.name,'OK',flush=True)
        return {'archive':p.name,'files':len(record['files']),'bytes':p.stat().st_size,'sha256_verified':True,'all_members_verified':args.full}
    with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(check,manifest['archives']))
    result={'all_verified':True,'archives':results,'files':sum(x['files'] for x in results),'bytes':sum(x['bytes'] for x in results)}
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='archives'}))

if __name__=='__main__':main()
