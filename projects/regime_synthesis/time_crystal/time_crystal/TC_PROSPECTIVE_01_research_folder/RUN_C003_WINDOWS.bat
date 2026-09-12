@echo off
setlocal
cd /d "%~dp0"

set CHAMBER=..\TIME-CRYSTAL-I_v1_1_0
set SRC=candidates\C003_source\rawdata.xls

if not exist "%CHAMBER%\run_external.py" (
  echo ERROR: TIME-CRYSTAL-I_v1_1_0 not found beside the campaign folder.
  pause
  exit /b 1
)

if not exist "%SRC%" (
  echo ERROR: C003 source workbook missing:
  echo %SRC%
  pause
  exit /b 1
)

echo Rebuilding neutral C003 candidate and matched control...
python tools\build_c003_candidate.py "%SRC%" .
if errorlevel 1 (
  echo C003 adapter failed.
  pause
  exit /b 1
)

echo.
echo Running blind C003 candidate...
python "%CHAMBER%\run_external.py" candidates\TC_P01_C003.zip locked_runs\C003 --blind
if errorlevel 1 (
  echo C003 blind run failed.
  pause
  exit /b 1
)

echo.
echo Running blind C003 matched control...
python "%CHAMBER%\run_external.py" candidates\TC_P01_C003_CTRL.zip locked_runs\C003_CTRL --blind
if errorlevel 1 (
  echo C003 control blind run failed.
  pause
  exit /b 1
)

echo.
echo TC_P01_C003 blind stage complete.
echo Candidate: locked_runs\C003\blind_verdict.json
echo Control:   locked_runs\C003_CTRL\blind_verdict.json
echo.
echo DO NOT reveal ground truth until both locked results have been inspected.
pause
