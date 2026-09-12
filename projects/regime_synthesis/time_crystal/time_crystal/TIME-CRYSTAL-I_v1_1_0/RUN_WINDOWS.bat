@echo off
setlocal
cd /d "%~dp0"

set PHYS=..\TC_PHYS_v001
set CLOSURE=..\TC_CLOSURE_v001
set MI=..\TC_EXT_MI_v001
set CTRL=..\TC_CTRL_v001
set RIGIDITY=..\TC_RIGIDITY_v001
set COLLECTIVE=..\TC_COLLECTIVE_v001

if not exist "%PHYS%\outputs\physics_validation.json" set PHYS=..\TC_PHYS_v001.zip
if not exist "%CLOSURE%\outputs\closure_result.json" set CLOSURE=..\TC_CLOSURE_v001.zip
if not exist "%MI%\outputs\external_validation.json" set MI=..\TC_EXT_MI_v001.zip
if not exist "%CTRL%\outputs\control_validation.json" set CTRL=..\TC_CTRL_v001.zip
if not exist "%RIGIDITY%\outputs\rigidity_result.json" set RIGIDITY=..\TC_RIGIDITY_v001.zip
if not exist "%COLLECTIVE%\outputs\collective_result.json" set COLLECTIVE=..\TC_COLLECTIVE_v001.zip

for %%P in ("%PHYS%" "%CLOSURE%" "%MI%" "%CTRL%" "%RIGIDITY%" "%COLLECTIVE%") do (
  if not exist %%P (
    echo ERROR: Missing required sibling artifact %%P
    pause
    exit /b 1
  )
)

echo Running chamber unit tests...
python -m unittest discover -s tests -p "test_*.py"
if errorlevel 1 (
  echo UNIT TESTS FAILED.
  pause
  exit /b 1
)

echo.
echo Running initial validation corpus...
python run_chamber.py "%PHYS%" "%CLOSURE%" "%MI%" "%CTRL%" "%RIGIDITY%" "%COLLECTIVE%" outputs
if errorlevel 1 (
  echo CHAMBER VALIDATION FAILED.
  pause
  exit /b 1
)

echo.
echo TIME-CRYSTAL-I v1.0.0 validation complete.
echo Opening HTML chamber interface...
start "" "TIME-CRYSTAL-I.html"
echo.
echo See outputs\RUN_LOG.txt and outputs\validation_results.json
pause
