@echo off
setlocal EnableExtensions
cd /d "%~dp0"
call :PYENV || exit /b 1
"%PYEXE%" high_re_stage.py adapter
set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" echo [PASS] High-Re route inputs are ready.
if not "%RC%"=="0" pause
exit /b %RC%

:PYENV
set "ENVROOT=%LOCALAPPDATA%\UNNS\JHTDB_HIGH_RE_SCALE_v011"
set "PYEXE=%ENVROOT%\Scripts\python.exe"
if exist "%PYEXE%" goto :CHECK
where py >nul 2>&1 || (echo ERROR: Python launcher not found.& exit /b 1)
py -3 -m venv "%ENVROOT%" || exit /b 1
:CHECK
"%PYEXE%" -c "import numpy,pandas,scipy,h5py,pyarrow" >nul 2>&1
if not errorlevel 1 exit /b 0
"%PYEXE%" -m pip install --upgrade pip || exit /b 1
"%PYEXE%" -m pip install -r requirements.txt || exit /b 1
exit /b 0
