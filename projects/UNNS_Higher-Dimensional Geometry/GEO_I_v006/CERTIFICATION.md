# GEO-I v006 — Programme C: effective arithmetic certification

Labels as in the other documents. Question: can embeddedness / stabilization be certified from an arithmetic or structural criterion that avoids enumerating all cells and testing all cell pairs?

## 0. Result

| ID | Result | Status |
|---|---|---|
| C-1 | **Finite reduction** (v004 S4 + v006): `U = conv(F)` for all `Q ≥ (d,d)`, `Q ≠ (d,d)` is decided by the base window `[d,3d−1]²`; boxes with `max(Q) ≥ 2d` are covered by an explicit cell list of size `O(|F|/d)`-ish (benchmark below); only the `d²−1` *small* boxes `Q = (d+r₁, d+r₂)` need individual certificates | S4 **PROVED** (v004); the thick/thin cell lists **CHECKED** per box; small boxes **CHECKED** |
| C-2 | **Sufficient-family certificate**: any subfamily of true cells whose exact union covers `conv(F)` proves `U = conv(F)`. Certificates are one-sided (a failure of a family proves nothing; the generic test is then used) | **PROVED** (trivial) + used in `theory/small_boxes.py` |
| C-3 | **Centre criterion for 0/1 binary boxes** (Theorem B2, `OBSTRUCTION_RANK.md` §1): embeddedness ⇔ no two cells share a centre. Cost: one pass over the cells, a hash table keyed by `(U, x|ᵤᶜ)`; no pairwise geometry | **PROVED** |
| C-4 | A *closed arithmetic criterion* for embeddedness of arbitrary modular lattices avoiding the cell enumeration | **OPEN** (not found; v004 T-FIN remains the finite criterion, still enumerating templates) |

## 1. Complexity accounting (measured, exact arithmetic)

`experiments/cert_benchmark.py` (data: `output/data/cert_benchmark.json`, Figure 6). `proof cells` = size of the explicit cover of `conv(F)` (`theory/modular_layers.py`); `generic 2-cells` = number of 2-cells of the full `K_abs` (the v005 certificate route).

| (d,s) | Q | \|F\| | proof cells | generic 2-cells | time proof / generic (s) |
|---|---|---|---|---|---|
| (7,3) | (14,14) | 32 | 13 | 249 | 0.008 / 0.036 |
| (11,4) | (22,25) | 54 | 23 | 679 | 0.010 / 0.108 |
| (11,4) | (30,30) | 86 | 46 | 1349 | 0.020 / 0.177 |
| (13,5) | (26,40) | 85 | 36 | 1267 | 0.023 / 0.146 |
| (16,3) | (32,32) | 68 | 22 | 1288 | 0.022 / 0.105 |
| (17,5) | (40,40) | 98 | 45 | 1912 | 0.018 / 0.172 |
| (21,8) | (42,60) | 124 | 51 | — (not run) | 0.023 / — |
| (25,7) | (50,60) | 124 | 48 | — | 0.025 / — |
| (29,12) | (58,58) | 120 | 36 | — | 0.029 / — |

The generic route grows like the number of *all* Graver parallelograms in the box (hundreds to thousands); the explicit cover grows like the number of fibre points (tens). The cover is then verified by exact rational polygon clipping, whose cost is polynomial in the cell count. A *deterministic proof* for all parameters would replace even this verification by the lemmas in `STABILIZATION.md` §3; that is only partially available (see there).

Window cost for `d ≤ D*`: `(2d)²` boxes per unit class; measured 0.01–0.03 s per thick/thin box (proof cells) and about 0.01–0.05 s per small box, i.e. `d = 30` classes complete in ~1 minute each (`output/data/window_full_d22_30_s*.jsonl`, field `seconds`). Compared with the v005 route (d = 14..21 took ≈ 2.2 h in total on the same hardware class), the d = 22..30 window needed a fraction of that.

## 2. Limits

* The proof-cell cover is a **certificate**, not a proof for all `(d,s,Q)`: its existence for every parameter is the content of G6-C1 and is only *checked* instance by instance.
* A sufficient-family failure at some box would be reported as `unresolved` (and sent to the generic test); no such box occurred in the shipped runs.
* Resource-limited items (see `REPORT.md`) are UNAVAILABLE, not PASS.
