@echo off
setlocal
cd /d "%~dp0"

set LOCK=..\TC_CLOSURE_LOCK_v001
set FREY=..\TC_CLOSURE_v001
set MI=..\TC_EXT_MI_v001
set CTRL=..\TC_CTRL_v001

if not exist "%LOCK%\LOCK.json" set LOCK=..\TC_CLOSURE_LOCK_v001.zip
if not exist "%FREY%\outputs\closure_result.json" set FREY=..\TC_CLOSURE_v001.zip
if not exist "%MI%\outputs\external_validation.json" set MI=..\TC_EXT_MI_v001.zip
if not exist "%CTRL%\outputs\control_validation.json" set CTRL=..\TC_CTRL_v001.zip

if not exist "%LOCK%" (
  echo ERROR: TC_CLOSURE_LOCK_v001 not found.
  pause
  exit /b 1
)
if not exist "%FREY%" (
  echo ERROR: TC_CLOSURE_v001 not found.
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

python run_rigidity.py "%LOCK%" "%FREY%" "%MI%" "%CTRL%" outputs
if errorlevel 1 (
  echo.
  echo TC_RIGIDITY_v001 failed.
  pause
  exit /b 1
)

echo.
echo TC_RIGIDITY_v001 finished.
echo See outputs\RUN_LOG.txt and outputs\rigidity_result.json
pause
