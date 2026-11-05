# PAPER_III_EVOLUTION v0.4

Manuscript III of the GEO-HD-1 programme: *Geometric Evolution under Collective UNNS Dynamics: Activation, Events, and Topological Prediction*. Author: UNNS Research Collective. Version 0.4. Baselines: Paper I v0.4, Paper II v0.4.

## Contents
- `PAPER_III_EVOLUTION_v0.4.pdf` - compiled manuscript (searchable).
- `tex/` - LaTeX sources (`main.tex`, `sections/`, `appendices/`, `refs.tex`, generated `tables/`).
- `figures/` - the 26 figures (PDF); `scripts/` - engine, computations, figure scripts, build.
- `results/` - JSON/log outputs of the computations quoted in the text.
- `crosswalk/PAPER_III_THEOREM_MAP.tsv` - derived theorem map for the 73 allocated records; `crosswalk/CROSSWALK_OBSERVATIONS.md`.
- `checks/check_paper_III.py` - manuscript-quality and spot checks (stdlib only). It is not an independent verification of the mathematics.
- `data/ALLOCATION_III.tsv` - the 73 allocated source rows (copy; the frozen 518-row crosswalk is not modified).

## Build
`scripts/build_paper.sh` removes all auxiliary files, regenerates the appendix tables (`scripts/gen_app.py`), builds the theorem-map appendix from the provenance file written by the compile, and runs pdflatex four times. Requires pdflatex and python3. Figures: `figs_a.py`, `figs_b.py`, `figs_c.py` (need matplotlib; not needed to build the PDF).

## Reproducing results
`scripts/c1_traj.py` (trajectories), `c2_tower.py 5|11 140` (towers), `c3_census.py` (census), `c4_event.py` (next-event and graph-level tests), `c5.py`-`c9_b2.py`, `xcheck_KD.py` (182-state cross-check). All use the stdlib engine `eng3.py`.

## NOT_RERUN
Inherited verifier suites and censuses are cited, not re-run: the 993-pair reachability table and its 24 resolved cases; the k=2 family scans; the 474 step-activation events; the 1,920-orbit G census; the B-T11 sample; the B-T10 ruler-function and rank claims; B2-T5; B2-T11 (16,028 pairs); B2-T14 loss-budget blindness; R3-T3, R3-T3', R3-T4 and A4-T7 (Paper II); the 1,783-state K(D) check; FIELD-I T32/T51. The programme sources are cited at their pinned commits and were not re-fetched.

## Scope
Finite-exact results are stated with their ranges and are not extrapolated. No universal organising law is claimed; Papers I-III prepare Manuscript IV.
