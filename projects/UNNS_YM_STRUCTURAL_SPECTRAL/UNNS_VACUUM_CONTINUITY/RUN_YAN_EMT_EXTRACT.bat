@echo off
setlocal
cd /d "%~dp0"
echo.
echo ============================================
echo UNNS EMT-I - Yanagihara Vector Extraction
echo ============================================
echo.
py -3.12 scripts\yan19_emt_extract.py --project-root "%CD%"
set RC=%ERRORLEVEL%
echo.
if not "%RC%"=="0" (
  echo EMT extraction FAILED with exit code %RC%.
) else (
  echo EMT extraction finished successfully.
  echo See data\derived\yanagihara_2019\
)
pause
exit /b %RC%
