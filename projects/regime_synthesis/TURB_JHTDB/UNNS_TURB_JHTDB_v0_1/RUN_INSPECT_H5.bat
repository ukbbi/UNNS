@echo off
setlocal
cd /d "%~dp0"

echo UNNS TURBULENCE - HDF5 SOURCE INSPECTION
echo.

py -c "import h5py, numpy" >nul 2>&1
if errorlevel 1 (
  echo Required Python packages are missing.
  echo Installing h5py and numpy...
  py -m pip install h5py numpy
  if errorlevel 1 (
    echo.
    echo INSTALLATION FAILED.
    pause
    exit /b 1
  )
)

if "%~1"=="" (
  py "%~dp0tools\validate\inspect_velocity_h5.py"
) else (
  py "%~dp0tools\validate\inspect_velocity_h5.py" "%~1"
)

if errorlevel 1 (
  echo.
  echo INSPECTION FAILED.
  pause
  exit /b 1
)

echo.
echo INSPECTION COMPLETE.
echo Upload outputs\records\H5_REPORT.json and H5_TREE.txt to ChatGPT.
pause
