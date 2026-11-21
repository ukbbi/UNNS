@echo off
cd /d "%~dp0"
python scripts\run_sib.py
if errorlevel 1 goto end
python scripts\verify_sib.py
:end
pause
