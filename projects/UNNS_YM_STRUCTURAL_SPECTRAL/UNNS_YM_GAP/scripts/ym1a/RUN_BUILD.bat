@echo off
setlocal
cd /d "%~dp0\..\.."
python scripts\ym1a\build.py
if errorlevel 1 (echo. & echo BUILD FAILED & pause & exit /b 1)
echo. & echo YM1A BUILD COMPLETE
pause
