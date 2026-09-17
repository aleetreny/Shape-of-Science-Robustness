#!/bin/sh
set -eu
TASK_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$TASK_ROOT"
exec "$TASK_ROOT/.venv-audit/bin/python" -m sos_prepare.cli "$@"
