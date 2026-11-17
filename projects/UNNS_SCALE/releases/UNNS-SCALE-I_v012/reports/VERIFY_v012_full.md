# UNNS-SCALE-I v012 verification report

mode: full

- PASS: fresh C++ rebuild of the exact bottleneck frontier, B=100, n=1..99, Cmax=10^7, reproduces F100.txt byte for byte
- PASS: fresh C++ rebuild, B=9, n=1..99, Cmax=10^7, reproduces F9_n1_99.txt
- PASS: fresh C++ rebuild, B=1000, n=1..999 (all window pairs of the scaled analogue), Cmax=10^7, reproduces F1000.txt
- PASS: fresh C++ rebuild, B=10^4, n=7,207,...,9807, Cmax=10^8, reproduces F10000.txt
- PASS: fresh C++ rebuild, B=10^6, n=1..99, Cmax=10^8, reproduces F1e6_n1_99.txt
- PASS: fresh C++ rebuild, B=999 to ceiling 10^6(n+1), n=1..99, Cmax=10^8, reproduces F999_for1e6_n1_99.txt
- PASS: all 4344 stored frontier points: lengths strictly increase, heights strictly decrease, final height >= B(n+1)
- PASS: every row flagged * reaches exactly the floor B(n+1): connection ceiling kappa = B(n+1) (scaled analogues B=100,1000,10^4,10^6)
- PASS: parity bound (v011): every frontier height >= (q(n)+1)^2 for all stored rows
- PASS: independent Python bidirectional BFS reproduces 109 staircase facts (distance at ceiling H_i equals l_i, at H_i-1 equals l_{i+1}) on B=100
- PASS: independent Python BFS reproduces 81 staircase facts on B=1000
- PASS: independent Python BFS reproduces the exact confined distance tau_n(kappa) at B=10^6 for 11 pairs
- PASS: ladder (227 (n,W) records): exact distance is non-increasing in the ceiling W for each n
- PASS: fresh C++ ladder re-run reproduces 25 stored exact distances (B=10^6)
- PASS: v012 ladder at ceiling 10^12 reproduces the v010 window distances d_W for 17 sampled pairs
- PASS: reduction-transfer lemma tau^{Q^2}_n(C) <= tau^{Q-1}_n(C)+2: B=100 vs 9 (292 exact checks, 0 violations); B=10^6 vs 999 (99 pairs, 0 violations, slack 0..2)
- PASS: reduction-based upper bounds tau^{10^6}_n(kappa) <= tau^999_n + 2 for larger n: 8 recomputed by C++, never below the exact ladder value where known
- PASS: law fits (tau_n(kappa) ~ a + b ln q(n)) recomputed: B=100 (n=1..99: R2=0.55; B=1000 (n=1..9: R2=0.68; B=10^4 (50 sam: R2=0.77; B=10^6 (exact : R2=0.86
- PASS: explicit exact-shortest confined routes (n=5,100,127,160,326; lengths [5, 5, 6, 5, 6]; minimum vertices [230400, 249975, 285750, 160356, 1298784]): edge-checked, length equals the exact DP value, max = B(n+1)
- PASS: v011 hub routes vs exact shortest confined distance (hub length, exact): [(39, 11), (34, 9), (40, 10), (30, 8), (35, 10), (30, 9), (25, 6), (39, 10), (30, 9), (32, 10), (26, 8), (29, 8)] -- exact never exceeds the hub route
- PASS: baselines v001-v011 unchanged (read-only hashing)

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

ALL CHECKS PASS
time 624 s