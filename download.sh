#!/bin/bash
set -eu
PROJECT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
cd "$PROJECT_DIR"
PYTHON_BIN="$PROJECT_DIR/.venv/bin/python"
if [ ! -x "$PYTHON_BIN" ]; then
  echo 'Falta el entorno .venv del proyecto. Pide prepararlo antes de descargar.' >&2
  exit 1
fi
if [ "${1:-start}" = 'status' ] || [ "${1:-start}" = '--help' ]; then
  exec "$PYTHON_BIN" -m sos_download.cli "$@"
fi
# Keep idle sleep away while this command runs; closing the lid can still suspend a Mac.
if [ -x /usr/bin/caffeinate ]; then
  exec /usr/bin/caffeinate -i "$PYTHON_BIN" -m sos_download.cli "$@"
fi
exec "$PYTHON_BIN" -m sos_download.cli "$@"
