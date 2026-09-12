@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ROUTE-LADDER-EXTRACT v0.1.1
echo Frozen STRUC-ROUTE-I to canonical chamber ladders
echo.

REM Reuse the already validated STRUC-ROUTE-I Python environment.
set "PYEXE=%LOCALAPPDATA%\UNNS\ROUTE_I_v010\Scripts\python.exe"

if exist "%PYEXE%" (
  "%PYEXE%" -c "import pandas,pyarrow" >nul 2>&1
  if not errorlevel 1 goto :RUN
)

echo STRUC-ROUTE-I Python environment with pandas + pyarrow was not found.
echo.
echo Expected:
echo   %PYEXE%
echo.
echo Run chambers\STRUC_ROUTE_I_v0_1_2\RUN_WINDOWS.bat once first.
echo That environment already contains the dependencies needed by this extractor.
echo.
pause
exit /b 1

:RUN
"%PYEXE%" "%~dp0extract_ladders.py"
set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" (
  echo EXTRACTION COMPLETE.
  echo.
  echo Next primary input:
  echo   ladders\struc_i\jhtdb_pilot_a\D_STITCH.csv
  echo and independently:
  echo   ladders\struc_perc_i\jhtdb_pilot_a\D_STITCH.csv
) else (
  echo EXTRACTION FAILED with exit code %RC%.
)
pause
exit /b %RC%
