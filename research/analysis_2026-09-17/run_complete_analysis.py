"""Finish controls once text is ready; audit only after all science jobs finish."""
import fcntl
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'data/analysis_v1'


def wait_released(directory):
    print('Waiting for',directory,flush=True)
    with (BASE/directory/'.run.lock').open('r+') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)


wait_released('controls/common_text_52k/queue')
models=json.loads((ROOT/'config/analysis_v1.json').read_text())['poolings']
for model in models:
    x=json.loads((BASE/'controls/common_text_52k'/model/'validation.json').read_text())
    if not x['complete'] or x['rows']!=52000 or x['truncated_rows']!=0:
        raise RuntimeError('Incomplete common-text input: '+model)
wait_released('neighbors')
x=json.loads((BASE/'neighbors/progress.json').read_text())
if x['state']!='requested_stages_complete' or x['requested']!='all':
    raise RuntimeError('Native neighbors are incomplete')
wait_released('robustness_controls')
subprocess.run([sys.executable,'-m','sos_analysis.compare_controls','all'],cwd=ROOT,check=True)
wait_released('shape')
x=json.loads((BASE/'shape/progress.json').read_text())
if x['state']!='requested_stages_complete' or set(x['stages'])!={'primary','global','centroids','raw','cls','sep','quality','stability'}:
    raise RuntimeError('Full shape comparison is incomplete')
subprocess.run([sys.executable,'-m','sos_analysis.report','--require-complete'],cwd=ROOT,check=True)
print('COMPLETE ANALYSIS AND FINAL NUMERICAL AUDIT',flush=True)
