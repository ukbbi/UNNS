@echo off
setlocal
cd /d "%~dp0"

set "ENVROOT=%LOCALAPPDATA%\UNNS\JHTDB_ROUTE_ADAPTER_v010"
set "PYEXE=%ENVROOT%\Scripts\python.exe"

if not exist "%PYEXE%" (
  echo Run RUN_ADAPTER_WINDOWS.bat once first to create the environment.
  pause
  exit /b 1
)

"%PYEXE%" -m pytest -q
set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" (
  echo ADAPTER TESTS PASSED.
) else (
  echo ADAPTER TESTS FAILED.
)
pause
exit /b %RC%
