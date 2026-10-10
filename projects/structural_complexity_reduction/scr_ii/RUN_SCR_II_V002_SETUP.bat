@echo off
setlocal
cd /d "%~dp0"
echo [SCR-II v002] PREP ONLY: validate -> calibration -> design audit.
call RUN_SCR_II_V002_VALIDATE.bat
if errorlevel 1 exit /b %ERRORLEVEL%
call RUN_SCR_II_V002_CALIBRATION.bat
if errorlevel 1 exit /b %ERRORLEVEL%
call RUN_SCR_II_V002_AUDIT.bat
if errorlevel 1 exit /b %ERRORLEVEL%
echo SCR-II v002 prep complete. No primary runner is included in this package.
pause
