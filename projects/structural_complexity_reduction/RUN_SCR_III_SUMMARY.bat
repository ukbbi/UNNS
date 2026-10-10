@echo off
setlocal
cd /d "%~dp0"
python -m scr_iii.scripts.summarize_primary
set RC=%ERRORLEVEL%
if not "%RC%"=="0" pause
exit /b %RC%
