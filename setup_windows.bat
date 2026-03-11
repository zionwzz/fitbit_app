@echo off
cd /d "%~dp0"

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  set PY_CMD=py -3
) else (
  where python >nul 2>nul
  if not %ERRORLEVEL%==0 (
    echo Python 3 was not found.
    echo Please install Python 3.11 or 3.12 first.
    pause
    exit /b 1
  )
  set PY_CMD=python
)

%PY_CMD% -m venv .venv
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip

if exist wheelhouse (
  python -m pip install --no-index --find-links=wheelhouse -r requirements.txt
) else (
  python -m pip install -r requirements.txt
)

echo.
echo Setup complete.
echo Double-click run_windows.bat to launch the app.
pause
