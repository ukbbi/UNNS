@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 field1.py --tests-only
) else (
    python field1.py --tests-only
)
set "rc=%errorlevel%"
echo.
echo FIELD-I tests exit code: %rc%
pause
exit /b %rc%
