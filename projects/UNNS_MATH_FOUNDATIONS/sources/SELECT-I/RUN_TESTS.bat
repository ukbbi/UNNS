@echo off
setlocal
cd /d "%~dp0" || exit /b 1
where py >nul 2>&1
if errorlevel 1 goto python_fallback
py -3 select1.py
exit /b %errorlevel%
:python_fallback
python select1.py
exit /b %errorlevel%
