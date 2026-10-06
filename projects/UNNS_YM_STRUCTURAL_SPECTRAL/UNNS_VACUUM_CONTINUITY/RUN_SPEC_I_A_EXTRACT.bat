@echo off
setlocal
cd /d "%~dp0"
echo.
echo ============================================
echo UNNS SPEC-I/A - Primary Spectral Anchor
echo ============================================
echo.
py -3.12 scripts\spec_i_a_extract.py
set RC=%ERRORLEVEL%
echo.
if not "%RC%"=="0" (
  echo SPEC-I/A extraction FAILED with exit code %RC%.
) else (
  echo SPEC-I/A extraction finished successfully.
  echo See output\spec_i_a\SPEC_I_A_RESULT.md
)
echo.
pause
exit /b %RC%
