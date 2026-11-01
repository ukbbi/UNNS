# HD-C2 / HD-C3 — geometric realization of histories and rewrites

**B-T5 (PROVED).**
(a) *Trace injectivity.* States along a history strictly increase (R(N) > 1), so the set of visited states determines the history: distinct histories from one source have distinct traces in valuation space.
(b) *Area bivector.* For a word w define Omega(w) = sum_{i<j} d_i ^ d_j.  An adjacent swap of labels a,b changes Omega by exactly d_a ^ d_b; a block replacement u -> v with equal total displacement changes Omega by Omega(u) - Omega(v), independent of prefix and suffix.  So Omega is a *potential* on the rewrite complex: the signed area of every closed combinatorial loop is 0, and the area between two histories is a weighted inversion statistic.  For arrangements of 2^2 3^4 in the (v2,v3)-plane Omega = det(D2,D3)(8 - 2*inv) = -7(8-2*inv), values -56..56 in steps of 14.
(c) *Closure triangle.* The recombination bigon 1^7 vs 2^2 3^4 from 4 is the lattice triangle (2,0),(0,4),(16,0) with sides 2*D(2), 4*D(3), 7*D(1): lattice area 28 = 4*|det(D2,D3)|, and the two paths meet only at their endpoints.
**B-T6 (FINITE-EXACT).** No two distinct labels N < M <= 400 have parallel displacement vectors, so every swap diamond has nonzero area in some coordinate plane (nondegenerate square).  Open: all N.
Join example (labels 2,5,8,9,35,63 at m=280, 840): four histories with pairwise distinct traces and four distinct Omega vectors in primes 2,3,5,7; abstract loop of the extended complex (swap space 4 points, rewrite space a circle).
Scope: this realizes the 1-skeleton and the bigons.  Higher cells of the extended complex are not realized as geometric solids; coherence cells are absent.
