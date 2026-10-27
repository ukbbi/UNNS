# GEO-I v009 — Mathematics (targeted proof closure)

Status vocabulary: PROVED, PROVED+CHECKED, CHECKED, FALSE, CORRECTED, OPEN, UNAVAILABLE. **TARGET and PROPOSED are not results**: v009 started with TARGET entries; every one is resolved below to a result status.
The v001–v008 results, the SELECT-I/II and FIELD-I lines and the Foundations volumes are unchanged. Section A at the end reproduces the complete v008 mathematics file verbatim; every v008 statement remains in force with its v008 status.

## 0. Registry of v009

| ID | Statement (short) | Status after v009 |
|---|---|---|
| G9-C1 | hollow box, `d≥3`, unit `s≢−1`: `H0 \ U0 = int T1 ⊔ int T2` | **OPEN** (A-OPEN). No counterexample in any completed survey (§3) |
| G9-T1 | proof of G9-C1 by continued-fraction/sail induction | **OPEN** — not proved, not refuted; §3.3 records what was established and what is missing |
| G9-T1H | `β1(U_{d,s,(d,d)}) = 2` for all such `(d,s)` | **OPEN** (needs G9-T1; finite homology checks recorded in v006–v008 are unchanged) |
| G9-CAP | `C_Q = H_Q \ H_0 ⊆ U_Q` for every nonexceptional small box | **OPEN** (B-OPEN). No counterexample for `d ≤ 22` (§4) |
| G9-T2 | proof of G9-CAP | **OPEN** |
| G9-T3 | `U = H` for all `d≥2`, units `s`, `Q ≥ (d,d)`, `Q ≠ (d,d)` | **OPEN** — requires G9-T1 and G9-T2; the conditional reduction (G8-T1 + G8-R1) is unchanged |
| G9-Z | a parity matrix with a zero column is never a minimal non-embedded box | **PROVED+CHECKED** (§1) |
| G9-C2 | does every coordinatewise-minimal non-embedded box of nullity 5 have `r_min = 3`? | **PROVED+CHECKED**: yes (§2) |
| G9-T4 | complete classification of minimal non-embedded boxes of nullity 5: 12 reduced orbits, all `r_min = 3` | **PROVED+CHECKED** (§2) |
| G9-T5 | every non-embedded 0/1 box of nullity `≤ 5` has `r_min = 3`; a counterexample to universal `r_min = 3` must have nullity `≥ 6` | **PROVED+CHECKED** (§2.4) |

Open in the long run (unchanged): G8-T3 universal `r_min ≤ 3`, G8-C3 (full support of minimal boxes), G8-C1 as a whole.

## 1. G9-Z — zero parity columns are excluded

**Setting.** `M` is an `m × n` binary matrix with columns `c_1..c_n`, `C = ker M ⊆ F_2^n`, `F = C \ 0`. Circuits are minimal supports of nonzero codewords. Cells (v006): points, and parallelotopes `P(x;S)`, `S` a family of pairwise disjoint circuits, `x ∈ C \ span(S)` (all `2^{|S|}` corners `x + span(S)` nonzero); the cell depends on `(S, x + span(S))`. Centre criterion (v006 B2): the box is non-embedded iff two distinct cells `(S,x),(T,y)` have the same union `U = ∪S = ∪T` and `x = y` off `U`. The box obtained by deleting coordinate `i` has code `C'' = {c' : Σ_{j≠i} c'_j c_j = 0}`; it is the sub-box `q − e_i`, i.e. the codewords vanishing at `i` with coordinate `i` dropped. A box is *minimal non-embedded* if it is non-embedded and every single-coordinate deletion is embedded.

**Theorem G9-Z.** If some column `c_i = 0`, and the box is non-embedded, then the box with coordinate `i` deleted is non-embedded. Hence a minimal non-embedded box has no zero parity column.

