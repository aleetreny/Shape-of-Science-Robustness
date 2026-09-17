from pathlib import Path
import json,subprocess,sys,hashlib
root=Path(__file__).resolve().parents[2]
assert json.loads((root/'research/robustness_2026-09-17/input52_preflight.json').read_text())['all_pass']
assert json.loads((root/'research/checklist_2026-09-17/input_preflight.json').read_text())['all_models_pass']
checkpoint=json.loads((root/'research/robustness_2026-09-17/input52_resume_checkpoint.json').read_text())
def verify_checkpoint():
 for name,digest in checkpoint.items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
verify_checkpoint()
subprocess.run([sys.executable,'-m','sos_deep.inputs52','model','--model','minilm','--condition','title','--max-shards','1'],cwd=root,check=True)
verify_checkpoint()
print('REAL 52K RESUME VERIFIED; FIRST BLOCK UNCHANGED',flush=True)
subprocess.run([sys.executable,'-m','sos_deep.inputs52','all'],cwd=root,check=True)
verify_checkpoint()
print('52K INPUT QUEUE COMPLETE; CHECKPOINT UNCHANGED',flush=True)
subprocess.run([sys.executable,'-m','sos_deep.audit_inputs52','--require-complete'],cwd=root,check=True)
print('52K INPUTS FINISHED AND AUDITED',flush=True)
