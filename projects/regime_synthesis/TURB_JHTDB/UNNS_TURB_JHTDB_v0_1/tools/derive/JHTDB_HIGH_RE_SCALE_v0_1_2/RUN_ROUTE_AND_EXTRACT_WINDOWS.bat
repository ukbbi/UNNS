@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "ENVROOT=%LOCALAPPDATA%\UNNS\JHTDB_HIGH_RE_SCALE_v011"
set "PYEXE=%ENVROOT%\Scripts\python.exe"
if not exist "%PYEXE%" (
  echo ERROR: Run RUN_ADAPTER_WINDOWS.bat first.
  pause
  exit /b 1
)
"%PYEXE%" high_re_stage.py route
set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" echo [PASS] Seven P_SCALE ladders are ready for STRUC-I and STRUC-PERC-I.
if not "%RC%"=="0" pause
exit /b %RC%
