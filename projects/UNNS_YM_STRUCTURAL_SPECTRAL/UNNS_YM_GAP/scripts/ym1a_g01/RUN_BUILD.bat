@echo off
setlocal
cd /d "%~dp0\..\.."
python scripts\ym1a_g01\build.py
if errorlevel 1 (echo. & echo G0.1 BUILD FAILED & pause & exit /b 1)
echo. & echo YM1A-G0.1 BUILD COMPLETE
pause
