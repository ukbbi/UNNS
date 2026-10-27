# GEO-I v011 — Mathematics (proofs, registry)

Statuses: PROVED, PROVED+CHECKED, CHECKED, FALSE, CORRECTED, OPEN, UNAVAILABLE. Frozen: v001–v010, both Mathematical Foundations volumes. Inherited statements are quoted with their v010 status and are *used*, not re-proved. Everything computed in this release is exact (integers, `fractions.Fraction`).

## 0. Inherited facts used (all from `docs_v010/MATHEMATICS.md`)
* **E1 (PROVED).** A binary box `C` is non-embedded iff some set `U ⊆ [n]` has two distinct partitions into circuits.
* **F1 (PROVED).** A minimal non-embedded box has `U=[n]` and `1 ∈ C`.
* **A1 (PROVED).** Minimal boxes = `AGL(k−1,2)`-classes of spanning subsets `X ⊆ AG(k−1,2)` (`|X| = p` distinct points; coordinates ↔ points; codewords `w_f = (⟨f,x⟩)_{x∈X}`, `f ∈ F_2^k`; `1 = w_{top}`); `k` = nullity, `p ≥ k+1` (`p = k` gives `C=F_2^p`, unique partition).
* **R (PROVED).** In a minimal box every word `≠ 0,1` has a unique decomposition into disjoint circuits.
* **L5 (PROVED).** Two distinct two-circuit decompositions of one word give a collision of generator rank exactly 3. **C1′ (PROVED, conditional).** W2 ⇒ `r_min = 3` for every minimal box, hence (deleting to a minimal sub-box, as G9-T5) for every non-embedded box.
* **T4 (PROVED+CHECKED).** Nullity ≤ 6: 1, 3, 12, 215 minimal classes (k=3,4,5,6), all W2, all rank 3.

---
## 1. Programme B — W2 and universal rank three

Throughout `X` is a minimal box (A1): `p` distinct points, `k` the nullity, `m_P` the number of blocks of a partition `P` of `1` into circuits, `d_B` the size of a block `B`, `S_P = Σ_{B∈P} d_B²`, `n_2` the number of partitions with `m_P = 2` (unordered `{w, 1+w}`).

### 1.1 Lemma G11-L5c (no circuits of size 1)
*In a minimal box no circuit has size 1; so every block has `d_B ≥ 2` and `m_P ≤ p/2`.*
Proof. Suppose `e_i ∈ C`. Then `{i}` is a circuit, and any circuit containing `i` equals `{i}` (a proper superset is not a minimal support). By E1/F1 the box has a set `U` with two distinct circuit partitions `S ≠ T`. If `i ∉ U`, both survive shortening at `i`. If `i ∈ U`, both contain the block `{i}`; removing it gives two distinct partitions of `U∖i` by circuits of `C` avoiding `i`, which are exactly the circuits of the shortening. Either way the shortened box is non-embedded (E1), contradicting minimality. ∎

### 1.2 Theorem G11-L5 (vector-space-partition structure)
For a partition `P = {B_1..B_m}` of `1` let `V_P = span{1_{B_i}} ⊆ C`. The `1_{B_i}` have disjoint non-empty supports, so `dim V_P = m`, `|V_P| = 2^m`, `1 ∈ V_P`, and the words of `V_P∖{0,1}` are the unions of proper non-empty sub-families of blocks. **(a)** Every `w ∉ {0,1}` lies in exactly one `V_P`. *Existence:* decompose `w` and `1+w` into circuits (every word is a disjoint union of circuits); together they are a partition `P` with `w ∈ V_P`. *Uniqueness:* if `w ∈ V_P`, the blocks inside `w` and the blocks outside it are circuit decompositions of `w` and `1+w`, unique by R, so `P` is determined. **(b)** Hence `{V_P/⟨1⟩}` is a *vector-space partition* of `C/⟨1⟩ ≅ F_2^{k−1}` into subspaces of dimension `m_P − 1 ≥ 1` (`m_P ≥ 2` since `1` is not a circuit for `k ≥ 2`, as all words have support in `[n]`). **(c) Counting identity:** counting nonzero vectors, `Σ_P (2^{m_P−1} − 1) = 2^{k−1} − 1`, i.e.
`Σ_P (2^{m_P} − 2) = 2^k − 2`. The two-block partitions are exactly the 1-dimensional parts (points) of this partition of `F_2^{k−1}`. ∎ (Checked on all 231 classified classes: `tests/test_geo11.py`, `verify.py`.)

