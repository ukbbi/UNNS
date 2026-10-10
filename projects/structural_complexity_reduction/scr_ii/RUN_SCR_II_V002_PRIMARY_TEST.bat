@echo off
setlocal
cd /d "%~dp0"
echo [SCR-II v002 PRIMARY] Running non-primary regression tests...
python -m unittest tests.test_v002_primary_runner tests.test_v002_primary_freeze -v
set RC=%ERRORLEVEL%
if "%RC%"=="0" echo SCR-II v002 primary-runner regression: PASS
pause
exit /b %RC%
