@echo off
setlocal EnableExtensions

set REPO=https://github.com/gaearon/conway-refinement.git
set SHA=264445c93b78554c408e99e4e7f663693b4e91ab
set DIR=CONWAY_VERIFY_TMP

where git >nul 2>nul || (
  echo ERROR: git is required.
  exit /b 1
)

where lake >nul 2>nul || (
  echo ERROR: lake is required. Install the Lean toolchain first.
  exit /b 1
)

if exist "%DIR%" rmdir /s /q "%DIR%"
git clone "%REPO%" "%DIR%" || exit /b 1
cd /d "%DIR%" || exit /b 1
git checkout --detach "%SHA%" || exit /b 1

for /f %%i in ('git rev-parse HEAD') do set ACTUAL=%%i
if /I not "%ACTUAL%"=="%SHA%" (
  echo ERROR: wrong checkout: %ACTUAL%
  exit /b 1
)

echo === PINNED COMMIT ===
git rev-parse HEAD
type lean-toolchain

echo === UPDATE / FETCH DEPENDENCIES ===
lake update || exit /b 1

echo === FULL BUILD ===
lake build || exit /b 1

echo === STATEMENT COMPATIBILITY ===
lake exe palomar-compatibility || exit /b 1

echo === AXIOM AUDIT ===
lake exe axioms || exit /b 1

echo === MODULE SYSTEM ===
lake exe module-system || exit /b 1

echo === STANDALONE MATHLIB ===
lake exe standalone-mathlib || exit /b 1

echo === STANDALONE COMBINATORIALGAMES ===
lake exe standalone-combinatorial-games || exit /b 1

echo === PROOF LINKS ===
lake exe proof-links || exit /b 1

echo.
echo CONWAY VERIFICATION BUILD PASSED AT %SHA%
exit /b 0
