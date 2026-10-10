@echo off
setlocal
set PYTHONDONTWRITEBYTECODE=1
cd /d "%~dp0"
echo [SCR-I v003] Canonical project validation and alignment check...
python scripts\validate_project_v003.py
if errorlevel 1 goto :fail
python -m unittest tests.test_v003_engine tests.test_v003_opt tests.test_v003_safe_io tests.test_upi
if errorlevel 1 goto :fail
echo.
echo SCR-I v003 validation: PASS
pause
exit /b 0
:fail
echo.
echo SCR-I v003 validation: FAIL
pause
exit /b 1
