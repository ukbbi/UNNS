@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "ENVROOT=%LOCALAPPDATA%\UNNS\ROUTE_I_v010"
set "PYEXE=%ENVROOT%\Scripts\python.exe"

if not exist "%PYEXE%" (
  echo STRUC-ROUTE-I Python environment was not found.
  echo Run RUN_WINDOWS.bat first.
  pause
  exit /b 1
)

if "%~1"=="" (
  echo Drag an existing STRUC-ROUTE-I RUN ZIP onto this BAT file.
  echo Example: jhtdb_pilot_a_20260904_204806.zip
  pause
  exit /b 1
)

echo Post-run stitching physics analysis:
echo   %~1
echo.
"%PYEXE%" "%~dp0analyze_run.py" "%~1" --viscosity 0.000185 --permutations 5000
set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" (
  echo COMPLETE.
  echo A folder named RUNZIP_STITCH_PHYSICS was created beside the ZIP.
) else (
  echo ANALYSIS FAILED.
)
pause
exit /b %RC%
