@echo off
setlocal
cd /d "%~dp0"
py -3.12 chambers\emt_geom\emt_geom.py --project-root "%CD%" --validate-only
pause
