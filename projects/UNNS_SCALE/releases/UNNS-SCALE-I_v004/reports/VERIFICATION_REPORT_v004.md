# UNNS-SCALE-I v004 Verification Report

Overall: **PASS**  (mode: full, 114 s)

## Checks
- OK  T-G identities (n=4t+1 -> 4 steps; n=16t+7 -> 5 steps) verified by poly_check for 13 scales
- OK  T-G small members below t0 (n=1,7): bound holds exactly except n=1 at B=1 where d_1(1)=5 (so T-G is stated for n>=5)
- OK  T-G exhaustive exact check n<4000 for B=1,2,3,10
- OK  D4-A B=10: 26 identities re-verified without sympy (division, endpoint, positivity, replay)
- OK  D4-A B=10: members below t0 satisfy the bound exactly
- OK  D4-C B=12: 3 identities re-verified without sympy (division, endpoint, positivity, replay)
- OK  D4-C B=12: members below t0 satisfy the bound exactly
- OK  D4-B B=10^6: 71 identities re-verified without sympy (division, endpoint, positivity, replay)
- OK  D4-B B=10^6: members below t0 satisfy the bound exactly
- OK  D4-B direct B=10^6 identities: 71 total, 71 of length<=4
- OK  D4-A B=10: open residues recomputed = stored (114 of period 176400, density 0.000646; v003 had 7/2520 = 0.002778)
- OK  D4-A B=10: every open n has 720 | n+1 (all residual structure is 2^4*3^2*5 | n+1)
- OK  D4-A B=10: open density < 1/1500 (<~0.00067), i.e. proved d_10<=5 outside a set of density 0.000646
- OK  D4-C B=12: open residues recomputed = stored (5 of 176400; density 2.83e-05); every open n has 25200 | n+1
- OK  D4-B B=10^6: inherited-only and combined open sets recomputed = stored (combined 64 of 529200, density 1.21e-04)
- OK  D4-A witness distances at 17 scales: paths valid, pointwise law d_B<=d_A (A|B) holds; both witnesses fall to 5 at B=20 and 4 at B=10^6
- OK  D4-A D_B=6 for B in {1,2,5,10} (divisor law from D_10=6): witnesses d=6 at B=1,2,5,10
- OK  D4-A pole probe (n+1=720*2^a*p): paths valid; d=6 only at (a,p)=(2,127),(3,61); d in {4,5} otherwise
- OK  D4 open-class members: all stored paths valid (B=12: 15 members, B=10: 342, B=10^6: 192)
- OK  D4 open-class members: B=12 max 5 (n=25199, 5 members at 5), B=10 hist {4:174,5:166,6:2}, B=10^6 all d=4
- OK  D4 d=5 witnesses at B=12 and B=10 (6 each, random) certified by disjoint balls (lower bound 5 independent)
- OK  D4-C d_12(25199)=5 certified => 5<=D_12<=6
- OK  D4-C pole probe B=12 (n+1=12600 s, 25200 s; 66 distinct n): paths valid, max d = 5, no distance 6
- OK  D4-B adversarial n at B=10^6 (99 n with smooth n+1 / exceptional classes): all paths valid, max d = 4
- OK  D4-B scan n<=3000 at B=10^6: hist {2:2,3:402,4:2596}, max 4, mean 3.8647
- OK  D4-B fresh exact recomputation reproduces stored distances at B=10^6 (random sample)
- OK  D4-B fresh exact recomputation reproduces stored adversarial distances
- OK  D4 random members of new closed classes satisfy their step bound by the exact engine (36 checked)

## Baseline protection (read-only hashing)
- v001: all files match
- v002: all files match
- v003: all files match

## Scope notes
- D_10 = 6 is CERTIFIED (two exact distance-6 witnesses; lower bound by disjoint balls on the full infinite graph, upper bound D_B<=6 from v003).
- D_12 is only 5<=D_12<=6; D_{10^6} is NOT determined (certified lower bound from data: 4; proved <=5 outside a residue set of density ~1.2e-4).
- Density statements are exact Fractions over residue classes; they are not statements about all n.
- No GitHub changes; nothing published; Gate 4 deferred.
