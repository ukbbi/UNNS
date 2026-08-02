@echo off
setlocal
cd /d "%~dp0"
python VERIFY_PACKAGE.py
if errorlevel 1 (
  echo.
  echo TEL-FINGERPRINT-I package verification failed.
  pause
  exit /b 1
)
echo.
echo TEL-FINGERPRINT-I package verification passed.
pause
