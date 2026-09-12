@echo off
setlocal EnableExtensions
cd /d "%~dp0"
call :PYENV || exit /b 1
"%PYEXE%" high_re_stage.py verify
set "RC=%ERRORLEVEL%"
echo.
if not "%RC%"=="0" pause
exit /b %RC%

:PYENV
set "ENVROOT=%LOCALAPPDATA%\UNNS\JHTDB_HIGH_RE_SCALE_v011"
set "PYEXE=%ENVROOT%\Scripts\python.exe"
if exist "%PYEXE%" exit /b 0
where py >nul 2>&1 || (echo ERROR: Python launcher not found.& exit /b 1)
py -3 -m venv "%ENVROOT%" || exit /b 1
"%PYEXE%" -m pip install --upgrade pip || exit /b 1
"%PYEXE%" -m pip install -r requirements.txt || exit /b 1
exit /b 0
