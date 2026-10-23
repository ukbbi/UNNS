@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (py -3 -m unittest discover -s tests -v) else (python -m unittest discover -s tests -v)
set EXITCODE=%ERRORLEVEL%
echo.
if %EXITCODE% NEQ 0 (echo RGG-2 TEST FAILURE) else (echo RGG-2 TESTS PASSED)
pause
exit /b %EXITCODE%
