@echo off
setlocal
cd /d "%~dp0"
echo [SCR-II] PRIMARY outcome-bearing run.
echo [SCR-II] Frozen primary seeds will be exposed. Do not run until setup/audit are accepted.
python scripts\run_primary.py
set RC=%ERRORLEVEL%
pause
exit /b %RC%
