# GEO-I v008 — Mathematical summary and theorem registry

Statuses: **PROVED**, **PROVED+CHECKED**, **CHECKED**, **FALSE**, **CORRECTED**, **OPEN**, **UNAVAILABLE**. *TARGET and PROPOSED are not results.* A failed proof is never recorded as a falsification; a numerical pattern is never recorded as a theorem; resource exhaustion is UNAVAILABLE, never PASS. Definitions of GEO-I v001–v007 are used unchanged; all earlier releases are frozen records (v007 documents are kept verbatim in `docs_v007/`).

## 1. Registry (v008)

| ID | Statement | Status | Where |
|---|---|---|---|
| **G8-T1** | filling lemma: `T1 ∪ T2 ⊂ U_{d,s,Q}` for all `d ≥ 3`, units `s`, `Q ≥ (d,d)`, `Q ≠ (d,d)` | **PROVED+CHECKED** | HOLLOW.md §2 |
| **G8-K1** | both hollow-box holes die at the first enlargement | **PROVED+CHECKED** | HOLLOW.md §0 |
| **G8-S** | squareless boxes = staircase `v < m_s(u)`; `N_sq(d,s) = 2(d−1)+Σ(m_s(u)−1)`; `Σ_{d=3}^{32}Σ_s N_sq = 29,890` | **PROVED+CHECKED** | SMALL_BOX.md §2 |
| **G8-R1** | G8-T2 for `(d,s)` ⇒ `conv(F_{(d,d)}) ⊂ U_Q` for all `Q ≥ (d,d)`, `Q ≠ (d,d)` | **PROVED** (conditional on G8-T2) | SMALL_BOX.md §4 |
| **G8-C1** | `U = conv(F)` for all small boxes `Q = (d+u,d+v)`, `0≤u,v<d`, `(u,v)≠(0,0)` | **OPEN** (CHECKED: all 26636 small boxes with 3≤d≤20 covered, 0 failures; inherited `d ≤ 30`, squareless `d ≤ 32`) | SMALL_BOX.md |
| G8-L1…L4 | local filling lemmas of the cap | **PROPOSED — not results** | SMALL_BOX.md §5 |
| **G8-T2** | `conv(F_{(d,d)}) ∖ U = int T1 ⊔ int T2` (`s ≢ −1`) | **OPEN**; CHECKED `3 ≤ d ≤ 72` | HOLLOW.md §0 |
| **G8-C2** | `β1(U_{(d,d)}) = 2` for `s ≢ −1` | **OPEN**; CHECKED (Betti `d ≤ 20`) | HOLLOW.md |
| G8-T4 | hole-disappearance index | G8-T1 part PROVED; `β1`-part CHECKED on shipped range | HOLLOW.md §4 |
| **B-NULL′, B-BASIS** | any collision ⇒ nullity ≥ 3; basis+extras exhaustive | **PROVED** | MINIMAL_RANK.md |
| **B-LOW (G8-T3a)** | every witness has rank ≥ 3 | **PROVED** | MINIMAL_RANK.md |
| **B-COMMON** | common-base collisions have rank ≤ r+t−1 | **PROVED** | MINIMAL_RANK.md |
| **B-SERIES** | blow-up/reduction theorem | **PROVED+CHECKED** | MINIMAL_RANK.md |
| **G8-T3b** | nullity 3 and 4 minimal boxes: classified, `r_min = 3` for all `n` | **PROVED+CHECKED** | MINIMAL_RANK.md |
| **G8-T3c** | `RM(1,k−1)` family minimal, `r_min = 3` | **PROVED** (+CHECKED `k=3,4,5`) | MINIMAL_RANK.md |
| G8-C3′ | common-base property of all minimal boxes | **OPEN**; CHECKED `n ≤ 8` and n=9 (1757/1757) | MINIMAL_RANK.md |
| **G8-C3** | every minimal box has a full-support collision (FS) | **OPEN**; CHECKED `n ≤ 9` (complete census) | MINIMAL_RANK.md |
| **G8-T3** | `r_min ≤ 3` for every minimal box | **OPEN** | MINIMAL_RANK.md |
| **G8-T5** | certification: COVER / GAP / HOMOLOGY / RANK formats, standalone `checker8.py`, tamper rejection | **PROVED+CHECKED** | CERTIFICATION.md |

Acceptance principle (v008): the release earns its place through **new general results** (G8-T1/K1, G8-S, G8-R1, B-LOW, B-COMMON, B-SERIES with the nullity-3/4 classification, the RM family), *not* through verification counts. **No decisive result on G8-C1 or G8-T3 is claimed.**

## 2. Inherited registry (v007, frozen verbatim)

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


## 3. Historical falsifications and regressions (frozen from v007/v006/v005; preserved, not relabelled as new)

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


## 4. Corrections and notes (v008)

* **CORRECTED (counting convention).** v007's census sizes (1, 3, 50, 2983, 5902 for `n = 4..8`) counted raw multisets of columns of rank `≤ n−3` (n = 8: rank ≤ 4 only). v008's complete census counts *basis+extras representatives* (B-BASIS), giving 1, 3, 11, 50, 273, 1757 minimal representatives for `n = 4..9`. The two are different counting conventions on different enumerations; neither contradicts the other; minimum rank is 3 in both.
* **CORRECTED (qualification status).** The v007 statements "n = 7 complete only under FS" and "n = 8 restricted" are superseded for `n ≤ 9` by B-NULL′ (nullity ≥ 3 for *every* non-embedded box, not only full-support ones), which makes `m ≤ n−3` exhaustive. The v007 text stays as written in `docs_v007/`.
* **CORRECTED (G8 numbering).** The G8-T2 label denotes the hollow-box complement statement (previously G7-T4/G7-C1H, v006 G6-C2).
* v008 does not modify GEO-I v001–v007, SELECT-I/II, FIELD-I or the Foundations volumes; inherited modules are listed with hashes in `PROVENANCE.json`; GitHub was not modified.

## 5. Independent validation paths

| Claim | Path 1 | Path 2 |
|---|---|---|
| G8-T1 | `theory/hollow.py:check_filling` (explicit cells, exact integer tests) | v005 exact polygon-subtraction routine over all cells: leftover empty at `Q=(d,d+1),(d+1,d)` |
| G8-S | brute-force definition vs staircase formula on every swept box | closed-form count equals v007's independent enumeration (29,890) |
| coverage of small boxes | `small_attack.py` (all cells, exact rational subtraction) | `checker8.py` COVER: own `F`, Graver, subdivision |
| nullity 3/4 classification | orbit enumeration + exact engines | basis+extras enumeration of rank `n−k`, compared as code-invariant sets (`n ≤ 8`) |
| binary collisions / ranks | `binary_01` + `rank_reduction` | `checker8.py` own coset-based engine and v005 cells/LP (inherited cross-validation) |
| GAP / HOMOLOGY | builder (`cell_cover.py`) | `checker8.py` recomputation (cells from scratch; ranks over `Q`; `∂∂=0`, Euler–Poincaré) |
