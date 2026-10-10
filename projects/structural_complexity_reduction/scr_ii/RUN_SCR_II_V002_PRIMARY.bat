@echo off
setlocal
cd /d "%~dp0"
echo [SCR-II v002 PRIMARY] Outcome-bearing run.
echo [SCR-II v002 PRIMARY] This exposes the frozen 30-instance primary grid.
echo [SCR-II v002 PRIMARY] Completed cells are checkpointed and the final result cannot be rerun.
python scripts\run_v002_primary.py
set RC=%ERRORLEVEL%
if not "%RC%"=="0" echo SCR-II v002 primary exited with code %RC%.
pause
exit /b %RC%
