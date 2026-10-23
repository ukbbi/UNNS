@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0" || goto directory_error

echo ================================================
echo UNNS Mathematical Foundations - Source Verification
echo ================================================
echo.
echo Checking individual files, not ZIP archives.
echo.

where python >nul 2>&1
if not errorlevel 1 goto use_python
where py >nul 2>&1
if not errorlevel 1 goto use_py

echo FAIL: Python 3 is required but was not found.
set "RC=1"
goto finish

:use_python
python "%~dp0verify_sources.py"
set "RC=%ERRORLEVEL%"
goto finish

:use_py
py -3 "%~dp0verify_sources.py"
set "RC=%ERRORLEVEL%"
goto finish

:directory_error
echo FAIL: Cannot open the project directory.
set "RC=1"

:finish
echo.
echo Finished; exit code: %RC%
pause
endlocal & exit /b %RC%
