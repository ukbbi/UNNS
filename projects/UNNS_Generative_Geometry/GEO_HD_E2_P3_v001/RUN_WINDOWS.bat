@echo off
REM E2-P3 verification (Windows).  Extract GEO_HD_E2_P3_v001.zip into GEO_HD_1_PROJECT, then double-click.
cd /d "%~dp0"
python -I RUN_VERIFY.py --fast
if errorlevel 1 ( echo VERIFY FAILED & exit /b 1 )
echo.
echo Optional full re-derivation of every row:  python -I RUN_VERIFY.py --full
echo Optional rebuild (about 15-30 minutes):    python src\build_p3.py --out rebuild_out
pause
