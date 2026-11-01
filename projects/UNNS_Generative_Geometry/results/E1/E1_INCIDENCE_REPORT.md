# E1 incidence report (generated from the verified atlas)

Atlas: `E1_ATLAS.json`, sha256 `029334533ff7da5a8506c2dc824eb0db87cb5a6d183f67a0719e7e0b572a2e5a`

Verifier: `verify_atlas.py` — 36/36 checks passed.

## Benchmark incidence

| value | R | occurrences (N,M) | out-edges (N -> target) | complete histories |
|---|---|---|---|---|
| 6 | 0 | none (source) | 1→24, 2→27, 3→32, 6→49 | 1: 6 |
| 72 | 3 | (1,18), (2,16), (5,10) | 1→288, 2→324, 3→384, 4→450, 6→588, 8→729, 9→800, 12→1014, 18→1444, 24→1875, 36→2738, 72→5329 | 4: 1-4-16-72; 1-4-18-72; 3-16-72; 10-72 |
| 784 | 5 | (1,196), (3,147), (6,96), (13,52), (27,27) | — | 8: 1-4-18-96-784; 1-4-18-147-784; 6-24-96-784; 6-24-196-784; 6-27-784; 6-49-196-784; 13-52-784; 13-196-784 |

## Checks

- PASS V1 state records (index set, R, source flag, out-degree, valuation) — 28 states
- PASS V2 occurrences = brute-force solutions of M(N+1)^2 = tN; N+1 <-> index set bijection — 62 occurrences
- PASS V3 occurrence <-> incoming edge identification is injective and consistent (S2.5)
- PASS V4 every edge: m divisible by N, T_N(m), N = m/gcd(m,t), v-displacement = 2v(N+1) - v(N) — 62 edges
- PASS V5 completeness: every SELECT-II edge between two recorded states is recorded
- PASS V6 complete histories = forward enumeration from all squarefree sources — H(6)=1, H(16)=2, H(72)=4, H(784)=8
- PASS V7 H(t) recorded for every state = forward path count
- PASS V8 every history: source squarefree, labelled edges valid, last-edge occurrence exists
- PASS V9 fibre geometry: vertices <-> index set, cell counts by inclusion-exclusion, chi = 1 — 24 nonempty fibres
- PASS V10 FR-1 Vol. I Def. 5.1 / S2.1: out-neighbours of 6
- PASS V10 FR-2 Vol. I Thm 1.2 / S2.2 / CTX 3.1: occurrences of 72 (N,M)
- PASS V10 FR-3 SELECT-II v002b B2 (S2.12): complete histories of 72
- PASS V10 FR-4 SELECT-II v002b B5: complete histories of 16 (different lengths)
- PASS V10 FR-5 SELECT-II v002b C4: route (k,d)=(8,3) of 72 comes from predecessor 16, which has
- PASS V10 FR-6 SELECT-II v002b C7: minimal merges <= 784 of preds (96, 27) of routes (16,7),(1,
- PASS V10 FR-7 SELECT-II v002b C6 (S2.15): 72 is a minimal common successor of each pair of predecessor
- PASS V10 FR-8 SELECT-II v002b B4: smallest non-source t with H(t)>R(t) (t<200)
- PASS V10 FR-10 Vol. I Thm 5.5 / S2.3: N = m/gcd(m,t) on every recorded edge
- PASS V10 FR-11 v001 Thm 2.1 (displacement): v(T_N(m)) - v(m) = 2v(N+1) - v(N) on every recorded edge
- PASS V10 FR-9 GEO-I v002 table (R, d_amb, d_aff, d_cell) for 72,144,3600,44100
- PASS V10 GEO-I v002 cell counts 3600 -> 11/17/8/1 and 44100 -> 15/28/18/4
- PASS V11 SEL_6: P(2,3,7) images 6->(1,1,0), 24->(3,1,0), 27->(0,3,0), 32->(5,0,0), 49->(0,0,2)
- PASS V12 SEL_6: 6 is a source (squarefree), has exactly one history H(6), four out-edges with labels 1,2,3,6
- PASS V13 SEL_72: 3 occurrences = 3 incoming edges (labels 1,2,5) and 4 complete histories
- PASS V14 SEL_72 fibre coordinates over primes (2,3): N=1->(1,0), N=2->(0,1), N=5->(1,1)
- PASS V15 histories of 72: endpoint projection collapses all 4; (endpoint,length) and (source,endpoint,length) leave H(1-4-16-72), H(1-4-18-72) identified; last-edge occurrence identifies H(1-4-16-72), H(3-16-72)
- PASS V16 NI-4 label sequence (1,) arises from several distinct sources and histories
- PASS V17 NI-5 equal index sets, different values and occurrence sets: D(72) = D(108) = {2,3,6}
- PASS V18 FIELD-I step C(72) = 72 + L^2/G = 108 (L=6, G=1) is not a SELECT-II out-neighbour of 72
- PASS V19 NI-7 projection onto primes (2,3,5) identifies 1 and 49
- PASS V20 confluence at 784: routes (16,7),(1,28) have predecessors 96 and 27; minimal merges <= 784 are {432,784}; bounded search to 5000 additionally gives 3750
- PASS V21 typed maps declared with domain/codomain/kind
- PASS V22 last-edge map onto O_72 is surjective
- PASS V22 last-edge map onto O_784 is surjective
- PASS V22 last-edge map onto O_16 is surjective
- PASS V23 last-edge map into O_72 is not injective (4 histories, 3 occurrences)
