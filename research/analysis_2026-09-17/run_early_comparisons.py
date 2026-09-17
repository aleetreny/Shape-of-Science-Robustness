"""Overlap bounded controls with remaining shape stability; no source edits."""
import fcntl
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
subprocess.run([sys.executable,'-m','sos_analysis.compare_controls','pooling'],cwd=ROOT,check=True)
folder=ROOT/'data/analysis_v1/neighbors'
with (folder/'.run.lock').open('r+') as lock:
    fcntl.flock(lock,fcntl.LOCK_EX)
    state=json.loads((folder/'progress.json').read_text())
    if state['state']!='requested_stages_complete' or state['requested']!='all':
        raise RuntimeError('Native neighbor computation ended before completion')
subprocess.run([sys.executable,'-m','sos_analysis.compare_controls','minilm'],cwd=ROOT,check=True)
print('EARLY CONTROLS COMPLETE',flush=True)
