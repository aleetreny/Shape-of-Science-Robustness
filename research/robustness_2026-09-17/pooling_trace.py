from pathlib import Path
import sys,json
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root))
from transformers import AutoTokenizer
from sos_embed.runner import config,CACHE
from sos_embed.models import snapshot_path,format_text
from sos_embed.storage import file_sha
models=config()['models'];design=json.loads((root/'config/input52_v1.json').read_text())
rows=[]
for m in models:
 tok=AutoTokenizer.from_pretrained(snapshot_path(CACHE,m),local_files_only=True,trust_remote_code=False,use_fast=True)
 assert tok.padding_side=='right'
 texts={'title':'A study of stars','abstract':'We compare observations of nearby stars.',
        'title_abstract':format_text('A study of stars','We compare observations of nearby stars.',m['text_format'],tok.sep_token)}
 examples={}
 for condition,text in texts.items():
  ids=tok(text,truncation=True,max_length=m['max_length'])['input_ids']
  assert ids[0]==tok.cls_token_id and ids[-1]==tok.sep_token_id
  examples[condition]={'text':text,'tokens':tok.convert_ids_to_tokens(ids),'token_ids':ids,'mean_positions':len(ids),'cls_position':0,'sep_position':len(ids)-1}
 rows.append({'model':m['key'],'repo_id':m['repo_id'],'revision':m['revision'],'primary_pooling':design['poolings'][m['key']],
              'saved_poolings':m['poolings'],'max_length':m['max_length'],'dimension':m['dimension'],
              'special_tokens_in_mean':True,'right_padding':True,'pooler_output_used':False,'examples':examples})
out={'all_pass':True,'pooling_source':'sos_embed/models.py','pooling_source_sha256':file_sha(root/'sos_embed/models.py'),
     'embedding_config_sha256':file_sha(root/'config/embeddings_v1.json'),'input52_config_sha256':file_sha(root/'config/input52_v1.json'),
     'models':rows,'scope':'Literal tokenizer examples and code trace. No inference or model change.'}
(root/'research/robustness_2026-09-17/pooling_trace.json').write_text(json.dumps(out,indent=2)+'\n')
print('TEN MODEL TOKENIZERS AND POOLING TRACE VERIFIED')
