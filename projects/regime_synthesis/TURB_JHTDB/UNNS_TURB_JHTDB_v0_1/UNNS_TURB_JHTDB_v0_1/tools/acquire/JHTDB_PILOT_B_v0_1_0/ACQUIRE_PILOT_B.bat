@echo off
setlocal
if "%JHTDB_TOKEN%"=="" (
  echo.
  echo JHTDB_TOKEN is not set in this Command Prompt.
  echo Set your registered JHTDB token for this session, then run this file again.
  echo Do not save the token inside the project.
  echo.
  exit /b 2
)
cd /d "%~dp0"
python acquire_pilot_b.py %*
set RC=%ERRORLEVEL%
endlocal & exit /b %RC%
