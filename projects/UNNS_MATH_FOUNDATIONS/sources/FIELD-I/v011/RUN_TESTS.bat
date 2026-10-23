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
python ..\v008\field8.py > output\field8_rerun.txt 2>&1
if errorlevel 1 set RC=1
python ..\v009\field9.py > output\field9_rerun.txt 2>&1
if errorlevel 1 set RC=1
python ..\v010\field10.py > output\field10_rerun.txt 2>&1
if errorlevel 1 set RC=1
python field11.py > output\field11_output.txt 2>&1
if errorlevel 1 set RC=1
echo exit code %RC%  (0 = no FAIL in field2, g_checks, field3 .. field11)
findstr /B /C:"FAIL" output\field2_rerun.txt output\g_checks_rerun.txt output\field3_rerun.txt output\field4_rerun.txt output\field5_rerun.txt output\field6_rerun.txt output\field7_rerun.txt output\field8_rerun.txt output\field9_rerun.txt output\field10_rerun.txt output\field11_output.txt
findstr /C:"ALL PASS" /C:"SOME FAIL" /C:"FAIL," /C:"summary" output\field2_rerun.txt output\g_checks_rerun.txt output\field3_rerun.txt output\field4_rerun.txt output\field5_rerun.txt output\field6_rerun.txt output\field7_rerun.txt output\field8_rerun.txt output\field9_rerun.txt output\field10_rerun.txt output\field11_output.txt
rem FIELD11_QUICK=1 shortens field11.py only (set FIELD11_QUICK=1 before running).
endlocal & exit /b %RC%
