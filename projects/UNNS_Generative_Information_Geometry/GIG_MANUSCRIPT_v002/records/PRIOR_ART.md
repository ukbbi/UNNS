# PRIOR_ART — GIG_MANUSCRIPT_v002 (carried over from v001; statement labels are mapped in THEOREM_CROSSWALK_v002.md and V001_TO_V002_MAP.md)
Authorship: UNNS Research Collective. No claim of replacing Shannon theory. "None located" = searched by the authors, nothing found; it is **not** a proof of novelty. Only references whose existence was confirmed by search or fetch are cited; fields not confirmed are flagged in the bibliography itself.

Reference status (bibliography.tex): fetched and checked — Kalai 1988; Blind–Mani-Levitska 1987; Edelsbrunner–Letscher–Zomorodian 2002; Björner–Tancer 2009; Barmak–Minian 2012 (arXiv 0907.2954: Prop 2.9, Thm 2.11); Eagon–Reiner 1998; Gasharov–Peeva–Welker 1999; Borsuk 1948; Hartley 1928; Quillen 1978; Carlsson 2009; Bayer–Sturmfels (arXiv alg-geom/9711023, Prop 1.1 checked; journal reference NOT confirmed, cited by arXiv id). Existence confirmed from listings only (no page-level check): Ziegler, Björner–Brenti, Miller–Sturmfels, Cover–Thomas, Lind–Marcus, Shannon 1948, Hatcher, Munkres (lemma number not rechecked), Björner Handbook chapter (page range omitted), Carlsson–Zomorodian (volume/pages omitted). Dropped as unverified: Zomorodian–Carlsson "Computing persistent homology", Bott–Tu.

## 1. Reconstruction of K_A from the coloured swap graph (thm:swap-reconstruction)
1. *Statement.* For arbitrary A ⊆ S_k, faces of K_A = components of the J-coloured subgraph of the legal-swap graph with exactly |W_J| vertices; hence f-vector, boundary matrices over F_2, all β_j are functions of (G_A, colours, k).
2. *Earlier mathematics.* Blind–Mani-Levitska/Kalai: a simple polytope is determined by its graph. Parabolic cosets of S_k (Björner–Brenti).
3. *Inherited.* Face structure of P_k; the coset/component idea.
4. *GIG-specific.* Applies to arbitrary induced subgraphs given colours; the counting criterion |Z| = |W_J|.
5. *Unresolved.* Whether a published statement about induced subgraphs of Cayley graphs of Coxeter groups with edge colours already contains this. Not located.

## 2. Forbidden-history duality (thm:AD)
1. Ĥ_j(K_A;F_2) ≅ Ĥ^{k-3-j}(Y_A;F_2) for ∅≠A⊊S_k.
2. Alexander duality (Hatcher Thm 3.44; Munkres).
3. The entire duality statement is classical once K_A is identified with a deformation retract of S^{k-2}∖|Y_A|.
4. GIG-specific: the dictionary (history complex ↔ complement of forbidden complex in the order sphere) and its use as the organising principle.
5. Unresolved: none for the theorem; novelty of the dictionary only.

## 3. Dead-set nerve theorem (thm:nerve, lem:star)
1. For prefix-defined A, Y_A ≃ N[D_A], the nerve on minimal forbidden prefixes.
2. Nerve theorem (Borsuk; Björner); Quillen closure.
3. Nerve theorem and fibre closure.
4. GIG-specific: star-intersection lemma identifying nonempty intersections of the Z_p with compatible prefixes and showing they are cones.
5. Unresolved: whether the nerve on forbidden prefixes appears in the literature on permutation patterns/permutohedral complexes. Not located.

## 4. Strong-collapse cores (thm:barmak, cor:core-suffices, tab:D21)
1. The core of N[D_A] determines the homology of K_A; no count-level statistic does (prop:counts-fail).
2. Barmak–Minian: dominated-vertex removal is a strong equivalence; unique cores.
3. The black-box theorems.
4. GIG-specific: corpus-scoped size census (219,145 patterns, 151 positive; inherited NOT_RERUN) and the counts-fail counterexamples.
5. Unresolved: the table is a corpus fact, not a theorem.

## 5. Face thresholds and the divisibility filtration (thm:face-threshold)
1. F ∈ X_C(m) ⇔ K_F | m with K_F = lcm of vertex labels; filtration monotone; Δβ_j formula.
2. lcm labelling of cell complexes (Bayer–Sturmfels); lcm lattice (Gasharov–Peeva–Welker).
3. The labelling convention and the rank–nullity identity.
4. GIG-specific: derivation of the labels from the SELECT-II prefix rule (Lemma F).
5. Unresolved: whether the sublevel-complex/cellular-resolution reading (ch15, sec:lcm) says anything about the minimal free resolution (prob:resolution). Interpretation only; nothing was computed.

## 6. Survival law for a cycle and the atlas (thm:AT1, obs:atlas)
1. For a j-cycle z: z ⊆ X_λ(m) and [z] ≠ 0 iff K_z | m and the feasible family avoids every minimal filling family (monotone in the lattice).
2. Persistence over a multi-parameter filtration (Carlsson 2009; Carlsson–Zomorodian) is the nearest framework; rank–nullity.
3. Elementary monotonicity argument.
4. GIG-specific: the finite-lattice law for the arithmetic filtration; the 32-class atlas (bounded, inherited NOT_RERUN).
5. Unresolved: relation of the atlas to the rank invariant of multi-parameter persistence; completeness of the atlas (prob:atlas-closure).

## 7. Lift calculus and the filling-dependence map (ch08)
1. Λ, first, last, two-sided suspension L_{c1,c2}; boundary lemma LT-0; filling dependence FI-1..4; J-1, J-2, J-6.
2. Suspension/join constructions in simplicial and polytopal topology. No specific source located.
3. Standard chain-complex identities.
4. GIG-specific: the operators on permutohedral cycles with arithmetic labels.
5. Unresolved: whether the lift is a known construction (e.g. inclusion of a facet product into P_{k+1}); J-7 and ND-1 are open.

## 8. Radius-two identity and accessibility profile (thm:radius2, thm:profile)
1. |B_2(w)| = 1 + d + s − q for the swap graph (bipartite, commuting-swap squares).
2. Elementary counting in bipartite graphs.
3. All ingredients.
4. GIG-specific: the application and its use in the observation ladder.
5. Unresolved: none expected; not claimed as deep.

## 9. Pairwise-adjacency locality, k = 6 (thm:pairwise, prop:triple)
1. For every digraph G on six events with ∅≠A_G⊊S_6, β_2(K_{A_G};F_2) = 0; triples can give β_2 = 5 (N = 674).
2. Symbolic dynamics (Lind–Marcus) for the form of the constraint; Čech/Mayer–Vietoris spectral sequence.
3. The spectral sequence.
4. GIG-specific: the finite lemmas F1–F3 (computer-assisted, re-derived) and the sharpness example.
5. Unresolved: k ≠ 6 (prob:locality-k); F1 and the F2 connectedness part have no human proof.

## 10. Entropy–topology separation and recovery (ch10, ch11)
1. Equal histories-count and different Betti vector (W1–W6); anchored window; (Q,S2) separation falsified in general; S_A falsified.
2. Hartley/Shannon (Cover–Thomas).
3. Definitions of entropies and mutual information.
4. GIG-specific: all computational observations; these are corpus-scoped.
5. Unresolved: radius-three sufficiency (prob:radius3).
