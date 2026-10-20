#!/usr/bin/env bash
# Bootstrap KodeFood Vendor Portal on Amazon Linux 2023 (or Amazon Linux 2).
# Run from this directory after cloning the course repo:
#   cd lessons/00-the-real-job/vendor_portal && bash setup_ec2.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

MODE="${MODE:-manual}"
PORT="${PORT:-8000}"

echo "==> Installing Python tooling (Amazon Linux) …"
if command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y python3 python3-pip python3-devel gcc
elif command -v yum >/dev/null 2>&1; then
  sudo yum install -y python3 python3-pip python3-devel gcc
else
  echo "Neither dnf nor yum found. Install Python 3 manually, then re-run."
  exit 1
fi

echo "==> Creating virtualenv …"
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Opening TCP $PORT in the OS firewall is not enough — also allow inbound"
echo "    $PORT in the EC2 security group from your IP (or 0.0.0.0/0 for a short demo)."

echo "==> Starting portal (MODE=$MODE, PORT=$PORT) …"
export MODE PORT
exec python app.py
