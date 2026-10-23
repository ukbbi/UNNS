@echo off
setlocal
cd /d "%~dp0"
python -m unittest discover -s tests -p "test_*.py" -v
if errorlevel 1 exit /b 1
python -m src.xvi_canonical_bridge_v001
if errorlevel 1 exit /b 1
echo Verified. Output: output\XVI_CANONICAL_BRIDGE_v001.json
endlocal
