# GEO-I v007 — Mathematical summary and theorem registry

Statuses: **PROVED**, **PROVED+CHECKED**, **CHECKED**, **FALSE**, **CORRECTED**, **OPEN**, **UNAVAILABLE**. *TARGET is not a status.* A failed proof is never recorded as a falsification; a numerical pattern is never recorded as a theorem; resource exhaustion is UNAVAILABLE, never PASS. Definitions of GEO-I v001–v006 are used unchanged.

## 1. Registry (v007)

| ID | Statement | Status | Where |
|---|---|---|---|
| **G7-T1** (Theorem A-COL) | for all `d ≥ 2`, all units `s`, all `Q` with `max(Q) ≥ 2d`: `U = conv(F)` | **PROVED+CHECKED** (new general theorem; machine check 8063 boxes `d ≤ 12`, 25–120 random boxes `14 ≤ d ≤ 45` per run) | COVERAGE.md §3–§4 |
| **G7-C1** | `U = conv(F)` for every `Q ≥ (d,d)`, `Q ≠ (d,d)` | **OPEN**; reduced to the small boxes `Q ∈ [d,2d−1]²`; CHECKED `d ≤ 30` (v006 window) and squareless zone `d ≤ 32` (v007, 29,890 boxes, 0 counterexample candidates) | COVERAGE.md §6 |
| HYP-LL | every sail step has a legitimate completion by `(0,±d)`, `(±d,0)` | **FALSE** (571 of 6602 boxes `d ≤ 10`; none with `r₁,r₂>0` and `max(Q) ≥ 2d`) — stays recorded | COVERAGE.md §5 |
| Lemma S4 | window `[d,3d−1]²` decides all `Q` | PROVED (v004, inherited) | — |
| **G7-T3** | `int T₁, int T₂` disjoint from `U`, `∂Tᵢ ⊂ U`; `β₁(U_{(d,d)}) ≥ 2` for all `d ≥ 3`, all units `s` | **PROVED+CHECKED** (exact certificate `3 ≤ d ≤ 64`) | HOLLOW_TOPOLOGY.md §2–§3 |
| **G7-T4 / G7-C1H** | `conv(F)∖U = int T₁ ∪ int T₂` (area `d`), `β₁ = 2` for `s ≢ −1`, `d ≥ 3` | **CHECKED** (`d ≤ 45`, inherited v006 record; Betti `d ≤ 20`); OPEN in general | HOLLOW_TOPOLOGY.md §0, §4 |
| H1 (v005) | `s = −1`: `β₁ = d` (fan graph) | PROVED (inherited) | — |
| **G7-B1** (B-DELTA) | witness rank = generator rank (`δ` in the span) | PROVED+CHECKED | BINARY_RANK.md §2 |
| **G7-B2** (B-COSET) | cells with union `U` = (circuit partition, nonzero coset of its span) | PROVED+CHECKED | BINARY_RANK.md §2 |
| F1 / F2 (B-MIN) | collisions have `r,t ≥ 2`; minimal box ⇒ `x ≡ 1` off `U` | PROVED(+CHECKED for F1) | BINARY_RANK.md §2 |
| **G7-B3** (B-NULL) | full-support collision ⇒ nullity ≥ 3 | PROVED+CHECKED | BINARY_RANK.md §2 |
| B-ATOM | rank-≤3 criterion for `(2,2)` full-support collisions | PROVED+CHECKED (57,219 collisions) | BINARY_RANK.md §2 |
| **G7-C2** | `r_min ≤ 3` for every minimal binary 0/1 box | **OPEN** (CHECKED: n ≤ 6 complete; n = 7 complete under FS; n = 8 restricted rank ≤ 4; no counterexample) | BINARY_RANK.md §3–§4 |
| FS | every minimal box has a full-support collision | **OPEN** (observed in all minimal boxes found) | BINARY_RANK.md §4 |
| G7-D1..D5 | certificate formats and standalone checker | PROVED+CHECKED (checker accepts all shipped certificates and rejects tampered ones) | CERTIFICATION.md |
| G6-C1, G6-C2, G6-C3 | v006 conjectures | superseded by G7-C1 / G7-T3, G7-T4 / G7-C2 (kept OPEN/CHECKED as stated in v006) | — |

