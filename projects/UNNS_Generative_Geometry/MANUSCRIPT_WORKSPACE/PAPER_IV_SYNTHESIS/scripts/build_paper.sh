#!/usr/bin/env bash
# Fresh build of Paper IV v0.4: regenerates cross-reference macros, registers and tables from the exact sources, then runs pdflatex four times.
set -e
export SOURCE_DATE_EPOCH=1793577600 FORCE_SOURCE_DATE=1   # reproducible PDF bytes
HERE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$HERE/scripts"
python3 gen_xref.py
python3 gen_registers.py
python3 gen_app.py
cd "$HERE/tex"
rm -f main.aux main.log main.out main.toc main.pdf
for i in 1 2 3 4; do pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null; done
mv main.pdf ../PAPER_IV_SYNTHESIS_v0.5.pdf
python3 ../scripts/finalize_status.py
echo "built: PAPER_IV_SYNTHESIS_v0.5.pdf"
