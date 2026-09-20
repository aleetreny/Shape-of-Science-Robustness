from pathlib import Path
import hashlib,importlib.util,json,re
from collections import Counter
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('tr',ROOT/'research/manuscript_spanish_2026-09-18/verify_translation.py');tr=importlib.util.module_from_spec(spec);spec.loader.exec_module(tr)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def cleaned(s):
 s=re.sub(r'\\Needspace\{[^}]*\}','',s)
 return re.sub(r'\}\{(?:scales|paired|input|pairs)\}\{[^}]+\}','}',s)
report={'documents':{},'tables':{},'new_scientific_values':False}
for lang,folder,decl in [('en','manuscript','Declarations'),('es','manuscript_es','Declaraciones')]:
 old=(HERE/'baseline'/folder/'main.tex').read_text();new=(ROOT/folder/'main.tex').read_text()
 assert new.split('\\section*{'+decl+'}',1)[1]==old.split('\\section*{'+decl+'}',1)[1]
 before=set(tr.numbers(cleaned(old),lang=='es'));after=set(tr.numbers(cleaned(new),lang=='es'))
 assert not after-before,(lang,'new numeric value',after-before)
 assert tr.equations(old)==tr.equations(new),(lang,'math changed')
 for cmd in ['citep','citet']:
  assert re.findall(r'\\'+cmd+r'\{([^}]+)\}',old)==re.findall(r'\\'+cmd+r'\{([^}]+)\}',new)
 report['documents'][lang]={'declarations_unchanged':True,'citation_order_unchanged':True,'math_unchanged':True,'all_written_numeric_values_present_in_baseline':True,'new_source_sha256':sha(ROOT/folder/'main.tex')}
 for name in ['T01','T02']:
  old=(HERE/'baseline'/folder/f'tables/editorial/{name}.tex').read_text();new=(ROOT/folder/f'tables/editorial/{name}.tex').read_text()
  assert re.findall(r'\d+(?:[.,]\d+)*',old)==re.findall(r'\d+(?:[.,]\d+)*',new),(lang,name,'table numbers')
  assert re.findall(r'\\citep\{[^}]+\}',old)==re.findall(r'\\citep\{[^}]+\}',new),(lang,name,'citations')
  report['tables'][lang+'/'+name]={'all_numeric_tokens_and_citations_unchanged':True}
(HERE/'invariants_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: scientific numeric values, math, citation sequence, declarations and table values preserved.')
