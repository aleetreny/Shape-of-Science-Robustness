from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
STAGE=ROOT/'data/compact_release_v1/package';OUT=ROOT/'output/compact_release'
selection=json.loads((STAGE/'SELECTION.json').read_text())
old=json.loads((STAGE/'PACKAGE_MANIFEST.json').read_text())
for r in old['members']:
    if r['path'].endswith(('.py','.c','.sh')):
        assert hashlib.sha256((STAGE/r['path']).read_bytes()).hexdigest()==r['sha256'],r['path']
source_commit=selection['source_code_commit']
code=[p for p in STAGE.rglob('*') if p.is_file() and not set(p.relative_to(STAGE).parts).intersection({'data','public_metadata','.git','__pycache__','downloads','reproduced'}) and p.name not in {'PACKAGE_MANIFEST.json','release-manifest.json'} and p.suffix!='.pyc']
manifest={'version':'1.1.0','scientific_source_commit':source_commit,'scientific_programs_unchanged':True,'new_utilities':['reproducibility/reproduce_analysis.py','.github/scripts/deposit.py','.github/workflows/deposit.yml'],'members':[{'path':str(p.relative_to(STAGE)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(code)]}
(STAGE/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');code.append(STAGE/'PACKAGE_MANIFEST.json')
for p in code:
    assert not any(s in p.relative_to(STAGE).parts for s in ['manuscript','manuscript_es','research','output','manuscript_variants'])
    assert p.name!='AGENTS.md'
def archive(name,files):
    target=OUT/name
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(files):
            info=zipfile.ZipInfo(str(p.relative_to(STAGE)),(2026,9,21,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info._compresslevel=9
            info.external_attr=(0o100755 if p.suffix=='.sh' else 0o100644)<<16
            z.writestr(info,p.read_bytes())
    with zipfile.ZipFile(target) as z:assert z.testzip() is None
    result={'name':name,'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'members':len(files)}
    print(json.dumps(result),flush=True);return result
jobs=[('code-and-guides.zip',code)]
for group in sorted({Path(f['path']).parts[1] for f in selection['included']}):
    paths=[STAGE/f['path'] for f in selection['included'] if Path(f['path']).parts[1]==group]
    jobs.append(('data-'+group.replace('_','-')+'.zip',paths))
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(lambda x:archive(*x),jobs))
for name in ['README.md','LICENSE','LICENSING.md','REPRODUCTION_CHECK.json']:
    p=STAGE/name;shutil.copy2(p,OUT/name);b=p.read_bytes();results.append({'name':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
r={'version':'1.1.0','doi':'10.5281/zenodo.22876602','source_code_commit':source_commit,'files':results,'total_bytes_excluding_manifest':sum(f['bytes'] for f in results),'scope':selection['scope']}
for p in [OUT/'release-manifest.json',STAGE/'release-manifest.json',HERE/'release-manifest.json']:p.write_text(json.dumps(r,indent=2)+'\n')
print('TOTAL',r['total_bytes_excluding_manifest'],flush=True)
