"""Build explicit, independently checksummed numerical archives; never edit sources."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import collections, csv, hashlib, json, os, time, zipfile
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'output/zenodo'
HERE = Path(__file__).resolve().parent
SAFE = ROOT / 'data/public_release_v1/metadata'
GROUPS = ['analysis_ready_v1','embeddings_v1','analysis_v1','checklist_v1','robustness_v2','prepaper_v1','morphology_pilot_v1','field_pair_summary_v1','robustness_closure_v1']
SUFFIXES = {'.npy','.npz','.parquet','.csv','.json','.py','.c','.md','.txt','.bib','.sh'}
TEXT_COLUMNS = {'title','abstract'}

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(8*1024**2),b''):h.update(b)
    return h.hexdigest()

def has_abstract(value):
    if isinstance(value,dict):
        return any((k.lower()=='abstract' and isinstance(v,str) and v) or has_abstract(v) for k,v in value.items())
    return isinstance(value,list) and any(has_abstract(v) for v in value)

def collect():
    groups=collections.defaultdict(list); excluded=[]; schemas={}
    for name in GROUPS:
        for p in sorted((ROOT/'data'/name).rglob('*')):
            if not p.is_file():continue
            rel=p.relative_to(ROOT).as_posix()
            if p.is_symlink() or p.suffix not in SUFFIXES or '__pycache__' in p.parts:
                excluded.append({'path':rel,'reason':'runtime/cache/lock/binary or unsupported format'});continue
            group='embeddings_'+p.relative_to(ROOT/'data'/name).parts[0] if name=='embeddings_v1' else name
            source=p; archive_path=rel; original_sha=None
            if p.suffix=='.json':
                try:
                    if has_abstract(json.loads(p.read_text())):
                        excluded.append({'path':rel,'reason':'contains historical plaintext abstracts','sha256':sha(p)});continue
                except (UnicodeError,ValueError):raise RuntimeError('Invalid JSON '+rel)
            if p.suffix=='.parquet':
                schema=pq.read_schema(p); columns=schema.names
                key=hashlib.sha256(str(schema).encode()).hexdigest()[:12]
                schemas.setdefault(key,{'columns':[{'name':f.name,'type':str(f.type)} for f in schema],'example':rel})
                if TEXT_COLUMNS.intersection(columns):
                    original_sha=sha(p)
                    table=pq.read_table(p,columns=[c for c in columns if c not in TEXT_COLUMNS])
                    archive_path='public_metadata/'+p.relative_to(ROOT/'data').as_posix()
                    source=SAFE/p.relative_to(ROOT/'data');source.parent.mkdir(parents=True,exist_ok=True)
                    pq.write_table(table,source,compression='zstd')
                    excluded.append({'path':rel,'reason':'title/abstract columns excluded; non-text columns exported separately','sha256':original_sha,'replacement':archive_path})
            groups[group].append((source,archive_path,rel,original_sha))
    (HERE/'data_exclusions.json').write_text(json.dumps(excluded,indent=2)+'\n')
    (OUT/'SCHEMAS.json').write_text(json.dumps(schemas,indent=2)+'\n')
    return groups

def build(group, files):
    destination=OUT/(group+'.zip'); side=HERE/(group+'.manifest.json')
    if destination.exists() and side.exists():
        old=json.loads(side.read_text())
        if old['archive_bytes']==destination.stat().st_size and sha(destination)==old['archive_sha256']:
            print(group,'verified existing archive',flush=True);return old
    started=time.monotonic(); records=[]; temporary=destination.with_suffix('.zip.partial')
    with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as z:
        for p, name, original, original_sha in files:
            h=hashlib.sha256(); info=zipfile.ZipInfo(name,(2026,9,20,12,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info._compresslevel=1;info.external_attr=0o100644<<16
            with p.open('rb') as stream,z.open(info,'w',force_zip64=True) as target:
                for block in iter(lambda:stream.read(8*1024**2),b''):
                    h.update(block);target.write(block)
            records.append({'path':name,'bytes':p.stat().st_size,'sha256':h.hexdigest(),'source':original,'original_sha256':original_sha})
        z.writestr('ARCHIVE_MANIFEST.json',json.dumps(records,indent=2)+'\n')
    os.replace(temporary,destination)
    result={'archive':destination.name,'archive_bytes':destination.stat().st_size,'archive_sha256':sha(destination),'seconds':time.monotonic()-started,'files':records}
    side.write_text(json.dumps(result,indent=2)+'\n')
    print(group,len(records),'files',round(result['archive_bytes']/1e9,3),'GB',round(result['seconds'],1),'s',flush=True)
    return result

def main():
    OUT.mkdir(parents=True,exist_ok=True);groups=collect()
    print('Preparing',len(groups),'archives',sum(len(x) for x in groups.values()),'files',flush=True)
    results=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs=[pool.submit(build,k,v) for k,v in sorted(groups.items(),key=lambda kv:sum(p.stat().st_size for p,*_ in kv[1]))]
        for job in as_completed(jobs):results.append(job.result())
    result={'release':'1.0.0','date':'2026-09-20','scope':'frozen vectors, selections, numerical analyses, non-text metadata; no plaintext abstract input tables or model weights','archives':sorted(results,key=lambda r:r['archive'])}
    (OUT/'DATA_MANIFEST.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'SHA256SUMS').write_text(''.join(f"{r['archive_sha256']}  {r['archive']}\n" for r in result['archives']))
    print('COMPLETE',sum(r['archive_bytes'] for r in results),'bytes',flush=True)

if __name__=='__main__':main()
