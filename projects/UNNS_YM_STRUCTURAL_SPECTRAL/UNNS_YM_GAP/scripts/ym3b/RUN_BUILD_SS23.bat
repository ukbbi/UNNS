@echo off
setlocal
cd /d %~dp0\..\..
python scripts\ym3b\build_ss23_b4.py
if errorlevel 1 pause
endlocal
