# GIG-I v001 — Theorem register

IDs `GIG-T*`, `GIG-Q*`, `GIG-C*` belong exclusively to this programme and do not replace or renumber any inherited result.
Tags: [EST] established · [INH] inherited · [ELEM] new elementary deduction (proved in PROOFS.md) · [FINITE-EXACT] exact computation on stated finite data · [CAND] candidate/conjecture · [OPEN].
Probability model is stated in each item; "uniform" = uniform on the finite fibre.

| ID | Statement (short) | Status | Proof / evidence |
|---|---|---|---|
| GIG-T1 | Reverse edges, finiteness, nonemptiness | [ELEM] (builds on [INH] predecessor rule) | PROOFS §1; tests `T1_ReverseEdges` |
| GIG-T2 | Information projection hierarchy and conditional-entropy decomposition | [EST] chain rule + [ELEM] nesting | PROOFS §2; `T3_Information` |
| GIG-T3 | `0 ≤ H(W\|T=t) ≤ A(t)`; equality iff uniform; every value in `[0,A(t)]` attained | [EST] + [ELEM] | PROOFS §3 |
| GIG-T4 | Exact decomposition for the four complete histories of 72 | [FINITE-EXACT] (proved by enumeration) | PROOFS §4; E1 |
| GIG-T5 | `A(72^r) ≥ log2 C(2r,r)` (self-contained proof) and exact counts r=1..10 | [ELEM] / [FINITE-EXACT] ([INH] in GEO-HD-1) | PROOFS §5; E2 |
| GIG-T6 | `H(C\|T=t) ≤ log2 β0(G_t)`, equality iff equal class sizes | [EST] + [ELEM] | PROOFS §6 |
| GIG-T7 | Recombination information profile: `I_r = log2 P_r / N`, monotone, strict until ρ, `I_r = H(W\|C,T)` iff `r ≥ ρ`; additivity over pieces; `I_1` Jensen bound and cycle law | [ELEM] | PROOFS §7; `T4_Profile` |
| GIG-T8 | Radius-2 formula: `\|B_2(v)\| = 1+d(v)+Σ_{x~v}(d(x)−1)−q(v)`; fine radius-≤2 data determine `(N,E,#squares)` and nothing about hexagonal cells | [ELEM] | PROOFS §8; tests; census check |
| GIG-T9 | Information-equivalent, topologically inequivalent arithmetic pieces exist at every level `r ≤ 2` (certificates W1–W6) | [FINITE-EXACT], computer-assisted existence | PROOFS §9; E4 §C; `test_certificates` |
| GIG-T10 | Complete-history fibres can carry nontrivial homology (`β1=1` at squarefree source 210) | [FINITE-EXACT] | E4 §B; `test_complete_history_loop` |
| GIG-Q1 | Do refined information profiles detect nontrivial history homology? | **Partially answered** — NO through radius 2 (T9); finite census says YES at radius 3 (k ≤ 5) → GIG-C1 | RESULTS/report.md |
| GIG-Q2 | Information-equivalent but topologically inequivalent structures? | **Answered YES** (T9) with an exact mechanism (T8: one hexagonal cell); restrictions recorded in the census | RESULTS/report.md |
| GIG-C1 | In the arithmetic census (distinct-label pieces, k ≤ 5), the fine radius-3 profile determines the permutohedral Betti vector | [CAND] [FINITE-EXACT support] | RESULTS/results_extended.json |
| GIG-C2 | The minimal separating radius is unbounded as k grows | [CAND] | OPEN_PROBLEMS |

---

## GIG-T1 — Reverse edges and finiteness  [ELEM]
For every integer `t ≥ 2`:
1. **(Reverse-edge characterisation)** There is a SELECT-II edge `m —N→ t` iff `(N+1)^2 | t`; the predecessor is `m = N t / (N+1)^2`.
2. **(Strict decrease)** `t/m = N + 2 + 1/N ≥ 4`, with equality iff `N = 1`.
3. **(Edge count)** The number of reverse edges is `τ(s(t)) − 1`, where `s(t) = ∏ p^{⌊v_p(t)/2⌋}` and `τ` counts divisors.
4. **(Finiteness)** Every history from `m0` to `t` has length `ℓ ≤ ⌊log_4(t/m0)⌋`; hence `F_t(m0)` and `F_t` are finite.
5. **(Nonemptiness)** A source is squarefree iff it has no reverse edge; every `t ≥ 1` has at least one complete history. Hence `A(t)` is defined for all `t ≥ 1` in the complete-history convention, and `A(t) = 0` iff `|F_t| = 1`.

