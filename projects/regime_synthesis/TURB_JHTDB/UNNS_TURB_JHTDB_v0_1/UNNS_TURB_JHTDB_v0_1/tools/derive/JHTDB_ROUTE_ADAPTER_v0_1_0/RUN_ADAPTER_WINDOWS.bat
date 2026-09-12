@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo JHTDB ROUTE ADAPTER v0.1.0
echo Physical extraction layer for STRUC-ROUTE-I
echo.

set "ENVROOT=%LOCALAPPDATA%\UNNS\JHTDB_ROUTE_ADAPTER_v010"
set "PYEXE=%ENVROOT%\Scripts\python.exe"

where py >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python launcher "py" not found.
  pause
  exit /b 1
)

py -3 -c "import sys; print('Using installed Python ' + sys.version.split()[0])"
if errorlevel 1 (
  echo ERROR: No installed Python 3 runtime found.
  py -0p
  pause
  exit /b 1
)

if exist "%PYEXE%" goto :ENV_READY

echo Creating short-path local Python environment:
echo   %ENVROOT%
if exist "%ENVROOT%" rmdir /s /q "%ENVROOT%" >nul 2>&1

py -3 -m venv "%ENVROOT%"
if not errorlevel 1 goto :ENV_READY

echo Standard venv failed. Trying virtualenv fallback...
py -3 -m ensurepip --upgrade >nul 2>&1
py -3 -m pip install --user --upgrade virtualenv
if errorlevel 1 goto :VENV_FAIL
if exist "%ENVROOT%" rmdir /s /q "%ENVROOT%" >nul 2>&1
py -3 -m virtualenv "%ENVROOT%"
if errorlevel 1 goto :VENV_FAIL

:ENV_READY
echo Checking dependencies...
"%PYEXE%" -c "import numpy,scipy,pandas,pyarrow,h5py" >nul 2>&1
if not errorlevel 1 goto :RUN

echo Installing dependencies...
"%PYEXE%" -m pip install --upgrade pip
if errorlevel 1 goto :PIP_FAIL
"%PYEXE%" -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 goto :PIP_FAIL

:RUN
echo.
echo IMPORTANT:
echo The full 10-frame x 5-scale run may take substantial time.
echo The 2 GB source remains local and read-only.
echo.
"%PYEXE%" "%~dp0run_adapter.py"
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo JHTDB ADAPTER COMPLETE.
  echo Load outputs\records\JHTDB_PILOT_A_ROUTE.zip into STRUC-ROUTE-I.
) else (
  echo JHTDB ADAPTER FAILED with exit code %RC%.
)
pause
exit /b %RC%

:VENV_FAIL
echo ERROR: Could not create the Python environment.
py -0p
pause
exit /b 1

:PIP_FAIL
echo ERROR: Dependency installation failed.
pause
exit /b 1