*Proof.* `c_i = 0` means `e_i ∈ C`, so `{i}` is a circuit and `C = C_0 ⊕ ⟨e_i⟩`, `C_0 = {c ∈ C : c_i = 0}`; dropping coordinate `i` maps `C_0` bijectively onto `C''`, and the circuits of `C''` are the circuits of `C` not containing `i` (a circuit containing `i` must equal `{i}`). Take a collision `(S,x),(T,y)` with union `U`.

*Case I: `i ∈ U`.* Circuits through `i` are `{i}` only, so `{i} ∈ S ∩ T`. If `S = T = {{i}}` then `U = {i}`, `x + y ∈ ⟨e_i⟩ = span(S)` and the cells coincide; so `S' = S \ {{i}}` and `T' = T \ {{i}}` are nonempty families of circuits of `C''`. Adding `e_i` does not change a coset of `span(S)`, so choose `x_i = y_i = 0`; drop coordinate `i`: `ξ, η ∈ C''`. Since `span(S) ∩ C_0 = span(S')`, `x ∉ span(S)` gives `ξ ∉ span(S')`, likewise `η ∉ span(T')`. The unions are `U \ {i}` and `ξ = η` off it. The cells are distinct: if `S' ≠ T'` clear; if `S' = T'` then `S = T` and `x + y ∉ span(S)`, with `(x+y)_i = 0` this gives `ξ + η ∉ span(S')`. So `C''` has a collision.

*Case II: `i ∉ U`.* Now `S, T` are families of circuits of `C''`.
(II-1) `S ≠ T`. If `span(S) = C''` then `C''` is a direct sum of disjoint circuits, whose circuits are exactly `S`, so `T ⊆ S` and, both partitioning `U`, `T = S`; contradiction. So `span(S) ≠ C''`, likewise `span(T) ≠ C''`. A vector space over `F_2` is not the union of two proper subspaces, so there is `z ∈ C'' \ (span(S) ∪ span(T))`; `(S,z)` and `(T,z)` are distinct cells with the same union and a common base: a collision in `C''`.
(II-2) `S = T` and the cosets differ. `δ := drop(x + y) ∈ C'' ` is supported in `U`, and `δ ∉ W := span(S)`. Decompose the codeword `δ` and the codeword `1_U + δ` (`1_U = ΣS ∈ C''`) into disjoint circuits (any binary codeword is a disjoint union of circuits: remove a circuit contained in its support and repeat); the union `T*` of the two families partitions `U` into circuits, and `δ ∈ span(T*)`, so `T* ≠ S` (otherwise `δ ∈ W`). Apply (II-1) to `S, T*`. ∎

*Check.* `experiments/zero_column.py`: all `6763` parity matrices with a zero column and `m ∈ {2,3}`, `2 ≤ n ≤ 8`: 2396 are non-embedded, none minimal; `tests/test_geo9.py` and `verify.py` additionally confirm that deleting the zero column never produces an embedded box (n ≤ 6).

**Consequence (scope closure).** The v008 census completeness (`rank_attack.py`, nonzero columns) is unrestricted: for general binary matrices the minimal non-embedded boxes coincide with those with nonzero columns. Coordinates on which every codeword vanishes (zero *generator* columns) were already excluded by minimality in v008 (B-SERIES).

## 2. Nullity five (G9-C2, G9-T4, G9-T5)

### 2.1 Reduction (frozen v006–v008 facts used)
For a minimal non-embedded box, no parity column is zero (G9-Z) and no coordinate vanishes on all of `C` (such a coordinate could be deleted without changing any cell or collision). With `k = dim C`, the generator matrix has `n` nonzero columns in `F_2^k` spanning it; grouping equal columns gives a *reduced support* `Σ ⊆ F_2^k \ 0` (spanning) and multiplicities. By B-SERIES (v008) the box is a blow-up of the reduced box, and blow-up preserves embeddedness, minimality, collisions and the set of witness ranks. Isomorphic supports (`GL(k,2)`) give isomorphic boxes. So the minimal non-embedded boxes of nullity `k` are classified by the orbits of spanning subsets `Σ ⊆ PG(k−1,2)` whose reduced box is minimal non-embedded, together with multiplicities.

