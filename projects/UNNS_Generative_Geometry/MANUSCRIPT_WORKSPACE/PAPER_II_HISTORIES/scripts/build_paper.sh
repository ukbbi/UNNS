#!/usr/bin/env bash
# Fresh build of Paper II v0.4: removes every auxiliary file, then runs pdflatex four times.
set -e
cd "$(dirname "$0")/../tex"
rm -f main.aux main.log main.out main.toc main.prov main.pdf appmap_table.tex
python3 ../scripts/make_appB_data.py
python3 ../scripts/make_appmap.py --placeholder
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
python3 ../scripts/make_appmap.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
cp main.pdf ../PAPER_II_HISTORIES_v0.4.pdf
echo "built: PAPER_II_HISTORIES_v0.4.pdf"
