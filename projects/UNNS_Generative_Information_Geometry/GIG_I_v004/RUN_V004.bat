@echo off
REM GIG-I v004 runner.  Usage:  RUN_V004.bat [test|quick|full|graph]
REM   test : unit tests (frozen hash checks included)   quick : minutes   full : about an hour on 2 CPUs
REM   graph: long optional job, graph-only reconstruction of one k=7 beta_3 regime (E17), e.g.  RUN_V004.bat graph H3-4
setlocal
cd /d "%~dp0"
set MODE=%1
if "%MODE%"=="" set MODE=test
if /I "%MODE%"=="test"  python -m unittest discover -s TESTS -v
if /I "%MODE%"=="quick" (cd EXPERIMENTS & python run_all.py --quick)
if /I "%MODE%"=="full"  (cd EXPERIMENTS & python make_pattern.py & python run_all.py)
if /I "%MODE%"=="graph" (cd EXPERIMENTS & python E17_h3_graph.py %2 3300)
endlocal
