@echo off
setlocal
cd /d "%~dp0"
python scripts\summarize_v002_primary.py
set RC=%ERRORLEVEL%
pause
exit /b %RC%
