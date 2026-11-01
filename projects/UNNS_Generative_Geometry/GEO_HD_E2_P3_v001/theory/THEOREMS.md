# E2-P3 — Theorems, proofs, and status

Status vocabulary: PROVED (proof below, independent of computation), CHECKED (finite exact computation with independently verified certificates; **not** a proof of the
general statement), SUPPORTED (no counterexample in the declared scope), OPEN, FALSE.  Nothing here is promoted to a discovery without the novelty gate (results/P3_THEOREM_AUDIT.md).

## P3-T0 — Coverage-Gap Reduction (elementary; **not** a qualifying result)  [PROVED]
With H = conv F ⊆ H′ = conv F′ (because F ⊆ F′) and U ⊆ H: U ∖ U′ = U ∩ 𝒢′ where 𝒢′ = H′ ∖ U′.  Hence  U ⊆ U′ ⇔ U ∩ 𝒢′ = ∅, and U′ = H′ ⇒ U ⊆ U′.
*Proof.* U ⊆ H ⊆ H′, so a point of U outside U′ lies in H′ ∖ U′, and conversely. ∎

## P3-L1 — Planar scaling reduction (GEO-I v004 S1, re-proved)  [PROVED]
Let k = 2, b > 1, o_i = ord_b(p_i), C = ⟨p_1⟩ ∩ ⟨p_2⟩ ⊆ (Z/b)^×, d = |C|, a = o_1/d, c = o_2/d.  Then Λ_b = diag(a,c) · Γ_{d,s} with s a unit mod d (s = 0, Γ = Z², if d = 1),
the box becomes (⌊q_1/a⌋, ⌊q_2/c⌋), and Graver vectors, cells, F, H and U correspond under the positive diagonal map diag(a,c).
*Proof.* C is a subgroup of the cyclic group ⟨p_1⟩ of order o_1, so C = ⟨p_1^a⟩ and p_1^i ∈ C ⇔ a | i; likewise C = ⟨p_2^c⟩.  If p_1^i p_2^j = 1 then p_1^i = p_2^{-j} ∈ C, so a | i and c | j.
Write i = a i′, j = c j′.  g_1 = p_1^a and g_2 = p_2^c both generate C (order d), so g_2 = g_1^u with u a unit mod d, and g_1^{i′} g_2^{j′} = 1 ⇔ i′ + u j′ ≡ 0 (mod d) ⇔ j′ ≡ s i′ (mod d), s = −u^{-1}.
Box: a i′ ≤ q_1 ⇔ i′ ≤ ⌊q_1/a⌋.  A positive diagonal linear map preserves the sign pattern and coordinatewise order of vectors, hence the conformal relation, hence Graver vectors; it maps cells
(affine images of cubes) to cells. ∎  (The code additionally verifies the identity Λ_b = diag(a,c)Γ_{d,s} exhaustively on a full period for every classified row; the independent audit repeats it on two periods.)

## P3-C1 — G12-T8 inheritance  [PROVED modulo GEO-I v005–v012; **inherited, not new**]
If the target is Γ_{d,s} (after P3-L1) with d ≥ 2, Q_norm ≥ (d,d), Q_norm ≠ (d,d), then U′ = H′ and hence U ⊆ U′ for every source with F ⊆ F′ (P3-T0).  This is class `INHERITED_G12T8`.

## P3-T3 — Corner-cube criterion for rectangular targets (any k)  [PROVED]
Setting: Λ′ = ⊕ o_i Z (rectangular; o = (1,…,1) for b′ = 1), F ⊆ F′, scaled box Q̃_i = ⌊q_i/o_i⌋ ≥ 1 for all i (if some Q̃_i = 0 the coordinate i carries no lattice point of F′ ⊇ F and the problem is the same problem in k−1 coordinates).
Let A_i = o_i Q̃_i, B = ∏[0,A_i], and O = {z : z_i < o_i ∀i} the open corner cube.

