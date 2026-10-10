@echo off
setlocal
cd /d "%~dp0"
python -m scr_iii.scripts.validate_engine_v002
set RC=%ERRORLEVEL%
echo.
echo Exit code: %RC%
pause
exit /b %RC%
