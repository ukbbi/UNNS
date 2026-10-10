@echo off
setlocal
cd /d "%~dp0"
echo [SCR-II] Running calibration only. No primary seeds are inspected.
python scripts\run_calibration.py
set RC=%ERRORLEVEL%
pause
exit /b %RC%
