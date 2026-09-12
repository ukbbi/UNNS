@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "PROJECTROOT=%~dp0..\..\.."
set "ADAPTER=%PROJECTROOT%\tools\derive\JHTDB_ROUTE_ADAPTER_v0_1_0"
set "ENVROOT=%LOCALAPPDATA%\UNNS\JHTDB_ROUTE_ADAPTER_v010"
set "PYEXE=%ENVROOT%\Scripts\python.exe"

where py >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python launcher "py" not found.
  pause
  exit /b 1
)

if exist "%PYEXE%" goto :ENV_READY

echo Creating local Python environment:
echo   %ENVROOT%
py -3 -m venv "%ENVROOT%"
if errorlevel 1 (
  echo ERROR: Could not create Python environment.
  pause
  exit /b 1
)

:ENV_READY
"%PYEXE%" -c "import numpy,scipy,pandas,pyarrow,h5py" >nul 2>&1
if not errorlevel 1 goto :RUN

echo Installing frozen adapter dependencies...
"%PYEXE%" -m pip install --upgrade pip
if errorlevel 1 goto :PIP_FAIL
"%PYEXE%" -m pip install -r "%ADAPTER%\requirements.txt"
if errorlevel 1 goto :PIP_FAIL

:RUN

echo.
echo JHTDB PILOT B - PREFLIGHT ONLY
echo.
"%PYEXE%" "%~dp0run_pilot_b.py" --preflight-only
set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" (
  echo PREFLIGHT COMPLETE.
) else (
  echo PREFLIGHT FAILED with exit code %RC%.
)
pause
exit /b %RC%

:PIP_FAIL
echo ERROR: Dependency installation failed.
pause
exit /b 1
