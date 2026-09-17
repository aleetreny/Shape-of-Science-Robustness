"""Wait for the current finite run, then derive and audit the delivery once."""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

root=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--stability-pid',required=True,type=int);args=p.parse_args()
target=root/'data/robustness_v2/input_stability100/audit.json'
print('Waiting for the existing 100-repeat run',args.stability_pid,flush=True)
while True:
    if target.exists() and json.loads(target.read_text())['all_complete']:break
    try:os.kill(args.stability_pid,0)
    except ProcessLookupError:raise RuntimeError('Existing run ended without audit. Inspect logs; do not duplicate it.')
    time.sleep(20)
for module in ['sos_deep.input_review','sos_deep.audit_closure','sos_deep.report']:
    print('Starting',module,flush=True)
    subprocess.run([sys.executable,'-m',module],cwd=root,check=True)
print('EXPANDED NUMERICAL DELIVERY COMPLETE; DOCUMENT AND VISUAL REVIEW STILL REQUIRED',flush=True)
