@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo STRUC-ROUTE-I v0.1.2
echo Python routing engine + local browser interface
echo.

REM ------------------------------------------------------------
REM Use the existing installed Python 3 runtime.
REM Do NOT request Python 3.11 or 3.12 specifically.
REM Keep the virtual environment outside the deep research path
REM to avoid Windows path-length / ensurepip problems.
REM ------------------------------------------------------------

set "ENVROOT=%LOCALAPPDATA%\UNNS\ROUTE_I_v010"
set "PYEXE=%ENVROOT%\Scripts\python.exe"

where py >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python launcher "py" was not found.
  echo Install Python 3 and enable the Python launcher.
  pause
  exit /b 1
)

REM Confirm that some Python 3 runtime is already installed.
py -3 -c "import sys; print('Using installed Python ' + sys.version.split()[0])"
if errorlevel 1 (
  echo.
  echo ERROR: No installed Python 3 runtime was found.
  echo Run:
  echo   py -0p
  echo to see the Python installations known to the launcher.
  pause
  exit /b 1
)

REM Reuse an existing healthy environment.
if exist "%PYEXE%" goto :ENV_READY

echo.
echo Creating short-path local Python environment:
echo   %ENVROOT%
echo.

REM Remove an incomplete environment from a previous failed attempt.
if exist "%ENVROOT%" rmdir /s /q "%ENVROOT%" >nul 2>&1

REM First choice: standard library venv using the EXISTING Python 3.
py -3 -m venv "%ENVROOT%"
if not errorlevel 1 goto :ENV_READY

echo.
echo Standard venv creation failed.
echo Attempting a virtualenv fallback with the same installed Python 3...
echo.

REM Try to ensure pip is available in the base runtime.
py -3 -m ensurepip --upgrade >nul 2>&1

REM Install virtualenv into the user's Python environment if needed.
py -3 -m pip install --user --upgrade virtualenv
if errorlevel 1 goto :VENV_FAIL

if exist "%ENVROOT%" rmdir /s /q "%ENVROOT%" >nul 2>&1
py -3 -m virtualenv "%ENVROOT%"
if errorlevel 1 goto :VENV_FAIL

:ENV_READY
echo.
echo Python environment:
"%PYEXE%" -c "import sys; print('  ' + sys.executable); print('  Python ' + sys.version.split()[0])"
if errorlevel 1 goto :VENV_FAIL

echo.
echo Checking chamber dependencies...
"%PYEXE%" -c "import fastapi,uvicorn,numpy,pandas,pyarrow,multipart" >nul 2>&1
if not errorlevel 1 goto :START

echo Installing chamber dependencies...
"%PYEXE%" -m pip install --upgrade pip
if errorlevel 1 goto :PIP_FAIL

"%PYEXE%" -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 goto :PIP_FAIL

:START
echo.
echo Starting STRUC-ROUTE-I at:
echo   http://127.0.0.1:8765
echo.
"%PYEXE%" "%~dp0app.py"
set "RC=%ERRORLEVEL%"

if not "%RC%"=="0" (
  echo.
  echo Chamber exited with code %RC%.
  pause
)
exit /b %RC%

:VENV_FAIL
echo.
echo ERROR: Could not create the Python environment.
echo.
echo Chamber location:
echo   %~dp0
echo.
echo Environment target:
echo   %ENVROOT%
echo.
echo Existing Python installations:
py -0p
echo.
pause
exit /b 1

:PIP_FAIL
echo.
echo ERROR: Python environment exists, but dependency installation failed.
echo Check the messages immediately above this line.
echo.
pause
exit /b 1
