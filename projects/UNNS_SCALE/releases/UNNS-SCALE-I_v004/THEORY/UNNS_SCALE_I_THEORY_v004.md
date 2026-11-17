# UNNS-SCALE-I v004 — Exceptional-Class Closure and Metric Certification

Local research release. v001, v002, v003 are frozen and only hashed (read-only). Nothing is published; Gate 4 (computational benefit at trillion scale) remains deferred.
All distances are distances **in the full infinite SELECT-II graph** (edges {kN, k(N+1)²}); nothing is truncated. Original-graph results only: **no extended route grammar was used or needed.**

Notation: d_B(n) = d(Bn, B(n+1)); D_B = sup_n d_B(n). Inherited from v003: 2 ≤ d_B(n); D_B ≤ 6 (U1-BND); pointwise law A | B ⇒ d_B(n) ≤ d_A(n) (so D_B ≤ D_A).
Evidence labels: **PROVED** (identity / exhaustive argument checked by sympy-free code), **CERTIFIED** (exact distance with independent disjoint-ball certificate), **EXPERIMENTAL** (finite data, no certificate of a supremum), **OPEN**.

## 0. Headline results

| Quantity | v003 status | v004 status | Label |
|---|---|---|---|
| D_10 | 5 ≤ D_10 ≤ 6 (n=60 gives 5) | **D_10 = 6** (d_10(365759)=6 and d_10(351359)=6, certified) | CERTIFIED |
| D_B for B ∈ {1,2,5,10} | D_1=6 only | **all equal 6** (divisor law from D_10 = 6) | CERTIFIED |
| B=10, d_10(n) ≤ 5 | outside 7 classes mod 2520 (density 1/360) | outside a residue set of density 114/176400 ≈ 6.46·10⁻⁴ (≈1/1548); every remaining n has 720 ∣ n+1 | PROVED |
| B=12 | d_12(n) ≤ 4 outside 2 classes mod 12600 (density 1/6300) | d_12(n) ≤ 5 outside a residue set of density 5/176400 ≈ 2.8·10⁻⁵; every remaining n has 25200 ∣ n+1; 5 ≤ D_12 ≤ 6 | PROVED / CERTIFIED |
| D_{10^6} | undecided | **4 ≤ D_{10^6} ≤ 6**; proved d ≤ 5 outside density 64/529200 ≈ 1.2·10⁻⁴; every exact distance computed at 10⁶ is ≤ 4 | open |
| New universal theorem (every B) | — | Theorem G: v2(n+1)=1 ⇒ d_B(n) ≤ 4 (n ≥ 5); v2(n+1)=3 ⇒ d_B(n) ≤ 5 (n ≥ 23) | PROVED |

Corrections to expectation: the exceptional classes of B=10 are **not** an artifact of search depth. They contain genuine distance-6 pairs. The hoped-for statement "D_10 = 5" is false.

## 1. Theorem G (2-adic route identities, valid for every scale B)

Let m = n+1.

* **G1.** If n = 4t+1 (m = 2s, s = 2t+1 odd) and t ≥ 1, then B·n ⇝ B·m in 4 steps:
  Bn → B m² = 4B s² (forward, label n) → 4B(s−1) = 8Bt (backward, q = s) → 8B(t+1)² (forward, label t) → 8B(t+1)²·(q−1)/q² with q = s+1 = 2(t+1), i.e. 2Bs = Bm (backward). 
* **G2.** If n = 16t+7 (m = 8s, s = 2t+1) and t ≥ 1, then 5 steps:
  Bn → 64Bs² → 64B(s−1) = 128Bt → 128B(t+1)² → 32Bs (q = 2(t+1)) → 8Bs = Bm (q = 2).

Proof: each step is a legal edge: forward steps need N | x (checked: the labels n, t divide the current numbers), backward steps need q² | x with q ≥ 2 (q = s ≥ 3 requires t ≥ 1; q = 2(t+1); q = 2). The endpoints are exactly Bn and B(n+1). The identities are B-free, i.e. they are statements about B = 1 that survive multiplication by any B (pointwise law). Machine check: `poly_check.verify_identity` (exact polynomial division in Z[t], Cauchy-bound positivity, numeric replay), for 13 scales; exhaustive exact-engine check for n < 4000, B ∈ {1,2,3,10}.
Exception for small n: d_1(1) = 5 > 4, so G1 is stated for n ≥ 5.

