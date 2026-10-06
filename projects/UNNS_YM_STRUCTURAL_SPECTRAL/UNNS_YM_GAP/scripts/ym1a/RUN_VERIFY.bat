@echo off
setlocal
cd /d "%~dp0\..\.."
python scripts\ym1a\verify.py
if errorlevel 1 (echo. & echo VERIFY FAILED & pause & exit /b 1)
echo. & echo YM1A VERIFY PASSED
pause
