# SIB-I v005 - Register
Notation as in v004 (W(x) includes the empty word; count(x)=|W(x)|-1). SCG-01: W(x)∩W(y)=W(gcd(x,y)).

| ID | Statement | Status |
|---|---|---|
| RCS-01 | For a linear homogeneous recurrence R and N dividing every coordinate of a state s: R(T_N s)=T_N(R s). Nonlinear/affine maps fail (Sylvester, 2x+1, x^2: 100% of tested (x,N)). | PROVED (T_N is multiplication by a scalar); VERIFIED-EXACT on tested boxes |
| RCS-02 | The words admissible at a state vector are W(g), g=gcd of coordinates. For the Fibonacci-type step, gcd(a_n,a_{n+1}) is constant along the sequence (400 random starts x 60 steps checked); the same argument covers Pell-type steps (gcd(y,x+2y)=gcd(x,y)). | PROVED (Euclid) for the Fibonacci-type step; VERIFIED |
| RCS-03 | Unimodular R (integer matrix with integer inverse where positive): |anc(s)| = |T-anc(s)|(k(s)+1), k = backward chain length. Proof: R and T commute and have equal domains; positivity depends on ratios only; distinctness because a rational vector is not an eigenvector of M^j (irreducible characteristic polynomials). | PROVED for Fibonacci/Pell/tribonacci-type steps; VERIFIED-EXACT: 90,000 + 90,000 + 64,000 states, 0 failures; independent forward closure on smaller boxes |
| RCS-03n | The factorization fails for non-unimodular order-1 steps a->2a (1908/5000) and a->3a (821/5000). | VERIFIED-EXACT (counterexamples listed in results/product_formula_failures.csv) |
| RCS-04 | Sunflower: gcd(a,b)=1 => W(ha)∩W(hb)=W(ha)∩W(h(a+b))=W(hb)∩W(h(a+b))=W(h). Petal size count(hc)-count(h), same for all coprime splits of c. | PROVED (SCG-01); VERIFIED on 14,880 + 1,498 explicit word-set triples |
| RCS-05 | Suppression: petal words of a sum are not admissible at the pair state (gcd h). E.g. F_12: 15 single-term words, 0 pair-level words; h=12: 72 vs 1. | VERIFIED; follows from RCS-02 |
| RCS-06 | Same-sum control: for c=F_n, n=6..23, the Fibonacci split F_{n-1} is the unique coprime split with maximal chain n-2 (independently rechecked n<=17). | VERIFIED-EXACT; classical Euclid extremality, not UNNS-specific |
| RCS-07 | Single-term activation fraction: n=4..60: Fibonacci 0.228 vs 0.390 matched integers, Lucas 0.281 vs 0.400 (2280 control draws each); full panels n<=84 (h=1): 0.217 and 0.289, matching the v004 active-term counts. | COMPUTED, descriptive |
| O1 | Non-homogeneous or nonlinear recurrences: is there any equivariant lift (e.g. via a rescaled state)? | OPEN |
| O2 | State vectors for recurrences of order >=4 and non-unimodular order>=2 steps | OPEN |
| O3 | Whether any recurrence-conditioned quantity separates UNNS from other scalar grammars beyond alphabet gating | OPEN |
