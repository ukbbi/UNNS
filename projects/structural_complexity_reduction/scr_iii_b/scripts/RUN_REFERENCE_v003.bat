@echo off
setlocal
cd /d "%~dp0\..\.."
python scr_iii_b\reference_check\validate_v003.py
exit /b %errorlevel%
