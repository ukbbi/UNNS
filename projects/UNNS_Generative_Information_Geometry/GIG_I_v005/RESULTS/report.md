# GIG_I_v005 stage 1 — report
1. **Exact criterion.** For K_z | m, [z] = 0 iff the admissible extra prefix sets contain one of four minimal families (B0 = {21}; B1 = {34,38,46}; B2, B3 with 15 and 17 sets). 589,839 of 2^20 families bound z. [FINITE-EXACT]
2. **PS-1 follows** (each family contains a whole gate set), but **its converse fails for roles 1 and 3**: gate 1 needs the extra set 46; gate 3 needs 11 further sets. Only gate 0 is necessary.
3. **Counterexamples** (CERTIFICATES/gate1_/gate3_counterexample.json): contents with labels < 4.5·10⁶ and sources m for which a gate is open yet [z] ≠ 0, with explicit cochain φ′ (φ′(z)=1, φ′∘∂₃=0) verified by an independent presence rule. v004 census (labels ≤ 16) could not see them.
4. **Mechanism.** v_p(D(I)) = max(0, Σ(v_p ℓ_j − 2 v_p(ℓ_j+1))); by CRT the per-prime exclusion masks combine freely.
Not done: classification of the 106 other β₂ regimes, H₃ lifting.
