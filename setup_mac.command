#!/bin/bash
cd "$(dirname "$0")"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD=python
else
  echo "Python 3 was not found. Please install Python 3.11 or 3.12 first."
  exit 1
fi

"$PYTHON_CMD" -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

if [ -d wheelhouse ]; then
  python -m pip install --no-index --find-links wheelhouse -r requirements.txt
else
  python -m pip install -r requirements.txt
fi

echo
echo "Setup complete."
echo "Double-click run_mac.command to launch the app."
