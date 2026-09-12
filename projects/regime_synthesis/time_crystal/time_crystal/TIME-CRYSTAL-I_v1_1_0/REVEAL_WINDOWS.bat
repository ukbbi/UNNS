@echo off
setlocal
cd /d "%~dp0"

set /p OUT=Blind output folder: 
set /p TRUTH=Ground truth JSON path: 

python reveal_external.py "%OUT%" "%TRUTH%"
if errorlevel 1 (
  echo Reveal failed.
  pause
  exit /b 1
)

echo.
echo See %OUT%\posthoc_comparison.json
pause
