# UNNS-SCALE-I v014 verification report

mode: full

- PASS: scale-transfer lemma: for 200 random scales A (<= 3 steps from 10^6 in G_{10^6}) and random m, the multiplied path edges (1146 edge checks, independent neighbour sets) are SELECT-II edges with height <= 10^6 m
- PASS: d_{G_{10^6}}(10^6, 4) <= 5: explicit path 10^6 -> 160000 -> 7600 -> 361 -> 18 -> 4 (edge-checked, heights <= 10^6)
- PASS: summary statistics recomputed from the stored sweep and exception files equal SUMMARY_v014.json
- PASS: all-n sweep of tau^4_n(10^6(n+1)), n = 1..999,999: {'2': 2, '3': 44, '4': 529358, '5': 186637, '6': 275303, '9': 8655} (digit 9 = no route of <= 6 steps); 8655 exceptions (n_min = 304559); exception list = positions of digit 9
- PASS: fresh C++ rebuild of sweep slices [(1, 3000), (150000, 152000), (249500, 251000), (304000, 312000), (500000, 503000), (700000, 705000), (996000, 1000000)] reproduces the stored digits
- PASS: independent Python balls (radius 3, sympy) reproduce the sweep digit for 2500 random n (no mismatch)
- PASS: independent Python: 400 random exceptions have no route of <= 6 steps at scale 4 inside [1, 10^6(n+1)]
- PASS: exceptions: tau^4 in {7, 8} for all 8655 ({7: 8015, 8: 640})
- PASS: fresh C++ rebuild of tau^4 (radius 4) for 300 random exceptions reproduces EXC_A4_R4
- PASS: fresh C++ rebuild of tau^1 (radius 4) for 300 random exceptions reproduces EXC_A1_R4
- PASS: fresh C++ rebuild of tau^361 (radius 3) for 300 random exceptions reproduces EXC_A361_R3
- PASS: fresh C++ rebuild of tau^18 (radius 4) for 15 random pairs with tau^4 = 8 reproduces EXC_A18_R4_on_eq8
- PASS: independent Python balls reproduce the exact tau^4 (7 or 8; lower bound = no meeting within radius 3+3) on random exceptions
- PASS: explicit routes at scale 10^6 (300 routes, lengths [14, 15, 16, 17, 18]): endpoints, ceiling 10^6(n+1), and every edge verified independently
- PASS: uniform bound: best chain bound max over all n = 18; 991443 pairs bounded by <= 16, 7992 by 17, 564 by 18 (histogram {12: 25, 13: 44, 14: 529363, 15: 186650, 16: 275361, 17: 7992, 18: 564})
- PASS: v013 erratum: corrected parity condition never violated by a connected pair (13504 pairs), v013 wording violated by 21 connected pairs (e.g. [(2, 7), (3, 11), (5, 19)])
- PASS: experimental observation table OBS_rho.json recomputed from the sweep
- PASS: baselines v001-v013 unchanged (read-only hashing)

## Baselines
- v001: OK
- v002: OK
- v003: OK
- v004: OK
- v005: OK
- v006: OK
- v007: OK
- v008: OK
- v009: OK
- v010: OK
- v011: OK
- v012: OK
- v013: OK

ALL CHECKS PASS
time 752 s