### 1.3 Proposition G11-L5b (Parseval identity)
`Σ_P (2^{m_P} S_P − 2p²) = p(2^k − 2p)`.
Proof. *Second moment.* Each coordinate `i` has `⟨f,x_i⟩` a nonzero functional of `f` (top bit of `x_i` is 1), so `w_i = 1` for `2^{k−1}` words; for `i ≠ j` the points are distinct and nonzero, hence linearly independent, so `(w_i,w_j)` is uniform on `F_2²` over `f`: `2^{k−2}` words have both `=1`. Thus `Σ_{w∈C}|w|² = p2^{k−1} + p(p−1)2^{k−2} = 2^{k−2}p(p+1)`.
*Block expansion.* The words are `0`, `1` (weight `p`) and, for each `P`, the unions of proper non-empty sub-families `T` of its blocks (G11-L5a). For fixed `P` with `m` blocks, `Σ_T (Σ_{i∈T} d_i)² = S(2^{m−1}−1) + (p²−S)(2^{m−2}−1) = S 2^{m−2} + p²(2^{m−2} − 1)`. Multiply by 4:
`4Σ_T(…)² = (2^m S − 2p²) + p²(2^m − 2)`.
Summing over `P` and using the counting identity: `4(2^{k−2}p(p+1) − p²) = Σ_P(2^m S − 2p²) + p²(2^k − 2)`, whence `Σ_P(2^m S − 2p²) = 2^k p(p+1) − 4p² − p²2^k + 2p² = p(2^k − 2p)`. ∎ (Independent direct check by Parseval on `F_2^k`: `Σ_f (Σ_x (−1)^{⟨f,x⟩})² = 2^k p`.)

### 1.4 Two elementary estimates
* For `m = 2`: `2^2 S − 2p² = 4(d_1²+d_2²) − 2(d_1+d_2)² = 2(d_1−d_2)² ≥ 0`.
* For `m ≥ 3`: Cauchy–Schwarz gives `S ≥ p²/m`, so `2^m S − 2p² ≥ p²(2^m/m − 2)`.
* **Lemma (threshold).** For `p ≥ 9` and every integer `3 ≤ m ≤ p/2`: `p(2^m/m − 2) ≥ 2^m − 2`.
Proof. Write the claim as `p ≥ f(m) := m(2^m−2)/(2^m−2m)` (the denominator is positive for `m ≥ 3`). `f(3) = 9`, `f(4) = 7`, `f(5) = 150/22 < 7`. For `m ≥ 5`: `2m ≥ f(m) ⇔ 4m − 2 ≤ 2^m`, true for `m ≥ 5` (18 ≤ 32 and induction), and `p ≥ 2m`. For `m = 3, 4` we use `p ≥ 9`. ∎ (Exactly checked for all 9 ≤ p ≤ 400; the inequality fails at `m = 3` for `p = 6,7,8`.)

### 1.5 Theorem G11-L6 (n₂ ≥ p − 1 for p ≥ 9)
*Every minimal non-embedded box with `p ≥ 9` has `n_2 ≥ p − 1` two-block partitions of `1` (in particular ≥ 8).*
Proof. By G11-L5c every partition has `m_P ≤ p/2`. By G11-L5b and §1.4,
`p(2^k − 2p) = Σ_{m_P=2} 2(d_1−d_2)² + Σ_{m_P≥3} (2^m S − 2p²) ≥ Σ_{m_P≥3} p²(2^{m}/m − 2) ≥ Σ_{m_P≥3} p(2^{m} − 2)`
(the last step is the threshold lemma, as `p ≥ 9`). By the counting identity `Σ_{m_P≥3}(2^m − 2) = 2^k − 2 − 2n_2`. Dividing by `p`: `2^k − 2p ≥ 2^k − 2 − 2n_2`, i.e. `n_2 ≥ p − 1`. ∎
**Sharpness (CHECKED).** `X = AG(k−1,2)` (`p = 2^{k−1}`) has `n_2 = p − 1`: present in the classification at `p = 4, 16, 32`.

