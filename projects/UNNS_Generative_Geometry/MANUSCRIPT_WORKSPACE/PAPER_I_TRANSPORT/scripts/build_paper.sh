#!/usr/bin/env bash
# Fresh build of Paper I v0.4: removes every auxiliary file, then runs pdflatex four times.
# The theorem map (appendix) is generated from the provenance records written by \prov during
# pass 1 (main.prov) into appmap_table.tex. The bibliography is a thebibliography environment
# (no BibTeX run). Figures are taken from ../figures (regenerate with scripts/make_figures_v02.py).
set -e
cd "$(dirname "$0")/../tex"
rm -f main.aux main.log main.out main.toc main.prov main.pdf appmap_table.tex
python3 ../scripts/make_appmap.py --placeholder
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
python3 ../scripts/make_appmap.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
cp main.pdf ../PAPER_I_TRANSPORT_v0.4.pdf
echo "built: PAPER_I_TRANSPORT_v0.4.pdf"