### 2.2 Theorem G9-T4 (nullity five)
There are exactly **12** orbits of spanning supports `Σ ⊂ F_2^5 \ 0` whose reduced box is minimal non-embedded; their sizes are `p = 8, 9, 10, 10, 11, 11, 12, 12, 13, 14, 15, 16` (the `p = 16` orbit is the first-order Reed–Muller support `RM(1,4)`, the 16 odd-weight vectors, already known minimal from v008). Every one has minimum witness rank **3**. Hence every minimal non-embedded 0/1 box of nullity 5, of any length `n` and with any parity matrix (zero columns included, G9-Z), has `r_min = 3`.

*Proof.* §2.1 reduces to the finite enumeration; B-LOW gives `r_min ≥ 3`. The enumeration: (1) all orbits of subsets of `PG(4,2)` are generated by adding one point at a time with an exact `GL(5,2)` isomorphism test (`theory/binary5.py`): 1371 non-empty orbits, 1326 spanning. Completeness of this list is confirmed by an independent computation, Burnside's lemma over all `9,999,360` elements of `GL(5,2)` (`tools/burnside5.c`), which gives 1372 orbits including the empty set (and 4, 10, 46 for `k = 2,3,4`, matching the generator). (2) For each spanning orbit the code has `32` words; embeddedness, all single deletions and all collisions are computed exactly (`experiments/binary5_attack.py`); 12 are minimal non-embedded, all with a witness of rank 3. (3) Independent validation: the v006 code path (`binary_01`, `centre_collisions`, `rank_reduction`) re-classified all `785` spanning supports with `≤ 16` points (this contains all 12 minimal ones) with **0 disagreements** (`experiments/binary5_crosscheck.py`). (4) Certificates `certificates/C5_rank5.json` (12 RANK certificates) are accepted by the standalone `checker8.py`. ∎ (The generator is also checked against the v008 classification: it reproduces the nullity 3 and 4 results.)

*Remark (not minimal boxes).* All `212` non-embedded spanning orbits of nullity 5 — minimal or not — have minimum witness rank 3 (`output/data/v9_minrank_all_nonembedded_k5.json`, Figure 7).

### 2.3 Answer to G9-C2
Yes: every coordinatewise-minimal non-embedded binary 0/1 box with `ν = 5` has `r_min = 3` (G9-T4).

### 2.4 Corollary G9-T5
Every non-embedded box of nullity `k ≤ 5` has `r_min = 3`. *Proof.* Delete coordinates successively (restrict to words vanishing there) until the box is minimal non-embedded; the nullity does not increase and stays `≥ 3` (B-NULL′), so it is 3, 4 or 5, and `r_min = 3` there (G8-T3b, G9-T4). A collision of a sub-box is a collision of the box with the same generators extended by zero coordinates, so the same rank is attained; B-LOW gives `≥ 3`. ∎ Consequently the universal statement G8-T3 can fail only at nullity `≥ 6`.

## 3. Hollow box (Programme A): what is and is not established

### 3.1 Frozen geometry
`F = {P_i} ∪ {A,B,C}` (§ v007/v008), `T1 = tri(A,P_{d−t},C)`, `T2 = tri(B,P_{d−1},C)`, area `d/2` each; `H0 = conv F`, `U0 = ∪` cells. G7-T3: `int T1, int T2` are disjoint from `U0` and their boundaries lie in `U0`; so `H0 \ U0 ⊇ int T1 ⊔ int T2`. G9-C1 is the reverse inclusion.

### 3.2 Reformulations used (all elementary; no new theorem)
* Central inversion `p ↦ (d,d) − p` maps `Γ ∩ [0,d]²` to itself and exchanges `0 ↔ C`, `A ↔ B`, `P_i ↔ P_{d−i}`.
* Sail facts: consecutive record minima `v_k, v_{k+1}` of `s·i mod d` form a lattice basis (`det = d`), the triangle `(0, v_k, v_{k+1})` is primitive, and `H0` is bounded by the sail from `A` to `B` and the two sides through `C`.
* G9-C1 is equivalent to: every point of `H0 \ (int T1 ∪ int T2)` lies in a Graver cell with all four corners in `F` (i.e. avoiding the origin).

