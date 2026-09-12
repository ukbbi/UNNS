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

echo STITCH-MECH v0.1.1 - PILOT B
echo N1 and N2 each contain 100 constrained nulls.
echo The run is resumable.
echo.
"%PYEXE%" "%~dp0run_pb.py"
set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" (
  echo STITCH-MECH PILOT B COMPLETE.
) else (
  echo STITCH-MECH PILOT B FAILED with exit code %RC%.
)
pause
exit /b %RC%
