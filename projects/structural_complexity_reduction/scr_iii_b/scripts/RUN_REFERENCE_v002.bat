@echo off
setlocal
cd /d "%~dp0"
python ..\reference_check\validate_v002.py
if errorlevel 1 (
 echo Preflight reference check failed.
 exit /b 1
)
echo V002 reference-formula preflight complete.
