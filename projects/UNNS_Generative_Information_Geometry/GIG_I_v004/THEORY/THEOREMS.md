# GIG-I v004 — Theorem register (arithmetic hole survival)

v001, v002, v003 are frozen baselines (imported read-only). Tags as in v003: [PROVED] · [FINITE-EXACT] · [BOUNDED-NEGATIVE] · [CAND] · [OPEN].
Notation: ranks 0..k-1; D(I) = denominator of ∏_{r∈I}(c_r+1)²/c_r (v003 D-V3); X_λ(m) the history complex of content λ at source m; Pref(F) as in v003 T17.

## Pattern data (k = 6) — CERTIFICATES/pattern_H2.json
z = the 96-face 2-cycle of the v003 anchors (rank coordinates); φ = the 6-hexagon cochain; P_z = ∪_{F∈supp z} Pref(F) (43 rank sets, listed in the certificate);
**gates**  G₀ = {024},  G₁ = {15, 125},  G₃ = {3, 34, 35, 345}  (rank sets; the "new" prefix sets of the obstructed truncated octahedra T_a, a ∈ {0,1,3}, not already in P_z).
K_z(λ) = lcm_{I∈P_z} D(I).

| ID | Statement | Status |
|----|-----------|--------|
| **PS-0** (combinatorial facts) | ∂₂z = 0; φ(z) = 1; among the 540 3-faces of P_6 exactly six (the truncated octahedra ({a,2,4,5}|y|w), a∈{0,1,3}, {y,w} = {0,1,3}∖{a}) have φ(∂F) = 1. The two orderings of (y,w) have the same new prefix sets. | **[PROVED]** (finite check over P_6) |
| **PS-1** (Parametric Hole-Survival Theorem) | Let λ = (c₀<…<c₅) be ANY six distinct positive integers and m ≥ 1. If K_z(λ) | m and for each a ∈ {0,1,3} some I ∈ G_a has D(I) ∤ m, then [z] ≠ 0 in H₂(X_λ(m); F₂); in particular β₂ ≥ 1. Equivalently: z survives unless a gate is open, where gate G_a is open iff D(I) | m for all I ∈ G_a. | **[PROVED]** |
| **PS-2** (gate-0 necessity) | If K_z | m and D({0,2,4}) | m then z = ∂c with an explicit 34-face 3-chain c valid for every content. | **[PROVED]** (universal filling certificate) |
| **PS-3** (gate 1, 3 necessity) | If K_z | m and gate G₁ (resp. G₃) is open then z bounds in X_λ(m). | **[BOUNDED-NEGATIVE]** — no exception among 18,980 regimes (E15, labels ≤ 16); a universal combinatorial filling does not exist (it uses arithmetic coincidences), so a proof would need number theory |
| **PS-4** (existence) | A content λ (under a role→rank bijection σ ∈ S₆) admits a regime with [z_σ] ≠ 0 iff every gate has a set I with D(σI) ∤ K_z^σ(λ). | **[PROVED]** (m = K_z is extremal) |
| **EX-1** (the mechanism is NOT the only one) | Census of ALL 8,008 six-contents with labels ≤ 16 and ALL their 346,859 source regimes: 158 regimes have β₂ > 0 (β₂ = 3 once, at (2,3,8,9,14,15), source 1680). **52 are explained by PS-1** (for some role→rank bijection); **106 are not** — they carry other H₂ patterns (E18: 33 coarse signatures, the commonest a 50-face cycle with 4 obstructed truncated octahedra, 32 regimes). 46 of the 8,008 contents admit a PS-1 hole regime (not only the anchors). | **[FINITE-EXACT]** |
| **EX-2** (soundness census) | 18,998 regimes with z ⊂ X: 18 satisfy the PS-1 hypotheses and all 18 have [z] ≠ 0; in the other 18,980 (some gate open) z bounds in every case — no exception to PS-3. | **[FINITE-EXACT]** / PS-3 **[BOUNDED-NEGATIVE]** |
| **PS3-0 / PS3-1** (k = 7, β₃) | Same statements for the combinatorial 3-cycles z₃ (two classes: x=14-type, x=15-type) and the cochain φ₃ of CERTIFICATES/H3_*.json: φ₃(∂F)=1 for exactly six 4-faces of P_7, namely ({a,2,4,5,6}|y|w) (a∈{0,1,3}); [z₃] ≠ 0 whenever K_{z₃} | m and no H₃-gate is open. | **[PROVED]** (given the finite check over P_7) |
| **H3-C** (explicit certificates) | For the four k=7 regimes (sources 4032, 4320, 6048, 6480): z₃ (weight 438–446, ≈1000 arrangements), φ₃ (6 faces), the six obstructed 4-faces with thresholds K_z₃·{2,3,5} (contents ∋ 8,9,4,5) / K_z₃·{2,3,7}, and verified 4-chain fillings in the 7 killing regimes of each content. | **[FINITE-EXACT]** |
| **H3-E** (existence) | Among all 7-contents with labels ≤ 18 (identity role map) the parametric criterion predicts exactly four hole regimes (those four); all four have β₃ = 1 by exact homology. | **[FINITE-EXACT]** |
| **OBS-1** | In all four β₃ regimes K_{z₃} = (anchor source)·x with x ∈ {14, 15}. | observation, 4 cases |
| **GR-1** (graph reconstruction of a β₃ regime) | For content (2,3,6,7,8,9,15), source 6480 (2,160 arrangements, β = (1,0,0,1,0,0,0)): the face poset derived from the uncoloured graph equals the true one in every dimension (f = 2160, 6000, 5980, 2521, 393, 12; ranks agree; Betti agree). Run time 1,069 s. The other three β₃ regimes were not reconstructed. | **[FINITE-EXACT]**, one regime |

## What is NOT claimed
No universal necessity for gates 1 and 3 (PS-3), no claim for k ≥ 8, and the PS-1 pattern is explicitly NOT the only H₂ mechanism (EX-1); no classification of the other patterns is given.
