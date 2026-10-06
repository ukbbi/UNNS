@echo off
setlocal
cd /d "%~dp0"
echo.
echo ============================================
echo UNNS SPEC-I/B - Independent Spectral Control
echo ============================================
echo.
py -3.12 scripts\spec_i_b_extract.py
set RC=%ERRORLEVEL%
echo.
if not "%RC%"=="0" (
  echo SPEC-I/B extraction FAILED with exit code %RC%.
) else (
  echo SPEC-I/B extraction finished successfully.
  echo See output\spec_i_b\SPEC_I_B_RESULT.md
)
echo.
pause
exit /b %RC%
