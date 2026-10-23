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
python ..\v004\field4.py > output\field4_rerun.txt 2>&1
if errorlevel 1 set RC=1
python ..\v005\field5.py > output\field5_rerun.txt 2>&1
if errorlevel 1 set RC=1
python ..\v006\field6.py > output\field6_rerun.txt 2>&1
if errorlevel 1 set RC=1
python ..\v007\field7.py > output\field7_rerun.txt 2>&1
if errorlevel 1 set RC=1
python field8.py > output\field8_output.txt 2>&1
if errorlevel 1 set RC=1
echo exit code %RC%  (0 = no FAIL in field2, g_checks, field3 .. field8)
findstr /B /C:"FAIL" output\field2_rerun.txt output\g_checks_rerun.txt output\field3_rerun.txt output\field4_rerun.txt output\field5_rerun.txt output\field6_rerun.txt output\field7_rerun.txt output\field8_output.txt
findstr /C:"ALL PASS" /C:"SOME FAIL" output\field2_rerun.txt output\g_checks_rerun.txt output\field3_rerun.txt output\field4_rerun.txt output\field5_rerun.txt output\field6_rerun.txt output\field7_rerun.txt output\field8_output.txt
endlocal & exit /b %RC%
