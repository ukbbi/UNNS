# GEO-I v008 — Small-Box Geometry and Minimal Obstruction Theorems

*Convex coverage, exceptional homology, and binary rank rigidity.*  Baseline: GEO-I v007 (kept frozen; its documents are in `docs_v007/`, v006 in `docs_v006/`).

## What this release is

A focused attempt on the two remaining parts of the planar/binary theory, with the release discipline that **nothing earlier is rewritten**: new deductions and corrections are documented separately (MATHEMATICS.md §4), disproved conjectures (HYP-LL, q_i>o_i ⇒ β₁=0, …) stay recorded, and GitHub / SELECT-I/II / FIELD-I / the Foundations volumes are untouched.

## Headline results (see REPORT.md for statuses and the honest limits)

* **G8-T1 (filling lemma, proved):** both hollow-box holes (G7-T3) are filled by explicit Graver parallelograms as soon as the box is enlarged in either direction; the topology of the exceptional box dies at the *first* step.
* **G8-S (proved):** the squareless small boxes are exactly the region under the staircase of record minima of `s·i mod d`; closed formula reproduces v007's 29,890.
* **G8-R1 (proved, conditional on G8-T2):** hollow-box structure ⇒ the whole square hull is covered in every larger box. Remaining geometry of G8-C1 is the cap beyond the square.
* **Binary rank:** B-LOW (`r_min ≥ 3`, proved), B-COMMON (a mechanism for rank 3), B-NULL′ (any collision ⇒ nullity ≥ 3), B-BASIS, B-SERIES (blow-up reduction); the complete classification of minimal boxes of nullity 3 and 4 (all `n`) with `r_min = 3`; the `RM(1,k−1)` infinite family; complete censuses `n ≤ 9`.
* **Still open:** G8-C1 (small-box coverage), G8-T2/G8-C2 (exact hollow topology), G8-C3/G8-T3 (full-support collision, `r_min ≤ 3` in general). No counterexample to any of them was found.

## Layout

```
README.md REPORT.md MATHEMATICS.md SMALL_BOX.md HOLLOW.md MINIMAL_RANK.md CERTIFICATION.md PRIOR_ART.md
theory/        v008: small_box.py cell_cover.py hollow.py binary_min.py rank_reduce.py   (+ v005–v007 modules, provenance in PROVENANCE.json)
experiments/   v008: small_attack.py hole_death.py rank_attack.py common_base.py make_certificates_v8.py figures_v8.py  (+ earlier experiments)
certificates/  checker8.py (standalone) C1_cover C2_gap C3_homology C4_rank (+ v007 D1–D5, checker.py)
geometry/ topology/ frozen/   inherited libraries (hash-checked)
tests/         test_geo8.py check_nullity_classification.py (+ test_geo6/7)
figures/       fig1…fig7 (exact data; fig6 left panel labelled ILLUSTRATIVE)
output/data/   v8_* data records;  output/reports/ verifier reports
verify.py  RUN_SMOKE.bat  RUN_FULL.bat  MANIFEST.sha256  PROVENANCE.json
```

## Running

Python 3.10+, `gmpy2` (optional but faster), `matplotlib` only for figures.
`python verify.py --smoke` (several minutes; the inherited v005 regression dominates) · `python verify.py` (full) · `python certificates/checker8.py certificates/C*.json` · `python tests/test_geo8.py`.
The verifier reports **v008 new checks**, **inherited v007 re-runs** and **inherited v005/v006 regressions** separately; earlier verifier counts are never re-counted as v008 tests. A computation that cannot run is reported UNAVAILABLE, never PASS.
