"""Wait on the active MiniLM output lock, then run the common-text queue."""
import fcntl
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
folder = ROOT / "data/analysis_v1/controls/minilm_512/minilm"
with (folder / ".run.lock").open("a+") as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)
    status = json.loads((folder / "validation.json").read_text())
    if not status["complete"] or status["rows"] != 500000:
        raise RuntimeError("MiniLM stopped before completion; do not silently continue")
subprocess.run([sys.executable, "-m", "sos_analysis.extra_embeddings", "common-all"],
               cwd=ROOT, check=True)
print("CONTROLES DE TEXTO COMPLETOS", flush=True)
