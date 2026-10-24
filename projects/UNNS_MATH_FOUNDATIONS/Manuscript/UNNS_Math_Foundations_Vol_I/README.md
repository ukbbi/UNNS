# The Mathematical Foundations of the UNNS Substrate — Volume I
**Generative Arithmetic and Structural Reachability** · 35 pages · 11 figures · 23 October 2026

The volume develops the arithmetic and generative foundations of the UNNS Substrate: the structure carried by the nest rule M(N+1)²/N and by the generative systems built on it, with theorems on fibres, collective rendezvous, rigidity, continuation orders, the integer graph, histories, and the incompatibility of three continuation constraints.

## Contents
- `UNNS_Math_Foundations_Vol_I.pdf` / `.tex` — the manuscript (seven chapters, five appendices, figures)
- `figs/`, `figure_sources/mkfigs.py` — figures; data figures are generated from exact integer computation
- `THEOREM_CROSSWALK.tsv` — the 60 registry records assigned to this volume
- `AUDIT.tsv` — where each record stands in the text and how it is proved (also Appendix D)
- `check_volume_i.py` (+ `checks_base.py`) — exact-integer verification: 18 additional checks, then 15 base checks; 33 PASS, 0 FAIL
- `SHA256_MANIFEST.sha256`

## Rebuild
```
pdflatex -interaction=nonstopmode -halt-on-error UNNS_Math_Foundations_Vol_I.tex   (twice)
python check_volume_i.py
python figure_sources/mkfigs.py     # optional; needs matplotlib; run from this folder
```
Requires LaTeX packages: amsmath, amssymb, amsthm, mathtools, hyperref, booktabs, longtable, microtype, fancyhdr, geometry, enumitem, lmodern, graphicx, tikz, caption.
