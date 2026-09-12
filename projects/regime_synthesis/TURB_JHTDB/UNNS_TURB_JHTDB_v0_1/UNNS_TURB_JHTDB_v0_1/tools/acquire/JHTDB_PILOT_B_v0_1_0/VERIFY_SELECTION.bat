@echo off
setlocal
cd /d "%~dp0"
python acquire_pilot_b.py --dry-run
set RC=%ERRORLEVEL%
endlocal & exit /b %RC%
