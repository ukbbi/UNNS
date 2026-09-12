@echo off
setlocal
cd /d "%~dp0"
python VERIFY_FREEZE.py
if errorlevel 1 (
  echo.
  echo FREEZE VERIFICATION FAILED.
  exit /b 1
)
echo.
pause
