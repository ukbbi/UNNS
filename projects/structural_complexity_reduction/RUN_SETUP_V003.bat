@echo off
setlocal
set PYTHONDONTWRITEBYTECODE=1
cd /d "%~dp0"
echo [SCR-I v003] Checking Python...
python --version || goto :fail
echo [SCR-I v003] Installing/verifying source lock, preregistration and design-preservation audit...
python scripts\setup_scr_i_v003.py
if errorlevel 1 goto :fail
echo.
echo SCR-I v003 setup completed. Refresh the dashboard.
pause
exit /b 0
:fail
echo.
echo SCR-I v003 setup FAILED.
pause
exit /b 1
