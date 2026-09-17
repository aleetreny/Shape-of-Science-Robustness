from pathlib import Path
import json,sys,subprocess,hashlib
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root))
assert json.loads((root/'research/checklist_2026-09-17/input_preflight.json').read_text())['all_models_pass']
subprocess.run([sys.executable,'-m','sos_followup.input_embeddings','model','--model','minilm','--max-shards','1'],cwd=root,check=True)
first=next((root/'data/checklist_v1/inputs/title_abstract/minilm/shards').glob('[0-9]*'))
checkpoint={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in first.iterdir()}
(root/'research/checklist_2026-09-17/resume_checkpoint.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
subprocess.run([sys.executable,'-m','sos_followup.input_embeddings','all'],cwd=root,check=True)
for name,digest in checkpoint.items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
print('INPUT QUEUE COMPLETE; ORIGINAL CHECKPOINT UNCHANGED',flush=True)
