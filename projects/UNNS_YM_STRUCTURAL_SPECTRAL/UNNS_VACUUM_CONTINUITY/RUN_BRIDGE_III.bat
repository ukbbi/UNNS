@echo off
setlocal
cd /d "%~dp0"
echo.
echo ============================================
echo UNNS BRIDGE-III - Structural vs Spectral
echo ============================================
echo.
py -3.12 scripts\bridge_iii.py
set RC=%ERRORLEVEL%
echo.
if "%RC%"=="0" (
  echo BRIDGE-III finished successfully.
  echo See output\bridge_iii\BRIDGE_III_RESULT.md
) else (
  echo BRIDGE-III did not establish coexistence.
  echo See output\bridge_iii\BRIDGE_III_RESULT.md
)
echo.
pause
exit /b %RC%
