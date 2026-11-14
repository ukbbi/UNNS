#!/bin/sh
set -e
cd "$(dirname "$0")"
python3 code/verify_prime_dyn.py | tee reports/verifier_stdout.txt
python3 code/make_figures.py
python3 code/make_tables.py
cd manuscript && for i in 1 2 3; do pdflatex -interaction=nonstopmode main.tex >/dev/null; done
cp main.pdf ../unns_prime_valuation_dynamics_v1_2.pdf
