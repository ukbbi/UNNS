@echo off
setlocal
cd /d "%~dp0"
echo [SCR-II] Validating engine and frozen preregistration...
python scripts\validate_engine.py
set RC=%ERRORLEVEL%
if not "%RC%"=="0" echo SCR-II validation FAILED with code %RC%.
if "%RC%"=="0" echo SCR-II engine validation: PASS
pause
exit /b %RC%
