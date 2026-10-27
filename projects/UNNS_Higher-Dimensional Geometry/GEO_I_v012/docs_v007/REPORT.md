# GEO-I v007 — Structural Closure of Modular Geometry: report

## 1. Summary

v007 earns its place by **new general mathematics**, not by a larger count:

1. **Theorem A-COL (G7-T1), PROVED+CHECKED.** For all `d ≥ 2`, all units `s` and every box with `max(Q) ≥ 2d`: `U = conv(F)`. Proof by an explicit column-strip cover (COVERAGE.md §2–§3), machine-checked on 8063 boxes (`d ≤ 12`, all units) and on random boxes up to `d = 45`. This removes the need for the false v006 "corner-sail" hypothesis HYP-LL (FALSE, classified with exact witnesses). **G7-C1 is reduced to the small boxes `Q ∈ [d,2d−1]²`** (squareless residue), where it stays OPEN: CHECKED to `d ≤ 30` (v006) and, in v007, 29,890 squareless boxes `3 ≤ d ≤ 32` with 0 counterexample candidates. Programme A: **A-PARTIAL**.
2. **Theorem G7-T3, PROVED+CHECKED.** For all `d ≥ 3` and all units `s` the hollow box `(d,d)` has two bounded complementary triangles of area `d/2` each, hence `β₁ ≥ 2` (HOLLOW_TOPOLOGY.md). v006 had only CHECKED for `d ≤ 45`. The exact complement (`= int T₁ ∪ int T₂`, `β₁ = 2` for `s ≢ −1`) remains CHECKED/OPEN. Programme C: **C-PARTIAL** (lower bound proved).
3. **Binary reduction theory (G7-B1..B3, B-ATOM), PROVED+CHECKED.** Cells with union `U` = (circuit partition, coset); witness rank = rank of the generators; full-support collisions force nullity ≥ 3; exact rank-≤3 criterion for `(2,2)` collisions. **G7-C2 (`r_min ≤ 3`) remains OPEN**; evidence: complete census `n ≤ 6`, `n = 7` complete (among nullity ≥ 3; complete under FS), `n = 8` restricted (rank ≤ 4): 1, 3, 50, 2983, 5902 minimal boxes, **all with minimum witness rank 3**. Programme B: **B-PARTIAL**.
4. **Certificates D1–D5** with an independent standalone checker (explicit finite subdivisions for coverage; minimality + rank + exact shared point for binary boxes; hollow certificates).

## 2. Gates

| Gate | Result |
|---|---|
| G1 continuity | inherited v005 regression suite (`regression_v005.py`, unmodified) passes; v006 tests/checks re-run |
| G2 stabilization advanced by a new theorem | **yes: G7-T1** (all `max(Q) ≥ 2d`); finite enumeration alone was not used for it |
| G3 binary rank | reduction theorems proved; `r_min ≤ 3` **not** proved; no rank ≥ 4 minimal box found |
| G4 hollow topology | lower bound proved for all `(d,s)`; upper bound CHECKED |
| G5 certificates | D1–D5 shipped; standalone checker; negative tests |
| G6 no unresolved item reported as a result | all unfinished items are OPEN / restricted / UNAVAILABLE in the registry; restricted censuses are labelled |
| G7 novelty only from verified literature comparison | **no novelty claim made**; comparison outstanding (PRIOR_ART.md) |
| G8 reproducibility | clean unzip runs `verify.py --smoke` / full without sibling folders; two independent paths per programme; manifest SHA-256 |
| G9 preservation | v001–v006, SELECT-I/II, FIELD-I, Foundations untouched; frozen libraries and inherited modules hash-checked; historical falsifications preserved (MATHEMATICS.md §2) |

## 3. What changed relative to v006

* **Proved** (new): A-COL, G7-T3, B-COSET/B-DELTA/B-NULL/B-ATOM/F1/F2.
* **Classified** (new): HYP-LL failures with exact witnesses (571/6602 boxes for `d ≤ 10`; none with `r₁,r₂>0` and `max(Q) ≥ 2d`).
* **Evidence extended**: squareless zone to `d ≤ 32`; hollow certificates to `d ≤ 64`; binary census to `n = 7` (complete among nullity ≥ 3) and `n = 8` (restricted); `n = 9` (rank ≤ 3: 4687 sets, no minimal box).
* **Not achieved**: a proof for the squareless small boxes; the covering upper bound for the hollow box; `r_min ≤ 3`; FS.

## 4. Verification levels (reported separately from archived v006 counts)

* **Archived (not re-counted here):** v006 smoke 20/20, v006 full 25/25, inherited v005 52/52.
* **v007 Level 1 (`verify.py --smoke`)** and **Level 2 (`verify.py`, full)**: results are written to `output/reports/verify_full.json` and `output/smoke/verify_smoke.json` with the groups `v007` (new checks) and `inherited` (regressions) counted separately. See `README.md` for the counts of the delivered run. Checks distinguish **REGENERATED** (recomputed here) from **SHIPPED RECORD** (verification of supplied data).

## 5. Limitations (honest)

1. The squareless small boxes are not proved; the search is finite (`d ≤ 32` here). A counterexample, if any exists, would have to be a box in that zone.
2. G7-T4 (the exact complement of the hollow box) is CHECKED only to `d = 45` (inherited), and the Betti number check through the chain complex runs to `d ≤ 20`.
3. The binary censuses are exhaustive only over the stated ranks; `n ≥ 8` is restricted. FS (existence of a full-support collision in every minimal box) is observed, not proved; if it failed, the `n = 7` census would not be complete.
4. The statement of A-COL for non-unit `s` and for `Q₁ < d` is only CHECKED on small ranges (remarks in COVERAGE.md).
5. The literature comparison is not done; nothing here is claimed as new to the literature, only as new to the GEO-I sequence.
