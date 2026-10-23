@echo off
setlocal
cd /d "%~dp0"
py -3 -m pip install -r requirements.txt || exit /b 1
py -3 -m unittest discover -s tests -v || exit /b 1
py -3 src\q_window.py --output output || exit /b 1
pause
