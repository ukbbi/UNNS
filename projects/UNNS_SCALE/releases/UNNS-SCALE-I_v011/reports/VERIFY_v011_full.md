# UNNS-SCALE-I v011 verification report

mode: full

- PASS: barrier theorem, brute force over all 192684 edges of G_300000: exact conservation of v_p for p>sqrt(C); parity of v_p changes only across p | N, whose larger endpoint is >= (p+1)^2: violations 0
- PASS: exhaustive finite graphs G_C (C=10^4,10^6,3e7): every component has constant v_p for p>sqrt(C) and constant parity for (p+1)^2>C; output equals stored
- PASS: independent scipy connected_components on G_10^7 agrees with the C++ union-find (components 5537802)
- PASS: parity lower bound kappa >= (q(n)+1)^2 holds for every answered pair of the exact Kruskal runs (B:answered = 100:44848, 1000:124396, 10000:84272, 999:473121)
- PASS: exact law kappa_B(n) = max(B(n+1), (q(n)+1)^2) on 216683 answered pairs (B=100 for n<B^2, B=1000, B=10^4): exceptions none
- PASS: Theorem E (primes p>B): every route of any length contains a vertex >= (p+1)^2 and the exact ceiling equals (p+1)^2 on 4088 primes (B=100,1000,10^4)
- PASS: fresh Kruskal re-run B=100 reproduces stored connection ceilings (99999 pairs)
- PASS: fresh Kruskal re-run B=1000 reproduces stored connection ceilings (199999 pairs)
- PASS: pair ceilings recomputed from the link certificates: classes {'direct': 692823, 'flip': 257432, 'bfs': 49487, 'prime': 258}; exact connection ceiling = B(n+1) proved for 999999 of 999,999 pairs; max ceiling 1000000000000
- PASS: explicit in-domain routes (12 pairs, lengths [25, 26, 29, 30, 30, 30, 32, 34, 35, 39, 39, 40]): edge-checked, maximum vertex exactly B(n+1)
- PASS: fresh Python bidirectional search re-derives explicit hub routes for 5 stored pairs
- PASS: flip-gadget routes B m -> 999 m'p ~> s p -> s(p+1)^2 -> s d (p+1-d) explicit and edge-checked for 60 sampled vertices (all <= 10^12, end vertex <= 10^9)
- PASS: bounded-search links (radius 2-4) to the hub: 658 stored paths edge-checked, all vertices <= B m, end vertex <= 10^9
- PASS: every stored minimal-height value (v009: n<=279 all routes <=4; v010: 458 finite H4 values) is >= (q(n)+1)^2
- PASS: fresh rebuild of conn.cpp (exact union-find to 10^9, kappa matrices, flip search) reproduces CN1_vertex_links.txt byte for byte
- PASS: fresh rebuild of conn2.cpp re-links all 49487 remaining vertices to the hub at the stored radius
- PASS: baselines v001-v010 unchanged (read-only hashing)

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

ALL CHECKS PASS
time 402 s