@echo off
setlocal
cd /d "%~dp0"
echo.
echo ============================================
echo UNNS STRUC BRIDGE - Rebuild Frozen Ladders
echo ============================================
echo.
where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3.12 scripts\make_struc_bridge.py
) else (
  python scripts\make_struc_bridge.py
)
set RC=%ERRORLEVEL%
echo.
if not "%RC%"=="0" (
  echo STRUC bridge rebuild FAILED with exit code %RC%.
) else (
  echo STRUC bridge rebuild finished successfully.
)
echo.
pause
exit /b %RC%
