@echo off
setlocal
set PYTHONDONTWRITEBYTECODE=1
cd /d "%~dp0"
echo [SCR-I v003] Canonical primary runner (cached basin geometry + Windows-safe checkpoints).
python scripts\run_scr_i_a_v003.py
set RC=%ERRORLEVEL%
echo.
if "%RC%"=="0" echo SCR-I-A v003 runner finished cleanly.
if not "%RC%"=="0" echo SCR-I-A v003 exited with code %RC%.
pause
exit /b %RC%
