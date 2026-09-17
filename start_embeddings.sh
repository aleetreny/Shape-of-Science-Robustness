#!/bin/bash
set -euo pipefail
EMBED_LAUNCH_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$EMBED_LAUNCH_ROOT"
mkdir -p data
# Keep terminal output and errors, preserving the calculation's exit status.
caffeinate -i ./embed.sh run --scope full 2>&1 | tee -a data/embeddings_run.log
