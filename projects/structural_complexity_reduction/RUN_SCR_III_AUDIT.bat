@echo off
setlocal
cd /d "%~dp0"
python -m scr_iii.scripts.run_audit
set RC=%ERRORLEVEL%
if not "%RC%"=="0" pause
exit /b %RC%
