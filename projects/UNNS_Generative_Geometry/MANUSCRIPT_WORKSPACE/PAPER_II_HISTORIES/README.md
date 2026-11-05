# PAPER_II_HISTORIES v0.1
Manuscript II of GEO-HD-1: Generative Histories, Arithmetic Recombination, and Higher-Dimensional Route Topology. Author line: UNNS Research Collective.
Build: `bash scripts/build_paper.sh` (needs pdflatex; figures in `figures/`, regenerate with `scripts/figs_a.py figs_b.py figs_c.py`). Checks: `python3 checks/check_paper_II.py`.
Exact engine: `scripts/engine.py`, `swaps.py`, `topo.py`, `rewrite.py`; computations `compute_all.py`, `compute_part2..8.py`, `cubes4.py`; outputs in `results/`.
Inherited verification of the source releases: NOT_RERUN (only the statements marked finite-exact in the text were recomputed here; items marked cited were not).
Limits: same-author work; no novelty claim; statements for k-label census, loop converse 4<=N<M<=60, 498/816 deficient fibres, and births/losses table are cited, not re-run.
