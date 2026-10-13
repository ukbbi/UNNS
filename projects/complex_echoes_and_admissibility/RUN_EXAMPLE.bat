@echo off
REM ESC-I v0.1 - run the built-in suite, then open the chamber.
cd /d "%~dp0"
where python >nul 2>nul && (python esc_i.py --suite --out output) || (py esc_i.py --suite --out output)
if errorlevel 1 (echo Python 3 was not found. Install it from python.org, then run this again. & pause & exit /b 1)
where python >nul 2>nul && (python admissibility.py --out output) || (py admissibility.py --out output)
start "" "%~dp0chamber.html"
echo.
echo Reports: %~dp0output\report.md, theorem_audit.md, admissibility_rules.md, admissibility_report.json
echo Single case example: python esc_i.py --matrix 1 1 0 1 --x0 0 1
pause
