@echo off
rem GEO-I v003 full verifier (long). Add --orbits-exhaustive to recompute every cached orbit state (hours).
cd /d "%~dp0"
python verify.py %*
if errorlevel 1 (echo.& echo FULL VERIFICATION FAILED) else (echo.& echo FULL VERIFICATION PASSED)
pause
