@echo off
setlocal
cd /d "%~dp0.."

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 scripts\BUILD_SYNTHESIS.py
) else (
    python scripts\BUILD_SYNTHESIS.py
)

if errorlevel 1 (
    echo.
    echo SYNTHESIS BUILD FAILED.
    exit /b 1
)

echo.
echo SYNTHESIS BUILD PASSED.
exit /b 0
