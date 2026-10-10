@echo off
setlocal
cd /d "%~dp0\.."
python scripts\validate_prereg.py
set RC=%ERRORLEVEL%
echo.
pause
exit /b %RC%
