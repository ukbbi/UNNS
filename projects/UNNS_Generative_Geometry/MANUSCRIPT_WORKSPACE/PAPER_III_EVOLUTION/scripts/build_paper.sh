#!/usr/bin/env bash
# Fresh build of Paper III v0.4: removes every auxiliary file, regenerates appendix data, runs pdflatex four times.
set -e
export SOURCE_DATE_EPOCH=1793577600 FORCE_SOURCE_DATE=1   # reproducible PDF bytes
cd "$(dirname "$0")/../tex"
rm -f main.aux main.log main.out main.toc main.prov main.pdf appmap_table.tex
python3 ../scripts/gen_app.py
python3 ../scripts/make_appmap.py --placeholder
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
python3 ../scripts/make_appmap.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
mv main.pdf ../PAPER_III_EVOLUTION_v0.4.pdf   # single PDF in the package
python3 ../scripts/finalize_status.py
echo "built: PAPER_III_EVOLUTION_v0.4.pdf"
