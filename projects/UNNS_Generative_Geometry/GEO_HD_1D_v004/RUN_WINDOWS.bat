@echo off
setlocal
set MODE=--fast
if /I "%1"=="full" set MODE=--full
for %%S in (Y0 Y1 Y2 Y3 Y4 Y5 Y6 Y7) do (
  echo === stage %%S ===
  python RUN_VERIFY.py %MODE% --shard %%S
  if errorlevel 1 ( echo STAGE %%S FAILED & exit /b 1 )
)
echo ALL STAGES PASSED
endlocal
