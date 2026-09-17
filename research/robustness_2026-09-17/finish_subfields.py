"""Continue only after the already active native run has succeeded."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--native-pid',type=int,required=True);args=p.parse_args()
audit=ROOT/'data/robustness_v2/subfields_native/audit.json'
while not audit.exists():
    try:os.kill(args.native_pid,0)
    except ProcessLookupError:raise SystemExit('Native Subfield process stopped without a completed audit; inspect, do not restart blindly')
    time.sleep(20)
assert json.loads(audit.read_text())['all_complete']
subprocess.run([sys.executable,'-m','sos_deep.subfield_controls'],cwd=ROOT,check=True)
print('SUBFIELD FOLLOW-UP COMPLETE',flush=True)
