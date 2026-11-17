# UNNS-SCALE-I v007 Verification Report

Overall: **PASS**  (mode: full, 315 s)

## Checks
- OK  Prop (divisor-generated, h with 2h|B, n=1 mod 2h+1): midpoint B(2h+1)(n-1) and four legal edges, 247 instances; covers 111 of the 614 exceptional n
- OK  Thm A'': 2727 shapes (v',w'<=6, B=10^6), 5454 random class members: both two-step halves legal and meet at z=(B/c)(v'/Q^2)P(Q(cn/v'+1)-P)
- OK  614 exceptional n of v005: explicit closed-form four-step route for each (shapes with v',w'<=40), 614 of 614; with v',w'<=12: 613; v',w'<=3: 481
- OK  Obstruction: for the shapes with v',w'<=1 and <=2, n=k*lcm(v'P) (k=1,2,3) is covered by no shape (P>1 always, so P | c(n/v')+1 fails when P | n/v')
- OK  Prop B (linear labels, q | cn/v'... ): 613 of 614 verified witnesses; the one miss [445499] has an extended (+-|+-) witness in v006 and a Thm A'' route above
- OK  Coverage of n<=2e6 by shapes v',w'<=K (recomputed for K<=4): K=1 0.7075; K=2 0.7972; K=3 0.9770; K=4 0.9813; K=6 0.9867; K=8 0.9910; K=12 0.9948

## Baseline protection (read-only hashing)
- v001: all files match
- v002: all files match
- v003: all files match
- v004: all files match
- v005: all files match
- v006: all files match

## Scope
- Constructive route families and an obstruction to finite covering by them; no universal bound for D_{10^6} is claimed.
- No GitHub changes; Gate 4 deferred.
