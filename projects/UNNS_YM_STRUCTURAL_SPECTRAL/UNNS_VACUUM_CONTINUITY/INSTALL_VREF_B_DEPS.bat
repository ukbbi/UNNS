@echo off
setlocal
cd /d "%~dp0"
echo Installing VREF-I/B Python dependencies...
py -3.12 -m pip install -r chambers\vref_i\requirements_b.txt
set RC=%ERRORLEVEL%
echo.
if not "%RC%"=="0" (
    echo Dependency installation FAILED with exit code %RC%.
) else (
    echo VREF-I/B dependencies installed successfully.
)
echo.
pause
exit /b %RC%
