# UNNS-SCALE-I v013 — Scale Descent and Confined-Route Bounds

Labels: PROVED / CERTIFIED (exact finite computation, independently re-checked) / EXPERIMENTAL / OPEN. Notation of v011–v012: G_C = SELECT-II graph on [1,C] (edges {kN, k(N+1)²}); τ^B_n(C) = d_{G_C}(Bn, B(n+1)); κ_B(n) = connection ceiling; the "confined length" is τ^B_n(B(n+1)).

## 1. PROVED statements (scale calculus)
**L1 (multiplier embedding).** For every M ≥ 1, s ↦ Ms maps edges of G_C to edges of G_{MC} (k ↦ Mk in {kN, k(N+1)²}). Hence for D | B and C′ = (B/D)·C: τ^B_n(C′) ≤ τ^D_n(C); in particular **τ^B_n(B(n+1)) ≤ τ^D_n(D(n+1))**: the confined length is non-increasing along divisibility.
**L2 (square descent; generalizes v012 and the reviewer's remark).** If s ≥ 2 and s² | B, put A = B(s−1)/s². Then Bm — Am is an edge for every m (backward step q = s: x(q−1)/q²), so τ^B_n(C) ≤ τ^A_n(C) + 2 for all C ≥ B(n+1). Iterating gives τ^B_n(C) ≤ 2k + τ^{A_k}_n(C) along any chain.
**L3 (the 10⁶ ladder).** 10⁶ m → 160000 m → 7600 m → 361 m → 18 m → 4 m → m is a path of six backward steps (q = 5, 20, 20, 19, 3, 2) for every m, with heights decreasing from 10⁶ m. So d_{G_{10⁶m}}(m, 10⁶m) ≤ 6 and, for every C ≥ B(n+1) and i = 1..6, τ^{10⁶}_n(C) ≤ 2i + τ^{A_i}_n(C) with (A_i) = (160000, 7600, 361, 18, 4, 1).
**L4 (prime-flip composite).** Let p > B be a prime, p ∤ B. If B and 1 are joined inside G_{p+2} and p+1 and B are joined inside G_{p+1}, then τ^B_p((p+1)²) ≤ d_{G_{p+2}}(B,1) + 1 + d_{G_{p+1}}(p+1,B), and κ_B(p) = (p+1)² exactly.
*Proof.* Multiply the first path by p (L1): Bp ~> p, heights ≤ (p+2)p < (p+1)². Step p → (p+1)² (N = p). Multiply the second path (read backward) by p+1: (p+1)² ~> B(p+1), heights ≤ (p+1)². The lower bound κ ≥ (p+1)² is v011 Cor. E. ∎
For B = 10⁶ the first leg is the ladder L3: **6 steps for every prime p > 10⁶** (uniform). The second leg is finite only if every prime r with odd exponent in p+1 satisfies (r+1)² ≤ p+1 (parity barrier in G_{p+1}), which is why the composite route applies to only a fraction of the primes (§2.4).
**Remark (what L1 does not give).** Scale monotonicity cannot by itself give a uniform bound: the pair at a small scale D is connected at its own ceiling D(n+1) only if D(n+1) ≥ (q(n)+1)² (v011), so for n with large barrier prime only the large scales are available.

## 2. CERTIFIED computations (exact bottleneck DP over whole graphs; engines of v012)
**2.1 Divisor lattice.** All 49 divisors D of 10⁶, n = 1..99, exact frontiers (Cmax = max(100D, 10⁴); 10⁸ for D = 10⁶). Checking L1 at every frontier point against every multiple D′ = MD: **735 divisor pairs, 86,409 checks (68,060 further points lie beyond the stored range), 0 violations.** Connected at κ_D for n ≤ 99: D = 1: 4/99; 10: 15/99; 25: 66/99; 50: 79/99; every D ≥ 100: 99/99. Mean confined length over the connected pairs decreases with scale: D = 100: 5.99; 10³: 5.75; 10⁴: 4.69; 10⁵: 4.66; 10⁶: 4.42.
**2.2 Generalized descent.** 28 (B, s) combinations (B = 100, 400, 900, 10⁴, 10⁶; every s² | B tested listed in results/descent/index.txt), n = 1..99: **3,484 checks, 0 violations**; slack of the bound τ^A+2 over the exact τ^B: 0 (423 times, i.e. the inequality is attained), 1 (1,023), 2 (1,655), 3 (226), 4 (157).
**2.3 Scale chain at 10⁶.** Exact frontiers at the six chain scales A_i (headroom 10⁶, n = 1..99): **612 checks of τ^{10⁶}_n(C) ≤ 2i + τ^{A_i}_n(C), 0 violations**. The best chain bound (min over i, using the exact lower-scale distance) exceeds the exact τ^{10⁶}_n(κ) by 0 (5 pairs), 1 (31), 2 (60), 3 (3); mean bound 6.04 vs exact 4.42, maximum 8 vs 6.
**2.4 The forced-excursion family (primes p > B).** Exact whole-graph DP at B = 100 (405 primes in (100, 3000)) and B = 1000 (262 primes in (1000, 3000)): **κ = (p+1)² for every prime** (Cor. E is sharp), and the exact shortest route with ceiling (p+1)² has length 5–10 (mean 8.73) at B = 100 and 9–15 (mean 12.70) at B = 1000. Exact bidirectional distances at larger p: B = 100, p = 5003…9973: 8–10 (8 primes); B = 1000, p = 10007…100003: 11–15 (8 primes); B = 10⁶: p = 1000037: 14, p = 1000081: 16 (others capped, > 10…14). Regression on ln p has slope 0.05 (B = 100) and −0.04 (B = 1000): **the confined length at the forced height does not grow with p over the tested range while the forced height (p+1)² grows without bound.** The composite bound of L4 applies to 111/405 (B = 100), 74/262 (B = 1000) and 53/362 (sampled, B = 10⁶) primes, is never below the exact value, and exceeds it by 1.95 / 2.23 steps on average (max 10 / 9); at B = 10⁶ the explicit composite routes have 11–24 steps (p = 1000003: 13) with first leg always 6.
**2.5 The seven capped pairs of v012 (B = 10⁶).** Upper bounds from L3 plus exact distances at the lower scale (C++ bidirectional BFS), lower bounds from the exhaustive capped searches:
| n | τ_n(B(n+1)) | n | τ_n(B(n+1)) |
|---|---|---|---|
| 726925 | **= 14** | 878636 | 12–13 |
| 36652 | 10–11 | 912390 | 12–13 |
| 492388 | 12–13 | 714750 | 12–14 |
| 783594 | 10–14 | | |
Explicit independent Python routes (edge-checked, all vertices ≤ B(n+1)) exist for n = 36652 (12 steps), 726925 (16), 783594 (14), 878636 (14).

## 3. EXPERIMENTAL / interpretation
- **Bounded forced length.** Hypothesis: T(B) := sup over primes p > B of τ^B_p((p+1)²) is finite. Data: T(100) = 10 (405 primes + 8 up to p = 9973), T(1000) ≥ 15, T(10⁶) ≥ 16 — so T appears to grow slowly with B, not with p. Combined with Cor. E: forced excursions cost unbounded *height* but (empirically) bounded *length*.
- The q(n)-correlation of v012 is unchanged; v013 adds scale-structure but no new asymptotic law.

## 4. Answer to the v013 question (constructive upper bounds)
No unconditional closed form F(B, n) is proved. What is now rigorous and constructive: (i) the relative bounds L1–L3 (non-increasing in scale, +2 per square-descent step, six-step ladder at 10⁶); (ii) the composite prime-flip bound L4 with a uniform six-step first leg; (iii) certified intervals for every pair that v012 left capped, one of them exact. A uniform bound over all n < 10⁶ would follow from a certified bound on d_{G_{10⁶(n+1)}}(A n, A(n+1)) for one chain scale A; the sampled values are 4–6 for A = 1 and 4–6 for A = 4 (giving 16 and 14), but a certificate over all 999,999 values of n was not computed (OPEN, expensive).

## 5. Not claimed
No proof that T(B) is finite or that τ_n(κ) is O(ln q(n)); no certificate for all n; D_{10⁶} ∈ {4,5,6}; Gate 4 (computational benefit including route discovery) remains deferred. v001–v012 untouched.
