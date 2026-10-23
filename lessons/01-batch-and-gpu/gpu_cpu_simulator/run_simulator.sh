#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-8080}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Starting KodeFood GPU vs CPU Interactive Simulator on http://127.0.0.1:${PORT}"
echo "Press Ctrl+C to stop."
cd "${DIR}"
python3 -m http.server "${PORT}"
