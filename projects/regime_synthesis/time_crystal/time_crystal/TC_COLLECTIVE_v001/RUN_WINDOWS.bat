@echo off
setlocal
cd /d "%~dp0"

set DATA=..\DTC_Data.zip
set LOCK=..\TC_CLOSURE_LOCK_v001
set MI=..\TC_EXT_MI_v001
set CTRL=..\TC_CTRL_v001

if not exist "%LOCK%\LOCK.json" set LOCK=..\TC_CLOSURE_LOCK_v001.zip
if not exist "%MI%\outputs\external_validation.json" set MI=..\TC_EXT_MI_v001.zip
if not exist "%CTRL%\outputs\control_validation.json" set CTRL=..\TC_CTRL_v001.zip

if not exist "%DATA%" (
  echo ERROR: DTC_Data.zip not found.
  pause
  exit /b 1
)
if not exist "%LOCK%" (
  echo ERROR: TC_CLOSURE_LOCK_v001 not found.
  pause
  exit /b 1
)
if not exist "%MI%" (
  echo ERROR: TC_EXT_MI_v001 not found.
  pause
  exit /b 1
)
if not exist "%CTRL%" (
  echo ERROR: TC_CTRL_v001 not found.
  pause
  exit /b 1
)

python run_collective.py "%DATA%" "%LOCK%" "%MI%" "%CTRL%" outputs
if errorlevel 1 (
  echo.
  echo TC_COLLECTIVE_v001 failed.
  pause
  exit /b 1
)

echo.
echo TC_COLLECTIVE_v001 finished.
echo See outputs\RUN_LOG.txt and outputs\collective_result.json
pause