Acceptance principle: v007 earns its place by **new general results** — G7-T1 (coverage for all boxes with `max(Q) ≥ 2d`, for all `d` and units `s`), G7-T3 (lower bound `β₁ ≥ 2` for all `d,s`), and the exact binary reduction theory (B-COSET, B-DELTA, B-NULL, B-ATOM) — not by larger verification counts.

## 2. Historical falsifications and regressions (preserved, not relabelled as new)

All are re-run by the inherited v005 regression suite inside `verify.py` (gate G1/G9):

* **q_i > o_i ⇒ β₁(U) = 0 is FALSE** (v003 guess; v005 refutation): `x = 2^10 7^10/15` (b = 15, primes (2,7), `q = (5,5)`, F has 4 points, `K_abs` embedded, Betti `(1,2,0)`), plus a table of ≥ 13 certified counterexamples.
* **HYP-LL FALSE** (v006), classified in v007 with exact witnesses (COVERAGE.md §5).
* **82944/5** (inherited witness): `F = {(1,1),(2,2),(4,0),(5,1)}`, edges `(1,1)–(5,1)` and `(2,2)–(4,0)` cross exactly at `(3,1)` (not in Λ): non-embedded; Betti `K_abs` `(1,2,0)` vs embedded image `(1,0,0)`.
* **`2^{10+2t} 3^4/5`**, `t = 0,1,…`: non-embedded family (same crossing), `β₁(K_abs) = 2`, `β₂(K_abs) = ⌊t/4⌋` unbounded.
* **3600 and `210^4`** benchmark boxes: embedded with the recorded cell counts `11/17/8/1` and `80/212/210/92/15`; not obstructions.
* **Parity 4 and 5**: `G5-C3` (span ≤ 2) FALSE (parity-4 witnesses all of span 3); `G5-C4` FALSE (irreducible witnesses of span 3 and 4).
* **b = 24**, residues `(5,7,13,23)`: all boxes `≤ (2,2,2,2)` embedded; first obstructions `(3,2,1,1)`, `(4,1,1,1)` with planar span 2 and support 4.
* **v006 census**: minimal binary boxes `n = 4,5,6`: `1, 3, 50`, all with minimum rank 3 (n = 7: 2983 in v006's restricted run, now regenerated; n = 8: 7 in v006's restricted run (rank ≤ 3), 5902 now in the rank ≤ 4 run).
* **The exceptional `(d,d)` box**: `Q = (d,d)` is excluded from the coverage statement because `conv(F) ⊄ U` there for `d ≥ 3` (G7-T3 gives two bounded complement components); its complement structure is G7-T3/T4.

## 3. Corrections and notes

* **CORRECTED (documentation only).** v005 `OBSTRUCTIONS.md` mentions 46 certificates; the certificate file has 80 individual witnesses (46 = case groups). Unchanged from v006.
* **CORRECTED (v007 internal).** The working name "corner-sail" for the covering construction was replaced by the *column-strip* construction (COVERAGE.md §2), which is what the proof uses; HYP-LL concerned the sail and is FALSE, but G7-T1 does not depend on it.
* **CORRECTED (v007 internal).** An early version of `atom_criterion` required `z`-constancy on every atom; the exact condition is componentwise (§2 of BINARY_RANK.md) and was re-verified exhaustively.
* Verification of *shipped records* is distinguished from regeneration in `verify.py` (check names say REGENERATED or SHIPPED).
* v007 does not modify GEO-I v001–v006, SELECT-I/II, FIELD-I or the Foundations volumes; inherited modules are listed with source hashes in `PROVENANCE.json`.

## 4. Independent validation paths

| Claim | Path 1 | Path 2 |
|---|---|---|
| coverage `U = conv(F)` on a box | v006 exact polygon subtraction against the strip-cell family | standalone checker: own `F`, Graver, explicit finite subdivision of `conv(F)`, piece-in-cell, disjointness, area sum |
| hollow lower bound | `hollow_geometry.check_hollow` | standalone checker (own implementation) and the v005 uncovered-region routine (area `2d`) |
| binary collisions / ranks | `binary_01.cells_01` + `rank_reduction` | checker's own coset-based cell enumeration (pair counts equal, ranks recomputed) and the v005 cells/LP engine (mod-24 cross-validation, inherited) |
