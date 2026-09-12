@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "ENVROOT=%LOCALAPPDATA%\UNNS\ROUTE_I_v010"
set "PYEXE=%ENVROOT%\Scripts\python.exe"

if not exist "%PYEXE%" (
  echo STRUC-ROUTE-I environment not found.
  echo Run RUN_WINDOWS.bat first.
  pause
  exit /b 1
)

"%PYEXE%" -m pytest -q
set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" (
  echo TESTS PASSED.
) else (
  echo TESTS FAILED.
)
pause
exit /b %RC%
