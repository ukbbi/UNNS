# GIG-I v001 — Report
*Generative Information Geometry in the UNNS Substrate · UNNS Research Collective · 5 November 2026*

All numbers below are produced by `EXPERIMENTS/run_all.py` (`results.json`, ~75 s) and `run_all.py --extended` (`results_extended.json`, 16 min), and re-derived by 28 automated tests. Sources: frozen SELECT-II / GEO-HD-1D v003–v004 (read-only; not modified, not imported). Probability model: uniform on the fibre unless stated. Status tags as in `THEORY/THEOREMS.md`.

## 1. Headline
1. **Entropy is blind to the shape of ancestry — and so, provably, are accessibility statistics up to radius 2.** Six exact arithmetic pairs (GIG-T9) have identical `A`, class entropy and within-class entropy, identical swap-neighbourhood statistics up to radius 0, 1 or 2, and different homology. The sharpest two differ by **one hexagonal 2-cell** and share `(N, E, #squares)`.
2. **Mechanism (GIG-T8, proved):** `|B_2(v)| = 1 + d(v) + Σ_{x~v}(d(x)−1) − q(v)`. Two-swap accessibility sees degrees and squares; braid hexagons first enter at radius 3.
3. **Inherited objects re-seen as information.** The 2-void `{2,3,8,9,14}@1008` has *exactly the same one-swap neighbourhood statistics* (96 vertices, 180 edges, same degree multiset) as the contractible `{1,2,3,5,7}@105`; they separate only at radius 2.
4. **Topology lives inside genuine endpoint fibres.** The complete-history fibre of 1 382 400 has 15 842 histories (13.951467 bits) and contains a loop piece `{2,3,14,15}@210` (squarefree source). The inherited loop `{2,3,8,9}@72` is the same vertex set up to permutohedron symmetry.
5. **Finite-exact detection radius.** Over every realizable admissible set found (28 / 2 566 / 203 322 sets for k = 3 / 4 / 5, labels ≤ 40 / 70 / 26): the fine accessibility profile separates all Betti vectors at radius 1 (k=4) and radius 3 (k=5); radius 2 fails for k=5 (exactly 2 ambiguous groups, W5 and W6). → conjecture GIG-C1.

## 2. Ambiguity and its decomposition (GIG-T1…T6) 
* **E1, endpoint 72** (complete-history fibre, uniform): histories `(1;1,1,2)`, `(1;1,2,1)`, `(3;3,2)`, `(10;5)`; classes 2,1,1.
  `A = 2`, `H(M|T) = 1.5`, `H(Q|M,T) = 0`, `H(C|M,Q,T) = 0`, `H(W|C,T) = 0.5` ⇒ **2 = 1.5 + 0.5 bits**. Fixed-source fibres: 2, 1, 1 histories (sources 1, 3, 10).
* **E2, `72^r`** (complete-history fibres, exact DP, nothing materialised beyond r = 4): 
  | r | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
  |---|---|---|---|---|---|---|---|---|---|---|
  | `\|F\|` | 4 | 100 | 3 601 | 194 864 | 14 177 856 | 1 258 011 667 | 127 958 272 791 | 14 628 387 999 697 | 1 831 257 259 071 051 | 247 547 117 576 968 617 |
  | `A` (bits) | 2.00 | 6.64 | 11.81 | 17.57 | 23.76 | 30.23 | 36.90 | 43.73 | 50.70 | 57.78 |
  The reference sequence (r ≤ 6) is reproduced exactly; `A(72^r) ≥ log2 C(2r,r)` has a self-contained proof (an explicit family of `C(2r,r)` histories from source 1). The bound is far from tight (r = 10: 57.8 bits versus 17.5). Increments of `A` per unit `r`: 4.64, 5.17, 5.76, 6.19, 6.47, 6.67, 6.84, 6.97, 7.08 — rising with shrinking steps; no limit is claimed.
* **E3, source 4, endpoint 65536 = 4^8** (fixed-source fibre, uniform): 18 histories in **four** contents, not two — `1^7` (1 history), `{1,3,4,5,15}` (10), `{2,2,3,3,3,3}` (3), `{2,3,6,7,7}` (4). The multiplier identity `R(1)^7 = R(2)²R(3)⁴` holds, and `{2²3⁴}` is admissible from 4 (3 orderings) but from 1 not at all. Chain: `A = 4.169925` = content `1.615805` + class-given-content `0` + ordering `2.554120` bits; each content is a single swap class.

