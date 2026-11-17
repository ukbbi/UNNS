# UNNS-SCALE-I v014 — Scale-Lifted Uniform Routing Certificates

Labels: PROVED / CERTIFIED (exact finite computation, independently re-checked on samples) / EXPERIMENTAL / OPEN. Notation of v011–v013: G_C = SELECT-II graph on [1,C] (edges {kN, k(N+1)²}); τ^A_n(C) = d_{G_C}(An, A(n+1)); B = 10⁶; "confined length" = τ^{10⁶}_n(10⁶(n+1)).

## 0. Result in one paragraph
The v013 lift target τ⁴_n(10⁶(n+1)) ≤ 6 for all n is **false**: 8,655 of the 999,999 pairs (all with n ≥ 304,559) need 7 or 8 steps at scale 4. Nevertheless the scale-transfer bound gives, for **every** n < 10⁶, the certified uniform bound **τ^{10⁶}_n(10⁶(n+1)) ≤ 18** (≤ 16 for 991,443 pairs, 17 for 7,992, 18 for 564). With v013's exact value 14 at n = 726925, the supremum of the confined length over the trillion experiment lies in **[14, 18]**.

## 1. PROVED
**T1 (scale transfer).** Let A ∈ G_B (A ≤ B) and k = d_{G_B}(B, A). Then for every n and every C ≥ B(n+1): τ^B_n(C) ≤ 2k + τ^A_n(C).
*Proof.* Let B = a₀, …, a_k = A be a path in G_B. By the multiplier embedding (v013 L1) m·a_i — m·a_{i+1} is an edge for every m; its largest vertex is ≤ B m. Using m = n and m = n+1 gives paths Bn ~> An and A(n+1) ~> B(n+1) of k edges with all vertices ≤ B(n+1) ≤ C; concatenate with a shortest An ~> A(n+1) route inside G_C. ∎
T1 contains v013 L2/L3: along the ladder 10⁶ → 160000 → 7600 → 361 → 18 → 4 → 1 (d_{G_{10⁶}}(10⁶, A_i) ≤ i). In particular **τ^{10⁶}_n(C) ≤ 10 + τ⁴_n(C)** and ≤ 12 + τ¹_n(C), ≤ 8 + τ^{18}_n(C), ≤ 6 + τ^{361}_n(C).
**T2 (parity transport; correction of v013, §5).** If u, w ∈ G_C and v_r(u) ≢ v_r(w) (mod 2), then (r+1)² ≤ C.
*Proof.* An edge {kN, k(N+1)²} changes exponent parities exactly at the primes of odd exponent in N, so a route u ~> w contains an edge with r | N (odd exponent), hence N ≥ r and its larger endpoint k(N+1)² ≥ (r+1)². All vertices are ≤ C. ∎

## 2. CERTIFIED computations
**2.1 All-n sweep at scale 4.** For every 1 ≤ n ≤ 999,999 the exact distance d_{G_W}(4n, 4(n+1)), W = 10⁶(n+1), was computed by exact radius-3 balls from both ends inside G_W (a distance ≤ 6 is found exactly; otherwise reported as "> 6"). Result:
| τ⁴ | 2 | 3 | 4 | 5 | 6 | ≥ 7 |
|---|---|---|---|---|---|---|
| pairs | 2 | 44 | 529,358 | 186,637 | 275,303 | **8,655** |
No exception occurs below n = 304,559; per 100,000 block: 0, 0, 0, 843, 1269, 1277, 1279, 1273, 1346, 1368.
**2.2 The exceptions.** Exact radius-4 computation: τ⁴ = 7 for 8,015 and τ⁴ = 8 for 640 of them; never more. Scale 1 (radius 4): τ¹ = 5 for 1,631, τ¹ = 6 for 7,024. Scale 18 (radius 4, run only on the 640 pairs with τ⁴ = 8): τ¹⁸ = 6 (5 pairs), 7 (13), 8 (58), > 8 (564). Scale 361 (radius 3): τ³⁶¹ = 6 for 23 pairs, otherwise > 6. Scales 7600 and 160000: > 6 for all.
**2.3 Uniform bound.** Combining T1 with these exact distances, the best bound min_i(2i + τ^{A_i}) over the six ladder scales is, over all n: 12 (25 pairs), 13 (44), 14 (529,363), 15 (186,650), 16 (275,361), 17 (7,992), **18 (564)**. Hence **τ^{10⁶}_n(10⁶(n+1)) ≤ 18 for all 999,999 n** (CERTIFIED), and in the trillion window every consecutive million-spaced pair satisfies d_{G_{10¹²}} ≤ 18 (G_{10¹²} ⊇ G_{10⁶(n+1)}); the ambient maximum 4 (v005) and the confined lower value 14 (v013, n = 726925) are unchanged.
**2.4 Explicit routes.** `results/ROUTES_v014.json` stores 300 explicit routes at scale 10⁶ (descent chain, scale-4 route, ascent chain; lengths 14–18, 180 of them for exceptions); every edge is re-checked independently by the verifier.

