@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "PYEXE=%LOCALAPPDATA%\UNNS\ROUTE_I_v010\Scripts\python.exe"
if not exist "%PYEXE%" (
  echo ERROR: STRUC-ROUTE-I Python environment not found:
  echo   %PYEXE%
  pause
  exit /b 1
)
"%PYEXE%" "%~dp0run_extract_pb.py"
set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" (
  echo EXTRACTION COMPLETE.
) else (
  echo EXTRACTION FAILED with exit code %RC%.
)
pause
exit /b %RC%
