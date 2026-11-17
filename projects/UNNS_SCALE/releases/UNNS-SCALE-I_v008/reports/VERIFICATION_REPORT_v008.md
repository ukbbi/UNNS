# UNNS-SCALE-I v008 Verification Report

Overall: **PASS**  (mode: full, 236 s)

## Checks
- OK  Thm L: (d,v,P,Q) coordinates give exactly the legal (N,q) pairs, bijectively (89 numbers, 959780 pairs, complete divisor enumeration)
- OK  Lemmas on all 12862 stored (+-|+-) routes of v006 (B=10^6): legality, midpoint law, integer system S1/S2, n | N Q^2 P'^2 (r-1), n+1 | M Q'^2 P^2 (q-1), n <= N(M+1)^2 q^2 (r-1): failures none
- OK  Absorption Lemma: each of 50345 primes l || n or l || n+1 (l not dividing B) divides N, M+1 or r-1 (resp. M, N+1 or q-1): unabsorbed 0
- OK  Growth: 1713 n with exact minimal route label T (complete enumeration): every n has a route; n <= T^4(T+1)^2; T >= l-1 for every prime l || n(n+1) coprime to B (violations 0); observed log T/log n: min 0.500, median 0.914
- OK  Growth: exact recomputation of the minimal label for 30 stored n agrees
- OK  Thm S (bounded forward labels): symbolic identities for D(r) (cubic term 0, r^2 coefficient K1(c0-1-m0), degenerate case q+1=c0(r+1)); 0 degenerate tuples for N,M<=40; search N,M<=6 with q=rho*q0, r=sigma*r0: exactly 126 routes, 25 distinct n (max 37179), all legal
- OK  Prime scan: 560 prime n (400 below 1e6, rest 1e9..1e10), exact: every prime has a (+-|+-) route, every route absorbs the prime in N (never in M+1 or r-1); minimal label >= p-1; sample recomputed
- OK  Erratum: shape (v',w',c,d)=(3,1,1,1) has rho=1/2 (P=1, no congruence condition): routes exist for all 10000 multiples of 3 in [3,30000]; n<1500 edge-checked independently (sympy BFS)
- OK  Corrected obstruction: shapes with P>1 (v',w'<=2) cover no multiple of L=lcm(v'P) (L has 116 digits); shapes with P=1 are not obstructed
- OK  Coverage n<=2e6 (recomputed for K<=8): uncovered with rho>1 only vs with rho<1 added: K=1 585051 -> 585051; K=2 405526 -> 405526; K=3 46086 -> 2698; K=4 37485 -> 2698; K=6 26668 -> 692; K=8 18059 -> 387; K=12 10497 -> 4; K=20 7803 -> 2; K=40 6170 -> 1
- OK  Adversarial: 28 numbers n = k*L_S (S=5..30; every constant-ratio shape with rho>1, v',w'<=12 and P<=S fails by construction) still have exact (+-|+-) routes; 25 of them have a minimal route with rho<1 (P=1) or P>S
- OK  Residual: n<=2e7 uncovered by all constant-ratio shapes with v',w'<=20 (rho>0): 48 numbers; each re-tested uncovered; every one has an exact (+-|+-) route (none without)

## Baseline protection (read-only hashing)
- v001: all files match
- v002: all files match
- v003: all files match
- v004: all files match
- v005: all files match
- v006: all files match
- v007: all files match

## Scope
- Exact route coordinates and necessary conditions, bounded-label finiteness, erratum to v007; no universal bound for D_{10^6} is claimed.
- No GitHub changes; Gate 4 deferred.
