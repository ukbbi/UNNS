@echo off
setlocal
cd /d "%~dp0"
echo.
echo ============================================
echo UNNS EMT-I - Secondary Geometry Checks
echo ============================================
echo.
py -3.12 chambers\emt_geom\emt_geom.py --project-root "%CD%"
set RC=%ERRORLEVEL%
echo.
if not "%RC%"=="0" (
  echo EMT geometry checks FAILED with exit code %RC%.
) else (
  echo EMT geometry checks finished successfully.
  echo See output\yanagihara_emt\geometry\reports\EMT_GEOM_REPORT.md
)
pause
exit /b %RC%
