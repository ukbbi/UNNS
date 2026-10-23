@echo off
setlocal
cd /d "%~dp0"
python -m unittest discover -s tests -p "test_*.py" -v
if errorlevel 1 exit /b 1
python -m src.xvi_proto_measure_2b_v001
exit /b %errorlevel%
