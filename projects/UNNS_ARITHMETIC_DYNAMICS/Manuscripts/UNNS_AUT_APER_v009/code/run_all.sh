#!/bin/sh
set -e
cd "$(dirname "$0")"
python3 reduction_check.py; python3 register_cycles.py; python3 mechanism_check.py
python3 orbit_predictions.py >/dev/null; python3 program_table.py >/dev/null; python3 worked_table.py >/dev/null; python3 figures.py >/dev/null
echo ALL_CHECKS_OK
