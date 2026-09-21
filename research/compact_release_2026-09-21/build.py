"""Select analysis measurements and identities; preserve every frozen source."""
from pathlib import Path
import collections, hashlib, json, zipfile, time
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
STAGE=ROOT/'data/compact_release_v1/package'
OUT=ROOT/'output/compact_release'
OLD=ROOT/'output/zenodo'
STAGE.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def decision(name):
    p=Path(name)
    if 'shards' in p.parts:return 'Omit inference shards: vectors and repeated row metadata.'
    if p.name in {'progress.json','inspected_pngs.json'}:return 'Omit runtime progress.'
    if p.suffix in {'.npy','.npz'}:
        keep=(any(w in p.name for w in ['selected','selection','row_index','row_indices','global_ids','query_ids','candidate_ids','mask','assignments','permutation','shared_counts','contrast','global_mean','one_subfield']) or 'selections' in p.parts or p.name=='cka_replicates.npy')
        if not keep:return 'Omit regenerable embeddings, centre-vector caches, or nearest-neighbour lists.'
    return None
with zipfile.ZipFile(OLD/'shape-of-science-code-v1.0.0-data-only.zip') as z:
    for item in z.infolist():
        if item.is_dir():continue
        dest=STAGE/item.filename;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(item))
manifest=json.loads((OLD/'DATA_MANIFEST.json').read_text()); kept=[];omitted=[]
for archive in manifest['archives']:
    n=0;total=0
    with zipfile.ZipFile(OLD/archive['archive']) as z:
        for item in archive['files']:
            reason=decision(item['path'])
            if reason:
                omitted.append({'path':item['path'],'bytes':item['bytes'],'sha256':item['sha256'],'reason':reason});continue
            data=z.read(item['path']);assert sha(data)==item['sha256'],item['path']
            dest=STAGE/item['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
            kept.append({**item,'source_archive':archive['archive']});n+=1;total+=len(data)
    print(archive['archive'],n,round(total/1e6,2),'MB selected',flush=True)
selection={'version':'1.1.0','date':'2026-09-21','source_code_commit':'cc61517dc2ea1e946c4fe391c4fcc80fa6e4819f','scope':'Reproduction from frozen model-derived measurements, including identities and selection data. Embedding inference and nearest-neighbour construction are not re-run by this distribution.','included':kept,'omitted':omitted}
(HERE/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
(STAGE/'SELECTION.json').write_text(json.dumps(selection,indent=2)+'\n')
print('SELECTED',len(kept),sum(f['bytes'] for f in kept),'bytes',flush=True)
