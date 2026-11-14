#!/bin/sh
# Reproduce all checks, tables and figures.  From the package root:  sh code/run_all.sh
set -e
cd "$(dirname "$0")"
python3 verify_graph_geometry.py
python3 make_tables.py
python3 make_figures.py
