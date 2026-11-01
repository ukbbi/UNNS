# E2-P3 Addendum 004 -- infinite family of 3D containment failures (append-only; E2-P3 v001 untouched)

Origin: research assessment of E2-P3 (received); proof re-derived and checked here.  Scope: rectangular target lattice -- a CONTROL, not an E2-P4 target.

**Statement.**  For integers a,b,c >= 0 put q = (2+6a, 2+3b, 3+3c), R = 2^q1 7^q2 13^q3, x = 2R^2/9.  Then (primes 2,7,13, box q) C(x) = R^2/3, the source relation
lattice is Lambda_9 (orders of 2,7,13 mod 9: 6,3,3), the target is Lambda_3 = { alpha_1 even } (rectangular, orders (2,1,1)), and U(x) is NOT contained in U(C(x)).

**Proof.**  num(x) = 2R^2 has exponents (2q1+1, 2q2, 2q3), so the box is q.  D(x) = { d = 2^i 7^j 13^k, i<=q1, j<=q2, k<=q3, d >= 2, d = 1 mod 9 }, all d = 1 mod 9, so 9 | G.
28 = 2^2*7 and 91 = 7*13 are in D (28 = 27+1, 91 = 90+1) with gcd(27,90) = 9, so G = 9.  Since 2^6 = 7^3 = 13^3 = 1 mod 9: 28*2^(6a) = 2^q1 * 7 (index 1 mod 9),
91^2 * 7^(3b) = 7^q2 * 13^2, 13^3 * 13^(3c) = 13^q3 are in D; their lcm with the other d's is R, and every d divides R, so L = R.  C(x) = 2R^2/9 + R^2/9 = R^2/3.
Source cell: u=(0,0,3), g=(0,1,-2), h=(2,0,-1); its corners (0,0,3),(0,1,1),(2,0,2),(2,1,0) satisfy 2^i 7^j 13^k = 1 mod 9, lie in the box (q >= (2,2,3)), and g,h are conformally minimal in the
lattice (minimality does not depend on the box), so P(u;g,h) is a 2-cell for every (a,b,c).  w = u + (5/6)g + (2/3)h = (4/3,5/6,2/3) lies in it.  The target is rectangular with orders o=(2,1,1) and
the box satisfies q >= o, so by P3-T3(a) U' = { z in box : max z_i/o_i >= 1 }; here z_i/o_i = (2/3, 5/6, 2/3) < 1, so w is not in U'.  QED

**Checked.**  results/P4_3D.json:p3_infinite_family -- all 8 instances (a,b,c) in {0,1}^3: G=9, L=R, next=R^2/3, cell corners in the source lattice, w in the cell, w in the open corner cube.  Independently
recomputed for (0,0,0) and (1,1,1) in RUN_VERIFY S5.  **Not claimed:** that the face-restriction essentiality of the base specimen persists for all (a,b,c) (the box changes the face lattices); that remains a separate analysis.
