# GEO-I v006 — Uniform Laws of Higher-Dimensional Arithmetic Geometry: Modular Stabilization, Obstruction Rank, and Effective Certification

Release date 25 Oct 2026. Builds on GEO-I v001–v005 (unchanged). Python 3.10+, `gmpy2`; `matplotlib` only to redraw figures.

## Headline results (labels: PROVED / PROVED+CHECKED / CHECKED / FALSE / OPEN / UNAVAILABLE)
1. **G6-C1 — stabilization for every unit s: CHECKED for all (d,s) with 2 ≤ d ≤ 30, OPEN beyond; not proved for all d.** The stabilization search is extended from D* = 21 to D* = 30 (complete base window, exact arithmetic, 0 unresolved boxes). For boxes with max(Q) ≥ 2d an explicit family of cells (squares, corner sails, chain cells) covers conv(F) exactly in every instance; the all-parameter covering lemma is *not* proved (STABILIZATION.md §3).
2. **G6-C2 — hollow box for s ≢ −1: CHECKED.** conv(F)∖U = two open triangles of area d/2 (d ≤ 45), β₁ = 2 (d ≤ 20); the triangle boundaries lie in U (PROVED).
3. **G6-C3 — minimum witness span ≤ 3: OPEN, no counterexample.** New exact theory for 0/1 boxes of binary lattices (cells = disjoint circuits; centre criterion, PROVED) and a complete census: every minimal box for n ≤ 6 coordinates, and the stated subfamilies for n = 7, 8, has minimum span exactly 3. Individual witnesses of span 4–6 occur (parity lattices) but do not affect the minimum.
4. **Certification:** finite reduction + explicit covers of size ~10–50 cells instead of 250–1900 generic 2-cells; centre criterion for binary 0/1 boxes. A general arithmetic criterion remains OPEN.

## Layout
`REPORT.md` (results, gates, honest limits) · `MATHEMATICS.md` (registry) · `STABILIZATION.md` · `OBSTRUCTION_RANK.md` · `CERTIFICATION.md` · `PRIOR_ART.md` · `theory/` (new: `modular_layers.py`, `small_boxes.py`, `binary_01.py`; inherited from v005 with hashes in `PROVENANCE.json`) · `geometry/ topology/ frozen/` (inherited, unchanged) · `experiments/` (new: `window_full.py`, `general_s.py`, `hollow_check.py`, `binary_rank_search.py`, `cert_benchmark.py`, `figures_v6.py`; inherited v005 scripts) · `tests/` (`test_geo6.py` new; v003–v005 tests inherited) · `regression_v005.py` (v005 verifier, gate G1) · `figures/` (6 figures from exact data) · `output/data|reports|certificates` · `verify.py` · `RUN_SMOKE.bat` · `RUN_FULL.bat` · `MANIFEST.sha256`.

## Verify
`python3 verify.py --smoke` (a few minutes) · `python3 verify.py` (full). Core checks use only this folder (no sibling releases). Items not run are reported UNAVAILABLE, never PASS.
