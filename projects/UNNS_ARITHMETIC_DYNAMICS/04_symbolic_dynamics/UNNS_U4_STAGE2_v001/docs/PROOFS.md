# UNNS_U4_STAGE2_v001 — Proofs

Author: UNNS Research Collective. Status vocabulary: **Proved (author-level)** = a complete proof is written here and every step is either elementary or cited to a named frozen/standard result; the independent verifier corroborates it on finite instances, which is *not* what makes it proved. **External review: pending** for every item. **Frozen import** = taken from a frozen release and not re-derived here.

## 0. Setting and definitions

G: vertex set N_{>0}; x ~ y iff {x,y} = {kN, k(N+1)^2} for some k, N >= 1. d = graph distance (d(x,x)=0).
Frozen imports used (all U3 / U3-COR v001, SHA in README): (I1) G is triangle-free (girth 4); (I2) deg(x)=1 iff x=1, N(1)={4}; (I3) x -> jx (j>=1) is an injective graph homomorphism; (I4) 2-8-36-9 is a 4-cycle and 6-24-96-784-27 is an induced 5-cycle.

**Window.** A finite F ⊂ N_{>0}. **Metric rule of memory m** on F: a predicate R on the (m+1)x(m+1) distance matrices D = (d(w_i,w_j)) of (m+1)-tuples w ∈ F^{m+1}. Its shift is X_R = { x ∈ F^Z : every window (x_n..x_{n+m}) satisfies R }. R sees only the distance matrix: it uses no vertex values, degrees, targets or tables. X_r(F) is the memory-1 rule [d(w_0,w_1) <= r]. "Conjugate" = topological conjugacy of subshifts.

Invariants used: a conjugacy preserves (i) the number P_n of points of least period n for every n, (ii) p_n = |Fix(sigma^n)|, (iii) topological entropy.

---

## U4.3-T2 — Fixed-point dichotomy

**Statement.** For every window F and every metric rule R of any finite memory m, |Fix(X_R)| ∈ {0, |F|}. Consequently X_R is not conjugate to any shift whose number of fixed points j satisfies 0 < j < |F|; in particular it is never conjugate to the golden-mean shift (one fixed point), since |F| = 1 would make X_R at most one point, while golden mean is infinite.

**Hypotheses.** F finite; R depends only on the distance matrix of the window (metric-only); any m >= 0.

**Proof.** A constant sequence a^Z has every window (a,…,a), whose distance matrix is the zero matrix for every a. Hence either R(0) holds, and then every a ∈ F gives a point of X_R, so |Fix| = |F|; or R(0) fails and Fix = ∅. For the second statement, golden mean has |Fix| = 1 (the point 0^Z). If X_R were conjugate to it, |Fix(X_R)| = 1 ∈ {0,|F|} forces |F| = 1, so X_R has at most one point; golden mean is infinite. ∎

**Falsification condition.** One finite F, one metric rule of memory m, with 0 < |Fix(X_R)| < |F|. (Exhaustively checked on 41,376 rules and 94,352 further rules: 0 found; this is corroboration of a proved statement, not evidence beyond it.)

**Does not establish.** Nothing about rules that read more than the distance matrix. Counter-scope (proved by exhibition, verified exactly): the degree-augmented rule "a repeat is allowed iff deg = 2, other transitions need d = 1" on F = {p, 4p}, p prime (deg(p)=2, deg(4p)>2), realises the golden-mean shift. So the obstruction is a property of *metric-only* rules, not of intrinsic rules in general. It does not say which finite shifts are realisable.

---

## U4.3-T3 — Real-spectrum obstruction (memory one only)

**Statement.** Let R be a memory-1 metric rule on F and B its 0/1 transition matrix. Then B is real symmetric, hence has only real eigenvalues; the nonzero spectrum of B (with algebraic multiplicity) is determined by (p_n)_{n>=1}, p_n = tr B^n. So X_R is not conjugate to any shift with a non-real nonzero eigenvalue in its p_n-determined spectrum, e.g. the directed 3-cycle with loops, whose matrix I+P has characteristic polynomial x^3-3x^2+3x-2 = (x-2)(x^2-x+1) and p_n = 3,3,6,15,33,….

**Hypotheses.** Memory exactly one. Metric-only. F finite.

**Proof.** The admissibility of (a,b) depends on the 2x2 distance matrix, i.e. on d(a,b)=d(b,a); so B_{ab}=B_{ba} for a≠b. For a=b the matrix is zero for all a, so B_{aa} is a constant ε; B is symmetric, so spectrum real. X_R is the vertex shift of B, so |Fix(σ^n)| = tr B^n. Newton's identities (generating series Σ p_n t^n = Σ_λ λt/(1-λt)) determine the multiset of nonzero eigenvalues from (p_n). A conjugacy preserves p_n. The target has the non-real eigenvalues e^{±iπ/3}, so no memory-1 metric shift is conjugate to it. ∎

**Lemma M1-P2.** A nonempty memory-1 metric shift has a point of least period 1 or 2. *Proof.* Nonempty means some pair (a,b) is admissible; if a=b the constant a^Z is a point; if a≠b, (b,a) is admissible by symmetry and (ab)^Z is a point of period 2. ∎

