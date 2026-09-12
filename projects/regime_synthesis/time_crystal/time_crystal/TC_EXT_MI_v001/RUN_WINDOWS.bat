@echo off
setlocal
cd /d "%~dp0"

if not exist "..\DTC_Data.zip" (
  echo ERROR: ..\DTC_Data.zip was not found.
  pause
  exit /b 1
)

if not exist "..\TC_CLOSURE_LOCK_v001\LOCK.json" (
  echo ERROR: ..\TC_CLOSURE_LOCK_v001 was not found.
  pause
  exit /b 1
)

python run_validate.py "..\DTC_Data.zip" "..\TC_CLOSURE_LOCK_v001" outputs
if errorlevel 1 (
  echo.
  echo TC_EXT_MI_v001 failed.
  pause
  exit /b 1
)

echo.
echo TC_EXT_MI_v001 finished.
echo See outputs\RUN_LOG.txt
pause
