@echo off
setlocal
cd /d "%~dp0"
echo [SCR-II] Setup: validate -> calibration -> design audit.
call RUN_SCR_II_VALIDATE.bat
if errorlevel 1 exit /b %ERRORLEVEL%
call RUN_SCR_II_CALIBRATION.bat
if errorlevel 1 exit /b %ERRORLEVEL%
call RUN_SCR_II_AUDIT.bat
if errorlevel 1 exit /b %ERRORLEVEL%
echo SCR-II setup complete. Primary remains untouched.
pause