**Falsification.** A memory-1 metric rule with a non-real nonzero eigenvalue, or a nonempty one with no point of period <=2. (0 of 456 checks and 0 of 124 survey rules.)

**Does not establish.** Nothing for memory >= 2: the survey and the Y_NB theorem below show the obstruction is *memory-one specific* (68,364 of 94,352 memory-2 rules have non-real recurrent spectrum). It does not show the 3-cycle with loops is unrealisable at memory 2 (open; not found in the survey).

---

## U4.3-T4 — Radius-one entropy obstruction for full k-shifts, k >= 3

**Statement.** For k >= 3 and every finite F, X_1(F) (sequences with d(x_n,x_{n+1}) <= 1) is not conjugate to the full k-shift. More precisely ρ(A+I) <= 1 + |F|/2 where A is the adjacency matrix of G[F], while conjugacy would force |F| = k and ρ(A+I) = k.

**Hypotheses.** Radius 1, memory 1, G triangle-free (I1), F finite.

**Proof.** Transition matrix B = A+I. If conjugate to the full k-shift: p_1 = tr B = |F| = k (fixed points), and entropy log ρ(B) = log k. A is symmetric, nonnegative, and G[F] is triangle-free on k vertices. ρ(A)^2 = ρ(A^2) <= max row sum of A^2, and the row sum at v is S(v) = Σ_{u~v} d(u) (degrees in G[F]). Neighbours of v are pairwise non-adjacent and for u ~ v the sets N(u), N(v) are disjoint (no triangle), so d(u) <= k - d(v) and S(v) <= d(v)(k-d(v)) <= k^2/4. Hence ρ(A) <= k/2 and ρ(A+I) = 1+ρ(A) <= 1+k/2 < k iff k > 2. Contradiction. ∎

**Falsification.** A finite F with X_1(F) conjugate to a full k-shift, k>=3. (Checked exactly on all triangle-free graphs tested k=3..7 with Sturm sequences: no eigenvalue of A+I in [k,∞); word-counting ratios for K_{⌊k/2⌋,⌈k/2⌉} are 2.414, 3.0, 3.449, 4.0 for k=3..6, strictly below k.)

**Does not establish.** Radius 2 or larger: realisation at radius 2 holds by a *star*: F = k neighbours of a vertex h gives all pairwise distances <= 2, so X_2(F)=F^Z is the full k-shift (needs vertices of unbounded degree/τ). k=2 is realised at radius 1 (F={1,4}). Nothing about non-conjugate embeddings/factors, or about other shifts at radius 1.

---

## U4.2-T4 — Parity-period theorem

**Setting.** Base: an irreducible component C of a metric memory-1 shift on F (so B symmetric on C). Realise each transition a→b (a≠b) by a geodesic of length d(a,b), and each repeat a→a by (a,4a,a) (length 2, convention). The *period* of the realisation is the gcd g of the lengths of all closed walks of the resulting weighted graph (roof function).

**Statement.** If C contains a loop, then g ∈ {1,2}; and g = 2 iff there is f : C → Z/2 with d(a,b) ≡ f(a)+f(b) (mod 2) for all admissible a≠b in C. In particular, for the golden-mean shift on {0,1} embedded as any two vertices with distance d, g = 2.

**Proof.** The loop is a closed walk of length 2, so g | 2. g=2 iff every closed walk has even length. For a strongly connected weighted digraph, all cycle weights are even iff there is a potential f with weight(a→b) ≡ f(b)-f(a) (mod 2) on every arc (standard: define f(v) = parity of the weight of a path from a base point; consistency is the evenness of cycles). Symmetry gives d(a,b) ≡ f(a)+f(b); loops have weight 2 ≡ 0, consistent. Golden mean: only arcs 0↔1 and the loop at 0; take f(0)=0, f(1)=d mod 2; then the arc weights d(0,1)≡f(0)+f(1) holds, so g=2. ∎

**Falsification.** A symmetric base with a loop and g ∉ {1,2}, or an instance where the potential criterion and closed-walk enumeration disagree. (400 random bases: histogram {2:290, 1:110}, criterion = enumeration in all; 870 golden-mean embeddings in 1..30, all period 2.)

**Does not establish.** Needs a loop (witness without loop: {2,36}: period 4). Depends on the repeat convention (repeat of cost 1 gives period 1). It is a statement about the *path-realisation tower*, not about the base shift's mixing or entropy.

---

## U4-M2 — Memory-two non-backtracking shift

**Definition.** For finite F, Y_NB(F) = { x ∈ F^Z : d(x_n,x_{n+1}) = 1 and d(x_n,x_{n+2}) = 2 for all n }. This is a memory-2 metric rule (admissible distance matrices: (d01,d12,d02) = (1,1,2)). The full shift Y_NB = Y_NB(N_{>0}) has a countable alphabet; all statements about periodic points hold for it and for any F containing the stated orbits.

