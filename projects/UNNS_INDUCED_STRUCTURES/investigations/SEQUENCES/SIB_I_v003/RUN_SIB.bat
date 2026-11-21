@echo off
cd /d "%~dp0"
py -3 scripts\run_sib.py
if errorlevel 1 goto end
py -3 scripts\verify_sib.py
:end
pause
