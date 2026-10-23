@echo off
setlocal
cd /d "%~dp0"
set "PY=py -3"
where py >nul 2>nul || set "PY=python"
%PY% -m unittest discover -s tests -p test_xvi_closure_v001.py -v
if errorlevel 1 (echo TESTS FAILED& pause& exit /b 1)
%PY% -m src.xvi_closure_v001 --output output/XVI_CLOSURE_v001.json
if errorlevel 1 (echo RUN FAILED& pause& exit /b 1)
echo Phase 1 finished. See output\XVI_CLOSURE_v001.json
pause
