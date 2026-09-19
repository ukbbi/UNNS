@echo off
setlocal
cd /d "%~dp0\.."

echo [1/4] Building exact corpus...
python scripts\BUILD_CORPUS.py
if errorlevel 1 goto :fail

echo [2/4] Building primary system spectra...
python scripts\BUILD_LADDERS.py
if errorlevel 1 goto :fail

echo [3/4] Freezing preregistered inputs...
python scripts\FREEZE.py
if errorlevel 1 goto :fail

echo [4/4] Verifying freeze...
python scripts\VERIFY.py
if errorlevel 1 goto :fail

echo.
echo BUILD AND FREEZE PASS
exit /b 0

:fail
echo.
echo BUILD FAILED
exit /b 1
