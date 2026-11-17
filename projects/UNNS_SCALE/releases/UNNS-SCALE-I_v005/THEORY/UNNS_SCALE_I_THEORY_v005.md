# UNNS-SCALE-I v005 — Trillion-Window Metric Closure and Infinite-Scale Investigation

Local research release. v001–v004 are frozen and only hashed (read-only). Nothing is published; Gate 4 (computational benefit at trillion scale) remains deferred.
Distances are in the **full infinite SELECT-II graph** (edges {kN, k(N+1)²}); no extended grammar is used.
Notation: d_B(n) = d(Bn, B(n+1)); D_B = sup_{n≥1} d_B(n); labels PROVED / CERTIFIED / EXPERIMENTAL / OPEN as in v004.

## Part A — the trillion-window metric theorem (CLOSED)

**Theorem A.** For B = 10⁶,

    M_{10⁶} := max_{1 ≤ n ≤ 999999} d_G(10⁶ n, 10⁶ (n+1)) = 4.

(The 999,999 pairs are exactly the consecutive million-spaced pairs with both endpoints ≤ 10¹².) Every pair is joined by a path of at most four SELECT-II edges, and at least one pair (n = 11, n = 13) needs exactly four.

**Proof structure (all of it machine-checked by `verify_all_v005.py`).**
1. *Identity members — 999,384 values of n.* v004 produced 71 residue-class identities of length ≤ 4 for B = 10⁶ (class n = Mt + r, labels polynomial in t, valid for t ≥ t0 ∈ {0,1}). Each is re-verified by exact polynomial division and positivity (`poly_check`), and — independently of any polynomial machinery — every one of the 999,384 members of the window is replayed with plain integers: at each step the label N must divide the current number (forward) or (N+1)² must divide it (backward), and the last vertex must equal 10⁶(n+1). A random sample of 400 members is additionally checked with the sympy edge test (`indep_check.check_path`), tying the replay to the edge rule.
2. *The case n = 1 — 1 value.* The class containing n = 1 is only valid for t ≥ 1, so n = 1 is a below-t0 member. It has an exact 3-step path (d = 3).
3. *The 614 remaining values.* For every n not covered by the identities, the exact distance was computed (untruncated meet-in-the-middle on complete neighbourhoods); all have d = 4. Explicit 4-step paths are stored in `results/A_window_uncovered_614.json` and edge-checked by the verifier.
4. *Partition.* 999,384 + 1 + 614 = 999,999; the three sets are pairwise disjoint and exhaust 1..999999 (checked by enumeration, not by counting).
5. *Lower bound.* d_{10⁶}(11) = d_{10⁶}(13) = 4: the complete balls of radius 2 around 10⁶·n and radius 1 around 10⁶(n+1) have sizes 23,582 / 146 (n = 11) and 24,585 / 128 (n = 13) and are disjoint, so no path of length ≤ 3 exists (certificates from v004, recomputed with sympy).

*Accounting correction.* v005-seed text counted 999,385 + 614 because n = 1 was counted through an identity valid only from t = 1. The exact partition is 999,384 + 1 + 614.

**What Theorem A does not say.**
* It is an *ambient-graph* statement. Intermediate vertices exceed 10¹²: the largest vertex on any stored window path is 3.32 × 10²² (in the 614 supplied paths; identity paths reach 2.0 × 10¹⁹). It is not a four-step bound inside the finite induced graph on [1, 10¹²], and it does not show that trillion states can be computationally replaced by million states.
* It says nothing about D_{10⁶} = sup over all n ≥ 1 (Part B).
* The unscaled graph has sup_n d_1(n) = 6 (v003/v004 certified), and D_10 = 6 (v004). Hence for the window: 6 (unscaled, B = 1) vs 4 (B = 10⁶) — a sharp change of ambient metric geometry. By the divisor law d_{10⁶}(n) ≤ d_10(n), and the two d_10 = 6 witnesses (n = 365759, 351359) have d_{10⁶} = 4.

