@echo off
setlocal
cd /d "%~dp0\.."
python scripts\validate_prereg.py
set RC=%ERRORLEVEL%
if not "%RC%"=="0" pause
exit /b %RC%
