@echo off
setlocal
cd /d "%~dp0" || exit /b 1
where py >nul 2>&1
if errorlevel 1 goto python_fallback
py -3 select2.py
exit /b %errorlevel%
:python_fallback
python select2.py
exit /b %errorlevel%
