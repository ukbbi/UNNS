# UNNS-SCALE-I v011 — Window Connectivity and Arithmetic Excursion Barriers

Labels: PROVED / CERTIFIED (exact finite computation, independently re-checked) / EXPERIMENTAL / OPEN. B = 10⁶, C = 10¹², graph = SELECT-II (edges {kN, k(N+1)²}), G_C = induced subgraph on [1,C].
New quantity: **connection ceiling** κ(x,y) = min over ALL routes (any length) of the maximum vertex. Always κ ≥ max(x,y), and H_ℓ(x,y) ≥ κ(x,y) for every length budget ℓ (H_ℓ = minimal ceiling for routes of ≤ ℓ steps, v009/v010).

## 1. Barrier theorems (PROVED)
For an edge {kN, k(N+1)²}: v_p(k(N+1)²) − v_p(kN) = 2v_p(N+1) − v_p(N).
**Theorem P (large primes; reviewer's invariant).** If p > √C then v_p is constant along every route inside G_C. (N+1 ≤ √C < p, so p ∤ N, p ∤ N+1.)
**Theorem P′ (parity barrier; strengthens P).** The parity of v_p changes across an edge only if v_p(N) is odd, i.e. p | N, so N ≥ p and the larger endpoint k(N+1)² ≥ (p+1)². Hence any route (any length, any ceiling) between x and y with v_p(x) ≢ v_p(y) (mod 2) contains a vertex ≥ (p+1)².
**Corollary Q.** For x = Bn, y = B(n+1) let q(n) = the largest prime with odd exponent in n(n+1) (n, n+1 coprime). Then κ(Bn, B(n+1)) ≥ max(B(n+1), (q(n)+1)²), and the same bound holds for H_ℓ for every ℓ.
**Corollary E (infinite family of necessary excursions).** For every B and every prime p > B with p ∤ B, every route of any length from Bp to B(p+1) contains a vertex ≥ (p+1)², so the excursion ratio is ≥ (p+1)/B → ∞. (First proved unbounded-growth statement for the minimal necessary excursion; it holds for all route lengths.)
**Consequence for the finite window.** G_{10¹²} is disconnected (e.g. 1 and 1,000,003). For window endpoints 10⁶m, m ≤ 10⁶, all prime factors are < 10⁶, and q(n)+1 ≤ n+2 ≤ 10⁶+1, so Theorem P′ never separates a window pair; indeed (q(n)+1)² ≤ B(n+1) for every n < 10⁶ (checked exhaustively).
Checks (CERTIFIED): brute force over all edges of G_{10⁵} (quick) / G_{3·10⁵} (full); exhaustive components of G_C for C = 10⁴, 10⁶, 3·10⁷: zero violations of constant v_p (p > √C) and constant parity ((p+1)² > C); component counts cross-checked with scipy at C = 10⁷.

## 2. Exact connection ceilings on scaled analogues (CERTIFIED, Kruskal union-find over edges ordered by larger endpoint)
For B = 10², 10³, 10⁴ with all pairs (Bn, B(n+1)) answered up to the stated ceiling:
- κ_B(n) = max(B(n+1), (q(n)+1)²) with **no exception** on 216,683 answered pairs (B = 10³: n ≤ 2·10⁵; B = 10⁴: n ≤ 10⁵; B = 100: n < 10⁴). For B = 10³ and 10⁴ every unanswered pair has predicted ceiling beyond the computed range (no contradiction).
- For primes p > B the ceiling is exactly (p+1)² (4,088 primes): Corollary E is tight there.
- In particular every window pair (n < B) has κ = B(n+1): connected inside [1, B(n+1)] by some route, **no excursion at all** for unlimited length.
- The law is not universal in B or n: B = 100 shows exceptions from n = 10,402 (> B²), and B = 999 (not of the form Q²·…) deviates for 185,699 of 473,121 pairs. Statement for general B: OPEN.

## 3. Window connectivity at B = 10⁶ (CERTIFIED — Theorem K)
Tools (PROVED lemmas): *Reduction:* B·m → 999·m is one backward step (q = 1000, since 10⁶ = 1000²). *Scaling:* for a prime p with N+1 < p for all labels involved, the vertices {s·p} with s·p ≤ C form a copy of G_{⌊C/p⌋}. *Flip gadget:* s·p — s(p+1)² (N = p) — s·d·(p+1−d) for every d | p+1 (backward q = (p+1)/d). *Hub:* the component of vertex 1 in G_{10⁹}, computed exactly by union-find over all 6.4·10⁸ edges.
Result for the 10⁶ vertices B·m, m = 1…10⁶: **692,823** have 999m in the hub (direct); **257,432** are linked by a flip gadget with explicit (s, d) and exact phase-1 ceilings κ(999m′, s) ≤ C/p; **49,487** are linked by a ≤2-step search that stays ≤ B·m; the last **258** large primes p (m = p ≥ 284,587) are linked via the vertex p (route B·p ~> p inside the p-copy of G_{1776}, then a ≤4-step search from p inside [1, B·p]). Hence:
**Theorem K.** All vertices 10⁶·m (1 ≤ m ≤ 10⁶) lie in one component of G_{10¹²}. For every 1 ≤ n ≤ 999,999 the endpoints 10⁶n and 10⁶(n+1) are joined by a route whose maximum vertex is exactly 10⁶(n+1), i.e. **κ(10⁶n, 10⁶(n+1)) = 10⁶(n+1) for all 999,999 pairs** (lower bound trivial, upper bound from the stored link certificates; ceilings recomputed in the verifier). A first pass left 124 pairs with a link ceiling above B(n+1); they were closed by re-linking the 258 prime vertices with ceiling B·m.
Explicit routes (sample of 12 pairs, edge-checked): 25–40 steps, max vertex exactly B(n+1) — versus ≤ 4 steps that must leave [1, 10¹²] for 997,002 pairs (v010).

## 4. Meaning: excursion necessity is a length-budget phenomenon
For the million-spaced pairs the shortest routes (≤4 steps) are wormholes that need heights up to 10¹⁹–10²²; with unlimited length no excursion above the larger endpoint is ever needed (Theorem K). The trade-off function τ(n,h) = shortest route length with ceiling h satisfies τ(n,10¹²) ≥ 5 for 997,002 n (v010; window distances 5–10, > 10 for 14 of 62 sampled), τ(n, B(n+1)) ≤ 25–40 on the sampled pairs (upper bounds only). Exact τ and its growth are OPEN. Unbounded excursion *is* forced for other pairs (Corollary E: primes p > B), at every length.

## 5. Not claimed
No exact τ(n,h); no proof of the κ-law for general B; no change to D_{10⁶} ∈ {4,5,6}; Gate 4 (computational benefit) stays deferred; v001–v010 untouched. Union-find correctness for the 10⁹ run rests on the same code that is cross-checked by scipy at 10⁷ and reproduced by the full verifier.
