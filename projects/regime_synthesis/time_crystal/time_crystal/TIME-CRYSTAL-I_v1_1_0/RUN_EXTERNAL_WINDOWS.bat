@echo off
setlocal
cd /d "%~dp0"

set CAND=%~1
if "%CAND%"=="" (
  echo Drag a candidate ZIP/folder onto this BAT, or enter its path below.
  set /p CAND=Candidate bundle path: 
)

if "%CAND%"=="" exit /b 1

set NAME=%~n1
if "%NAME%"=="" set NAME=candidate
set OUT=external_outputs\%NAME%

python -c "import numpy" >nul 2>&1
if errorlevel 1 (
  echo NumPy is required for External Analysis Mode.
  echo Run: python -m pip install numpy
  pause
  exit /b 1
)

python run_external.py "%CAND%" "%OUT%" --blind
if errorlevel 1 (
  echo.
  echo External analysis failed.
  pause
  exit /b 1
)

echo.
echo Blind analysis complete.
echo Output: %OUT%
echo You may load %OUT%\blind_verdict.json in TIME-CRYSTAL-I.html
pause
