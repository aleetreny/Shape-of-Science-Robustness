"""Finish the already-authorized recipe sensitivity after its paired parent."""
import json
import subprocess
import time
from pathlib import Path

root=Path(__file__).resolve().parents[2]
parent=root/'data/checklist_v1/input_comparisons/audit.json'
print('Waiting for the audited primary input comparison',flush=True)
while not parent.exists():time.sleep(20)
assert json.loads(parent.read_text())['all_complete']
subprocess.run([str(root/'.venv-analysis/bin/python'),'-m','sos_followup.input_recipe_control'],cwd=root,check=True)
print('INPUT RECIPE SENSITIVITY FINISHED',flush=True)
