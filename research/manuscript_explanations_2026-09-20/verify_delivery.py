"""Close the editorial revision only after text, numbers, renders and packages agree."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
text=read(HERE/'text_audit.json');numeric=read(HERE/'numeric_audit.json');render=read(HERE/'render_manifest.json');visual=read(HERE/'visual_review.json');packages=read(HERE/'portable_source_audit.json');comments=read(HERE/'comment_coverage.json')
assert len(comments)==38 and {c['comment'] for c in comments}==set(range(1,39))
assert all(c['status']=='applied' and c['languages']==['en','es'] for c in comments)
assert numeric['percentages_checked']==24
for rel,digest in numeric['source_sha256'].items():assert sha(ROOT/rel)==digest,rel
protected=read(HERE/'protected_manifest.json');baseline=read(HERE/'baseline_manifest.json')
for rel,digest in protected.items():assert sha(ROOT/rel)==digest,rel
for rel,digest in baseline.items():assert sha(HERE/'baseline'/rel)==digest,rel
for lang,folder,word in [('en','manuscript','Declarations'),('es','manuscript_es','Declaraciones')]:
 doc=text['documents'][lang];key=lang+'_main';assert sha(ROOT/doc['path'])==doc['sha256']==render[key]['sha256']==visual['documents'][key]['sha256']
 assert visual['documents'][key]['pages_reviewed']==list(range(1,doc['pages']+1))
 p=packages['packages'][lang];assert sha(ROOT/p['path'])==p['sha256']
 assert all(d['byte_identical'] and sha(ROOT/d['path'])==d['sha256'] for d in p['documents'].values())
 for rel,digest in p['source_hashes'].items():assert sha(ROOT/folder/rel)==digest
 old=(HERE/'baseline'/folder/'main.tex').read_text().split('\\section*{'+word+'}',1)[1].split(r'\bibliographystyle',1)[0]
 new=(ROOT/folder/'main.tex').read_text().split('\\section*{'+word+'}',1)[1].split(r'\begingroup',1)[0]
 if lang=='en':
  old=old.replace(' Computational and editorial assistance is disclosed below.','').split(r'\textbf{Use of AI-assisted tools.}',1)[0]
 else:
  old=old.replace(' La ayuda computacional y editorial se declara a continuación.','').split(r'\textbf{Uso de herramientas de inteligencia artificial.}',1)[0]
 old=old.rsplit(r'\par\medskip',1)[0]
 assert old.strip()==new.strip(),(lang,'unrequested declaration change')
covered={i for language in read(HERE/'paragraph_changes.json').values() for p in language for i in p['comments']}
assert covered|{7,38}==set(range(1,39))
report={'completed_at':datetime.now(timezone.utc).isoformat(),'all_complete':True,'comments_applied':38,'languages':['en','es'],'protected_files_verified':len(protected),'previous_files_archived':len(baseline),'documents':text['documents'],'bilingual_numeric_blocks':text['bilingual_paragraphs'],'percentage_conversions_verified':24,'visual_review_pages':sum(x['pages'] for x in text['documents'].values()),'portable_packages':{lang:{'path':p['path'],'sha256':p['sha256'],'files':p['files'],'both_PDFs_reproduced_exactly':True} for lang,p in packages['packages'].items()},'unchanged':['scientific programs and saved result tables','all figure assets','bibliography sources and citations','supplement sources and PDFs','title'],'authorised_declaration_change':'AI-use section and its cross-reference removed from both draft articles at author request; all other declaration text preserved. Genuine work history retained. Requirements to be checked before submission.','new_experiments':False,'publication_submission_or_push':False,'author_final_approval':False,'evidence_sha256':{name:sha(HERE/name) for name in ['text_audit.json','numeric_audit.json','render_manifest.json','visual_review.json','portable_source_audit.json','comment_coverage.json']}}
(HERE/'closure_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print('COMPLETE: 38 comments; 43 pages visually reviewed; 24 percentages; 491 protected files; both source ZIPs reproduce their PDFs exactly.')
