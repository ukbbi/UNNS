@echo off
setlocal
cd /d "%~dp0"
echo.
echo ============================================
echo UNNS Battelli 2019 - Unsmoothed Extraction
echo ============================================
echo.
where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3.12 scripts\battelli19_extract.py
) else (
  python scripts\battelli19_extract.py
)
set RC=%ERRORLEVEL%
echo.
if not "%RC%"=="0" (
  echo BATTELLI extraction FAILED with exit code %RC%.
) else (
  echo BATTELLI extraction finished successfully.
  echo See data\derived\battelli_2019\
)
echo.
pause
exit /b %RC%
