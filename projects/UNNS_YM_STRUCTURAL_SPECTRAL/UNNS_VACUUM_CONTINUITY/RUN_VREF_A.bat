@echo off
setlocal
cd /d "%~dp0"

echo.
echo ============================================
echo UNNS VREF-I/A - Refinement Validation
echo ============================================
echo.

where py >nul 2>nul
if %ERRORLEVEL%==0 (
    py -3 chambers\vref_i\vref_a.py --project-root "%CD%"
) else (
    python chambers\vref_i\vref_a.py --project-root "%CD%"
)

set RC=%ERRORLEVEL%
echo.
if not "%RC%"=="0" (
    echo VREF-I/A FAILED with exit code %RC%.
    echo No physical conclusion should be drawn.
) else (
    echo VREF-I/A finished successfully.
    echo See output\reports\VREF_A_REPORT.md
)
echo.
pause
exit /b %RC%
