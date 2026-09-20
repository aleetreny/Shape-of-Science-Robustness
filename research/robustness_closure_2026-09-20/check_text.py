from pathlib import Path
from collections import Counter
import ast,hashlib,importlib.util,json,re
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('translation',ROOT/'research/manuscript_spanish_2026-09-18/verify_translation.py');tr=importlib.util.module_from_spec(spec);spec.loader.exec_module(tr)
tree=ast.parse((ROOT/'research/manuscript_full_2026-09-18/check_text.py').read_text());fs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'group','remove','prose'}];ns={'re':re};exec(compile(ast.Module(body=fs,type_ignores=[]),'<pure prose helpers>','exec'),ns)
count=lambda s:len(re.findall(r"\b[A-Za-zÀ-ÿ0-9]+(?:[-'][A-Za-zÀ-ÿ0-9]+)*\b",ns['prose'](re.sub(r'\\Needspace\{[^}]*\}', '', s))))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'documents':{},'bilingual':{}}
for document in ['main','supplement']:
 en=(ROOT/'manuscript'/f'{document}.tex').read_text();es=(ROOT/'manuscript_es'/f'{document}.tex').read_text()
 for command in ['citep','citet','label','ref','input']:
  assert re.findall(r'\\'+command+r'\{([^}]*)\}',en)==re.findall(r'\\'+command+r'\{([^}]*)\}',es),(document,command)
 for level in ['section','subsection']:assert en.count('\\'+level+'{')==es.count('\\'+level+'{'),(document,level)
 for lang,text in [('en',en),('es',es)]:
  original=(HERE/'baseline_documents'/('manuscript' if lang=='en' else 'manuscript_es')/f'{document}.tex').read_text()
  assert set(re.findall(r'\\cite[pt]\{([^}]*)\}',text))==set(re.findall(r'\\cite[pt]\{([^}]*)\}',original))
 if document=='main':
  ens=en.split(r'\section{Introduction}',1)[1].split(r'\section*{Declarations}',1)[0];ess=es.split(r'\section{Introducción}',1)[1].split(r'\section*{Declaraciones}',1)[0]
  for text,word,lang in [(en,'Declarations','en'),(es,'Declaraciones','es')]:
   orig=(HERE/'baseline_documents'/('manuscript' if lang=='en' else 'manuscript_es')/'main.tex').read_text();assert text.split('\\section*{'+word+'}',1)[1]==orig.split('\\section*{'+word+'}',1)[1]
   assert next(l for l in orig.splitlines() if r'\LARGE\bfseries' in l) in text
  enp=ens.split('\n\n');esp=ess.split('\n\n');assert len(enp)==len(esp),(len(enp),len(esp))
  for i,(a,b) in enumerate(zip(enp,esp)):
   a=re.sub(r'\}\{(?:scales|paired|input|pairs)\}\{[^}]+\}', '}',a);b=re.sub(r'\}\{(?:scales|paired|input|pairs)\}\{[^}]+\}', '}',b)
   assert Counter(tr.numbers(a))==Counter(tr.numbers(b,True)),('main paragraph',i,Counter(tr.numbers(a))-Counter(tr.numbers(b,True)),Counter(tr.numbers(b,True))-Counter(tr.numbers(a)))
  report['bilingual']['main_paragraphs']=len(enp)
 else:
  assert Counter(tr.numbers(tr.body(en)))==Counter(tr.numbers(tr.body(es),True)),('supp numbers',Counter(tr.numbers(tr.body(en)))-Counter(tr.numbers(tr.body(es),True)),Counter(tr.numbers(tr.body(es),True))-Counter(tr.numbers(tr.body(en))))
 assert [x.replace(',','.') for x in tr.equations(en)]==[x.replace(',','.') for x in tr.equations(es)],(document,'equations')
 for lang,folder,pdfdir,text in [('en','manuscript','output/pdf',en),('es','manuscript_es','output/pdf/es',es)]:
  pdf=ROOT/pdfdir/f'{document}.pdf';reader=PdfReader(pdf);pages=[p.extract_text() for p in reader.pages];alltext='\n'.join(pages);(HERE/f'{lang}_{document}_text.txt').write_text(alltext)
  assert all(len(p.strip())>60 for p in pages),(lang,document,'empty pages');assert not any(t in alltext for t in ['??','\ufffd','TODO','Writing plan']),(lang,document,'unfinished')
  log=pdf.with_suffix('.log').read_text();bad=[w for w in ['Overfull','Missing character','undefined references','undefined citations','Citation `'] if w in log];assert not bad,(lang,document,bad)
  for word,prefix,total in [('Table' if lang=='en' else 'Tabla','' if document=='main' else 'S',2 if document=='main' else 20),('Figure' if lang=='en' else 'Figura','' if document=='main' else 'S',4 if document=='main' else 11)]:
   for n in range(1,total+1):assert re.search(word[0]+r'\s*'+word[1:]+r'\s+'+prefix+str(n)+r'\s*:',alltext),(lang,document,word,n)
  r={'pages':len(pages),'sha256':sha(pdf)}
  if document=='main':
   body=text.split(r'\section{Introduction}' if lang=='en' else r'\section{Introducción}',1)[1].split(r'\section*{Declarations}' if lang=='en' else r'\section*{Declaraciones}',1)[0];abstract=text.split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0];r.update(body_words=count(body),abstract_words=count(abstract));assert count(abstract)<=200,(lang,'abstract too long',count(abstract))
  report['documents'][lang+'_'+document]=r
# Each printed table row preserves numbers after locale formatting.
for p in sorted((ROOT/'manuscript/tables/tex').glob('*.tex')):
 q=ROOT/'manuscript_es/tables/tex'/p.name;enrows=[x for x in p.read_text().splitlines() if ' & ' in x];esrows=[x for x in q.read_text().splitlines() if ' & ' in x];assert len(enrows)==len(esrows),p.name
 for i,(a,b) in enumerate(zip(enrows,esrows)):assert tr.numbers(a)==tr.numbers(b,True),(p.name,i,tr.numbers(a),tr.numbers(b,True))
# Source CSV bytes must match between languages. Captions and notes remain localized.
files=list((ROOT/'manuscript').rglob('*.csv'))
for p in files:assert sha(p)==sha(ROOT/'manuscript_es'/p.relative_to(ROOT/'manuscript')),p
report.update(csv_files_bilingually_identical=len(files),tables=22,figures=15,title_declarations_citations_retained=True)
(HERE/'text_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps(report,indent=2,ensure_ascii=False))