## 3. EXPERIMENTAL / observations
- The exception rate depends on ρ(n) = q(n)/(1000√(n+1)) (parity-barrier tightness: (q+1)² vs 10⁶(n+1)): 0.14 % for ρ < 0.1, 0.45 %, 1.1 %, 0 %, 0 % for the next bins, 1.6 % for ρ ∈ [0.5,0.6), and 6.6–6.7 % for each ρ ∈ [0.6, 1) (results/OBS_rho.json). No theory explains the thresholds (n ≈ 250,000 for the change of the distance profile, n ≈ 304,559 for the first exception).
- Non-chain scales A ∈ G_{10⁶} can do much better on exceptions: an unarchived exploratory scan on 12 exceptions (scales at distance 3 and 4 from 10⁶, radius 3) gave bounds 12 for 1 and 14 for 5 of them (e.g. scales 18 and 48), while 7 had no scale with τ^A ≤ 6. These are not part of the certificate.

## 4. Corrections to the v013 record (v013 itself is frozen)
**E1 (necessary condition in v013 L4).** The condition "every prime r with odd exponent in p+1 satisfies (r+1)² ≤ p+1" was stated for general B; the correct necessary condition is T2: every prime r with v_r(B) ≢ v_r(p+1) (mod 2) satisfies (r+1)² ≤ p+1 (suggested by the reviewer). Counterexample to the old wording: B = 11, p = 43, since 11 — 44 is the N = 1 edge though 11 has odd exponent in 44 and 12² > 44. Over B ≤ 60, p ≤ 1500 (13,504 pairs): the corrected condition is never violated by a connected pair, the old wording by 21 connected pairs (results/ERRATA_parity.json). For B = 10⁶ (all exponents even) the two conditions coincide, so the v013 statements about B = 10⁶ stand verbatim; the constructive composite theorem and all route checks are unaffected.
**E2 (notation).** "T(100) = 10", "T(1000) ≥ 15", "T(10⁶) ≥ 16" in v013 §3 are finite maxima over the tested primes; T(B) := sup_{p>B} τ^B_p((p+1)²) is OPEN, including finiteness.
**E3 (v013 §4, sampled values).** "4–6 for A = 1 and 4–6 for A = 4 (giving 16 and 14)" should read: a scale-4 bound of 6 gives 16, a scale-1 bound of 6 gives 18. Note that τ⁴ ≤ 6 is false (§2.1).

## 5. Answer to the v014 question
The proposed lift "τ⁴ ≤ 6 for all n ⇒ confined length ≤ 16" is refuted as a premise (8,655 counterexamples) but the same transfer principle yields a uniform certified bound of 18, with 99.14 % of the pairs ≤ 16.

## 6. Not claimed
The value 18 is an upper bound, not the maximum: the true supremum of the confined length is in [14, 18]; no exact confined length is known for the 564 pairs with bound 18, nor for the six capped pairs of v013. The sweep is one C++ implementation, verified by slice rebuilds and by independent Python balls on 2,500 random pairs and 400 random exceptions, not by a second full independent sweep. No theory of the exception set; T(B) finiteness, D_{10⁶} ∈ {4,5,6} and Gate 4 (computational benefit including route discovery) remain open. v001–v013 untouched.
