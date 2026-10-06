@echo off
setlocal
cd /d "%~dp0\..\.."
python scripts\at20\verify.py
if errorlevel 1 (
  echo.
  echo VERIFY FAILED
  pause
  exit /b 1
)
echo.
echo VERIFY PASSED
pause
