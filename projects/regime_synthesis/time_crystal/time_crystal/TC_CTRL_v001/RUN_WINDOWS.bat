@echo off
setlocal
cd /d "%~dp0"

if exist "..\TC_CLOSURE_LOCK_v001\LOCK.json" (
    python run_controls.py "..\TC_CLOSURE_LOCK_v001" outputs
    goto :done
)

if exist "..\TC_CLOSURE_LOCK_v001.zip" (
    python run_controls.py "..\TC_CLOSURE_LOCK_v001.zip" outputs
    goto :done
)

echo ERROR: TC_CLOSURE_LOCK_v001 was not found beside this package.
echo Expected either:
echo   ..\TC_CLOSURE_LOCK_v001\
echo or:
echo   ..\TC_CLOSURE_LOCK_v001.zip
pause
exit /b 1

:done
if errorlevel 1 (
    echo.
    echo TC_CTRL_v001 failed.
    pause
    exit /b 1
)

echo.
echo TC_CTRL_v001 finished.
echo See outputs\RUN_LOG.txt and outputs\control_validation.json
pause
