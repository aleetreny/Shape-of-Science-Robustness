"""Audit authored text and citation coverage without running scientific code."""
from pathlib import Path
import re,json,hashlib
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
TMP=ROOT/'data/manuscript_full_v1';TMP.mkdir(exist_ok=True)
def group(s,i):
 assert s[i]=='{'
 level=1;j=i+1
 while level:
  if s[j]=='{' and s[j-1]!='\\':level+=1
  if s[j]=='}' and s[j-1]!='\\':level-=1
  j+=1
 return s[i+1:j-1],j
def remove(s,cmd,n=1):
 pat=re.compile(r'\\'+cmd+r'\*?(?:\[[^\]]*\])?\s*\{')
 while m:=pat.search(s):
  end=m.end()-1
  for _ in range(n):
   while s[end].isspace():end+=1
   _,end=group(s,end)
  s=s[:m.start()]+' '+s[end:]
 return s
def prose(s):
 for cmd,n in [('PanelFigure',4),('section',1),('subsection',1),('input',1),('cite[pt]?',1),('ref',1),('label',1),('begin',1),('end',1)]:s=remove(s,cmd,n)
 s=re.sub(r'\$[^$]*\$',' ',s)
 s=re.sub(r'\\[A-Za-z]+(?:\[[^\]]*\])?',' ',s)
 return s
s=(ROOT/'manuscript/main.tex').read_text()
abstract=s.split('\\begin{abstract}')[1].split('\\end{abstract}')[0]
body=s[s.index('\\section{Introduction}'):s.index('\\section*{Declarations}') if '\\section*{Declarations}' in s else s.index('\\section*{Author contributions}')]
count=lambda t:len(re.findall(r"\b[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*\b",prose(t)))
sections={}
for part in re.split(r'(?=\\section\{)',body):
 if part.startswith('\\section{'):
  title=part.split('{',1)[1].split('}')[0];sections[title]=count(part)
report={'abstract_words':count(abstract),'body_words':count(body),'sections':sections,'method':'Regex words, hyphenated words once; headings, citations, figures/captions, input tables, math and declarations excluded.'}
(OUT/'word_count.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
def flatten(path):
 content=path.read_text()
 def replace(m):
  if m.group(1)=='preamble':return ''
  f=ROOT/'manuscript'/(m.group(1)+'.tex')
  return flatten(f)
 return re.sub(r'\\input\{([^}]+)\}',replace,content)
flat='\n'.join(flatten(ROOT/'manuscript'/name) for name in ['main.tex','supplement.tex'])
(TMP/'validation_flattened.tex').write_text(flat)
keys=set(k.strip() for chunk in re.findall(r'\\cite\w*(?:\[[^\]]*\])?\{([^}]+)\}',flat) for k in chunk.split(','))
entries=[]
for name in ['references.bib','context_references.bib']:
 for block in re.split(r'(?m)(?=^@)',(ROOT/'manuscript'/name).read_text()):
  m=re.match(r'@\w+\{([^,]+),',block)
  if m and m.group(1) in keys:entries.append(block)
assert len(entries)==len(keys)
(TMP/'cited_references.bib').write_text('\n'.join(entries))
print('Unique citation keys:',len(keys))
