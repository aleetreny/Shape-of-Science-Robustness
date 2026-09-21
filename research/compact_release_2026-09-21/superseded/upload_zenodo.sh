#!/bin/sh
# Upload only the prepared release. Keep the Mac awake until the command exits.
set -eu
UPLOAD_PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ -x "$UPLOAD_PROJECT_DIR/.venv-analysis/bin/python" ]; then
    UPLOAD_PYTHON="$UPLOAD_PROJECT_DIR/.venv-analysis/bin/python"
else
    UPLOAD_PYTHON=$(command -v python3 || true)
fi
if [ -z "$UPLOAD_PYTHON" ]; then
    printf '%s\n' 'Hace falta Python 3.9 o posterior.' >&2
    exit 1
fi
if [ -x /usr/bin/caffeinate ]; then
    exec /usr/bin/caffeinate -i "$UPLOAD_PYTHON" "$UPLOAD_PROJECT_DIR/scripts/zenodo_upload.py" "$@"
fi
exec "$UPLOAD_PYTHON" "$UPLOAD_PROJECT_DIR/scripts/zenodo_upload.py" "$@"
