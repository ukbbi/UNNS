@echo off
cd /d %~dp0
if "%1"=="test" (python -m unittest discover -s TESTS & goto :eof)
python EXPERIMENTS\run_all.py
python -m unittest discover -s TESTS
python EXPERIMENTS\make_manifest.py
