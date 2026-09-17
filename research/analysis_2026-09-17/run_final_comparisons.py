"""Wait for the active prerequisites, verify completion, then compare controls."""
import fcntl
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "data/analysis_v1"


def released(folder):
    path = folder / ".run.lock"
    if not path.exists():
        raise RuntimeError(f"Expected an already started prerequisite: {folder}")
    with path.open("r+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)


for directory in ("shape", "neighbors", "controls/common_text_52k/queue"):
    print("Waiting for", directory, flush=True)
    released(BASE / directory)

shape = json.loads((BASE / "shape/progress.json").read_text())
expected = {"primary", "raw", "cls", "sep", "quality", "stability", "global", "centroids"}
if shape["state"] != "requested_stages_complete" or set(shape["stages"]) != expected:
    raise RuntimeError("The full shape comparison has not completed")
neighbors = json.loads((BASE / "neighbors/progress.json").read_text())
if neighbors["state"] != "requested_stages_complete" or neighbors["requested"] != "all":
    raise RuntimeError("The full neighbor comparison has not completed")
models = json.loads((ROOT / "config/analysis_v1.json").read_text())["poolings"]
for model in models:
    result = json.loads((BASE / "controls/common_text_52k" / model / "validation.json").read_text())
    if not result["complete"] or result["rows"] != 52000 or result["truncated_rows"] != 0:
        raise RuntimeError(f"Incomplete common text control: {model}")
extended = json.loads((BASE / "controls/minilm_512/minilm/validation.json").read_text())
if not extended["complete"] or extended["rows"] != 500000:
    raise RuntimeError("The MiniLM 512 control is incomplete")

subprocess.run([sys.executable, "-m", "sos_analysis.compare_controls", "all"], cwd=ROOT, check=True)
print("ALL ROBUSTNESS COMPARISONS COMPLETE", flush=True)
