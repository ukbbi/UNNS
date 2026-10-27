# GEO-I v006 — Programme B: minimum witness rank (G6-C3)

Labels: **PROVED**, **PROVED+CHECKED**, **CHECKED** (exact finite computation, not a proof for all parameters), **FALSE**, **OPEN**, **CORRECTED**, **UNAVAILABLE**.
Frozen definitions (v004/v005): a *witness* of a non-embedded box is `(A,B,δ)` (two parallelotope cells with generator sets `A,B` and base offset `δ`) whose relative interiors meet without being a common face; `d_span = rank[A,B,δ]`. The *minimum witness span* of a box is the least `d_span` over its witnesses. A box is *minimal* if it is non-embedded and every smaller box is embedded.

## 0. Result

| ID | Statement | Status |
|---|---|---|
| **G6-C3** | every minimal non-embedded box has minimum witness span ≤ 3 | **OPEN**. No counterexample in the new search. |
| G6-C3-bin | …restricted to 0/1 boxes `q = (1,…,1)` of *binary* relation lattices `Λ = {α : Σ αᵢcᵢ = 0 in F₂ᵐ}` | **CHECKED**: every minimal box found has minimum span exactly 3 (no minimal box with span 2 and none with span ≥ 4). Census: n = 4: 1, n = 5: 3, n = 6: 50, n = 7: 2983 (code dimension ≥ 3), n = 8: 7 (code dimension ≥ 5) minimal boxes. |
| B-Thm | exact structure theory of 0/1 boxes of binary lattices (cells = disjoint circuits; centre criterion) | **PROVED** (§1) |
| parity | parity lattice `Λ_n`, box `1ⁿ`: n = 4: 3 witnesses (all span 3, minimal box); n = 5: 90 (span 3: 75, span 4: 15); n = 6: 1440 (span 3: 360, 4: 315, 5: 585, 6: 180); n = 7: 20370 | **CHECKED** (n = 4, 5, 6 independently by the v005 engine; n = 7 by the new engine only) |
| min vs individual | for n = 5, 6 the *minimum* span is 3 while individual witnesses have span up to n. Span ≥ 4 for single witnesses does not refute G6-C3 | **CHECKED** |
| mixed-modulus / non-0-1 boxes at k = 5, 6 | `minimal_boxes` of the v005 engine did not finish for the parity lattice mod 3 at k = 5 (bound 2) within 300 s | **UNAVAILABLE** (no exhaustive search; only individual boxes were analysed: mod 3, k = 5, boxes (2,1,1,1,1) and (2,2,1,1,1) have minimum span 2; k = 6 box 1⁶ minimum 3) |

A refutation of G6-C3 would be a certified *minimal* box all of whose witnesses have span ≥ 4. The new engine can find such a box only among 0/1 boxes of binary lattices; none exists for n ≤ 6 (complete over all binary column multisets) and, within the stated rank bounds, n = 7, 8. Nothing is claimed about odd moduli, mixed moduli, or boxes with entries ≥ 2 beyond the cases listed.

## 1. Exact theory of 0/1 boxes (B-Thm, PROVED)

Setting: columns `c₁,…,cₙ ∈ F₂ᵐ∖{0}` (repeats allowed), `Λ = {α ∈ Zⁿ : Σ αᵢcᵢ = 0}` (every exponent-2 residue lattice is of this form; the b = 24 and parity lattices are examples), box `q = 1ⁿ`. The fibre is `F = {nonzero 0/1 vectors x with Σ xᵢcᵢ = 0}` = the nonzero codewords of the binary code `C = ker M`.