## GIG-T2 — Information projection and decomposition  [EST + ELEM]
Fix a fibre `F` (complete-history or fixed-source) with any probability distribution on `W`. A legal swap preserves source, content and endpoint, so
`σ(T) ⊆ σ(M,Q) ⊆ σ(C) ⊆ σ(W)`, i.e. each level of the hierarchy determines the previous one. Consequently, exactly,
`H(W|T) = H(M|T) + H(Q|M,T) + H(C|M,Q,T) + H(W|C,T)`, with `H(W|M,Q,C,T) = H(W|C,T)`, and `H(C|T) = H(M,Q|T) + H(C|M,Q,T)`.

## GIG-T3 — Ambiguity bounds  [EST + ELEM]
For a nonempty finite fibre of size `N`: `0 ≤ H(W|T=t) ≤ A(t) = log2 N`; equality at the top iff the distribution is uniform, at the bottom iff it is a point mass; and for every `h ∈ [0, A(t)]` some distribution attains `H = h`. For `|F_t| ≥ 2` conditional entropy can be arbitrarily small although `A(t)` is fixed.

## GIG-T4 — The four histories of 72  [FINITE-EXACT]
`F_72 = {(1;1,1,2), (1;1,2,1), (3;3,2), (10;5)}`. Swap classes have sizes `2,1,1`; the first two histories are one class (swap of the last two labels at state 4), the others are singletons from distinct sources. Uniform model, bits:
`A(72) = H(W|T) = 2`; `H(M|T) = 1.5`; `H(Q|M,T) = 0`; `H(C|M,Q,T) = 0`; `H(W|C,T) = 0.5`; `H(C|T) = 1.5`; **`2 = 1.5 + 0.5`**.
Fixed-source fibres: `|F_72(1)| = 2` (1 bit), `|F_72(3)| = |F_72(10)| = 1`. A nonuniform example with `p = (1/2,1/4,1/8,1/8)` has `H = 1.75 < 2`.

## GIG-T5 — Growth family 72^r  [ELEM / FINITE-EXACT]
(a) For all `r ≥ 1`, `|F_{72^r}| ≥ C(2r,r)`, hence `A(72^r) ≥ log2 C(2r,r)`; an explicit family of `C(2r,r)` complete histories from source 1 is given in the proof.
(b) Exact counts `|F_{72^r}|`, r = 1..10: 4, 100, 3601, 194864, 14177856, 1258011667, 127958272791, 14628387999697, 1831257259071051, 247547117576968617 (r ≤ 7 in `results.json`, r ≤ 10 in `e2_long_table.json`).
(c) Observation [FINITE-EXACT]: `A(72^r)` increments `A(72^{r+1}) − A(72^r)` (bits): 4.644, 5.170, 5.758, 6.185, 6.471, 6.668, 6.837, 6.968, 7.079 — increasing but with shrinking steps; no limit is claimed (OPEN).

## GIG-T6 — Class entropy vs. component count  [EST + ELEM]
Uniform model, `k = β0(G_t)` components of sizes `n_1..n_k`: `H(C|T=t) = −Σ (n_i/N) log2(n_i/N) ≤ log2 k`, equality iff all `n_i` are equal. Also `H(W|C,T=t) = Σ (n_i/N) log2 n_i ≤ log2 n_max` and `A(t) = H(C|T=t) + H(W|C,T=t) ≤ log2 β0 + log2 n_max`.

## GIG-T7 — Recombination information profile  [ELEM]
Uniform model, graph `G_t` on `N` vertices, `ρ` = largest component diameter.
(a) `I_r = (1/N) log2 P_r` with the integer `P_r = ∏_w |B_r(w)|`; hence equal `I_r` (same `N`) ⇔ equal `P_r`.
(b) `I_0 = 0`; `I_r ≤ I_{r+1}`.
(c) `I_r < I_{r+1}` for every `r < ρ`, and `I_r = I_ρ` for all `r ≥ ρ`.
(d) `I_r = H(W|C,T=t)` **iff** `r ≥ ρ`; always `I_r ≤ H(W|C,T=t)`.
(e) **Additivity.** If the fibre is a disjoint union of pieces `p` of sizes `n_p`, then `I_r(fibre) = Σ_p (n_p/N) I_r(p)`, and Betti numbers of the disjoint union add.
(f) **First-step law.** `|B_1(w)| = 1 + deg(w)`, so `I_1 ≤ log2(1 + 2E/N) = log2(3 + 2(β1(G) − β0)/N)`, with equality iff `G` is regular. Consequently `I_1 ≥ log2 3 ⇒ β1(G) ≥ 1` (a forest has `I_1 < log2 3`), and quantitatively `β1(G) ≥ β0 + N(2^{I_1} − 3)/2`.
(g) What (f) does **not** give: `β1(G)` is the graph cycle rank; the homology of the history complex is `β1(K_A) ≤ β1(G)`.

