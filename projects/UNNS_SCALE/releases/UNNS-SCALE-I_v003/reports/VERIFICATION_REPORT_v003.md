# UNNS-SCALE-I v003 Verification Report

Overall: **PASS**  (mode: full, 90 s)

## Checks (each re-derived from stored results; independent code where stated)
- OK  D0 Prop 1.1: edge ratio (N+1)^2/N >= 4 > 2 >= (n+1)/n  (N<2000 exhaustive; identity (N+1)^2-4N=(N-1)^2)
- OK  D0 Prop 1.2 pointwise law d_B(n)<=d_A(n), A|B: 181500 exact pairs, 0 violations
- OK  D0: all surveyed distances in {2,..,6}
- OK  D0 Cor 1.3(d): mean route length monotone along divisor pairs (survey)
- OK  D0/D1 independent (sympy ball) recomputation matches stored survey: 72 pairs
- OK  D1 exact engine reproduces stored survey (960 pairs)
- OK  D1 results present for B=1,2,3,4,5,6,7,8,10,12
- OK  D1 every histogram sums to 6000 and mean matches
- OK  D1 histograms equal the table quoted in THEORY
- OK  D1 independent certificates re-run (explicit path + disjoint balls): 20
- OK  D1 B=7 attains 6 at n=163 and B=1 at n=163: D_7=6 certified
- OK  D1 no n<=6000 gives d_12(n)=5 (finite max 4)
- OK  D2 all 909 identities re-verified without sympy (division, endpoint, positivity, numeric replay)
- OK  D2 covered + exceptional classes are pairwise disjoint (partition of N)
- OK  D2 densities sum to 1 and match stored fractions
- OK  D2 densities as quoted: 12:6299/6300, 2/4:209/210, 10/5:359/360, 6:839/840, 3:247/252
- OK  D2 random members of covered classes (n up to ~10^7) satisfy d_B(n)<=K by the exact engine: 280 checked
- OK  D2 B=12: n=25199 lies in an exceptional class and has d=5
- OK  D2 worked example in THEORY (B=12, n=6t+1) is the stored identity
- OK  D3 certified D_B=6 list as quoted
- OK  D3 pointwise law: 181500 pairs, 0 violations
- OK  D3 all D=6 scales are coprime to 30
- OK  D3 closed under divisors
- OK  D4 smooth probe present for B=1,2,4,6,12,24,48
- OK  D4 witness paths valid (first three d>=5 per B)
- OK  D4 hist quoted: B=12 has 12 d=5, B=24 has 5, B=48 has 2, B=1 has one d=6 (n=171499)
- OK  D4 max witnesses (incl. B=1, n=171499, d=6) re-certified independently
- OK  D4 mean route length by class (gcd(B,6)=1: 4.171, 2|B: 3.971, 3|B: 3.749, 6|B: 3.705)
- OK  D4 shortening table (P(delta>0), mean delta): 2:(.200,.208) 3:(.378,.476) 6:(.444,.542) 12:(.460,.560) 96:(.470,.572)
- OK  D4 exit lemma data: delta>0 never exceeds 2 in the survey

## Baseline protection (read-only hashing)
- v001: all files match
- v002: all files match

## Scope notes
- Finite maxima are CERTIFIED LOWER bounds on D_B, never suprema (THEORY section 0).
- Theorem 3.1 gives upper bounds only on explicit residue classes; the exceptional classes are OPEN at that K.
- D_B < 6 for any B is NOT established; D_B = 6 is certified for the 21 scales listed (and their divisors).
- Sympy-free polynomial verification (poly_check) and sympy-ball certificates (indep_check) share no code with sym_lib / exact_lib.
- No GitHub changes; nothing published; Gate 4 deferred.