Consequence: the "s-odd pivot identity" found during the B=10 investigation (n ≡ 359 mod 720, m = 360 s, s odd) is G2 with the odd factor 45 absorbed into s. The three odd/even splits v2(n+1) ∈ {0, 2, 4, 5, 6, …} are **not** covered by any identity of this pivot shape (searches for v2(n+1)=j, j=0,2,4,…,9 with ≤4 steps after the pivot found none, negative search, see §6).

## 2. D4-A — B = 10

v003 left seven classes n ≡ 359, 719, 1079, 1259, 1439, 2159, 2519 (mod 2520), density 7/2520 = 1/360.
v004 adds Theorem G and 26 further identities (all of length 5; M ∈ {5040, 12600, 25200, 176400}) found by the linear-form symbolic search (`fast_sym`, heuristic: it may miss routes but never invents one; every identity is re-verified by `poly_check`). Examples: n ≡ 1259 (mod 5040) and n ≡ 3779 (mod 5040) are closed completely by **one** identity each.

Result: d_10(n) ≤ 5 for all n outside a set of 114 residues mod 176400 (density 0.000646). **Every** residue left open satisfies 720 | n+1. The unresolved set is therefore a "pole family": n+1 divisible by 2⁴·3²·5, where the scale 10 = 2·5 supplies too little extra content for a fixed-length symbolic route.

**Exact distances in the open family** (`D4_open_class_members_exact.json`, 342 members = first 3 members of each open class): d=4: 174, d=5: 166, **d=6: 2**.
* n = 365759, n+1 = 2⁶·3²·5·127: d_10 = **6** (6-path stored; lower bound: balls of radius 3 around 10n (1,027,634 integers) and radius 2 around 10(n+1) (21,021 integers) are disjoint ⇒ no path of length ≤ 5; sympy implementation `indep_check`, independent of the search engine).
* n = 351359, n+1 = 2⁷·3²·5·61: d_10 = **6**, same certificate type.
Since D_B ≤ 6 (v003), **D_10 = 6**, and by the divisor law D_1 = D_2 = D_5 = D_10 = 6.

Pole-family probe (`D4A_B10_pole_probe.json`): n+1 = 720·2^a·p, a = 0..5, p prime in [7,139] (186 values): d ∈ {4,5} except exactly two sporadic 6's, (a,p) = (2,127) and (3,61). Distance 6 is rare and sporadic, not a regular sub-lattice: consistent with the failure of every uniform symbolic route.

Shortening of the two witnesses (`D4A_B10_witness_shortening.json`): d = 6 at B=1,2,5,10; 5 at B=20 (both); at B=30,60,120,… 4 (n=365759: 4 for every B ≥ 30 tested; n=351359: 5 at B=40,50,100, else 4). Both fall to 4 at B = 10⁶.

## 3. D4-B — B = 10⁶ (prioritised as requested)

(i) *Inherited* upper bounds: d_{10⁶}(n) ≤ d_10(n), so d_{10⁶}(n) ≤ 5 outside the 114 open residues mod 176400 (the B=2,4,5 identities of v003 add nothing).
(ii) *Direct* cover at B = 10⁶ (K = 4 with a K = 5 fallback that was never needed): 71 identities, **all of length ≤ 4**, closing density 0.99938 of the integers at length ≤ 4. Combined with (i), the set where no ≤5 route is proved has density 64/529200 ≈ 1.2·10⁻⁴ (all residual n again have 720 | n+1).
(iii) *Exact distances* (full graph, untruncated): n ≤ 3000 (hist {2:2, 3:402, 4:2596}, mean 3.8647); 99 adversarial n (n+1 ∈ {2520·k, 720·k, 27720, 55440, 720720, …}, exceptional-class members of B=10, n=60 family): max 4; smallest members of the 64 open classes: all 4; 192 members of the open classes (3 per class): all 4. The two d_10 = 6 witnesses have d_{10⁶} = 4.
(iv) n = 60 (d_10(60) = 5) has d_{10⁶}(60) = 3, so the v003 witness for D_10 ≥ 5 does **not** transfer to 10⁶.

Status: **4 ≤ D_{10⁶} ≤ 6, open.** No distance-5 pair has been found at 10⁶; no universal ≤ 4 or ≤ 5 theorem is proved. The data are EXPERIMENTAL support for "D_{10⁶} = 4", nothing more. The acceptance condition "D_B = 5" (universal bound ≤ 5 plus an exact distance-5 witness) is **not** met; neither is "D_B = 6".

## 4. D4-C — B = 12

