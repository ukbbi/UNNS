# HD-E2 — what can and cannot be said between SELECT-II and FIELD-I

Snapshot relation R_P = {(m, x) : v_P(m) = v_P(x)} is defined (bridge_tests.R_P) and compared only on explicit trajectories.
**B-T12 (PROVED / FINITE-EXACT).**
* One-step obstruction (PROVED): R(N) = (N+1)^2/N >= 4 with equality only at N = 1 ((N+1)^2 - 4N = (N-1)^2); every rigid FIELD-I step ratio is <= 2.  So no single FIELD-I step in the rigid regime coincides with a SELECT-II edge.
* Restricted intertwining (PROVED given the inherited x_{n+3} = 4x_n; checked on 480 rigid-orbit states): C^3(x) = 4x = T_1(x), where T_1 is the SELECT-II edge with label 1.  Sampling a rigid FIELD-I orbit every third step is exactly the SELECT-II history 1^k; snapshot relation: SELECT-II states 4^(k+1) are R_{2,3}-related to FIELD-I index 3k.
* This is a statement about C^3 restricted to the rigid domain.  It is NOT a conjugacy, not an equivalence of C with any SELECT-II map, and says nothing about transient strands (arithmetic progressions, whose steps (n+c+1)/(n+c) are < 4).
Not attempted: HD-E3 boundary-event correspondence, a common organizing law.
