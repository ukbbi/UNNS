@echo off
setlocal
cd /d "%~dp0"
python -m scr_iii.scripts.run_nulls_v002
set RC=%ERRORLEVEL%
echo.
echo Exit code: %RC%
pause
exit /b %RC%
