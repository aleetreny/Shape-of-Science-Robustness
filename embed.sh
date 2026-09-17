#!/bin/sh
set -eu
EMBED_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$EMBED_ROOT"
if [ ! -x "$EMBED_ROOT/.venv-embed/bin/python" ]; then
    echo 'Falta el entorno .venv-embed. Consulte EMBEDDINGS.md.' >&2
    exit 1
fi
export HF_HUB_DISABLE_IMPLICIT_TOKEN=1
export TOKENIZERS_PARALLELISM=false
exec "$EMBED_ROOT/.venv-embed/bin/python" -m sos_embed.cli "$@"
