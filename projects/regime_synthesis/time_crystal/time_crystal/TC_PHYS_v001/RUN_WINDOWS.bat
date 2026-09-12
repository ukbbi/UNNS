@echo off
setlocal
cd /d "%~dp0"

if not exist "Data.zip" (
  echo Data.zip was not found beside this package.
  echo Copy the original Data.zip here and run again.
  pause
  exit /b 1
)

python run_phys.py Data.zip outputs
if errorlevel 1 (
  echo.
  echo TC_PHYS_v001 failed.
  pause
  exit /b 1
)

echo.
echo TC_PHYS_v001 finished.
echo See outputs\physics_validation.json and outputs\RUN_LOG.txt
pause
