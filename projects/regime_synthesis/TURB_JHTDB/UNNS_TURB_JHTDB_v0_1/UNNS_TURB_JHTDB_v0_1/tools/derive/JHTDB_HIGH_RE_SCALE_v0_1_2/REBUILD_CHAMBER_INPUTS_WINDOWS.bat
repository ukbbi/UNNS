@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 REBUILD_CHAMBER_INPUTS.py
) else (
  python REBUILD_CHAMBER_INPUTS.py
)

set RC=%errorlevel%
echo.
if %RC%==0 (
  echo [PASS] Deterministic chamber-input rebuild completed.
) else (
  echo [FAIL] Chamber-input rebuild failed with exit code %RC%.
)
pause
exit /b %RC%
