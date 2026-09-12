@echo off
setlocal
cd /d "%~dp0"

set CHAMBER=..\TIME-CRYSTAL-I_v1_1_0
set CAND_SRC=candidates\C002_sim_recon\time_evolution_L_14_N=300_Jt=0.07_eps=3.1416.csv
set CTRL_SRC=candidates\C002_sim_recon\time_evolution_L_14_N=300_Jt=0.07_eps=0.0000.csv

if not exist "%CHAMBER%\run_external.py" (
  echo ERROR: TIME-CRYSTAL-I_v1_1_0 not found beside the campaign folder.
  pause
  exit /b 1
)

if not exist "%CAND_SRC%" (
  echo ERROR: Candidate source missing:
  echo %CAND_SRC%
  pause
  exit /b 1
)

if not exist "%CTRL_SRC%" (
  echo ERROR: Control source missing:
  echo %CTRL_SRC%
  pause
  exit /b 1
)

python -c "import numpy, pandas" >nul 2>&1
if errorlevel 1 (
  echo ERROR: NumPy and pandas are required.
  echo Run: python -m pip install numpy pandas
  pause
  exit /b 1
)

echo Rebuilding neutral C002 candidate and matched control...
python tools\build_c002_candidate.py "%CAND_SRC%" "%CTRL_SRC%" .
if errorlevel 1 (
  echo C002 adapter failed.
  pause
  exit /b 1
)

echo.
echo Running blind C002 candidate...
python "%CHAMBER%\run_external.py" candidates\TC_P01_C002.zip locked_runs\C002 --blind
if errorlevel 1 (
  echo C002 blind run failed.
  pause
  exit /b 1
)

echo.
echo Running blind C002 matched control...
python "%CHAMBER%\run_external.py" candidates\TC_P01_C002_CTRL.zip locked_runs\C002_CTRL --blind
if errorlevel 1 (
  echo C002 control blind run failed.
  pause
  exit /b 1
)

echo.
echo TC_P01_C002 blind stage complete.
echo Candidate: locked_runs\C002\blind_verdict.json
echo Control:   locked_runs\C002_CTRL\blind_verdict.json
echo.
echo DO NOT reveal ground truth until both locked results have been inspected.
pause
