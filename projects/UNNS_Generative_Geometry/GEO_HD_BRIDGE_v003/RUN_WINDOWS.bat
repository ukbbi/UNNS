@echo off
cd /d "%~dp0"
set PYTHONDONTWRITEBYTECODE=1
for %%S in (Z0 Z1 Z2 Z3 Z4 Z5 Z6 Z7) do (
  echo == %%S ==
  python RUN_VERIFY.py --shard %%S
  if errorlevel 1 goto fail
)
echo ALL SHARDS PASSED
exit /b 0
:fail
echo FAILURE
exit /b 1
