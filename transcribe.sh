#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"

if [[ ! -x "$VENV_PYTHON" ]]; then
  echo "Virtualenv not found at $SCRIPT_DIR/.venv" >&2
  echo "Run: python3 -m venv \"$SCRIPT_DIR/.venv\"" >&2
  echo "Then: \"$SCRIPT_DIR/.venv/bin/pip\" install -r \"$SCRIPT_DIR/requirements.txt\"" >&2
  exit 1
fi

exec "$VENV_PYTHON" "$SCRIPT_DIR/transcribe_audio.py" "$@"
