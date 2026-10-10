@echo off
setlocal
cd /d "%~dp0.."
python scripts\validate_prereg.py
if errorlevel 1 exit /b 1
python scripts\prereg_hash.py
if errorlevel 1 exit /b 1
echo.
echo SCR_I_PREREG_v001 validation complete.
endlocal
