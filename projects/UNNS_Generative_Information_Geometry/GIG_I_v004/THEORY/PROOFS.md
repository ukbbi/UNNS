# GIG-I v004 — Proofs

## PS-1 (Parametric Hole-Survival Theorem)
Let λ and m be as stated and write 𝔉 = {I : D(I) | m} (feasible family, v003 Lemma F).
1. *z lies in X_λ(m).* By v003 T17 a face F is present iff Pref(F) ⊆ 𝔉. Every face of supp z has Pref(F) ⊆ P_z and K_z | m gives P_z ⊆ 𝔉. So all 96 faces, and their boundary faces (monotonicity of K_F), are present; z is a cycle (PS-0).
2. *φ∘∂₃ = 0 on C₃(X_λ(m)).* By PS-0, φ(∂F) = 0 for every 3-face of P_6 other than the six T. A 3-face of X_λ(m) is a 3-face of P_6 with Pref ⊆ 𝔉. If it were one of the six, say a T with first block {a,2,4,5}, then Pref(T) ⊆ 𝔉; Pref(T) ∖ P_z is the gate set G_a (the two orderings give the same set, PS-0), so D(I) | m for all I ∈ G_a — the gate would be open, contradicting the hypothesis.
3. φ(z) = 1, so z ∉ im ∂₃ (otherwise φ(z) = φ(∂₃c) = 0). Hence [z] ≠ 0. ∎

## PS-0 and PS-2 (finite certificates)
PS-0 is the exhaustive check of φ(∂F) over the 540 3-faces of P_6 (E15/`make_pattern.py`, also re-implemented independently in TESTS). PS-2: the set W₀ of 3-faces F of P_6 with Pref(F) ⊆ P_z ∪ Pref(T₀) is present in every X_λ(m) with K_z | m and D(024) | m (because P_z ∪ Pref(T₀) ⊆ 𝔉). Gaussian elimination over F₂ produces a 34-face chain c ⊆ W₀ with ∂c = z; its boundary is recomputed and compared with z (assert in `universal_filling`). ∎

## PS-4 (existence)
If some m admits [z] ≠ 0 via PS-1 then K_z | m, and a gate closed at m is closed at every divisor of m, in particular at K_z; conversely closed gates at K_z give PS-1's hypothesis at m = K_z. ∎

## PS3 (k = 7)
Identical argument in P_7: φ₃∘∂₄ vanishes on every 4-face of P_7 except six (computed over all 4-faces of P_7, E16), z₃ is a cycle with φ₃(z₃)=1, and the obstructed faces are ({a,2,4,5,6}|y|w); their new prefix sets over P_{z₃} form the H₃-gates stored in the certificate. ∎

## Why PS-3 is not proved
For gates 1 and 3 the guaranteed faces (Pref ⊆ P_z ∪ Pref(T_a)) do not support a filling of z (checked: `universal_filling(1)`, `universal_filling(3)` return None), although in every content examined the actual present faces do. Present faces beyond the guaranteed ones arise from divisibility relations such as D(I) | lcm of other D's, which are number-theoretic, not combinatorial. Hence necessity there is a census statement.
