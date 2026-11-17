# UNNS-SCALE-I v003 — Scaled-Successor Metric Geometry

Local research release. v001 and v002 are frozen and untouched; nothing is published; GitHub is read-only reference.

**Evidence labels used throughout.**
PROVED = mathematical proof in this document (or inherited from frozen v001/v002/U1-BND and marked *inherited*).
CERTIFIED = exact, untruncated computation with an independent certificate (explicit path + disjoint-ball lower bound), valid for the listed finite cases only.
EXPERIMENTAL = finite exact data; pattern not proved.
OPEN = not decided.

A finite maximum is **never** reported as a supremum. Every finite maximum below is a CERTIFIED *lower* bound for D_B.

---

## 0. Objects

G = SELECT-II arithmetic graph on ℕ>0: edges {kN, k(N+1)²} (k,N ≥ 1); forward move x ↦ x(N+1)²/N when N | x, backward move x ↦ x·(q−1)/q² when q² | x (q ≥ 2). Edge labels are unique. d = graph distance in G (the whole graph; never a truncation).

For a scale B ≥ 1 and n ≥ 1 write

  d_B(n) := d(Bn, B(n+1)),  D_B := sup_{n≥1} d_B(n).

d_1(n) = d(n,n+1) is the distance in G itself; the inherited U1-BND theorem gives sup_n d_1(n) = 6, and the scale-copy isomorphism (v001 Theorem 2: {Bu,Bv} ∈ E ⇔ {u,v} ∈ E, labels preserved) gives sup d_{G[BN]}(Bn,B(n+1)) = 6 for every B — the *internal* supremum never changes. D_B is the *ambient* quantity.

## 1. D0 — Exact elementary laws (PROVED)

**Proposition 1.1 (d_B(n) ≥ 2).** Every edge {kN, k(N+1)²} joins numbers with ratio (N+1)²/N = N + 2 + 1/N ≥ 4. But B(n+1)/(Bn) = 1 + 1/n ≤ 2. So Bn and B(n+1) are never adjacent (and never equal): d_B(n) ≥ 2. ∎

**Proposition 1.2 (pointwise divisibility law).** If A | B then d_B(n) ≤ d_A(n) for every n.
*Proof.* Put c = B/A. The map u ↦ cu sends edges of G to edges of G (v001 Theorem 2; here only the easy direction is needed: {kN,k(N+1)²} ↦ {(ck)N, (ck)(N+1)²}). Hence d(cx, cy) ≤ d(x,y). Take x = An, y = A(n+1). ∎

**Corollary 1.3.**
(a) D_B ≤ D_A whenever A | B (Scaling Lemma, scale-wise).
(b) D_{lcm(A,B)} ≤ min(D_A, D_B).
(c) {B : D_B ≤ k} is an up-set under divisibility; certified *lower* bounds propagate **down**: if d_B(n) = k for one n, then D_A ≥ k for every A | B (indeed d_A(n) ≥ k at the same n).
(d) For every N, the mean route length μ_B(N) = (1/N)Σ_{n≤N} d_B(n) satisfies μ_B(N) ≤ μ_A(N) when A | B.
(e) D_B ≤ D_1 = 6 for all B (inherited).

**Lemma 1.4 (exit lemma).** If d_B(n) < d_1(n) then every shortest path from Bn to B(n+1) contains a vertex that is not a multiple of B. Equivalently, a shortest path lying entirely inside BN forces d_B(n) = d_1(n).
*Proof.* A path of length L inside BN pulls back, by the isomorphism G[BN] ≅ G, to a path of length L from n to n+1 in G, so L ≥ d_1(n). If a shortest ambient path were inside BN, d_B(n) ≥ d_1(n); with 1.2 (A=1) equality holds. ∎
So *all* shortening is produced by routes through the exterior of the scaled lattice (vertices whose boundary labels were quantified in v002).

**Lemma 1.5 (pivot).** d_B(n) ≤ 1 + d(B(n+1)², B(n+1)).
*Proof.* n | Bn, so forward label N = n is legal: Bn ↦ (Bn/n)(n+1)² = B(n+1)². ∎

## 2. D1 — Exact distance certificates (CERTIFIED)

