@echo off
setlocal
cd /d "%~dp0"
echo [SCR-II] Running design audit only. No primary seeds are inspected.
python scripts\run_design_audit.py
set RC=%ERRORLEVEL%
pause
exit /b %RC%
