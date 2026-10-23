@echo off
setlocal
cd /d "%~dp0"
if not exist output mkdir output
set RC=0
python ..\v002\field2.py > output\field2_rerun.txt 2>&1
if errorlevel 1 set RC=1
python ..\v002\synthesis\g_checks.py > output\g_checks_rerun.txt 2>&1
if errorlevel 1 set RC=1
python ..\v003\field3.py > output\field3_rerun.txt 2>&1
if errorlevel 1 set RC=1
python field4.py > output\field4_output.txt 2>&1
if errorlevel 1 set RC=1
echo exit code %RC%  (0 = no FAIL in field2.py, g_checks.py, field3.py, field4.py)
findstr /B /C:"FAIL" output\field2_rerun.txt output\g_checks_rerun.txt output\field3_rerun.txt output\field4_output.txt
findstr /C:"ALL PASS" /C:"SOME FAIL" output\field2_rerun.txt output\g_checks_rerun.txt output\field3_rerun.txt output\field4_output.txt
endlocal & exit /b %RC%
