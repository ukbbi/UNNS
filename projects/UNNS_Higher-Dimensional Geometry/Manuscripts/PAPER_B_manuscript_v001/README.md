# PAPER_B_manuscript_v001
Universal Rank-Three Obstructions in Binary Arithmetic Occurrence Geometry (GEO-I Milestone II), author line: UNNS Research Collective.

Contents
- PAPER_B_manuscript_v001.pdf  searchable PDF (compiled from tex/main.tex)
- tex/        LaTeX sources, figures/ (14 PDFs + figure_data.json), refs.tex (bibliography)
- scripts/    independent engine geo2.py, classify.py, crosscheck.py, lit_checks.py, verify6.py, small_p.py, inv6*.py, equiv6.py, gen_tables.py, figs.py (+fig14.dot), verify_all.sh
- logs/       outputs of all computations; src/ release certificates + checkers used
- theorem_source_registry.tsv, VERIFICATION_REPORT.md, MANIFEST.sha256

Rebuild: `cd scripts && ./verify_all.sh` (acceptance gate, ~25 s, exits non-zero on any failure), then `python3 gen_tables.py && python3 figs.py`, then `pdflatex main.tex` x3 in tex/.
Scope: frozen binary 0/1 Graver-cell model only. Paper A and the GEO-I releases (commit 343f9aef2b6697466058165c5fc2ddf0f00e882b) were not modified. Releases are archived research releases, not peer-reviewed.
