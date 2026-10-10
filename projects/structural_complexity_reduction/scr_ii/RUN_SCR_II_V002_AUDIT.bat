@echo off
setlocal
cd /d "%~dp0"
echo [SCR-II v002] Running design audit only. NO v002 primary seeds are inspected.
python scripts\run_v002_audit.py
set RC=%ERRORLEVEL%
pause
exit /b %RC%
