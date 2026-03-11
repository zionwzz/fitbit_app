@echo off
cd /d "%~dp0"

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  set PY_CMD=py -3
) else (
  set PY_CMD=python
)

if not exist wheelhouse mkdir wheelhouse
%PY_CMD% -m pip download -r requirements.txt -d wheelhouse

echo.
echo Windows wheelhouse build finished.
echo Zip this folder and share it with Windows colleagues.
pause