**(a) Shape of the target.**  U′ = { z ∈ B : max_i z_i/o_i ≥ 1 } = B ∖ O.
**(b) Criterion.**  U ⊆ U′ ⇔ U ∩ O = ∅ ⇔ no cell of the source complex meets O.
**(c) Short-vector necessity.**  If U ∩ O ≠ ∅ then the scaled source lattice Λ̃ = diag(o)^{-1}Λ contains a nonzero vector v ≥ 0 with |v|_1 ≤ k−1 (inside the scaled box).
**(d) Edges never obstruct.**  No cell of dimension ≤ 1 meets O (any k).
**(e) k = 2: unconditional containment (P3-T2a).**  For k = 2 and every rectangular target (including Z²), U ⊆ U′ for every source with F ⊆ F′.
**(f) Dimension reduction.**  If an m-cell, m = k, meets O then one of its (k−1)-faces (itself a cell) meets O.  Hence for k = 3 every obstruction is carried by a 2-dimensional cell.

*Proof.*  (a) Grid cubes K_n = ∏[n_i o_i, (n_i+1)o_i], 0 ≤ n_i < Q̃_i, and their faces are exactly the cells of Λ′ (Graver vectors of Λ′ in [−q,q] are ±o_i e_i; a grid face is a cell iff 0 is not one of its vertices).
(⊇) Let z ∈ B with some z_i ≥ o_i.  Let Φ(z) = ∏ I_i with I_i = {z_i} if z_i/o_i ∈ Z and I_i = [n_i o_i,(n_i+1)o_i], n_i = ⌊z_i/o_i⌋ otherwise (then z_i < A_i, so (n_i+1)o_i ≤ A_i).
Φ(z) is a grid face containing z.  Every vertex of Φ(z) has i-th coordinate ≥ o_i > 0 (if I_i is an interval, z_i ≥ o_i gives n_i ≥ 1 and the lower endpoint is n_i o_i ≥ o_i; otherwise I_i = {z_i} and z_i ≥ o_i), so 0 is not a vertex, Φ(z) is a cell, and z ∈ U′.
(⊆) A cell is a grid face ∏ I_i that does not have 0 as a vertex; 0 is a vertex iff every I_i has lower endpoint 0, so some I_i ⊆ [o_i, ∞), hence every point of the cell has z_i ≥ o_i. ∎(a)
(b) U ⊆ H ⊆ conv F′ ⊆ B, so z ∈ U ∖ U′ ⇔ z ∈ U ∩ O by (a). ∎(b)
(c) Let z ∈ U ∩ O in a cell with vertices v^(j) ∈ F ⊂ Λ, z = Σ λ_j v^(j).  In scaled coordinates ṽ ∈ N^k∖{0} and Σ_i z̃_i < k (each z̃_i < 1), while Σ_i z̃_i = Σ_j λ_j |ṽ^(j)|_1.  So some vertex has |ṽ|_1 < k, i.e. ≤ k−1. ∎(c)
(d) A point is a 0-cell in F, hence not in O (nonzero nonnegative integer vector has a coordinate ≥ 1).  Let [P,R] be a Graver segment, P, R ∈ F, g = R − P Graver (either orientation), and suppose z = (1−t)P + tR ∈ O.
In scaled coordinates z̃_i < 1 forces P̃_i = 0 or R̃_i = 0 for each i (otherwise z̃_i ≥ 1): the supports of P̃ and R̃ are disjoint.  Then g̃ = R̃ − P̃ agrees with R̃ on supp R̃ and equals −P̃ elsewhere on supp P̃, so
R̃ is conformal to g̃ (R̃_i g̃_i ≥ 0, |R̃_i| ≤ |g̃_i|), R ∈ Λ∖{0}, and R ≠ g because P ≠ 0.  Hence g is not conformally minimal: contradiction. ∎(d)
(e)/(f) Let C be a full-dimensional (m = k) cell with C ∩ O ≠ ∅ and suppose ∂C ∩ O = ∅.  O is connected and O = (O ∩ int C) ⊔ (O ∖ C) with both parts open, the first nonempty, so O ⊆ int C and 0 ∈ closure(O) ⊆ C.
C lies in the closed orthant, 0 is an extreme point of the orthant, hence 0 is an extreme point of C, i.e. a vertex of C — but vertices lie in F ∌ 0.  Contradiction, so ∂C ∩ O ≠ ∅; ∂C is a union of (k−1)-faces, which are cells. ∎(f)
For k = 2, ∂C is a union of Graver segments, which miss O by (d); for cells of dimension ≤ 1, (d) applies directly; so U ∩ O = ∅ and U ⊆ U′ by (b).  (If Q̃ has a zero coordinate, apply the 1-dimensional case of (d).) ∎(e)

