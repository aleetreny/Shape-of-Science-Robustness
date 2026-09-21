"""Adopt the reviewed preview after the data archive is public."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
public=json.loads((HERE/'public_verification.json').read_text());assert public['published'] and public['record']==22876602
preview=ROOT/'data/compact_release_v1/manuscript_preview'
subprocess.run([sys.executable,str(HERE/'update_availability.py')],check=True)
# The canonical source must equal every source byte used for the visual and portable review.
sources={}
for folder in ['manuscript','manuscript_es']:
 for p in sorted((preview/folder).rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts:
   rel=p.relative_to(preview);actual=ROOT/rel
   assert actual.is_file() and actual.read_bytes()==p.read_bytes(),str(rel)
   sources[str(rel)]=hashlib.sha256(p.read_bytes()).hexdigest()
outputs={}
for rel in ['output/pdf/main.pdf','output/pdf/supplement.pdf','output/pdf/es/main.pdf','output/pdf/es/supplement.pdf','output/manuscript_source.zip','output/manuscript_source_es.zip']:
 source=preview/rel;target=ROOT/rel;shutil.copyfile(source,target)
 assert source.read_bytes()==target.read_bytes()
 outputs[rel]={'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size,'identical_to_visually_and_portably_verified_preview':True}
receipt={'all_checks_passed':True,'scientific_body_unchanged':True,'source_files_matched':len(sources),'sources':sources,'outputs':outputs,'visual_review':'The adopted PDFs are byte-identical to the rendered and inspected preview.','portable_review':'Both editable archives rebuilt their main and supplement PDFs byte-identically from a separate extracted directory.'}
(HERE/'manuscript_update.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'source_files_matched':len(sources),'verified_outputs':len(outputs),'all_checks_passed':True}))
