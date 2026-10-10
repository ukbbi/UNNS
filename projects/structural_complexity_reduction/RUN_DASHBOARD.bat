@echo off
setlocal
set PYTHONDONTWRITEBYTECODE=1
cd /d "%~dp0"
echo ============================================================
echo  Structural Complexity Reduction - SCR-I Dashboard v003
echo ============================================================
echo.
if not exist "dashboard\dashboard_server.py" (
  echo ERROR: dashboard\dashboard_server.py was not found.
  pause
  exit /b 2
)
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "dashboard\dashboard_server.py"
  set RC=%errorlevel%
) else (
  where python >nul 2>nul
  if not %errorlevel%==0 (
    echo ERROR: Python 3 was not found in PATH.
    pause
    exit /b 3
  )
  python "dashboard\dashboard_server.py"
  set RC=%errorlevel%
)
if not "%RC%"=="0" (
  echo.
  echo Dashboard exited with code %RC%.
  pause
)
exit /b %RC%