**Lemma B1 (cells).** The cells of `K_abs` of dimension ≥ 1 are exactly `P(x; S₁,…,S_r)`, `x ∈ C`, with `S_j` pairwise **disjoint circuits** (minimal nonempty supports of codewords), generator `g_j = (1−2xᵢ)_{i∈S_j}` and all `2ʳ` corners nonzero. *Proof.* A Graver vector of `Λ` inside the box differences of two codewords is `±1` on a set `S` and zero elsewhere, with `S` a circuit (conformal minimality). If two generators of one cell shared a coordinate `i`, the coordinate would take the values `uᵢ, uᵢ+a, uᵢ+b, uᵢ+a+b` with `a,b ∈ {±1}`, which leaves `{0,1}`. The sign pattern is forced by `x`. ∎

**Theorem B2 (centre criterion).** For cells `c = P(x;S₁..S_r)`, `c' = P(y;T₁..T_t)` (`r,t ≥ 1`): `relint c ∩ relint c' ≠ ∅` iff `U := ∪Sⱼ = ∪T_l` and `x = y` outside `U`; the point `z = (½ on U, x outside U)` then lies in both relative interiors. Hence the box is embedded iff no two distinct cells share a centre `(U, x|ᵤᶜ)`. *Proof.* A coordinate in `Sⱼ∖∪T_l` would be strictly between 0 and 1 on `c` and in `{0,1}` on `c'`; so the supports agree and the two linear systems `tⱼ ∈ (0,1)` / `s_l ∈ (0,1)` are solved by `t = s = ½`; outside `U` both cells are constant. ∎

(Machine check: `tests/test_geo6.py`, and `verify.py` cross-validates Theorem B2 against the v005 cell/zonotope engine, which uses a different criterion.) Example: parity `n = 4`, box `1⁴`: one centre `(½,½,½,½)` carries the three square cells `{12|34}, {13|24}, {14|23}` → three witnesses, each of affine span 3 (support 4): the octahedral configuration of v005.

**Witness classes.** v005 counts witnesses as `(A,B,δ)` up to translation and swap; the new engine reports both the number of cell pairs and the number of such classes (`n_witnesses`); they differ for `n ≥ 6` (parity 6: 1710 pairs, 1440 classes). Minimum spans are unaffected.

## 2. Search procedure and validation

* `theory/binary_01.py`: exact cell enumeration (integers), centre grouping, exact rational rank for `d_span`, minimality by single-coordinate deletion (restriction to a face of the box; every smaller 0/1 sub-box of a 0/1 box is such a restriction, because the lattice of the smaller box is obtained by deleting the coordinate).
* `experiments/binary_rank_search.py N MMAX`: all multisets of `N` nonzero columns of `F₂ᵐ` of rank exactly `m ≤ MMAX` (code dimension `N − m`). Rank `m = N` gives the trivial lattice. Completeness: n ≤ 6 full; n = 7: m ≤ 4 (code dimension ≥ 3; code dimensions 1, 2 not run); n = 8: m ≤ 3 (code dimension ≥ 5; **UNAVAILABLE** for code dimension ≤ 4).
* **Two independent paths.** `verify.py` compares the new engine with the v005 engine (cells from the realized fibre complex + open-zonotope criterion; residues mod 24 for the same binary columns) on 180 random binary lattices for n = 3, 4, 5 (smoke: 36) plus 15 for n = 6 and the parity-6 histogram (full): witness classes and minimum spans agree in every case.
* Regressions (gate G1): parity 4 at `(1,1,1,1)` = 3 witnesses, span 3; parity 5 at `1⁵`; b = 24 residues (5,7,13,23) boxes (4,1,1,1), (3,2,1,1): support 4, planar witness (the `regression_v005.py` suite, unchanged v005 checks).

## 3. What is not shown

* No proof of span ≤ 3 (or of any bound) for all minimal boxes. A natural route is the structure of Theorem B2: a witness is a pair of cells with equal centre; the difference `δ` is supported on `U`; the span is `rank[g's, g''s, δ]`. We did not find a proof that a minimal box always contains a witness of rank ≤ 3.
* No search of non-binary lattices at `k ≥ 5` that is exhaustive; no search of 0/1 boxes of lattices with exponent > 2.
* Box entries ≥ 2 at `k = 5, 6` only for the individual boxes listed above.
