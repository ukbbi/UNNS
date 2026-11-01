@echo off
setlocal
set MODE=--fast
if /I "%1"=="full" set MODE=--full
for %%S in (W0 W1 W2 W2b W3 W4 W5 W6) do (
  echo === stage %%S ===
  python RUN_VERIFY.py %MODE% --shard %%S
  if errorlevel 1 ( echo STAGE %%S FAILED & exit /b 1 )
)
echo ALL STAGES PASSED
endlocal
