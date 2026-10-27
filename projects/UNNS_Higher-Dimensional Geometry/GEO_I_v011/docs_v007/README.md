# GEO-I v007 — Structural Closure of Modular Geometry

Uniform covering theorems, binary obstruction rank, and exceptional (hollow-box) topology. Self-contained; Python 3.10+, `gmpy2` (`pip install gmpy2`), `matplotlib` only for figures.

## Quick start
```
python3 verify.py --smoke     # Level 1, a few minutes
python3 verify.py             # Level 1 + Level 2 (full)
python3 certificates/checker.py certificates/D1_coverage.json certificates/D2_rank.json certificates/D3_hollow.json
python3 tests/test_geo7.py
```
Windows: `RUN_SMOKE.bat`, `RUN_FULL.bat`.

## Main results
* **Theorem A-COL** (G7-T1): `U = conv(F)` for every `d ≥ 2`, every unit `s`, every box with `max(Q) ≥ 2d` — PROVED+CHECKED (`COVERAGE.md`). G7-C1 is reduced to the small boxes; OPEN there.
* **Theorem G7-T3**: the hollow box `(d,d)` has `β₁ ≥ 2` for all `d ≥ 3`, all units `s` — PROVED+CHECKED (`HOLLOW_TOPOLOGY.md`).
* **Binary theory** (`BINARY_RANK.md`): coset description of cells, rank = generator rank, nullity ≥ 3 for full-support collisions, exact `(2,2)` rank criterion. `r_min ≤ 3` still OPEN; 1, 3, 50, 2983, 5902 minimal boxes for `n = 4..8` (n = 8 restricted), all of minimum rank 3.
* **Certificates** with an independent standalone checker (`CERTIFICATION.md`).

## Layout
`COVERAGE.md REPORT.md MATHEMATICS.md BINARY_RANK.md HOLLOW_TOPOLOGY.md CERTIFICATION.md PRIOR_ART.md` — documents. `theory/` (`corner_sail.py` = column-strip construction, `coverage_lemmas.py`, `binary_circuits.py`, `centre_collisions.py`, `rank_reduction.py`, `hollow_geometry.py`, plus inherited v005/v006 modules listed in `PROVENANCE.json`). `experiments/` (`coverage_attack.py`, `rank_counterexamples.py`, `hollow_attack.py`, `band_hulls.py`, `make_certificates_v7.py`, `figures_v7.py`, inherited scripts). `certificates/` (D1–D5 + `checker.py`). `figures/` (7 figures; Fig 4 and Fig 7 are marked ILLUSTRATIVE). `output/data` (records), `output/reports` (verifier reports). `docs_v006/` (the two v006 documents kept unchanged). `MANIFEST.sha256`, `PROVENANCE.json`.

## What is NOT claimed
No proof of coverage for the squareless small boxes; no proof of `r_min ≤ 3`; no proof of the hollow-box upper bound; no novelty claim relative to the literature (`PRIOR_ART.md`). Restricted censuses are labelled restricted; shipped records are distinguished from regenerated computations in `verify.py`.
