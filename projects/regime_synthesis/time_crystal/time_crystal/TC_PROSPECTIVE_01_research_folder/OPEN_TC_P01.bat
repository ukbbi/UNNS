@echo off
setlocal
cd /d "%~dp0"

if not exist "tools\build_tc_p01_data.py" (
  echo ERROR: tools\build_tc_p01_data.py is missing.
  pause
  exit /b 1
)

echo Refreshing TC_PROSPECTIVE_01 campaign data...
python tools\build_tc_p01_data.py
if errorlevel 1 (
  echo.
  echo Campaign data build failed.
  pause
  exit /b 1
)

echo.
echo Opening TC_P01.html...
start "" "TC_P01.html"
exit /b 0
