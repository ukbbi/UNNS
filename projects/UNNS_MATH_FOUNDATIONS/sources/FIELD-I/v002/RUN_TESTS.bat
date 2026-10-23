@echo off
setlocal
cd /d "%~dp0"
if not exist output mkdir output
python field2.py > output\field2_output.txt 2>&1
set RC=%ERRORLEVEL%
echo field2.py exit code %RC%  (0 = no FAIL)
findstr /B /C:"FAIL" output\field2_output.txt
findstr /C:"ALL PASS" /C:"SOME FAIL" output\field2_output.txt
endlocal & exit /b %RC%
