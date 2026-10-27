@echo off
python verify.py
python experiments\make_figures.py
python experiments\export_data.py
pause
