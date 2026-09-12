@echo off
setlocal
cd /d "%~dp0"
set "PYEXE=%LOCALAPPDATA%\UNNS\ROUTE_I_v010\Scripts\python.exe"
if not exist "%PYEXE%" (
  echo ROUTE-I environment not found.
  pause
  exit /b 1
)
"%PYEXE%" -m pytest -q
set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" (echo TESTS PASSED.) else (echo TESTS FAILED.)
pause
exit /b %RC%
