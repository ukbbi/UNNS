#!/bin/sh
# Reproduce everything: verification, figures, tables, PDF. Run from this directory.
set -e
python3 verify_graph_ent.py
python3 make_figures.py
python3 make_tables.py
cd ../manuscript && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex && cp main.pdf unns_graph_entropy_v1_5.pdf && cp main.pdf ../unns_graph_entropy_v1_5.pdf
