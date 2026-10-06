@echo off
setlocal
cd /d "%~dp0\..\.."
python scripts\ym1a_g0\verify.py
if errorlevel 1 (echo. & echo G0 VERIFY FAILED & pause & exit /b 1)
echo. & echo YM1A-G0 VERIFY PASSED
pause