## P3-T3(h) — The even-sum family (parametric obstruction classification)  [PROVED]
Let k = 3, rectangular target (scaled as above) and scaled source lattice Λ̃ = E_3 = { x ∈ Z³ : x_1 + x_2 + x_3 even } (index 2).  Then U ⊄ U′ ⇔ max_i Q̃_i ≥ 2 (with all Q̃_i ≥ 1).
*Proof.* (⇐) Say Q̃_3 ≥ 2.  g = (0,1,−1) and h = (1,0,−1) lie in E_3 and are conformally minimal there (their proper conformal subvectors (0,1,0), (0,0,−1), (1,0,0) have odd sum), the four points
(0,0,2), (0,1,1), (1,0,1), (1,1,0) lie in F (box Q̃ ≥ (1,1,2)), so P((0,0,2); g, h) is a cell.  Its point (2/3,2/3,2/3) = (0,0,2) + (2/3)g + (2/3)h lies in O, so U ⊄ U′ by (b).
(⇒) If all Q̃_i = 1: F = {(1,1,0),(1,0,1),(0,1,1)} (+ no (1,1,1), odd), only three points, so there is no 2-cell; U consists of points and Graver segments, which miss O by (d). ∎
This is the mechanism of E2-P1 (Z³ target) and of Control C; it shows that the E2-P1 failure is a statement about a **family**, and that its smallest failing box is (1,1,2) up to permutation.

## P3-T4 — Corner-cube predictor  [PROVED correctness; evaluated]
For rectangular targets with Q̃ ≥ 1 the procedure `corner_cube_predict` (build the SOURCE complex, reduce to maximal cells, solve for each cell the exact LP max{s : z(t)_i + s·o_i ≤ o_i, 0 ≤ t ≤ 1}) returns NOT_CONTAINED iff U ⊄ U′, because a cell meets O iff the optimum is > 0 (strict inequalities z_i < o_i ⇔ positive slack).  It never builds the target complex.
Input assumptions: same P and Q; Λ′ rectangular; Q̃ ≥ 1.  Unavailable otherwise (reported as `None`/UNAVAILABLE).  `short_vector_screen` implements (c) and is sound (never excludes a failing row).
Complexity: the source complex plus one LP with ≤ k+1 variables per maximal source cell, versus target complex construction (≈ ∏Q̃_i cells) plus closed splitting; see results/P3_3D.json for measured agreement and timings.

## P3-T1 / P3-T2 — summary of what is and is not established
* T2 (inaccessibility of uncovered regions): for **rectangular** targets the uncovered region is exactly the corner cube O and it is inaccessible to all source cells when k = 2 (P3-T3(e)); in k = 3 it is accessible exactly through 2-cells (P3-T3(f)).
  For d′ ≥ 2 targets (hollow / sub-threshold) **no general inaccessibility theorem is proved**; CP3-A remains OPEN there (exact finite audit: results/P3_PLANAR.json).
* T1 (finite templates): proved for the even-sum family (P3-T3(h)); the pure-lattice scan (index ≤ 8, boxes {1,2}³) lists every failing (Λ̃, Q̃) it found and checks that the corner-cube predictor reproduces each verdict; it is **evidence, not a classification theorem**.

## CP3-A (residual planar containment)  [OPEN beyond the proved classes]
Proved: containment for INHERITED_G12T8 targets (inherited), for rectangular targets (P3-T3(e), new but elementary).  Exact audit: see results/P3_PLANAR.json for the number of hollow-box / sub-threshold rows, each with an exact verdict.
No counterexample is recorded unless listed in results/P3_COUNTEREXAMPLES.json.
