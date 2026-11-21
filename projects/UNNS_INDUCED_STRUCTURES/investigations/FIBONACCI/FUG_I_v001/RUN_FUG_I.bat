@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 scripts\fug_i.py && py -3 scripts\verify.py
) else (
    python scripts\fug_i.py && python scripts\verify.py
)
if errorlevel 1 (
    echo.
    echo FUG-I verification failed.
    exit /b 1
)
echo.
echo FUG-I v001 completed successfully.
