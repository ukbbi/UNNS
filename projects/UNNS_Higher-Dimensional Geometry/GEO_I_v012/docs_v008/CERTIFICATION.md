# GEO-I v008 — Programme D: certificates, validation paths, cost

Four reviews are kept **separate**: (1) *proof review* — the arguments in MATHEMATICS/SMALL_BOX/HOLLOW/MINIMAL_RANK, read by a human; (2) *exact recomputation* — `theory/` and `experiments/` regenerate data in exact integer/rational arithmetic; (3) *certificate verification* — `certificates/checker8.py`, a standalone program (standard library only, imports nothing from this release, run with `python3 -I`); (4) *integrity checking* — `MANIFEST.sha256` and `PROVENANCE.json`. A passing certificate check never validates a universal proof.

## 1. Certificate kinds (checker8.py)

| Kind | File | What the checker recomputes | A VALID certificate shows |
|---|---|---|---|
| **COVER** | `C1_cover.json` (14 boxes: bottom, left, interior; squareless and non-squareless; `d = 7..13`) | `F`, `conv(F)` vertices (must equal the claimed exact hull), Graver property of every generator, corners in `F`, cell incidence, every piece convex and inside its cell, pairwise disjoint interiors, area sum `= area(conv F)` | `conv(F) ⊂ U` for that box |
| **GAP** | `C2_gap.json` (hollow boxes `(d,d)`, 10 types) | `F`, hull, **all** Graver segments and **all** Graver parallelograms with corners in `F`; exact point `z` | `z ∈ conv(F)` and `z ∉ U`: `U ≠ conv(F)`. Applied to a small box a VALID GAP is a **decisive counterexample** to G8-C1; none exists |
| **HOMOLOGY** | `C3_homology.json` (8 planar complexes of `U`: hollow boxes and their enlargements) | face walks lie on listed edges, `∂1∂2 = 0` (computed), each edge in ≤ 2 faces, ranks over `Q`, Betti numbers, Euler–Poincaré `V−E+F = b0−b1+b2` | the Betti numbers of the **supplied** complex. That the complex is the planar subdivision of `U` is a COVER/arrangement statement, not certified here |
| **RANK** | `C4_rank.json` (8 boxes from the nullity-3/4 classification and blow-ups, `n ≤ 10`) | codewords, circuits, cells as (circuit partition, coset), all collisions, all deletions, ranks (exact Gaussian elimination over `Q`), shared point `z`, nullity and series-class count | box minimal non-embedded, min rank as claimed, nullity ≥ 3 |
| D1_coverage, D2_rank, D3_hollow | v007 files, unchanged | as in v007 | accepted by `checker8.py` too |

A **RANK counterexample** to `r_min ≤ 3` would additionally need the complete exclusion of all witnesses of rank ≤ 3; the checker recomputes *all* witness ranks, so a claimed `min_rank = 4` is rejected if any rank-3 witness exists (`tests/test_geo8.py` tests the rejection of a wrong `min_rank`).

## 2. Failure behaviour (tests/test_geo8.py)

Rejected with a reason: a COVER with a tampered piece, a tampered hull, a non-Graver generator; a GAP point outside the hull, and the hollow-box GAP after enlarging the box (the hole is filled, G8-T1); a HOMOLOGY with wrong Betti numbers or a broken face cycle; a RANK with wrong `min_rank`, wrong nullity, or an embedded box.

## 3. Reproducibility

Deterministic: no random seeds in v008 code except `verify.py` samples drawn with fixed seeds (`random.Random(6)`, `Random(77)`, `Random(1)`, …). No wall-clock timeouts decide a result: a computation that does not finish is reported **UNAVAILABLE**. `RUN_SMOKE.bat` / `RUN_FULL.bat` call `verify.py`; check names say REGENERATED or SHIPPED.

## 4. Cost accounting

`output/data/v8_cost.json` records wall-clock seconds per programme step as measured in the build run (machine dependent; illustrative, not a result). v007's `D5_cost.json` is retained.

## 5. Not certified

G8-T1, G8-S, G8-R1, B-LOW, B-COMMON, B-SERIES, the nullity-3/4 classification and the RM family are *proofs* (with finite computations where stated); the checker validates only finite instances of them.
