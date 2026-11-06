@echo off
REM GIG-I v002 Windows runner.  Usage:  RUN_V002.bat [test|quick|full]
setlocal
cd /d "%~dp0"
set MODE=%1
if "%MODE%"=="" set MODE=test
if /I "%MODE%"=="test"  python -m unittest discover -s TESTS -v
if /I "%MODE%"=="quick" (cd EXPERIMENTS & python run_all.py --quick)
if /I "%MODE%"=="full"  (cd EXPERIMENTS & python run_all.py)
endlocal
