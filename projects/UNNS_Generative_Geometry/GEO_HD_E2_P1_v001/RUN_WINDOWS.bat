@echo off
setlocal
cd /d "%~dp0"
set PY=python
where python >nul 2>nul || set PY=py -3
%PY% RUN_VERIFY.py
if errorlevel 1 (echo EXACT_FAIL & exit /b 1)
%PY% -m unittest discover -s tests
%PY% -c "import matplotlib" >nul 2>nul && %PY% src\make_figures.py
pause
