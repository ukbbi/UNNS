# UNNS-SCALE-I v012 — Length–Height Trade-off and Arithmetic Routing

Labels: PROVED / CERTIFIED (exact finite computation, independently re-checked) / EXPERIMENTAL (empirical law) / OPEN.
Setting as in v011: graph SELECT-II (edges {kN, k(N+1)²}), G_C = induced subgraph on [1,C], B = 10⁶, pairs P_n = (Bn, B(n+1)).

## 0. Objects
- **τ_n(C)** = d_{G_C}(Bn, B(n+1)): the minimal route length when every vertex must be ≤ C (∞ if disconnected).
- **Frontier** H_ℓ(n) = min over routes of ≤ ℓ steps of the maximum vertex (v009/v010). H_ℓ is non-increasing in ℓ; τ_n(C) = min{ℓ : H_ℓ(n) ≤ C}. The *length–height frontier* is the staircase of pairs (ℓ_i, H_i) at which H_ℓ strictly drops.
- **κ(n)** = lim_ℓ H_ℓ(n) = connection ceiling (v011). Always κ ≥ B(n+1).
- Known: τ_n(∞) ≤ 4 for all n (v005); τ_n(10¹²) > 4 for 997,002 of 999,999 pairs (v010, Thm W); τ_n(B(n+1)) < ∞ for all n (v011, Thm K); G_C has infinite excursions forced by prime parity (v011, Thm P′, Cor. E).

## 1. PROVED statements
**P1 (staircase).** τ_n(C) is non-increasing in C, takes values in {2,3,…}, and is determined by the frontier. H_4(n) = min{C : τ_n(C) ≤ 4}; H_ℓ(n) ≥ max(B(n+1), (q(n)+1)²) for all ℓ (v011 Cor. Q).
**P2 (reduction transfer).** Let B = Q². For every C ≥ B(n+1): τ^{Q²}_n(C) ≤ τ^{Q−1}_n(C) + 2, where τ^{Q−1}_n is the same quantity for the pair ((Q−1)n, (Q−1)(n+1)).
*Proof.* q = Q gives a backward step Q²m → (Q−1)m (it needs Q² | Q²m, which always holds); apply it to both endpoints, both images and the intermediate route stay ≤ C. ∎ (For B = 10⁶: 10⁶m → 999m.)
**P3 (parity vector).** An edge {kN, k(N+1)²} changes the exponent parity vector by exactly the squarefree kernel of N. Hence every route must contain steps whose N_i satisfy sqf(n(n+1)) | ∏ sqf(N_i) and p | N_i ⇒ a vertex ≥ (p+1)². (Restatement of v011 Thm P′; it explains why the *barrier prime* q(n) is the natural scale for the confined route length in §3.) No lower bound on τ_n(κ) beyond 2 follows from it.

