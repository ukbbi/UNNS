@echo off
setlocal
cd /d "%~dp0"
echo [SCR-II v002] Validating frozen multiplicity benchmark prep...
python scripts\validate_v002_prep.py
set RC=%ERRORLEVEL%
if "%RC%"=="0" echo SCR-II v002 prep validation: PASS
pause
exit /b %RC%
