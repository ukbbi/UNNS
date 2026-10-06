@echo off
setlocal
cd /d "%~dp0\..\.."
python scripts\at20\extract.py
if errorlevel 1 (
  echo.
  echo EXTRACTION FAILED
  pause
  exit /b 1
)
echo.
echo EXTRACTION COMPLETE
pause
