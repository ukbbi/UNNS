# HD-C1 / HD-CQ1 — active coordinates and irreducible multi-prime obstructions

**B-T1 Passive-coordinate theorem (PROVED).** A prime p that divides no label of A never binds: Delta_p(N) = 2 v_p(N+1) >= 0 for N in A, and the admissibility requirement v_p(state) >= v_p(N) = 0 is empty.  Hence admissibility of every history over A, and every complex built from it, depends only on the active primes P_act(A) = {p : p | N for some N in A}.  (Verified on 85,369 random histories in the builder and 61,473 independently; dropping an ACTIVE prime changes admissibility in ~4,000 control cases.)  Passive coordinates still evolve: they matter for occurrence geometry, not for admissibility.
Corollary: valuation-span rank is not an obstruction dimension (C-B1, C-B2).

**Definitions.** For a distinct-label content C and resource vector e = (v_p(m))_{p active}: relax(p) sets the p-constraint to infinity.  Feature = Betti vector of the permutohedral GF(2) route complex.  p is *essential* if relaxing p alone makes the complex contractible; *support* = smallest prime set whose constraints alone preserve the Betti vector; *cut order* = smallest number of simultaneously relaxed primes that makes the complex contractible.

**B-T3 Irreducible multi-prime obstructions (PROVED by explicit exact computation, independently reproduced):**
| feature | alphabet | source | primes needed (all essential) |
|---|---|---|---|
| 2 components | {2,3,4,5,6} | 4 | 2,3,5 |
| 2 components | {2,3,4,5,6,7} | 4 | 2,3,5,7 |
| loop (b1=1) | {2,3,4,5,8} | 32 | 2,3,5 |
| loop (b1=1) | {2,3,4,5,6,7} | 24 | 2,3,5,7 |
In each case relaxing ANY single active prime leaves a contractible complex, so the obstruction is genuinely 3- (resp. 4-)dimensional in the sense of HD-CQ1.  The candidate alphabets A3*, A4* of the specification are among these; source 30 is only a feasibility control (contractible).
Mechanism: in these examples the obstruction is a conjunction of independent single-prime blockers (cut order 1), not a synergy.

**B-T4 Census (FINITE-EXACT; box cap 500 resource vectors per content).** k=4 labels in 2..30 (23,751 contents, 6,522 features), k=5 labels in 2..16 (3,003 contents, 2,864 features) and k=5 containing label 2 with others in 3..26 (10,626 contents, 8,544 features):
* disconnections occur with support 2, 3, 4;  loops with support 2 and 3 (never 4 for k<=5);  voids only with support 2;
* cut order is 1 in every one of about 17,900 nontrivial feature instances: no synergistic (cut order >= 2) obstruction was found.
Open: loops/voids of support >= 4/3, synergy, and a general-s family (see OPEN_PROBLEMS).