### 1.6 Proposition G11-L6b (the case k = 7, p = 8)
`p = k+1` means `M` has rank 1: `C = h^⊥`, `h` a single parity check. A zero entry `h_i = 0` gives `e_i ∈ C`, impossible by G11-L5c; so `h = 1` and `C` is the even-weight code `E_8` (`1 ∈ C`). Its circuits are the 28 weight-2 words; its partitions of `1` are the 105 perfect matchings, none with two blocks, so `n_2 = 0` — but `E_8` is **not minimal**: shortening at any coordinate gives `E_7`, whose sets `U` of six coordinates still have ≥ 2 perfect matchings (non-embedded, E1). So no minimal box has `(k,p) = (7,8)`. ∎ (Re-checked by computer in `tests/test_geo11.py`: 28 circuits, 0 two-block partitions, deletion non-embedded.)

### 1.7 Theorem G11-T3 (= G10-C1, W2)
*Every minimal non-embedded binary box has at least two two-circuit partitions of the all-ones word.*
Proof. Let `X` be minimal with nullity `k` and `p` points, `p ≥ k+1`. If `p ≥ 9`: G11-L6 gives `n_2 ≥ p−1 ≥ 8`. If `p ≤ 8`, then `k ≤ p − 1 ≤ 7`; `k = 7` forces `p = 8`, impossible by §1.6; for `k ≤ 6` use the finite classification: G10-T4 (and v008/v009) — 1, 3, 12, 215 minimal classes, all with `n_2 ≥ 3, 4, 8, 16`. Independent re-enumeration in this release: **all** subsets of `AG(2,2)`, `AG(3,2)`, `AG(4,2)` (k = 3,4,5; 1, 37, 19,373 labelled minimal subsets by the E1 criterion) have `n_2 ≥ 3, 4, 8`. ∎

### 1.8 Theorem G11-T4 (universal minimum rank three)
By G11-T3 and G10-C1′ (via G10-L5 = two distinct two-circuit decompositions ⇒ a rank-3 collision, and B-LOW: rank ≥ 3), `r_min = 3` for every minimal non-embedded box, and (deleting to a minimal sub-box, as in G9-T5) for every non-embedded box of the frozen binary 0/1 model. Consequently the v010 implication "`r_min ≥ 4 ⇒ ν ≥ 7`" is vacuous (G10-C2: FALSE as an existence statement). Scope: the frozen binary 0/1 geometric model; no statement about other models. ∎

### 1.9 What was *not* needed
No new classification beyond nullity 6; no enumeration at nullity 7. The proof of W2 for `k ≥ 7` is structural. The Parseval/knapsack feasibility scan (`G11-V1`) was an exploratory step; the proof does not use it.

---
## 2. Programme A — the cap (status: partial; G11-C1/T1/T2 remain OPEN)
See `CAP.md`. Summary: the one-sided cap (`v = 0`, `1 ≤ u < d`, and by transposition `u = 0`) is covered by an explicit family of ≤ ~d+2 Graver cells, verified exactly for 39,590 triples (`d ≤ 60`) and certified by 544 independent CAPCOVER certificates; its correctness reduces to an arithmetic lemma G11-A that is CHECKED on 657,526 triples (`d ≤ 150`) but not proved. The mixed corner (`u,v ≥ 1`) is CHECKED for non-degenerate boxes only (`d ≤ 15`); the universal theorem and the stabilization corollary G11-T2 are OPEN.

## 3. Registry
See `THEOREM_REGISTRY.tsv` (19 rows). Headline: **G11-T3 PROVED+CHECKED, G11-T4 PROVED, G11-C1/T1/T2 OPEN.**