**Theorem.**
1. (Equivalence) x ∈ Y_NB iff every x_n ~ x_{n+1} and x_{n+2} ≠ x_n (non-backtracking bi-infinite walks of G).
2. (Absence) Y_NB has no point of least period 1, 2 or 3.
3. (Presence) Y_NB has points of least period 4 and 5, and infinitely many distinct periodic orbits of each of those periods.
4. (Dead end) Vertex 1 never occurs in a point of Y_NB.
5. (Not memory one) For no F, F′ is Y_NB(F) nonempty and conjugate to a nonempty memory-1 metric shift X_R(F′).
6. (Non-real spectrum) On F={2,8,36,9} the nonzero spectrum of the transition operator is {±1,±i} with multiplicity 2; on the 5-cycle window p_n = 10 if 5|n, 0 otherwise; both contain non-real eigenvalues, so neither is conjugate to a memory-1 metric shift (T3).

**Proof.**
1. d(x_n,x_{n+1}) = 1 is adjacency. Given x_n~x_{n+1}~x_{n+2}: d(x_n,x_{n+2}) ∈ {0,1,2}; it is 0 iff x_{n+2}=x_n (backtrack), 1 iff x_n~x_{n+2} (a triangle; excluded by I1), else 2. So d = 2 iff no backtrack.
2. Period 1: x~x false. Period 2: x_{n+2}=x_n gives d(x_n,x_{n+2})=0≠2. Period 3: x_{n+3}=x_n and x_{n+2}~x_{n+3} give d(x_n,x_{n+2})=1≠2.
3. The 4-cycle (2,8,36,9) read cyclically: consecutive terms are adjacent, opposite terms are non-adjacent and distinct, so at distance 2 (a path through a neighbour exists). The induced 5-cycle (6,24,96,784,27): terms two apart are non-adjacent (induced) and joined by a path of length 2, distance 2. The cyclic sequences have distinct vertices over their length so least periods are 4 and 5. For j >= 1, x ↦ jx is an injective homomorphism (I3), so images of non-backtracking walks are non-backtracking (item 1), giving orbits of the same least period for every j; distinct j give distinct orbits (the minimal element of the orbit is j·min).
4. N(1)={4} (I2). If x_n=1 then x_{n-1}=x_{n+1}=4, so d(x_{n-1},x_{n+1})=0≠2.
5. By 2, Y_NB(F) has no point of period <=2 for any F. If nonempty, a conjugacy to a nonempty memory-1 metric shift would carry a point of period <=2 (Lemma M1-P2) to one of Y_NB(F), contradicting 2 and invariance of P_n.
6. Directed edges of the 4-cycle form two directed 4-cycles under non-backtracking transitions; each permutation matrix has spectrum {±1,±i}. The 5-cycle: two directed 5-cycles, p_n = 10 if 5|n else 0. Non-real eigenvalues then conflict with T3. ∎

**Falsification.** A point of Y_NB of least period 1, 2 or 3; a point containing 1; a periodic orbit of period 4 or 5 failing the distance conditions; or a metric-only presentation of it as a memory-1 shift. (Verifier: equivalence on 668,310 non-backtracking paths for a <= 2500 with 0 triangles; period-4/5 certificates; scaling j <= 40; counts of periodic points on ball windows: ball(1,3): p_1..p_10 = 0,0,0,16,0,12,0,32,0,40; ball(1,4) with 119 vertices: p = 0,0,0,360,660,2016,….)

**Does not establish.** The topological entropy of the infinite Y_NB (countable alphabet): **open**. Exploratory lower bounds from Hashimoto spectral radii on hub windows (12, 60, 360): 2.81, 3.69, 5.21 — observations, not theorems. No universality. No statement that Y_NB generates any target sequence. Y_NB is a *constraint* defining admissible histories; it is not an autonomous generator. The Ihara–Bass relation for the window versions is prior art (not claimed).

---

## Interpretation of the memory-two survey (2C) — observations, not theorems

Preregistered survey: 10 windows (U3 r=1 realised embeddings); memories 1,2; rules enumerated exhaustively if <=14 window types, else 20,000 random subsets. Results (final, exact classifier; see amendments A1, A2): memory 1: 124 rules, 114 nonempty, 0 non-real, 0 with no period<=2 point, 0 fixed-point violations, 64 distinct 12-term signatures. Memory 2: 94,352 rules, 85,894 nonempty, 68,364 with non-real recurrent spectrum, 6,422 nonempty with no point of period <=2, 87,783 reversal-asymmetric, 0 fixed-point violations, 42,615 distinct signatures.

* Memory 2 overcomes the memory-1 real-spectrum and low-period obstructions (observed; Y_NB gives a proved instance), while T2 persists at every memory (proved, and 0 violations observed).
* Signature matches are a *necessary* condition only: NB_5_cycle 139, NB_4_cycle 522 matched at memory 2; full 2- and 3-shift 1 each at both memories; golden mean 0 (excluded by T2); directed 3-cycle with loops 0 at both memories — **not found ≠ impossible**.
* The survey is over 10 windows only; it says nothing about larger F.
