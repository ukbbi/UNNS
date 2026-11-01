@echo off
setlocal
set MODE=--fast
if /I "%1"=="full" set MODE=--full
for %%S in (Z0 Z1 Z2 Z3 Z4 Z5 Z6 Z7) do (
  echo === stage %%S ===
  python RUN_VERIFY.py %MODE% --shard %%S
  if errorlevel 1 ( echo STAGE %%S FAILED & exit /b 1 )
)
echo ALL STAGES PASSED
endlocal
