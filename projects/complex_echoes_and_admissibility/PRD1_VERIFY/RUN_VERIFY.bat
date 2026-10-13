@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if not errorlevel 1 (
    py -3 independent_check_prd1.py
) else (
    python independent_check_prd1.py
)
set "RESULT=%ERRORLEVEL%"
echo.
if not "%RESULT%"=="0" (
    echo Verification failed or Python could not be launched. Exit code: %RESULT%
) else (
    echo Verification completed. Check RUN_RESULT.json and compare with INDEPENDENT_PRD1_RESULT.json.
)
pause
exit /b %RESULT%
