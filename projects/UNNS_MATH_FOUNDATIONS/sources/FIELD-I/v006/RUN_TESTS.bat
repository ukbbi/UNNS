@echo off
setlocal
cd /d "%~dp0"
if not exist output mkdir output
set RC=0
echo FIELD-I v006 complete regression and modular-collapsing investigation
echo.
python ..\v002\field2.py > output\field2_rerun.txt 2>&1
if errorlevel 1 set RC=1
python ..\v002\synthesis\g_checks.py > output\g_checks_rerun.txt 2>&1
if errorlevel 1 set RC=1
python ..\v003\field3.py > output\field3_rerun.txt 2>&1
if errorlevel 1 set RC=1
python ..\v004\field4.py > output\field4_rerun.txt 2>&1
if errorlevel 1 set RC=1
python ..\v005\field5.py > output\field5_rerun.txt 2>&1
if errorlevel 1 set RC=1
python field6.py > output\field6_output.txt 2>&1
if errorlevel 1 set RC=1
findstr /B /C:"FAIL" output\field2_rerun.txt output\g_checks_rerun.txt output\field3_rerun.txt output\field4_rerun.txt output\field5_rerun.txt output\field6_output.txt
findstr /C:"ALL PASS" /C:"SOME FAIL" output\field2_rerun.txt output\g_checks_rerun.txt output\field3_rerun.txt output\field4_rerun.txt output\field5_rerun.txt output\field6_output.txt
echo.
echo FIELD-I v006 exit code %RC%  (0 means no FAIL)
endlocal & exit /b %RC%