**Method.** Distances are ≤ 6, so a distance is decided by meet-in-the-middle with radii (1,1),(2,2),(3,2),(3,3). Neighbourhoods are *complete* (all divisors N of x for forward moves, all q with q² | x for backward moves; factorisation by trial division + Miller–Rabin + Pollard ρ). No graph truncation occurs. d(u,v) > r+s iff B_r(u) ∩ B_s(v) = ∅, so every lower bound is a disjoint-ball certificate and every upper bound is an explicit path. `indep_check.py` re-derives neighbourhoods with sympy (no shared code with `exact_lib.py`) and re-certifies the maximum witnesses.

**Table D1 (n ≤ 6000, exact; values are counts of n with d_B(n) = k).**

| B | k=2 | k=3 | k=4 | k=5 | k=6 | mean | finite max |
|---|---|---|---|---|---|---|---|
| 1 | 2 | 23 | 3587 | 2280 | 108 | 4.4115 | 6 |
| 2 | 2 | 29 | 5105 | 864 | 0 | 4.1385 | 5 |
| 3 | 2 | 1513 | 3844 | 641 | 0 | 3.8540 | 5 |
| 4 | 2 | 35 | 5933 | 30 | 0 | 3.9985 | 5 |
| 5 | 2 | 31 | 4302 | 1665 | 0 | 4.2717 | 5 |
| 6 | 2 | 1517 | 4354 | 127 | 0 | 3.7677 | 5 |
| 7 | 2 | 355 | 3920 | 1670 | 53 | 4.2362 | 6 |
| 8 | 2 | 37 | 5953 | 8 | 0 | 3.9945 | 5 |
| 10 | 2 | 37 | 5512 | 449 | 0 | 4.0680 | 5 |
| 12 | 2 | 1520 | 4478 | 0 | 0 | 3.7460 | 4 |

First witnesses of the finite maximum (all independently certified; d = exact):
- B=1: n=163, d=6, path 163→652→2608→3406050→113400→7056→164.
- B=7: n=163, d=6, path 1141→4564→18256→3012352→27541504→331776→1148 — **D_7 = 6 (CERTIFIED, since D_7 ≤ 6)**.
- B=2: n=6, d=5: 12→98→896→224→56→14.  B=3: n=1, d=5: 3→12→54→243→24→6.
- B=4: n=503, d=5: 2012→1016064→15872→524288→8064→2016.  B=5: n=1, d=5: 5→20→90→405→40→10.
- B=6: n=6, d=5: 36→294→2688→672→168→42.  B=8: n=719, d=5.  B=10: n=60, d=5: 600→4900→1210320→9760→2440→610.
- **B=12: no n ≤ 6000 has d_12(n) = 5, but n = 25199 does**: 302388→7620480000→1661299920000→273375000→1209600→302400 (d=5, balls of radius 2,2 disjoint, sizes 2125 / 18993). So **D_12 ≥ 5**: the finite maximum 4 on n ≤ 6000 was *not* the supremum.

Hence (Cor. 1.3(c) with the smooth-n+1 witnesses of §5): D_B ≥ 5 is certified for every B dividing one of 5, 7, 10, 48 (so for 1,2,3,4,6,8,12,16,24,48 and 5,10) and D_B = 6 is certified for B | 7.

## 3. D2 — Universal upper bounds on residue classes (PROVED, with explicit exceptional sets)

**Symbolic path identities.** For a class n = Mt + r the states are integer polynomials in t. A move is polynomial division: forward by a label N(t) | S(t), backward by q(t)² | S(t) with label N = q−1. A sequence of K moves from B(Mt+r) to B(Mt+r+1) is an *identity in ℤ[t]*; it is a legal path for every integer t ≥ t₀, where t₀ is the least bound after which every label, every cofactor and every state is ≥ 1 (Cauchy bound + finite check; `poly_check.py`, sympy-free). Members t < t₀ are checked exactly with the untruncated engine.

**Example (B=12, n = 6t+1, K=4, t ≥ 1; n=1 checked exactly).**
 12(6t+1) →[+(12t+2)]→ 54(4t+1)² →[−(4t) , q=4t+1]→ 216t →[+(2t)]→ 108(2t+1)² →[−(6t+2), q=6t+3]→ 12(6t+2).

**Theorem 3.1 (PROVED).** For the pairs (B,K) below, d_B(n) ≤ K for every n lying in the listed classes; the stated fraction is the exact natural density (Σ 1/M over classes). All identities verified independently; all t < t₀ members verified exactly.

