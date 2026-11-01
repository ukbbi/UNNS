@echo off
setlocal
set MODE=--fast
if /I "%1"=="full" set MODE=--full
for %%S in (X0 X1 X2 X3 X4 X5 X6 X7) do (
  echo === stage %%S ===
  python RUN_VERIFY.py %MODE% --shard %%S
  if errorlevel 1 ( echo STAGE %%S FAILED & exit /b 1 )
)
echo ALL STAGES PASSED
endlocal
