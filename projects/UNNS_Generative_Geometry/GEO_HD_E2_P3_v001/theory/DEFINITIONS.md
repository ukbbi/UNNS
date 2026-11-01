# E2-P3 — Definitions

All statements are for FIELD-I states x = a/b (reduced), active prime set P = {p_1..p_k}, exponent box Q = [0,q_1]×…×[0,q_k], q_i = ⌊v_{p_i}(a)/2⌋,
and a transition x → x′ = C(x) = a′/b′ with the **same** P and Q (E2-P2 "admissible"; checked, not assumed).

* Λ_b = ker(χ_b : Z^k → (Z/b)^×), χ_b(α) = ∏ p_i^{α_i}.  F = (Λ_b ∩ Q)∖{0}, F′ = (Λ_{b′} ∩ Q)∖{0}.  FIELD-I gives F ⊆ F′.
* Region Graver set G = conformally minimal nonzero vectors of Λ_b ∩ [−q,q]  (= Graver ∩ box).
* **Cell** P(w; g_1..g_m) = { w + Σ t_i g_i : t_i ∈ [0,1] }, g_i ∈ G independent, all 2^m vertices in F (m = 0 point, 1 Graver segment).
  U = U(Λ,Q) = union of all cells; H = conv F; U ⊆ H (every cell is the hull of its vertices).  Primed objects for the target.
* **Coverage gap** 𝒢′ = H′ ∖ U′.
* **Maximal cells**: cells not contained (vertex-wise, hence geometrically, by convexity) in another cell.
* **Planar normal form (GEO-I v004 S1, re-proved in THEOREMS P3-L1).**  k = 2: o_i = ord_b(p_i), C = ⟨p_1⟩∩⟨p_2⟩ ⊆ (Z/b)^×, d = |C|, a = o_1/d, c = o_2/d,
  Λ_b = diag(a,c)·Γ_{d,s},  Γ_{d,s} = {(i,j) : j ≡ s·i (mod d)}, s a unit mod d; Q_norm = (⌊q_1/a⌋, ⌊q_2/c⌋).
* **Target classes (planar).**
  * `INHERITED_G12T8`: d ≥ 2 and Q_norm ≥ (d,d), Q_norm ≠ (d,d)  (U′ = H′ by GEO-I v012 G12-T8).
  * `RESIDUAL_EXCEPTIONAL_HOLLOW_BOX`: d ≥ 2, Q_norm = (d,d).   `RESIDUAL_SUBTHRESHOLD_BOX`: d ≥ 2, min Q_norm < d.
  * `RESIDUAL_D1_RECTANGULAR`: d = 1 (Λ_b = o_1Z × o_2Z), b > 1.   `TARGET_Z2_TRIVIAL`: b′ = 1 (Λ′ = Z²).
  * `OUTSIDE_NORMALIZED_MODEL`: the exhaustive period check of the normal form failed (never occurred).
* **Rectangular target** (any k): Λ_{b′} = ⊕ o_i Z (index = ∏ o_i, o_i = ord_{b′}(p_i)); scaled box Q̃ = (⌊q_i/o_i⌋); b′ = 1 gives o = (1..1).
* **Corner cube** of a rectangular target: O = {z ∈ R^k : z_i < o_i for all i} (open).
* **Verdicts.**  CONTAINED (U ⊆ U′), NOT_CONTAINED (with certificate), UNAVAILABLE (limit reached; never silently dropped).
* **Certificates** (exact rational; checked by `certificate_check.py`, which imports nothing from the engine):
  * NONCONTAINMENT: source cell, witness w, parameters t ∈ [0,1]^m with w = base + Σ t_i g_i, and for every maximal target cell an inequality a·x ≤ c valid on all
    its vertices (hence on the cell) with a·w > c strictly.
  * CONTAINMENT: a closed-splitting tree of the source cell; each leaf polytope has all its vertices inside one target cell.
  * HULL-COVER tree for H′ (root checked to equal conv F′): leaves in single target cells, or `gap` leaves carrying a witness point outside every target cell.
* **Gates.** SOURCE_PASS, GEOMETRY_PASS, PLANAR_AUDIT_COMPLETE, 3D_WITNESS_PASS / NO_WITNESS_IN_SCOPE, THEOREM_PASS / COUNTEREXAMPLE / OPEN,
  C3_CANDIDATE / SCOPED_THEOREM_ONLY / RESEARCH_NEGATIVE, plus EXACT_PASS (does not imply novelty), PLANAR_THEOREM_PASS, 3D_THEOREM_PASS.
