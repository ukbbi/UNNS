@echo off
setlocal
cd /d "%~dp0"
echo [SCR-II v002] Running calibration only. NO v002 primary seeds are inspected.
python scripts\run_v002_calibration.py
set RC=%ERRORLEVEL%
pause
exit /b %RC%