| B | K | identities | max modulus | density with d_B ≤ K proved | exceptional density (undecided at this K) |
|---|---|---|---|---|---|
| 12 | 4 | 35 | 12600 | 6299/6300 ≈ 0.99984127 | 1/6300 (2 classes mod 12600) |
| 2 | 5 | 90 | 1260 | 209/210 ≈ 0.99523810 | 1/210 (12 classes mod 2520) |
| 4 | 5 | 50 | 1260 | 209/210 | 1/210 (12 classes mod 2520) |
| 10 | 5 | 91 | 2520 | 359/360 ≈ 0.99722222 | 1/360 (7 classes) |
| 6 | 5 | 62 | 2520 | 839/840 ≈ 0.99880952 | 1/840 (3 classes mod 2520) |
| 5 | 5 | 308 | 2520 | 359/360 | 1/360 (7 classes) |
| 3 | 5 | 273 | 2520 | 247/252 ≈ 0.98015873 | 5/252 (50 classes; search budget, classes remain refinable) |

(The exact numbers are in `results/D2_B*_K*.json`; the verifier recomputes them.)

**Proposition 3.2 (an exceptional set is unavoidable for B=12, K=4).** n = 25199 ≡ 12599 (mod 12600) has d_12(n) = 5 (CERTIFIED, §2). So no K=4 identity can cover the class (12600, 12599): the K=4 statement of Theorem 3.1 is as strong as the truth allows, up to the second exceptional class (12600, 2519), whose first members have exact distance 4 or 5.

**What Theorem 3.1 does *not* say.** It does not prove D_B ≤ 5 for B = 2,3,4,5,6,10 nor D_12 ≤ 5: the exceptional classes are infinite refinement chains (n+1 divisible by growing smooth numbers). Their first members have exact distance 4 or 5 in every case examined (none has 6), which is EXPERIMENTAL support only. **D_B ≤ 5 for these B is OPEN.**

## 4. D3 — Divisibility hierarchy