## GIG-T8 — The radius-2 formula  [ELEM]
Let `A` be a set of arrangements, `G` the induced subgraph of the permutohedron graph `P_k`, `d(v)` degrees, `q(v)` the number of square faces of `K_A` through `v`. Then for every vertex
`|B_2(v)| = 1 + d(v) + Σ_{x~v}(d(x) − 1) − q(v)`,
two vertices at distance 2 have 1 or 2 common neighbours, and 2 exactly when they are opposite corners of a square face. Therefore the **fine** radius-≤2 data determine `N`, `E` and the number of square faces `Q = (N + 2E + Σ_v d(v)(d(v)−1) − Σ_v |B_2(v)|)/4`, and they contain no direct information on hexagonal (braid) 2-cells, whose boundary 6-cycles first affect balls at radius 3.

## GIG-T9 — Information-equivalent, topologically inequivalent pieces  [FINITE-EXACT, computer-assisted existence]
Each row is an ordered pair of arithmetic pieces (content, source). Both pieces in a row have the same `N`, the same class sizes, hence the same `A`, `H(C|T)`, `H(W|C,T)`; they agree on the fine accessibility signature for all radii `< s` and differ at radius `s` ("separating radius"). Betti numbers are permutohedral over GF(2).

| ID | Piece A (content @ source) | β(A) | Piece B | β(B) | N | agree through r | separating radius s | what differs |
|---|---|---|---|---|---|---|---|---|
| W1 | {2,3,14,15} @ 210 *(squarefree)* | (1,1,0,0) | {1,2,3,4} @ 6 *(squarefree)* | (1,0,0,0) | 16 | 0 | 1 | E = 20 vs 21 |
| W2 | {2,3,8,9} @ 72 *(inherited loop)* | (1,1,0,0) | {2,3,5,6} @ 30 | (1,0,0,0) | 16 | 0 | 1 | E = 20 vs 21 |
| W3 | {2,3,8,9,14} @ 1008 *(inherited 2-void)* | (1,0,1,0,0) | {1,2,3,5,7} @ 105 | (1,0,0,0,0) | 96 | 1 | 2 | same E = 180 and degree multiset; squares 66 vs 60, hexagons 32 vs 40 |
| W4 | {2,3,8,9,10} @ 72 | (1,1,0,0,0) | {1,2,3,5,9} @ 18 | (1,0,0,0,0) | 40 | 1 | 2 | same E = 64; squares 21 vs 19 |
| W5 | {2,3,9,15,21} @ 189 | (1,1,0,0,0) | {1,2,12,13,26} @ 52 | (1,0,0,0,0) | 24 | 2 | 3 | same N, E = 32 and square count 7; **one hexagonal 2-cell** (1 vs 2) |
| W6 | {2,3,8,21,26} @ 273 *(squarefree)* | (2,1,0,0,0) | {6,8,9,14,15} @ 168 | (2,0,0,0,0) | 18 (classes 6+12) | 2 | 3 | same N, E = 17, no squares; hexagons 0 vs 1 |

Euler characteristics agree with alternating Betti numbers in every row (`χ = N − E + Q − H + …`). In W5 and W6 the topology differs by exactly one hexagonal 2-cell, invisible to every accessibility statistic of radius ≤ 2.

## GIG-T10 — Topology in complete-history fibres  [FINITE-EXACT]
`F_{1 382 400}` (complete histories) has 15 842 histories (`A = 13.951466861933` bits), 292 pieces (112 with distinct labels), 309 swap classes, largest piece 1 075 histories. Exactly one distinct-label piece has nontrivial higher homology: content `{2,3,14,15}` at the squarefree source 210, `β = (1,1,0,0)`. Uniform-model chain: `H(M,Q|T) = 6.404265`, `H(C|M,Q,T) = 0.010778`, `H(W|C,T) = 7.536423` bits (sum `13.951467`). The inherited loop `{2,3,8,9}@72` is the same vertex set up to the symmetries of the permutohedron.
Census [FINITE-EXACT]: squarefree-realizable loops occur for k = 4 and k = 5; no squarefree-realizable 2-void was found for k = 5, labels ≤ 26 (see `OPEN_PROBLEMS.md`).

## GIG-Q1 / GIG-Q2 dispositions
* **Q2 (answered, affirmative):** T9 gives six exact witnesses; T8 explains the sharpest ones: radius-≤2 accessibility cannot see hexagonal braid cells.
* **Q1 (partial):** entropy-level (`r=0`), one-swap (`r≤1`) and two-swap (`r≤2`) accessibility do **not** detect homology (T9). Within the finite arithmetic census a radius-3 profile does (GIG-C1) — a conjecture, not a theorem; its extent is recorded in `RESULTS/results_extended.json`.
