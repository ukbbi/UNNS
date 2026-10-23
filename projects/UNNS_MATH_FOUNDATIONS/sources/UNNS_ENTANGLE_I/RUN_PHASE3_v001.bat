@echo off
cd /d "%~dp0"
python -m unittest discover -s tests -p "test_*.py" -v
if errorlevel 1 exit /b 1
python -m src.measure_rep_phase3_v001
