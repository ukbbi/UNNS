@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "ENVROOT=%LOCALAPPDATA%\UNNS\ROUTE_I_v010"
set "PYEXE=%ENVROOT%\Scripts\python.exe"

if not exist "%PYEXE%" (
  echo ERROR: STRUC-ROUTE-I Python environment not found:
  echo   %PYEXE%
  pause
  exit /b 1
)

"%PYEXE%" -c "import numpy,pandas,pyarrow" >nul 2>&1
if errorlevel 1 (
  echo ERROR: ROUTE-I environment is missing numpy/pandas/pyarrow.
  pause
  exit /b 1
)

"%PYEXE%" "%~dp0run_pb.py" --check
set "RC=%ERRORLEVEL%"
echo.
pause
exit /b %RC%
