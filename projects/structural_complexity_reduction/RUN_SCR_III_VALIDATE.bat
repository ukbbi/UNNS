@echo off
setlocal
cd /d "%~dp0"
python -m scr_iii.scripts.validate_engine
set RC=%ERRORLEVEL%
if not "%RC%"=="0" pause
exit /b %RC%
