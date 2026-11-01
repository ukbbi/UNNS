@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 RUN_CHECKS.py
) else (
  python RUN_CHECKS.py
)
if errorlevel 1 (
  echo GEO-HD-1 tests: FAIL
  exit /b 1
)
echo GEO-HD-1 tests: PASS
exit /b 0
