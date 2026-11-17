# UNNS-SCALE-I v009 verification report

mode: full

- PASS: E2: S2 (=B) and S1 hold but n=Q^2 a N/B = 27/5 is not an integer (converse of L' needs B | Q^2 a N)
- PASS: E1: shape (1,2,1,1) rho=2 at n=3: first congruence holds (u=4), second fails (u'=3 mod 2): no route
- PASS: every shape (K=8, 4369 shapes) yields exactly one consistent residue class, modulus P v' w' (or its CRT-reduction dividing it)
- PASS: class membership <=> route (n >= n0), 2797 random shape/n tests: failures 0
- PASS: union of K=8 shapes equals union of their classes on 2<=n<6000: mismatches 0
- PASS: covering search: no finite certificate reached; rigorous uncovered-density upper bounds {'4': '2.01e-03', '8': '2.99e-04', '12': '8.12e-06'}; dead nodes {'4': 0, '8': 0, '12': 0}
- PASS: re-run K=4 covering (independent run): uncovered upper bound 2.02e-03 <= 5e-3, finished=False
- PASS: height table: 337 stored minimal-height shortest paths re-checked (legal, endpoints, length d, max=hmin): failures 0; inside-domain 51, forced-outside 286
- PASS: height over ALL simple routes of length<=4 (278 n): stored per-length minimal paths legal: failures 0; forced outside [1,B(n+1)] even with all routes<=4: 197; n where a non-shortest route is strictly lower than every shortest: 90 of 268
- PASS: distances in the table are all <= 4 (d in [2, 3, 4])
- PASS: wormhole family n=3k, 4|B: legal 4-route with max vertex B(n+2)^2 (k=1..40), excursion ratio (n+2)^2/(n+1)
- PASS: baselines v001-v008 unchanged (read-only hashing)

## Baselines
- v001: OK
- v002: OK
- v003: OK
- v004: OK
- v005: OK
- v006: OK
- v007: OK
- v008: OK

ALL CHECKS PASS
time 22 s