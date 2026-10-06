@echo off
setlocal
py -3.12 -m pip install --no-cache-dir pymupdf pandas numpy
set RC=%ERRORLEVEL%
echo.
if not "%RC%"=="0" (
  echo EMT extraction dependency installation FAILED.
) else (
  echo EMT extraction dependencies installed successfully.
)
pause
exit /b %RC%