## 2. CERTIFIED exact results (bottleneck DP over the whole graph G_{Cmax})
Engine `tau_exact.cpp`: f_ℓ(v) = min over ≤ℓ-step walks from Bn to v of the maximum vertex, iterated (Jacobi) over **all** edges of G_{Cmax}; H_ℓ(n) = f_ℓ(B(n+1)). Exact for every ceiling ≤ Cmax; no heuristics. Independently checked by a Python bidirectional BFS that shares no code (staircase facts τ(H_i) = ℓ_i and τ(H_i − 1) = ℓ_{i+1} are reproduced), by a C++ rebuild, and for explicit routes by an edge checker.
| analogue | pairs | Cmax | max τ_n(κ) | mean τ_n(κ) | all reach κ = B(n+1)? |
|---|---|---|---|---|---|
| B = 10², n = 1..99 | 99 | 10⁷ | 10 | 5.99 | yes |
| B = 10³, n = 1..999 (window pairs) | 999 | 10⁷ | 15 | 8.63 | yes |
| B = 10⁴, 50 sampled n ≤ 9999 | 50 | 10⁸ | 13 | 8.38 | yes |
| **B = 10⁶, n = 1..199** | 199 | 10⁸ / 2·10⁸ | **6** | 4.78 | yes |
(τ_n(κ) here is the exact shortest route length with ceiling B(n+1).) The frontier of the 199 pairs at B = 10⁶ shows, e.g., n = 5: 4 steps need height 6,230,016, 5 steps need only 6,000,000 (= v009's example, reproduced).
**Window ladder at B = 10⁶** (`ladder.cpp`: exact bidirectional BFS inside G_W with node cap; 69 pairs, n from 100 to 987,507): exact τ_n(B(n+1)) is known for 62 pairs, **maximum 13**, mean 8.76; for 7 pairs the search hit the cap and only a lower bound is available (n = 36652 > 9; 492388, 714750, 878636, 912390 > 11; 726925 > 13; 783594 > 9). For the 63 exactly resolved pairs τ_n(10¹²) ∈ [4,13] (mean 7.7); at ceilings 10¹³ and 10¹⁴ (38 pairs each) the maximum drops to 10 and 7, in line with P1.
**Correction to v011.** The 12 hub routes (25–40 steps) are far from optimal: the exact shortest confined routes for the same 12 pairs have length 6–11 (hub/exact ratio 3.0–4.0). The vertex-1 hub is a feature of that *construction*, not of the arithmetic: independent shortest confined routes for n = 5, 100, 127, 160, 326 have minimum vertices 230,400, 249,975, 285,750, 160,356, 1,298,784 — they never descend toward small numbers.
**Reduction transfer (checked).** P2 holds with zero violations in 292 exact comparisons (B = 100 vs 9) and for 99 pairs B = 10⁶ vs 999; the bound τ^{999}_n(10⁶(n+1)) + 2 is within 0–2 of the exact τ^{10⁶}_n(κ) for n ≤ 99 (slack 0: 22, 1: 36, 2: 41 pairs). For larger n the same bound (B = 999 inside G_{10⁸}) is an exact upper bound but looser: n = 100, 127, 203, 326, 522, 838, 1061, 2154 → 5, 6, 6, 6, 7, 9, 11, 11 (exact 5, 6, 6, 6, 6, 6, 7, 7).

## 3. EXPERIMENTAL law: confinement length tracks the barrier prime
Least-squares fits of exact τ_n(κ) against ln q(n) (q(n) = largest prime with odd exponent in n(n+1)):
| analogue | pairs | intercept | slope (ln q) | R² |
|---|---|---|---|---|
| B = 10² | 99 | 2.53 | 1.15 | 0.55 |
| B = 10³ | 999 | 1.67 | 1.46 | 0.68 |
| B = 10⁴ (sample) | 50 | 1.90 | 1.03 | 0.77 |
| B = 10⁶ (exact n ≤ 199 + ladder to 10⁶) | 258 | 1.91 | 0.82 | 0.86 |
Regression on ln n alone has R² = 0.25 (B = 10³). Reading: the number of steps needed to stay below the larger endpoint grows roughly like a constant times ln of the largest prime that must be "flipped" (consistent with P3: that prime forces a vertex ≥ (q+1)², and the flip gadget of v011 then needs a descent whose depth grows with ln q). **Not a theorem**: slopes differ between B, censored pairs (the longest) are excluded from the B = 10⁶ fit so the fit is biased low, and R² < 1.

## 4. The length–height trade-off at B = 10⁶ (what is now known)
| ceiling C | τ_n(C) |
|---|---|
| ∞ (full graph) | ≤ 4 for all 999,999 pairs (v005) |
| 10¹⁴ | 3–7 (38 sampled pairs, exact) |
| 10¹³ | 3–10 (38 sampled pairs, exact) |
| 10¹² (window) | > 4 for 997,002 pairs (v010); 4–13 on 63 sampled pairs, ≥ 14 for n = 726925 |
| B(n+1) = larger endpoint | finite for all 999,999 (v011); exact 2–13 on 261 pairs; 6 for all n ≤ 199 |
So the price of confinement is roughly a factor 2–3 in route length (4 → 8–13) rather than the factor 6–10 suggested by v011's hub routes, and the price of *tightening* the ceiling from 10¹⁴ to B(n+1) is 0–6 extra steps (mean 3.2) on the 27 exactly resolved pairs with n ≥ 1000.

## 5. Not claimed
No proof of the q(n) law or of any growth rate of τ_n(κ); exact τ for the 7 capped pairs and for B = 10⁶ at n > 199 beyond the ladder sample is open; the whole-graph DP is limited to Cmax ≈ 3·10⁸ (memory), so exact τ at ceiling 10¹² for B = 10⁶ is available only through the ladder; whether max_n τ_n(κ) is unbounded as B → ∞ is OPEN (data: max 10 → 15 → 13 → ≥ 14 over B = 10², 10³, 10⁴, 10⁶ with different n-ranges); D_{10⁶} ∈ {4,5,6} and Gate 4 (computational benefit; route *discovery* cost must be included) remain deferred. v001–v011 untouched.