## Part B — the infinite-scale question D_{10⁶} = sup_{n≥1} d_{10⁶}(n) (EXPLORATORY, OPEN)

Known: 4 ≤ D_{10⁶} ≤ 6 (lower bound from Theorem A; upper bound from D_B ≤ 6). Proved d_{10⁶}(n) ≤ 5 outside a residue set of density 1.2·10⁻⁴ (v004). **Nothing in Part B changes this range.** The checks recorded below are data, not claims of a universal result.

**B1. Structure of the 614 exceptional n.**
* They are the window values outside the 71 direct length-≤4 identities. gcd(n+1) over them is 180 (not 720: the statement "720 ∣ n+1 for every unresolved n" in v004 refers to the larger set that is open for length ≤ 5, where the inherited B = 10 identities are also used; the K ≤ 4 gap is wider).
* 80 of the 614 have 7-smooth n+1 (2ᵃ3ᵇ5ᶜ7ᵈ); v₂(n+1) ∈ {2,…,13}, with v₂ = 2 for 304 of them.
* Path shapes (direction sequences): 524 are + − + −, 80 are + + − −, 5 are + − − +, 5 are + − − −. The shape does not correlate with 7-smoothness (64 of the 80 smooth values use + − + −). Labels, expressed as affine functions of m = n+1, vary from n to n (first-step label is the pivot n = m−1 in many cases, otherwise unrelated rational multiples of m). **No single repeating pattern emerged from the 614 paths**; a universal lift would need many valuation-adaptive classes, as in v004.

**B2. Deeper symbolic cover at B = 10⁶ (K = 4).** Resuming the v004 cover for 25 minutes added 55 length-4 identities (all re-verified by `poly_check`), reducing the window values outside identity classes from 614 + 1 to 407, with 2,154 refinement classes still pending. The refinement front does not close in finite time: the same pole-chain behaviour as in v004 (§5–6 there).

**B3. Exact distances outside the window** (`B_outside_window_scan.json`): 299 values with n+1 in the families that matter — 720·2ᵃ·p (the shape of both B = 10 distance-6 witnesses; a = 0..5, p prime 7..139: 132 values reached before the time budget), random 7-smooth multiples of 720 in [10⁶, 10¹⁰] (69), random multiples of 180 up to 5·10⁶ (98). **All have d = 4.** No distance 5 or 6 was found at B = 10⁶.

**B4. Status.** EXPERIMENTAL support for "D_{10⁶} = 4"; no proof, no certified obstruction. The two ways forward are unchanged: (i) a family of valuation-adaptive length-4 identities that provably covers every residue class (blocked so far by the pole chains), or (ii) an exact distance-5 or -6 witness with a disjoint-ball certificate. Distance-5/6 witnesses at B = 10 occur only sporadically (2 of ~190 in the 720·2ᵃ·p family) and both collapse to 4 at B = 10⁶, so (ii) is unlikely to be found by sampling alone.

## Evidence summary

| | PROVED / CERTIFIED | EXPERIMENTAL | OPEN |
|---|---|---|---|
| Window B = 10⁶, 1 ≤ n ≤ 999999 | **max = 4 (Theorem A)** | | |
| D_{10⁶} | 4 ≤ D ≤ 6; ≤ 5 outside density 1.2·10⁻⁴ | 299 + window values all ≤ 4 | exact value ∈ {4,5,6} |
| D_10 | = 6 (v004) | | |

## Reproducibility
`code/verify_all_v005.py [--quick]` (quick ≈ 4 s, full ≈ 1–2 min; no bytecode). Layout: this folder sits next to `UNNS-SCALE-I_v004` (needed for the lower-bound certificates) and the older releases; all are only read/hashed. `code/build_A.py` rebuilds the identity record from v004; `code/partB_scan.py` and `code/resume_gen.py` reproduce the exploratory data (time-budgeted).
