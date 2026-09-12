@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "PROJECTROOT=%~dp0..\..\.."
set "ENVROOT=%LOCALAPPDATA%\UNNS\JHTDB_ROUTE_ADAPTER_v010"
set "PYEXE=%ENVROOT%\Scripts\python.exe"

if not exist "%PYEXE%" (
  echo ERROR: Expected adapter Python environment not found:
  echo   %PYEXE%
  pause
  exit /b 1
)

"%PYEXE%" "%~dp0verify_pilot_b.py"
set "RC=%ERRORLEVEL%"
echo.
pause
exit /b %RC%