By Prop. 1.2 the function B ↦ d_B(n) is order-reversing for divisibility, pointwise in n. This was re-checked on **181,500** exact pairs (A | B, n ≤ 150 or 500; B ≤ 96): **0 violations** (a check of the theorem's implementation, not its proof).

Certified lower bounds L(A) = max{d_B(n) : A | B, data in hand} (valid by 1.3(c)):

- L(A) = 6, i.e. **D_A = 6 CERTIFIED** (D_A ≤ 6 is proved), for A ∈ {1, 7, 11, 13, 17, 19, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 91}: these are exactly the scales B ≤ 96 at which a 6 occurred for some n ≤ 500 (and B=1,7 at n=163). The list is closed under divisors (7 | 91, 13 | 91).
- L(A) = 5 for A ∈ {2,3,4,5,6,8,9,10,12,14,15,16,18,21,22,23,24,25,26,27,29,33,34,35,38,39,42,45,46,48,49,50,51,55,57,58,62,63,65,66,69,70,74,77,78,81,82,85,86,87,93,94,95} (≤ 96): a distance-5 pair exists at A or at a multiple of A in our data.
- L(A) = 4 only for A ∈ {20,28,30,32,36,40,44,52,54,56,60,64,68,72,75,76,80,84,88,90,92,96}. This is a limit of the *finite data*, not a property of D_A: e.g. 20 | 60 and no 5 was found at 60 within the surveyed range, but the smooth probe (§5) finds 5s for B=12, 24, 48, and it was not run for B=20, 60, 120.
- **Observed regularity (EXPERIMENTAL):** every scale at which a 6 appeared (n ≤ 500) is coprime to 30; not every B coprime to 30 shows one (23, 29, 49, 77 do not within n ≤ 500). No multiple of 2, 3 or 5 shows a 6 anywhere in our data. Multiples of 2 or 3 reach 5 only on sparse n (B=4: n = 503, 683, 719, …; B=12: n = 25199, 37799, 201599, …).

**Strict shortening of the worst case is not established.** Neither outcome of the proposed dichotomy is proved: D_B = 6 is certified for B | 7, … ; for B=2,3,4,5,6,10,12 the certified range is 5 ≤ D_B ≤ 6 and the question whether D_B = 6 or 5 is **OPEN** (Theorem 3.1 shows that if 6 occurs it occurs only inside the exceptional classes).

## 5. D4 — Metric interpretation: typical shortening vs worst-case stabilisation

**Smooth probe (EXPERIMENTAL data, CERTIFIED witnesses).** The exceptional classes are n+1 ≡ 0 modulo large smooth numbers. Exact distances at n+1 ∈ {7-smooth numbers ≤ 3·10⁶} (budget-limited):
B=1: one d=6 at n=171499 plus 387 d=5; B=2: 227 d=5; B=4: 104 d=5; B=6: 103 d=5; **B=12: 12 d=5** (n=25199, 37799, 201599, …); **B=24: 5 d=5** (n=264599, 680399, …); **B=48: 2 d=5** (n=1133999, 2116799). Each is certified. So even B=24 and B=48 have D_B ≥ 5 although all n ≤ 6000 (resp. 500) gave ≤ 4: *finite maxima systematically under-report D_B, and the failure sits on arithmetically special n*.

**Typical shortening (EXPERIMENTAL, surveyed, exact).** δ_B(n) := d_1(n) − d_B(n) ≥ 0 (Prop. 1.2). On n ≤ 500, B ≤ 96:

| B | P(δ>0) | mean δ | δ-values |
|---|---|---|---|
| 2 | 0.200 | 0.208 | 0,1,2 |
| 3 | 0.378 | 0.476 | 0,1,2 |
| 4 | 0.320 | 0.330 | 0,1,2 |
| 5 | 0.122 | 0.124 | 0,1,2 |
| 6 | 0.444 | 0.542 | 0,1,2 |
| 7 | 0.180 | 0.180 | 0,1 |
| 12 | 0.460 | 0.560 | 0,1,2 |
| 24 | 0.464 | 0.566 | 0,1,2 |
| 48 | 0.468 | 0.570 | 0,1,2 |
| 96 | 0.470 | 0.572 | 0,1,2 |

Mean route length by divisibility class (n ≤ 500, B ≤ 96): gcd(B,6)=1: 4.171; 2|B, 3∤B: 3.971; 3|B, 2∤B: 3.749; 6|B: 3.705, with μ_{24}=3.710, μ_{48}=3.706, μ_{60}=3.706, μ_{96}=3.704.

**Interpretation.**
1. *Exact self-similarity and ambient shortening coexist, and they live in different places.* The scaled copy BN is isomorphic to G (internal geometry rigid, internal sup 6, labels preserved). The ambient distance can only be shorter (1.2), and by the exit lemma 1.4 *every* instance of shortening uses a route through the exterior of BN.
2. *Typical routes get shorter along divisibility chains and the gain saturates*: P(δ>0) and mean δ rise from 0.12–0.20 (B=5, 2) to ≈0.47 / ≈0.57 and are nearly flat from B=12 on (P(δ>0) 0.460 → 0.470 and mean δ 0.560 → 0.572 between B=12 and B=96, n ≤ 500). EXPERIMENTAL; no proof of a limit.
3. *Worst-case routes do not shorten uniformly.* D_7 = 6 is certified: the worst-case route of B=7 is exactly that of B=1 (n=163). For multiples of 2 or 3 the worst case is ≥ 5 (certified at B=12, 24, 48 on smooth n+1) and 6 is excluded by data on every n tested but not by proof (OPEN).
4. *Characterisation proved so far:* shortening is monotone for divisibility (1.2, 1.3), strict shortening needs exterior routes (1.4), and for 2 ≤ B ≤ 12 the set of n whose route is *not* decided at the stated K is a thin explicit union of residue classes (Thm 3.1).

## 6. Counterexamples recorded (PROVED/CERTIFIED)
- "D_12 ≤ 4" (from n ≤ 6000) is false: n = 25199.
- "d_B(n) = 6 ⇒ n = 163 only" is false in general: B=1 has 108 such n ≤ 6000; B=7 has 53.
- Equality D_B = D_A is certified for A=1, B=7 (both 6). A *strict* inequality D_B < D_A is **not certified for any pair** (it would need a universal upper bound D_B ≤ 5 together with a 6-witness at A).

## 7. Open problems
- O1. Is D_B ≤ 5 for some B ≥ 2? (Needs a proof that the exceptional chains contain no 6.)
- O2. Is D_B ≥ 5 for *every* B? (Certified for all divisors of 2,3,4,5,6,8,10,12,24,48 and the B above.)
- O3. Does μ_B(N) converge along divisibility chains (plateau ≈ 3.70)?
- O4. Closed form for the exceptional classes (n+1 smooth).

Gate 4 (computational benefit at 10¹² scale) remains deferred. No GitHub changes.
