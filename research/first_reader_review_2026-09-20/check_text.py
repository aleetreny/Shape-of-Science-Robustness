"""Read-only checks of editorial accuracy, bilingual correspondence and PDF layout logs."""
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import ast,csv,hashlib,importlib.util,json,re
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
for rel,digest in read(HERE/'baseline_manifest.json').items(): assert sha(HERE/'baseline'/rel)==digest,rel
for rel,digest in read(HERE/'protected_manifest.json').items(): assert sha(ROOT/rel)==digest,('protected',rel)
spec=importlib.util.spec_from_file_location('tr',ROOT/'research/manuscript_spanish_2026-09-18/verify_translation.py');tr=importlib.util.module_from_spec(spec);spec.loader.exec_module(tr)
tree=ast.parse((ROOT/'research/manuscript_full_2026-09-18/check_text.py').read_text());fs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'group','remove','prose'}];ns={'re':re};exec(compile(ast.Module(body=fs,type_ignores=[]),'<pure helpers>','exec'),ns)
count=lambda s:len(re.findall(r"\b[A-Za-zÀ-ÿ0-9]+(?:[-'][A-Za-zÀ-ÿ0-9]+)*\b",ns['prose'](re.sub(r'\\Needspace\{[^}]*\}','',s))))
texts={lang:(ROOT/folder/'main.tex').read_text() for lang,folder in [('en','manuscript'),('es','manuscript_es')]}
bodies={lang:s.split(r'\section{Introduction}' if lang=='en' else r'\section{Introducción}',1)[1].split(r'\section*{Declarations}' if lang=='en' else r'\section*{Declaraciones}',1)[0] for lang,s in texts.items()}
for cmd in ['citep','citet','label','ref','input']:
 pattern=r'\\'+cmd+r'\{([^}]*)\}'
 assert re.findall(pattern,texts['en'])==re.findall(pattern,texts['es']),cmd
 for lang,folder in [('en','manuscript'),('es','manuscript_es')]:
  old=(HERE/'baseline'/folder/'main.tex').read_text()
  assert set(re.findall(pattern,old))==set(re.findall(pattern,texts[lang])),(lang,cmd)
  if cmd!='ref':assert re.findall(pattern,old)==re.findall(pattern,texts[lang]),(lang,cmd)
assert tr.equations(texts['en'])==[x.replace(',','.') for x in tr.equations(texts['es'])]
pars={lang:s.split('\n\n') for lang,s in bodies.items()};assert len(pars['en'])==len(pars['es'])
for i,(a,b) in enumerate(zip(pars['en'],pars['es'])):
 a=re.sub(r'\}\{(?:scales|paired|input|pairs)\}\{[^}]+\}','}',a);b=re.sub(r'\}\{(?:scales|paired|input|pairs)\}\{[^}]+\}','}',b)
 assert Counter(tr.numbers(a))==Counter(tr.numbers(b,True)),(i,Counter(tr.numbers(a))-Counter(tr.numbers(b,True)),Counter(tr.numbers(b,True))-Counter(tr.numbers(a)))
for folder in ['manuscript','manuscript_es']:
 assert (ROOT/folder/'tables/editorial/T01.tex').read_bytes()==(ROOT/folder/'tables/tex/T01.tex').read_bytes()
 manifest=read(ROOT/folder/'tables/manifest.json')
 assert manifest['T01']['editorial_source']['sha256']==sha(ROOT/folder/'tables/editorial/T01.tex')
 old=read(HERE/'baseline'/folder/'tables/manifest.json')
 assert {k:v for k,v in old.items() if k not in {'T01','T02'}}=={k:v for k,v in manifest.items() if k not in {'T01','T02'}}
 for key in ['T01','T02']:
  assert old[key]['sources']==manifest[key]['sources']
  assert manifest[key]['editorial_source']['sha256']==sha(ROOT/folder/f'tables/editorial/{key}.tex')
  assert (ROOT/folder/f'tables/editorial/{key}.tex').read_bytes()==(ROOT/folder/f'tables/tex/{key}.tex').read_bytes()
for lang,folder in [('en','manuscript'),('es','manuscript_es')]:
 s=texts[lang];old=(HERE/'baseline'/folder/'main.tex').read_text()
 assert next(l for l in old.splitlines() if r'\LARGE\bfseries' in l) in s
 assert 'OpenAI Codex' not in s
 assert ('AI-assisted tools' if lang=='en' else 'herramientas de inteligencia artificial') not in s
 for sentence in (['The author declares no competing interests.','This research received no external funding.'] if lang=='en' else ['El autor declara que no tiene conflictos de interés.','Esta investigación no recibió financiación externa.']):assert sentence in s
 abstracts={k:v.split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0].strip() for k,v in texts.items()}
 assert count(abstracts['en'])<=200,count(abstracts['en'])
report={'checked_at':datetime.now(timezone.utc).isoformat(),'protected_files':len(read(HERE/'protected_manifest.json')),'bilingual_paragraphs':len(pars['en']),'documents':{}}
for lang,pdfdir in [('en','output/pdf'),('es','output/pdf/es')]:
 p=ROOT/pdfdir/'main.pdf';pdf=PdfReader(p);pages=[x.extract_text() for x in pdf.pages];alltext='\n'.join(pages)
 assert all(len(s.strip())>60 for s in pages)
 assert all(x not in alltext for x in ['??','\ufffd','TODO','OpenAI Codex'])
 for token in ['Overfull','Missing character','undefined references','undefined citations','Citation `']: assert token not in p.with_suffix('.log').read_text(),(lang,token)
 for word,total in [('Table' if lang=='en' else 'Tabla',2),('Figure' if lang=='en' else 'Figura',4)]:
  for n in range(1,total+1):assert re.search(word[0]+r'\s*'+word[1:]+r'\s+'+str(n)+r'\s*:',alltext),(lang,word,n)
 (HERE/f'{lang}_main_text.txt').write_text(alltext)
 report['documents'][lang]={'path':str(p.relative_to(ROOT)),'pages':len(pdf.pages),'sha256':sha(p),'abstract_words':count(abstracts[lang]),'body_words':count(bodies[lang])}
(HERE/'text_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
(HERE/'abstracts.json').write_text(json.dumps({k:{'text':v,'words':count(v)} for k,v in abstracts.items()},indent=2,ensure_ascii=False)+'\n')
print(report)
