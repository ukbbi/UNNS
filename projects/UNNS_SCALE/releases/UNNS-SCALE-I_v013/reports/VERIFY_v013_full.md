# UNNS-SCALE-I v013 verification report

mode: full

- PASS: scale ladder 10^6 m -> 160000 m -> 7600 m -> 361 m -> 18 m -> 4 m -> m consists of six edges for every sampled m (independent neighbour sets)
- PASS: generalized descent: B m -- B(s-1)/s^2 m is an edge whenever s^2 | B (sampled B, s, m)
- PASS: multiplier embedding: edges of G_C map to edges under s -> M s (sampled)
- PASS: summary statistics recomputed from stored data equal SUMMARY_v013.json
- PASS: embedding lemma tau^{D'}_n(M h) <= tau^D_n(h) (M = D'/D): 86409 exact checks over 735 divisor pairs of 10^6, n=1..99: 0 violations
- PASS: generalized descent tau^B_n(C) <= tau^A_n(C)+2: 3484 exact checks over 28 (B,s) combinations: 0 violations; slack distribution [(0, 423), (1, 1023), (2, 1655), (3, 226), (4, 157)]
- PASS: scale-chain bound tau^{10^6}_n(C) <= 2i + tau^{A_i}_n(C): 612 exact checks (n=1..99, six levels): 0 violations; best chain bound - exact: [(0, 5), (1, 31), (2, 60), (3, 3)]
- PASS: prime family B=100: 405 primes, kappa = (p+1)^2 for 405 of them; exact tau at the forced ceiling mean 8.73 max 10; composite flip bound applicable 111 times, never below exact (0 violations), slack mean 1.95
- PASS: prime family B=1000: 262 primes, kappa = (p+1)^2 for 262 of them; exact tau at the forced ceiling mean 12.70 max 15; composite flip bound applicable 74 times, never below exact (0 violations), slack mean 2.23
- PASS: fresh C++ rebuild of lattice frontiers D=[1, 2, 4, 5, 10, 20, 25, 50, 100, 200, 1000, 10000] (n=1..99) reproduces the stored files
- PASS: fresh C++ rebuild of descent frontiers [(100, 2), (400, 4), (900, 6), (10000, 100), (10000, 5)] reproduces the stored files
- PASS: fresh C++ rebuild of 51 prime-family frontiers at B=100 (cap 10^7) reproduces FP_100.txt rows
- PASS: fresh C++ rebuild of chain frontier A=361 (B=10^6 headroom, n=1..99, Cmax=10^8) reproduces FC_361.txt
- PASS: fresh C++ rebuild of chain frontier A=4 (B=10^6 headroom, n=1..99, Cmax=10^8) reproduces FC_4.txt
- PASS: fresh C++ rebuild of 27 prime-family frontiers at B=1000 reproduces FP_1000.txt rows
- PASS: uniform first leg: 10^6 -> 160000 -> 7600 -> 361 -> 18 -> 4 -> 1 (6 edges, max vertex 10^6), hence p->... leg of the composite route has 6 steps for every prime p > 10^6
- PASS: composite prime-flip routes at B=10^6 recomputed for 362 primes (53 applicable, each explicit route edge-checked, max vertex exactly (p+1)^2 = forced ceiling)
- PASS: fresh C++ ladder re-run reproduces 18 stored exact prime-family distances at the forced ceiling (p+1)^2
- PASS: capped v012 pairs: intervals {'36652': (10, 11), '492388': (12, 13), '714750': (12, 14), '726925': (14, 14), '783594': (10, 14), '878636': (12, 13), '912390': (12, 13)} consistent; 4 explicit routes edge-checked (independent Python search) with max vertex <= B(n+1)
- PASS: fresh C++ ladder re-run reproduces the 7 best-scale distances behind the upper bounds of the capped pairs
- PASS: lower bound for the pair n=726925: exhaustive bidirectional search at scale 10^6 (cap 2.5M nodes) finds no route of length <= 13 inside [1, B(n+1)]; hence tau = 14 exactly
- PASS: baselines v001-v012 unchanged (read-only hashing)

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

ALL CHECKS PASS
time 557 s