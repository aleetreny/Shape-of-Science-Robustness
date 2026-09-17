import json,time,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2]
models=[m['key'] for m in json.loads((root/'config/embeddings_v1.json').read_text())['models']]
last=-1
while True:
    complete=0
    for m in models:
        for c in ['title','abstract','title_abstract']:
            p=root/'data/checklist_v1/inputs'/c/m/'validation.json'
            if p.exists() and json.loads(p.read_text()).get('complete'):complete+=1
    if complete!=last:print('Condiciones completas',complete,'/30',flush=True);last=complete
    if complete==30:break
    time.sleep(20)
embed=root/'.venv-embed/bin/python';analysis=root/'.venv-analysis/bin/python'
subprocess.run([str(embed),'-m','sos_followup.audit_inputs','--require-complete'],cwd=root,check=True)
subprocess.run([str(analysis),'-m','sos_followup.input_analysis'],cwd=root,check=True)
print('PILOT FINISHED AND AUDITED',flush=True)
