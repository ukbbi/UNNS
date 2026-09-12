@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo JHTDB PILOT B - PROTOCOL FREEZE
echo.
echo This must be run before Pilot-B analysis.
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0LOCK_PROTOCOL.ps1"
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PROTOCOL FREEZE COMPLETE.
) else (
  echo PROTOCOL FREEZE FAILED.
  echo Do not begin Pilot-B analysis until the missing frozen target is resolved.
)
pause
exit /b %RC%
