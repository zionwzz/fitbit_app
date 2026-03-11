@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo Virtual environment not found.
  echo Please run setup_windows.bat first.
  pause
  exit /b 1
)

set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
".venv\Scripts\python.exe" -m streamlit run app.py --server.address localhost --server.port 8501 --browser.gatherUsageStats false
