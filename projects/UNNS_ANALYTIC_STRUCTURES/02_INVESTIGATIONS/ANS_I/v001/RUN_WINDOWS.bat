@echo off
rem ANS-I v001 verification (Windows). Usage: RUN_WINDOWS.bat [A|B|C|D|E]  (default C)
setlocal
cd /d "%~dp0"
set PYTHONDONTWRITEBYTECODE=1
set STAGE=%~1
if "%STAGE%"=="" set STAGE=C
set PY=py -3
py -3 --version >nul 2>&1 || set PY=python
%PY% --version >nul 2>&1 || (echo Python 3.8 or newer was not found. & set RC=9009 & goto end)
%PY% verify.py --stage %STAGE%
set RC=%ERRORLEVEL%
:end
echo.
if "%RC%"=="0" (echo VERIFICATION PASSED) else (echo VERIFICATION FAILED, exit code %RC%)
if /i not "%ANS_NOPAUSE%"=="1" pause
exit /b %RC%
