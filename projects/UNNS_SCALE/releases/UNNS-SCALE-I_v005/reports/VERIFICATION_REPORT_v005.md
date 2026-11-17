# UNNS-SCALE-I v005 Verification Report (Part A: trillion-window metric theorem)

Overall: **PASS**  (mode: full, 104 s)

## Checks
- OK  71 symbolic identities of length <=4 re-verified by poly_check (division, positivity, replay): 71
- OK  per-n replay: 999384 identity-member paths replayed with integer arithmetic, all legal and ending at 10^6(n+1) (bad=0)
- OK  replay cross-checked against the independent sympy edge test on 400 random identity members (full 4-step paths)
- OK  n=1: explicit path of length 3 (<=4), valid edges, endpoints 10^6 and 2*10^6
- OK  the 614 supplied paths: every step a legal edge, 4 steps, correct endpoints
- OK  partition: identity members (999384) + {1} + uncovered (614) = 999999 = all of 1..999999, pairwise disjoint
- OK  lower bound: d(10^6 n,10^6(n+1)) = 4 at n=11 and n=13 (disjoint complete balls radii 2,1; sizes (23582, 146) and (24585, 128))
- OK  ambient excursion: largest vertex on any window path = 3.322e+22 (identity paths 1.996e+19, supplied paths 3.322e+22): exceeds 10^12 -> ambient-graph theorem
- OK  THEOREM A: every n in 1..999999 has d<=4 and d=4 occurs  =>  M_{10^6} = 4 (conjunction of all Part A checks above)
- OK  Part B: 55 additional K<=4 identities at B=10^6 re-verified by poly_check
- OK  Part B: with the 55 new identities the window has 407 values of n outside all identity classes (of the 614+1), a subset of the 614 supplied paths
- OK  Part B: the 614 exceptional n: gcd(n+1)=180, 80 have 7-smooth n+1, path shapes {'++--': 80, '+-+-': 524, '+--+': 5, '+---': 5} (no single shape)
- OK  Part B: outside-window exact scan at B=10^6: 299 values (720*2^a*p, smooth 720|n+1, random 180|n+1), max d = 4
- OK  Part B: fresh exact recomputation of 25 random scan values agrees

## Baseline protection (read-only hashing)
- v001: all files match
- v002: all files match
- v003: all files match
- v004: all files match

## Scope
- Part A is closed: finite window only; endpoints within 10^12, intermediate vertices may exceed it.
- Part B (D_{10^6} in {4,5,6}) is exploratory: its checks record data only; no universal conclusion is claimed.
- No GitHub changes; Gate 4 deferred.
