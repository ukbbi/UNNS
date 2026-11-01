@echo off
REM GEO-HD-1D v001 - staged verification (each stage is short). Usage: RUN_WINDOWS.bat [full]
setlocal
set MODE=--fast
if /I "%1"=="full" set MODE=--full
for %%S in (V0 V1 V2 V3 V4 V5 V6 V7 V8 V9) do (
  echo === stage %%S ===
  python RUN_VERIFY.py %MODE% --shard %%S
  if errorlevel 1 ( echo STAGE %%S FAILED & exit /b 1 )
)
echo ALL STAGES PASSED
endlocal
