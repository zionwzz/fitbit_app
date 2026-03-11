#!/bin/bash
cd "$(dirname "$0")"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD=python
else
  echo "Python 3 was not found."
  exit 1
fi

mkdir -p wheelhouse
"$PYTHON_CMD" -m pip download -r requirements.txt -d wheelhouse

echo
echo "macOS wheelhouse build finished."
echo "Zip this folder and share it with Mac colleagues."
