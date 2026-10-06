@echo off
setlocal
cd /d "%~dp0"

echo.
echo ============================================
echo UNNS VREF-I/B - Structural Vacuum Accessibility
echo ============================================
echo.

where py >nul 2>nul
if %ERRORLEVEL%==0 (
    py -3.12 chambers\vref_i\vref_b.py --project-root "%CD%"
) else (
    python chambers\vref_i\vref_b.py --project-root "%CD%"
)

set RC=%ERRORLEVEL%
echo.
if not "%RC%"=="0" (
    echo VREF-I/B FAILED with exit code %RC%.
    echo No scientific conclusion should be drawn.
) else (
    echo VREF-I/B finished successfully.
    echo See output\reports\VREF_B_REPORT.md
)
echo.
pause
exit /b %RC%
