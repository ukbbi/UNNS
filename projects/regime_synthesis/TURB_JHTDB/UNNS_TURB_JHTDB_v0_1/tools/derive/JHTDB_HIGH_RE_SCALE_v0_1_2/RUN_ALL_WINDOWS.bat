@echo off
setlocal EnableExtensions
cd /d "%~dp0"
call VERIFY_SOURCE_WINDOWS.bat || exit /b 1
call RUN_ADAPTER_WINDOWS.bat || exit /b 1
call RUN_ROUTE_AND_EXTRACT_WINDOWS.bat || exit /b 1
echo.
echo [COMPLETE] HIGH-RE SCALE STAGE FINISHED.
pause
