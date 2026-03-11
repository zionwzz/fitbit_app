#!/bin/bash
cd "$(dirname "$0")"

if [ ! -x ".venv/bin/python" ]; then
  echo "Virtual environment not found."
  echo "Please run setup_mac.command first."
  exit 1
fi

export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
".venv/bin/python" -m streamlit run app.py --server.address localhost --server.port 8501 --browser.gatherUsageStats false
