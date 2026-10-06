@echo off
setlocal
cd /d %~dp0\..\..
python scripts\ym3b\run_ym3b.py
if errorlevel 1 pause
endlocal
