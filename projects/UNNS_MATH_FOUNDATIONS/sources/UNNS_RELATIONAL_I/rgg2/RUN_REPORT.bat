@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (py -3 run_report.py) else (python run_report.py)
set EXITCODE=%ERRORLEVEL%
echo.
if %EXITCODE% NEQ 0 (echo REPORT GENERATION FAILED) else (echo Report and example data are under output\)
pause
exit /b %EXITCODE%
