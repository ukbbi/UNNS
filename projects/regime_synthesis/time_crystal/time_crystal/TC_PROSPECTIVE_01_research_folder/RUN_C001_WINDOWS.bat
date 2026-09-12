@echo off
setlocal
cd /d "%~dp0"

set ARCHIVE=..\4T-DTC_upload.tar
set CHAMBER=..\TIME-CRYSTAL-I_v1_1_0

if not exist "%ARCHIVE%" (
  echo ERROR: %ARCHIVE% not found.
  pause
  exit /b 1
)

if not exist "%CHAMBER%\run_external.py" (
  echo ERROR: %CHAMBER% not found.
  pause
  exit /b 1
)

echo Rebuilding neutral candidate and no-recompilation control...
python tools\build_4t_candidate.py "%ARCHIVE%" .
if errorlevel 1 (
  echo Adapter failed.
  pause
  exit /b 1
)

echo.
echo Running blind primary candidate...
python "%CHAMBER%\run_external.py" candidates\TC_P01_C001.zip locked_runs\C001 --blind
if errorlevel 1 (
  echo Primary blind run failed.
  pause
  exit /b 1
)

echo.
echo Running blind no-recompilation control...
python "%CHAMBER%\run_external.py" candidates\TC_P01_NRCTRL.zip locked_runs\NRCTRL --blind
if errorlevel 1 (
  echo Control blind run failed.
  pause
  exit /b 1
)

echo.
echo TC_P01_C001 blind stage complete.
echo Primary: locked_runs\C001\blind_verdict.json
echo Control: locked_runs\NRCTRL\blind_verdict.json
echo DO NOT reveal ground truth until the locked results have been inspected.
pause
