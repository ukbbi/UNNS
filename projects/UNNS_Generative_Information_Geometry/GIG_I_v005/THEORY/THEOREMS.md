# GIG-I v005 (stage 1) — theorems

Setting: six distinct labels λ, source m, the common 96-face 2-cycle z and 6-face obstruction cochain φ of v003/v004 (rank coordinates).
For a face F of P_6, F ∈ X_λ(m) iff D(I) | m for every I ∈ Pref(F) (GIG-T16/T17). With K_z | m the family A(m) ⊇ P_z (43 prefix sets); the remaining freedom
is the subset S = A(m) \ P_z of the 20 remaining prefix sets EXTRA = {8,9,10,11,21,24,25,26,27,34,38,40,41,42,43,46,56,57,58,59} (rank bitmasks).

**PS-5 (exact survival criterion) [FINITE-EXACT, GF(2) over all 2^20 families].** For K_z | m: [z] = 0 in H_2(X_λ(m);F_2) iff S contains one of the four minimal families
- B0 = {21}
- B1 = {34, 38, 46}
- B2 = {8,9,10,11,24,25,26,27,40,41,43,56,57,58,59}
- B3 = {8,9,10,11,24,26,27,34,40,41,42,43,46,56,57,58,59}.
Equivalently [z] ≠ 0 iff K_z | m and S contains none of B0..B3. 589,839 of the 1,048,576 families bound. The criterion holds for every content (it is a statement about P_6 only).

**PS-1 is a corollary [PROVED given PS-5].** Every B_i contains a complete gate set (G0={21} ⊂ B0, G1={34,38} ⊂ B1, G3={8,24,40,56} ⊂ B2,B3), so "all gates closed" excludes all four families.

**PS-2 (gate 0) [FINITE-EXACT]** B0 = {21}: gate 0 open ⇒ z bounds, for every content (agrees with v004's universal 34-face filling).

**PS-3′ (gate 1 and gate 3 are NOT necessary) [FINITE-EXACT, explicit certificates].** v004 Open Problem P1 is refuted: there are contents and sources with G1 open (resp. G3 open) in which [z] ≠ 0.
- Gate 1: labels (634404, 1566830, 1769151, 2255330, 3302454, 3302705) with the source m in CERTIFICATES/gate1_counterexample.json — T_1 present, φ′ with φ′(z)=1, φ′∘∂_3 = 0 verified.
- Gate 3: see CERTIFICATES/gate3_counterexample.json (obstructed octahedra of roles 1 and 3 all present, [z] ≠ 0).
The v004 census (labels ≤ 16) showed no such case only because small labels cannot realise the required prime patterns.

**PS-6 (realisation mechanism) [PROVED].** v_p(D(I)) = max(0, Σ_{j∈I}(v_p(ℓ_j) − 2 v_p(ℓ_j+1))), so A(m) = ∩_p {I : w_p(I) ≤ v_p(m)}. By the Chinese Remainder Theorem the per-prime weight vectors can be prescribed independently (odd primes; entries 0, 1,2,… or −2,−4,…); hence any intersection of single-prime masks is realised by some content. The shipped certificates come from this construction (E21).

Not claimed: a closed-form description of which (λ,m) realise each B_i-exclusion pattern; the classification of the 106 other β₂ regimes; anything about H_3.
