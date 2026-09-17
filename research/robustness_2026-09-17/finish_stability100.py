import json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
audit=ROOT/'data/robustness_v2/input_recipes/audit.json'
print('Waiting for input primary and recipe comparisons, PID 93472',flush=True)
while not audit.exists():
    try:os.kill(93472,0)
    except ProcessLookupError:raise SystemExit('Input comparison driver stopped without recipe audit; inspect before restarting')
    time.sleep(20)
assert json.loads(audit.read_text())['all_complete']
subprocess.run([sys.executable,'-m','sos_deep.input_stability100'],cwd=ROOT,check=True)
print('INPUT 100-REPEAT FINISHER COMPLETE',flush=True)
