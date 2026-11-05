# PAPER_IV_SYNTHESIS v0.5
The Geometry of Generation in the UNNS Substrate: A Mathematical Synthesis — UNNS Research Collective.

## Contents
- PAPER_IV_SYNTHESIS_v0.5.pdf — searchable manuscript (the single root PDF)
- tex/ — LaTeX sources (main.tex, sections/, appendices/, refs.tex, generated xref.tex and tables/)
- figures/ — fig01..fig22 PDFs; scripts/figs_*.py are their exact sources
- crosswalk/ — PAPER_IV_SOURCE_MAP.tsv, SYNTHESIS_PROPOSITIONS.tsv, MODEL_COMPATIBILITY.md
- checks/check_paper_IV.py — integrity checks (run from the package root: python3 checks/check_paper_IV.py)
- results/ — recorded computations; scripts/ — recomputation and build scripts
- STATUS.json — build status and PDF SHA-256

## Rebuild
`./scripts/build_paper.sh` (needs pdflatex, python3 with matplotlib).

## Limits
- The checker tests manuscript integrity; it is not independent certification of the mathematics.
- Verification inherited from Papers I-III (v0.4) is NOT_RERUN; only the witnesses and lemma checks listed in the manuscript were recomputed here.
- Finite-exact results are stated for their checked ranges and not extrapolated.
- C3 is unclaimed. No universal law is claimed.
- The source repository was read-only.
- Open questions O1-O8 each list the nearest proved theorem and the missing obligation.
