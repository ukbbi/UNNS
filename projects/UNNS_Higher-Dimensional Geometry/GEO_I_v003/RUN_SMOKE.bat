@echo off
rem GEO-I v003 smoke verifier (about a minute or two)
cd /d "%~dp0"
python verify.py --smoke
if errorlevel 1 (echo.& echo SMOKE VERIFICATION FAILED) else (echo.& echo SMOKE VERIFICATION PASSED)
pause
