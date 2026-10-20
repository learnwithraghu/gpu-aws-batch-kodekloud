#!/usr/bin/env bash
# Start the KodeFood Vendor Portal (Stage 1 by default).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

MODE="${MODE:-manual}"
PORT="${PORT:-8000}"
export MODE PORT

if [[ ! -d .venv ]]; then
  echo "Creating .venv …"
  python3 -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
else
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

echo "Starting KodeFood Vendor Portal (MODE=$MODE) on port $PORT …"
exec python app.py