## 3. The recombination information profile (GIG-T7)
`I_r = log2(P_r)/N` with the integer `P_r = ∏|B_r(w)|` (so equality of profiles is an exact integer test); strictly increasing until the largest component diameter `ρ`, then equal to `H(W|C,T)`; additive over (source, content) pieces. First-step law: `I_1 ≤ log2(3 + 2(β1(G) − β0)/N)`, hence `I_1 ≥ log2 3 ⇒` the swap graph has a cycle. Verified on every census set and on 5 real fibres.

## 4. Information versus topology (GIG-T8–T10)
| pair | A | B | N | agree up to radius | differ at | what differs |
|---|---|---|---|---|---|---|
| W1 | {2,3,14,15}@210 β=(1,1,0,0) | {1,2,3,4}@6 β=(1,0,0,0) | 16 | 0 | 1 | E = 20 vs 21 |
| W2 | {2,3,8,9}@72 β=(1,1,0,0) | {2,3,5,6}@30 β=(1,0,0,0) | 16 | 0 | 1 | E = 20 vs 21 |
| W3 | {2,3,8,9,14}@1008 β=(1,0,1,0,0) | {1,2,3,5,7}@105 β=(1,0,0,0,0) | 96 | 1 | 2 | same E = 180; squares 66/60, hexagons 32/40 |
| W4 | {2,3,8,9,10}@72 β=(1,1,0,0,0) | {1,2,3,5,9}@18 β=(1,0,0,0,0) | 40 | 1 | 2 | same E = 64; squares 21/19 |
| W5 | {2,3,9,15,21}@189 β=(1,1,0,0,0) | {1,2,12,13,26}@52 β=(1,0,0,0,0) | 24 | 2 | 3 | same E = 32, squares 7; **hexagons 1/2** |
| W6 | {2,3,8,21,26}@273 β=(2,1,0,0,0) | {6,8,9,14,15}@168 β=(2,0,0,0,0) | 18 (6+12) | 2 | 3 | same E = 17, no squares; **hexagons 0/1** |

Every pair has `χ = N − E + Q − H + … = Σ(−1)^i β_i` on both sides; W1, W6 (A side) and the complete-history loop live at squarefree sources. In W5 and W6 the permutohedral Betti numbers differ while the *cubical* Betti vectors of W5 and W6 coincide ((1,2,0,0,0) and (2,1,0,0,0) on both sides) — the hexagon fill is exactly what the radius-2 data cannot see.

## 5. Census (finite-exact; labels ≤ L, all lcm-closure sources)
| k | L | realizable sets | ambiguous groups at fine radius 0 / 1 / 2 / 3 | loops (β1>0) | 2-voids | squarefree-realizable loops |
|---|---|---|---|---|---|---|
| 3 | 40 | 28 | 0 / 0 / 0 / 0 | 0 | 0 | 0 |
| 4 | 70 | 2 566 | 2 / 0 / 0 / 0 | 7 sets (2 orbits) | 0 | 3 sets |
| 5 | 26 | 203 322 | 59 / 156 / **2** / 0 | 3 469 sets | 15 sets | 176 sets |
"Ambiguous group" = ≥ 2 sets with equal fine signature up to that radius and different Betti vectors. `I_r` (scalar) gives identical verdicts. Observed separating radius: k=4 → 1, k=5 → 3. No squarefree-realizable 2-void occurs in the range.

## 6. What this does and does not establish
* Proved: T1–T8 (elementary but exact, and new in this form). T9/T10 are exact existence statements by explicit integer computation, cross-validated against an independent frozen engine (2 499 histories lists, 2 129 + 300 Betti computations, 288 thresholds — `crosscheck_frozen.json`).
* **Not** claimed: that the detection radius is 3 for every k, or that radius 3 suffices beyond the census (GIG-C1, C2 are conjectures); anything about contents with repeated labels beyond graph-level information; any link to the earlier Chronotopos entropy functionals (defined on a different model; not imported).
* Limits of the census: label bounds are finite and counts of realizable sets still grew between L = 45 and 70 for k = 4, so frequency figures are bounds-dependent; the *qualitative* separating-radius statement is what is recorded.
* Candour on novelty: counting, the chain rule, and Jensen are textbook; the content is in the arithmetic inputs (swaps preserve source/content, reverse-edge lemma, complete-history fibres), the exact decomposition for 72 and `72^r`, the radius-2 formula in the permutohedral setting, and the explicit arithmetic witnesses.

## 7. Next questions that follow from the data (not scheduled)
GIG-C1 at k = 6 (the first level with 3-cubes and Petrie hexagons — a *graph-isomorphic* information-equivalent pair would be the strongest possible form of T9); whether the separating radius grows with `k`; a complete-history 2-void; the limit of `A(72^r)/r`.
