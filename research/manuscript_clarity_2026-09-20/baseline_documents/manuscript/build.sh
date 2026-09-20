#!/bin/sh
# Compile only; never run scientific calculations or rebuild source data.
set -eu
MANUSCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_DIR=$(dirname "$MANUSCRIPT_DIR")
OUTPUT_DIR="$PROJECT_DIR/output/pdf"
LOCAL_TECTONIC="$PROJECT_DIR/data/manuscript_layout_v1/toolchain/tectonic"
mkdir -p "$OUTPUT_DIR"
if [ -x "$LOCAL_TECTONIC" ]; then
  LATEX_COMPILER="$LOCAL_TECTONIC"
elif command -v tectonic >/dev/null 2>&1; then
  LATEX_COMPILER=$(command -v tectonic)
else
  printf '%s\n' 'Tectonic is required. Install it, or upload this manuscript folder to Overleaf and choose main.tex / supplement.tex.' >&2
  exit 1
fi
export SOURCE_DATE_EPOCH=1789732800
cd "$MANUSCRIPT_DIR"
"$LATEX_COMPILER" --keep-logs --outdir "$OUTPUT_DIR" main.tex
"$LATEX_COMPILER" --keep-logs --outdir "$OUTPUT_DIR" supplement.tex
printf '%s\n' "PDFs ready in $OUTPUT_DIR"
