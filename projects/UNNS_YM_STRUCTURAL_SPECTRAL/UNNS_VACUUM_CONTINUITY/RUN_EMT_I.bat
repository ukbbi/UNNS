@echo off
setlocal
cd /d "%~dp0"
echo.
echo ============================================
echo UNNS EMT-I - Independent EMT Representation
echo ============================================
echo.
py -3.12 chambers\emt_i\emt_i.py --project-root "%CD%"
set RC=%ERRORLEVEL%
echo.
if not "%RC%"=="0" (
  echo EMT-I FAILED with exit code %RC%.
  echo No scientific conclusion should be drawn.
) else (
  echo EMT-I finished successfully.
  echo See output\yanagihara_emt\reports\EMT_I_REPORT.md
)
pause
exit /b %RC%
