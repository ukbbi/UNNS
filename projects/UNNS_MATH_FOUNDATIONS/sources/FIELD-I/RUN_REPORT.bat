@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 field1.py --report-only
) else (
    python field1.py --report-only
)
set "rc=%errorlevel%"
echo.
echo FIELD-I report exit code: %rc%
pause
exit /b %rc%
