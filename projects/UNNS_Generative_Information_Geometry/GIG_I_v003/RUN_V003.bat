@echo off
REM GIG-I v003 Windows runner.  Usage:  RUN_V003.bat [test|quick|full]
REM   test  : unit tests (v001/v002 frozen-regression included).  Set GIG_FROZEN_SRC=<...\GEO_HD_1D_v004\src> for the frozen cross-check.
REM   quick : reduced experiments (minutes)       full : complete experiments (about one hour on 2 CPUs)
setlocal
cd /d "%~dp0"
set MODE=%1
if "%MODE%"=="" set MODE=test
if /I "%MODE%"=="test"  python -m unittest discover -s TESTS -v
if /I "%MODE%"=="quick" (cd EXPERIMENTS & python run_all.py --quick)
if /I "%MODE%"=="full"  (cd EXPERIMENTS & python run_all.py)
endlocal
