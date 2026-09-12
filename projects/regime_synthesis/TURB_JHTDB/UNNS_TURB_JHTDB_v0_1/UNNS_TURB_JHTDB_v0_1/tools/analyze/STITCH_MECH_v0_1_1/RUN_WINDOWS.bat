@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo STITCH-MECH v0.1.1
echo JHTDB scale-time stitching mechanism test
echo.

set "ENVROOT=%LOCALAPPDATA%\UNNS\ROUTE_I_v010"
set "PYEXE=%ENVROOT%\Scripts\python.exe"

if not exist "%PYEXE%" (
  echo ERROR: STRUC-ROUTE-I Python environment was not found:
  echo   %PYEXE%
  echo.
  echo Run chambers\STRUC_ROUTE_I_v0_1_2\RUN_WINDOWS.bat once first.
  pause
  exit /b 1
)

"%PYEXE%" -c "import numpy,pandas,pyarrow" >nul 2>&1
if errorlevel 1 (
  echo ERROR: Existing ROUTE-I environment is missing numpy/pandas/pyarrow.
  pause
  exit /b 1
)

echo The run is resumable.
echo If Windows or the terminal is closed, launch this BAT again.
echo Completed N1/N2 null rows are preserved and the run continues.
echo.
echo Expect this phase to be substantially longer than one ROUTE-I run:
echo two new 100-null constrained ensembles are required.
echo.

"%PYEXE%" "%~dp0run_mech.py"
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo STITCH-MECH COMPLETE.
) else (
  echo STITCH-MECH FAILED with exit code %RC%.
)
pause
exit /b %RC%
