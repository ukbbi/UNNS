@echo off
setlocal
cd /d "%~dp0.."
py -3 scripts\run_preflight.py
if errorlevel 1 python scripts\run_preflight.py
pause
