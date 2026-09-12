@echo off
setlocal
cd /d "%~dp0"
python -m pip install --upgrade -r requirements.txt
if errorlevel 1 (
  echo.
  echo SETUP FAILED.
  exit /b 1
)
echo.
echo SETUP COMPLETE.
endlocal
