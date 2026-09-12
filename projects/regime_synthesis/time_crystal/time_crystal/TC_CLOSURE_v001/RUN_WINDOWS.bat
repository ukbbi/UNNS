@echo off
setlocal
cd /d "%~dp0"

if not exist "..\Data.zip" (
  echo ERROR: ..\Data.zip was not found.
  echo TC_CLOSURE_v001 must sit beside Data.zip in the Time_crystal folder.
  pause
  exit /b 1
)

if not exist "..\TC_PHYS_v001\outputs\physics_validation.json" (
  echo ERROR: frozen TC_PHYS_v001 physics validation was not found.
  pause
  exit /b 1
)

python run_closure.py "..\Data.zip" "..\TC_PHYS_v001" outputs
if errorlevel 1 (
  echo.
  echo TC_CLOSURE_v001 failed.
  pause
  exit /b 1
)

echo.
echo TC_CLOSURE_v001 finished.
echo See outputs\RUN_LOG.txt and outputs\closure_result.json
pause