### 3.3 Result
The continued-fraction induction (A1–A5) was **not** completed. The sail structure (A1) is standard; a decomposition of the polygon `H0 \ (T1 ∪ T2)` into rational pieces each covered by one cell is available for every tested pair (exact certificates, `v8` and survey below), but a uniform description of the covering cells in terms of the partial quotients, and the proof that the induction step preserves the exact complement, were not obtained. The number of residual convex pieces left by successive subtraction of the cells (fragments of `T1 ∪ T2`) grows with `d` (6, 10, 13, 18 pieces for `s = 2`, `d = 7, 9, 11, 13`), so a finite template library does not settle the question. **G9-C1/G9-T1: OPEN (A-OPEN).** No counterexample was found (§3.4); nothing is claimed beyond the completed scope.

### 3.4 Adversarial survey (CHECKED within scope; **not** a proof)
* Inherited exact-complement data (unchanged): all units `s ≠ d−1` for `d = 3..45` (`hollow_general_s.json`) and `d = 51..72` (`v8_hollow_51_72.json`); v009 adds `d = 46..50` (`v9_hollow_46_50.json`: 141 pairs). Together: every `d ≤ 72`, every unit, exact complement = two triangles.
* v009 (`experiments/hollow_attack9.py`): `853` further exact pairs with `d = 73..110`, including all composite `d`; `s ∈ {2..6, d−2..d−4, (d±1)/2, (d±1)/3, d/2±1}` and `s ≈ d/k (k = 5..9)` with their inverses (maximum partial quotient `54`): exact complement of area `d` equal to `T1 ∪ T2` in every case; no counterexample (`output/data/v9_hollow_attack_p*.json`). Exact method: v005 all-cells polygon subtraction (rational arithmetic).
* Label: *no counterexample within the completed scope*; this is **not** a general theorem.

## 4. Cap (Programme B)

### 4.1 Statement and frozen facts
`C_Q := H_Q \ H_0`, `Q = (d+u, d+v)`, `0 ≤ u,v < d`, `(u,v) ≠ (0,0)`. v008 facts: G8-T1 (the triangles are inside `U_Q`), G8-S (squareless iff `v < m_s(u)`), the extension points `R_i, T_j, K`, G8-R1 (conditional on G9-C1).

### 4.2 Result
B1–B5 (a uniform local-to-global proof of the cap) were **not** completed; G9-CAP/G9-T2 remain **OPEN (B-OPEN)**. The surveys below are the adversarial verification.

### 4.3 Survey (CHECKED within scope; not a proof)
`experiments/cap_attack.py` tests the stronger statement `H_Q ⊆ U_Q` (hence also the cap statement) on every nonexceptional small box and every unit: v008 `d = 3..20` (26,636 boxes, all covered) and v009 extension `21..22` (`10,110` boxes). A cap failure would need positive area of uncovered region outside `H_0`; none exists. Squareless boxes are included (checked against G8-S).

## 5. Consolidation (G9-T3)
OPEN: it needs G9-T1 and G9-T2. The conditional chain stays as in v008: G9-T1 ⇒ (G8-R1 with G8-T1) square hull covered in all `Q ≠ (d,d)`; G9-T2 ⇒ cap covered; with the earlier theorems `s = ±1` and G7-T1 (`max(Q) ≥ 2d`) the universal statement `U = H`. The case `s ≡ −1` keeps its own result `β1 = d` and is excluded from the two-hole equality.

## 6. Honest summary of what changed
* New proved results: G9-Z, G9-T4 (with G9-C2), G9-T5 (nullity ≤ 5 universality of `r_min = 3`).
* Not achieved: the two planar proofs. The planar stabilization question (`U = H` for all small boxes and the hollow-box complement) is **not** closed by this release; the release does not claim closure.

---
# Section A — GEO-I v008 mathematics (verbatim, unchanged)

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
