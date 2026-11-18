# UNNS Intrinsic–Selected Hierarchy — v1.4 (editorial)

14 November 2026. Built from `UNNS_Intrinsic_Selected_v1_4.tex` (pdflatex twice). v1.3 and earlier are unchanged.

## Changes from v1.3 (no mathematical statement changes)
1. Cross-references written explicitly (`Definition~\ref{…}`, `Corollary~\ref{…}`, …); `cleveref` removed. Fixes "Theorem 2.2 / 4.2 / 5.6 / Theorems 6.1 and 6.2" labels that appeared in some builds.
2. `\vv` defined with `\providecommand` before `\renewcommand`, so the source builds with or without newtx.
3. Figure 3 and Appendix C: CC BY-SA 4.0 attribution completed (title, author, licence link, statement of cropping).
4. Figure 3: label "27" moved off the axis tick.

PDF font note: the supplied PDF was built with lmodern+mathptmx (newtx not installed in the build environment); the source uses newtx automatically when available.
Checks: `check_examples.py`, `check_projection.py`, `verify_figures.py` (unchanged, all pass). `patch14.py` records the exact edits from v1.3.
