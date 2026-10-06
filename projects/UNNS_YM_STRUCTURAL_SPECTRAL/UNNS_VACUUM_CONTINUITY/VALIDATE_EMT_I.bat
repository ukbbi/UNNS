@echo off
setlocal
cd /d "%~dp0"
py -3.12 chambers\emt_i\emt_i.py --project-root "%CD%" --validate-only
pause
