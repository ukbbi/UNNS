# UNNS-SCALE-I v006 Verification Report

Overall: **PASS**  (mode: full, 11 s)

## Checks
- OK  E1: all 49 divisors 2^a 5^b of 10^6 present
- OK  E1: 36 scales with a distance->=5 witness: explicit paths valid; 36 lower bounds re-derived with the primality-audited complete-ball checker
- OK  E1: D_A = 6 certified for A in [1, 2, 4, 5, 8, 10]
- OK  E1: divisor-lattice consistency (a witness at B forces D_A >= d for every A | B): holds
- OK  E1: scales with no distance-5 case in the time-boxed search (before E3): [800, 1600, 4000, 8000, 20000, 40000, 62500, 100000, 125000, 200000, 250000, 500000, 1000000]
- OK  E3: d_800(551339) = 5 certified (path + audited balls [5935, 80927]): D_800 >= 5
- OK  E3: scales [1600, 4000, 8000, 20000, 40000, 62500, 100000, 125000, 200000, 250000, 500000, 1000000]: max distance found [4] (exact, time-boxed; NOT upper bounds)
- OK  Audit: D_10 = 6 (n=365759, 351359), D_4 = 6 (62459), D_8 = 6 (122939), D_1 = 6 (365759), d_12(25199) = 5: every factorisation proved (max prime factor 6.69e+11 < 3.3e24)
- OK  Prop 1 (d<=4 iff B_2(x) meets B_2(y)): consistent with the exact distance engine on 60 random pairs (and the meeting length equals d when d<=4)
- OK  E2b+E2c: 12862 (+-|+-) four-step witnesses verified by direct integer arithmetic (sets {'outside': 297, 'exceptional': 614, 'small': 400, 'random': 1498, 'random window': 5990, '720*smooth': 1063, 'random to 1e9': 3000}); n with no (+-|+-) witness: []
- OK  E2: census of 14 n with complete radius-2 balls: every n meets with min total length 4; pair counts {'+-|+-': 14, '++|++': 4, '+-|++': 1}

## Baseline protection (read-only hashing)
- v001: all files match
- v002: all files match
- v003: all files match
- v004: all files match
- v005: all files match

## Scope
- Exploratory release: no universal bound for D_{10^6} is claimed. Finite-window theorem (v005 Part A) is untouched.
- Lower bounds use complete balls with proved factorisations; upper bounds are explicit edge-checked paths.
- No GitHub changes; Gate 4 deferred.
