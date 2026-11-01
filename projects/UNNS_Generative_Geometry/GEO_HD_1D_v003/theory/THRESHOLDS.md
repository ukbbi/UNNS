# THRESHOLDS -- Stage A (arithmetic foundation; D6-T1, D6-T2)

Scope: all statements are about histories from a FIXED source m (an arbitrary positive integer). Complete histories (squarefree source) are a separate restriction and are not used here.
Status words: PROVED (hand proof in this file, plus independent numerical corroboration), FINITE-EXACT (exhaustive in a stated box, no proof), OPEN.
Same-author caveat: all proofs and the independent verifier were written by the same author (Claude); this is not human review. C3 is NOT claimed; novelty is NOT assessed.

Relation to earlier releases (nothing is re-derived for its own sake): D6-T1 and D6-T2 of the v002 specification are the theorems D-T7, D-T7', D-T8 of GEO_HD_1D_v002 (preserved, byte-identical). The new items below are the prefix-set form (P), the gcd reduction (G), and saturation (S).

## D6-T1  Threshold law (PROVED, = v002 D-T7)
Delta_p(N) = 2 v_p(N+1) - v_p(N). For an ordering w = (N_1..N_l): K(w) = prod_p p^{b_p}, b_p = max(0, max_j -sum_{i<=j} Delta_p(N_i)). Then w is admissible from m iff K(w) | m, and K(w) is the smallest admitting source.

### (P) Prefix-set form (PROVED, new)
For a finite multiset S of labels put kappa(S) = prod_p p^{max(0, -sum_{x in S} Delta_p(x))}. Then
  K(w) = lcm_{j=1..l} kappa({N_1,..,N_j}).
*Proof.* sum_{i<=j} Delta_p(N_i) depends only on the multiset {N_1..N_j}, so b_p(w) = max_j max(0, -Delta_p({N_1..N_j})). QED
Consequences. (i) A set S is *feasible* at m iff kappa(S) | m iff m * prod_{x in S}(x+1)^2/x is an integer; w is admissible iff all its prefix sets are feasible. (ii) For distinct labels, admissible histories are exactly the maximal chains emptyset < S_1 < ... < C of feasible subsets, so the whole route theory is a theory of the family F(m) of INFEASIBLE proper subsets. (iii) If w, w'' differ by two swaps at different positions, the intermediate word has K | lcm(K(w), K(w'')) (its prefix sets are prefix sets of the two ends).
A set S is infeasible iff for some prime p: sum_{x in S} Delta_p(x) < -v_p(m): a *knapsack-type threshold* per prime, which is the resource-contention picture used in OBSTRUCTIONS.md.

### (G) Dependence on the source only through gcd(m, P(C)) (PROVED)
Let P(C) = prod of the labels with multiplicity. Then K(w) | P(C) for every arrangement, hence w is admissible from m iff it is admissible from gcd(m, P(C)). *Proof.* Delta_p(N) >= -v_p(N), so b_p <= sum of v_p over the labels. QED. (Verifier X1.)

## D6-T2  Induced-subgraph monotonicity and saturation (PROVED, = v002 D-T7', D-T8(c) plus (S))
(a) The swap graph of content C at m is the subgraph of the arrangement graph induced on A(m) = {w : K(w) | m}; if m | m* then A(m) is contained in A(m*) and classes only merge or appear, they never split. The number of classes is not monotone.
(S) Saturation. If P(C) | m then A(m) is everything and the swap graph is connected (the arrangement graph of a multiset under adjacent exchanges is connected). *Proof.* by (G). QED
(b) The graph depends only on the lcm-closed set {K(w)}; every graph shape that occurs occurs at a source in the finite lcm-closure.

## Baseline (v002 D-T10, re-verified by direct simulation in X3)
Content {2,3,14}, source 14q: thresholds 14,14,28,28,21,21; connected iff 28 | 14q or 42 | 14q iff 2|q or 3|q; so 2 classes iff gcd(q,6)=1 else 1 (q < 240 in the fast run, q < 600 in --full).
