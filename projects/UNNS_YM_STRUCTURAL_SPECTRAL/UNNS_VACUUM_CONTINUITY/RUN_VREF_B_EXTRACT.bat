@echo off
setlocal
cd /d "%~dp0"

echo.
echo ============================================
echo UNNS VREF-I/B - CEA 2017 Vector Extraction
echo ============================================
echo.

where py >nul 2>nul
if %ERRORLEVEL%==0 (
    py -3.12 scripts\cea17_extract.py --project-root "%CD%"
) else (
    python scripts\cea17_extract.py --project-root "%CD%"
)

set RC=%ERRORLEVEL%
echo.
if not "%RC%"=="0" (
    echo VREF-I/B EXTRACTION FAILED with exit code %RC%.
    echo No scientific conclusion should be drawn.
) else (
    echo VREF-I/B extraction finished successfully.
    echo See data\derived\cea_2017\
)
echo.
pause
exit /b %RC%
