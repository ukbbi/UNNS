@echo off
setlocal
cd /d "%~dp0"
py -3.12 scripts\yan19_geom_extract.py
pause