The two v003 classes were n ≡ 2519 and n ≡ 12599 (mod 12600), d_12 ≤ 4 elsewhere.
* n ≡ 2519 (mod 12600): **closed completely** by one 5-step identity (t0 = 0): d_12 ≤ 5 on the whole class.
* n ≡ 12599 (mod 12600): identities of length 4 (M=88200, r=12599) and 5 (M=88200, r=50399) plus Theorem G leave 5 residues mod 176400 open, each with 25200 | n+1 (density 2.8·10⁻⁵).
* Exact: 15 members of the open classes: d=4: 10, d=5: 5 (n=25199 certified, d=5); a further 66 distinct values n+1 ∈ {12600 s, 25200 s} (s ≤ 40 and s ∈ {127, 509, 1021}; `D4C_B12_pole_probe.json`) gave only 4 and 5.
Status: **5 ≤ D_12 ≤ 6** (certified lower bound 5; no distance-6 witness found; no universal ≤5 proof because of the residual density 2.8·10⁻⁵).

## 5. Why the exceptional classes resist (D4-D explanation)

* Factorisation: every unresolved class has n+1 divisible by a large smooth number (720 for B=10 and 10⁶; 25200 for B=12). The recurrent obstruction is "pole chains": refining a class (multiplying the modulus by 2, 3, 5 or 7) closes a fraction of the sub-classes but leaves sub-classes with larger smooth divisors of n+1, with density shrinking geometrically but never reaching zero in any finite refinement.
* Valuation patterns: the 2-adic identities G1/G2 handle v2(n+1) = 1 and 3 uniformly. No identity of the same pivot shape exists for v2(n+1) ∈ {0, 2, 4, …, 9} (K = 4 after the pivot). 3- and 5-adic analogues for B=1 (p=3,5; j=1,2; all residues u) were searched: none.
* Scale divisibility: a larger scale gives the route more room (B=10⁶ = 2⁶5⁶ has 49 divisors): typical d ≈ 3–4 and even both d_10 = 6 witnesses collapse to 4. This is the same direction as v003's shortening law; the failure of uniform shortening at B=10 and B=12 comes from the open smooth families, not from the typical case.
* Heuristic caveat: the symbolic search is restricted to linear-form states (products of (a·t+b)^e) and bounded caps; **failure to find an identity is never evidence that none exists**, except where an exact d=6 is certified (B=10).

## 6. Negative / unresolved results (kept on purpose)

1. Pivot-only routes (first step +n, then ≤ 4 steps from B·m² to B·m) cannot close even s for B=10 (C=360) or B=12 (C=12600), and no pivot route exists for v2(n+1) ∈ {0,2,4,…,9} (B = 1 and 10).
2. K=5 covers of the residual B=10 classes (5040-periodic start) close ≈ 40 % of each pole class in 130 s; deeper levels grow without closing (3254 pending sub-classes after 420 s).
3. B=12 pole class: 704 s of K=5 search closed 2/7 of the class at level 88200; the rest is open.
4. Heuristic (not a proof): the "gadget" move K(x−1) → (K/g)(x+g−2) needs g | (x−1) and g | K; this suggests why a bounded-length identity struggles to be uniform in the valuation of n+1 — the divisibility that must be supplied grows with the valuation.
5. B = 10⁶: no universal conclusion.

## 7. Synthesis

| | PROVED | CERTIFIED | EXPERIMENTAL | OPEN |
|---|---|---|---|---|
| universal | Theorem G (all B) | | | route grammar for v2(n+1) ∉ {1,3} |
| B = 10 | d ≤ 5 outside density 6.5·10⁻⁴ (all remaining n have 720 ∣ n+1) | **D_10 = 6** (and D_1=D_2=D_5=6) | d=6 sporadic in 720·2^a·p | exact characterisation of the d=6 set |
| B = 10⁶ | d ≤ 4 on a set of density 0.99938 (direct K=4 cover); ≤ 5 outside 1.2·10⁻⁴ | D ≥ 4 | all 3,300+ exact distances ≤ 4 | D_{10⁶} ∈ {4,5,6} |
| B = 12 | d ≤ 5 outside 2.8·10⁻⁵ | D_12 ≥ 5 | no d=6 among ≈80 distinct n tested | D_12 ∈ {5,6} |

Refined thesis for the scale hypothesis: *exact structural self-similarity + widespread metric shortening ⇏ uniform metric shortening* — now with a concrete certified instance (B = 10: the worst case equals the unscaled worst case, 6).

## 8. Reproducibility

`code/verify_all_v004.py [--quick]` re-checks every stored result with code independent of the search engines (poly_check, indep_check), recomputes all densities from the stored identities, re-runs random exact distances, and hash-checks v001–v003 read-only. `code/finalize_v004.py` rebuilds the cover result files from `results/raw/`. Raw cover outputs are in `results/raw/`.
