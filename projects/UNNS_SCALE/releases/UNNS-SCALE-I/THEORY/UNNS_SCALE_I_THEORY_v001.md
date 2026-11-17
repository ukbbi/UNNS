# UNNS-SCALE-I — Theory v001
Nested scale projection of the SELECT-II arithmetic graph

Status vocabulary: **PROVED** (proof below, plus computational cross-check where stated) · **CERTIFIED** (finite exact certificate) · **EXPERIMENTAL** (computed, no proof) · **OPEN**.

## 0. Setting (definitions only; nothing frozen is altered)

SELECT-II transition: `T_N(x) = x (N+1)^2 / N`, defined when `N | x`.
The undirected arithmetic graph `G` has vertex set `ℕ>0` and edge set
`E = { {kN, k(N+1)^2} : k, N ≥ 1 }`.
A *forward move* `+N` from `u` needs `N | u` and gives `u(N+1)^2/N`; a *backward move* `−N` needs `(N+1)^2 | u` and gives `uN/(N+1)^2`.
Notation: `τ(u)` number of divisors; `s(u) = #{ q ≥ 2 : q² | u }`; `G[S]` induced subgraph; `S_B : x ↦ Bx`.

**Lemma 0 (labelled edges, degree).**
(a) Every edge has a unique representation `(k, N)` with smaller endpoint `u = kN` and larger endpoint `v = k(N+1)^2`.
(b) `deg_G(u) = τ(u) + s(u)`.

*Proof.* (a) `gcd(N, (N+1)^2) = 1`, so `v/u = (N+1)^2/N` is a reduced fraction; it determines `N`, and then `k = u/N`. (b) Forward moves from `u` are indexed by divisors `N | u` (τ(u) of them, neighbours `> u`); backward moves by `q = N+1 ≥ 2` with `q² | u` (s(u) of them, neighbours `< u`). By (a) distinct moves give distinct neighbours, and no move is a loop. ∎
*Cross-check:* G2e (degree formula = adjacency length in the built graph, u = 1..546, no mismatch).

## 1. Exact two-level representation

**Theorem 1 (nested coordinates) — PROVED.** For `B ≥ 1` the map `n ↦ (⌊n/B⌋, n mod B)` is a bijection `ℤ≥0 → ℤ≥0 × {0,…,B−1}`, with inverse `(q, r) ↦ Bq + r`. It restricts to a bijection `[0, BM) → [0, M) × [0, B)`. For radices `B₁,…,B_d` the mixed-radix digit map is a bijection `[0, ∏B_i·M) → [0,M) × ∏[0,B_i)`.

*Proof.* Division with remainder is unique. ∎
*Checks (Gate 1):* exhaustive for `B ∈ {10, 100, 1000}`; 200,009 points including all boundaries for `B = 10⁶` on `[0, 10¹²]`; mixed radices `10⁴×10⁴×10⁴`, `10⁶×10⁶`, `10²×…`, `10×…`.

*Range remark (recorded off-by-one).* `[0, 10¹²)` is exactly `10⁶` blocks of `10⁶`. The positive range `1..10¹²` additionally needs `q = 10⁶` for the single point `n = 10¹²` (`r = 0`).
*Information remark.* `(q, r)` carries exactly `log₂ 10¹² ≈ 39.86` bits; the representation changes geometry, not information.

## 2. The exact scale copy

**Theorem 2 (scale-copy isomorphism) — PROVED.** For every `B ≥ 1` and `u, v ∈ ℕ>0`:
`{Bu, Bv} ∈ E  ⇔  {u, v} ∈ E`,
with the same label `N` and direction. Hence `S_B` is a label-preserving isomorphism `G → G[Bℕ>0]`.

*Proof.* (⇐) the Scaling Lemma of the frozen U2-SQ release (multiply the cofactor `k` by `B`). (⇒) Let `Bu = kN`, `Bv = k(N+1)^2`. Then `B | gcd(kN, k(N+1)^2) = k·gcd(N,(N+1)^2) = k`. Write `k = Bk'`; then `u = k'N`, `v = k'(N+1)^2`. ∎

**Corollary 2.1 (window form).** The edges of `G` with both endpoints in `{B, 2B, …, BM}` are exactly the `B`-multiples of the edges of `G[1..M]`. For `B = 10⁶`, `M = 10⁶`: the multiples of `10⁶` in `[1, 10¹²]` span an induced subgraph isomorphic to `G[1..10⁶]`.

**Corollary 2.2 (non-expansion) — PROVED.** `d_G(Bu, Bv) ≤ d_G(u, v)`.
(The same inequality is the frozen Scaling Lemma; Theorem 2 additionally identifies the induced subgraph.)

*Checks (Gate 2, G2a/G2b):* the induced subgraph on multiples of `B` inside `G[1..300000]` equals the `B`-fold image of `G[1..⌊300000/B⌋]` for `B ∈ {2,3,4,6,10,12,30,100}`, edge for edge; local law below for `B` up to `10⁶`.

## 3. Cross-scale dynamics: the boundary law

**Theorem 3 (boundary-crossing law) — PROVED.** Let `u = Bx`.
(i) A forward move `+N` (`N | Bx`) lands in `Bℕ` ⇔ `N | x`.
(ii) A backward move `−N` (`(N+1)^2 | Bx`) lands in `Bℕ` ⇔ `(N+1)^2 | x`.
(iii) The in-lattice moves at `Bx` are exactly the images of the moves at `x`, hence
`deg_G(Bx) = deg_G(x) + ε_B(x)`, with exit count
`ε_B(x) = [τ(Bx) − τ(x)] + [s(Bx) − s(x)]`.

*Proof.* By Theorem 2's argument, an edge with both endpoints in `Bℕ` has `B | k`. (i) Forward: `Bx = kN`; if the neighbour is in `Bℕ` then `k = Bk'` and `x = k'N`, so `N | x`; conversely `x = jN` gives `k = Bj` and neighbour `Bj(N+1)^2 ∈ Bℕ`. (ii) Backward: `Bx = k(N+1)^2`, neighbour `kN`; identical argument. (iii) Count via Lemma 0(b). ∎

*Worked example.* `B = 10⁶`, `x = 1`: `τ(10⁶) = 49`, `s(10⁶) = 15`, `deg = 64`, `deg(1) = 1`, so the vertex `10⁶` keeps 1 in-lattice edge (`10⁶ → 4·10⁶`, label 1) and has `ε = 63` exits, among them `10⁶ → 4.5·10⁶` (label 2), i.e. `(q,r): (1,0) → (4, 500000)`.
*Checks (G2b):* 4,500 lattice vertices for each `B ∈ {10, 10², 10³, 10⁶}` (`x = 1..3000` plus 1,500 random `x < 10⁶`, so `u` up to `10¹²`): zero mismatches in stay/leave prediction, in-lattice neighbourhood equality, and degree identity. Mean exits: 18.9, 49.7, 87.3, 260.2 for the four `B`.

**Reading.** Scale-preserving dynamics = moves with labels dividing `x` (copy of `G`); cross-scale dynamics = labels that divide `Bx` but not `x` (the exits). The scale copy is a thin skeleton: the window `[1,10¹²]` has `e(10¹²) = 644,932,606,630` edges, of which only `e(10⁶) = 643,494` (fraction ≈ 9.98·10⁻⁷) lie inside the `10⁶`-lattice (Gate 2, G2f; `e(L) = Σ_{m=2}^{⌊√L⌋} ⌊L/m²⌋`, verified against enumeration for five values of `L`).

## 4. Obstruction: no exact outer-coordinate quotient

**Theorem 4 — PROVED.** For every `B ≥ 2` there is no map `F_B` on outer coordinates with `π(T_N(x)) = F_B(π(x))` for all `x`, where `π(n) = ⌊n/B⌋` and `T_N`, `N = 1`, is the move `n ↦ 4n` (defined for all `n`).

*Proof.* `x = Bq` and `y = Bq + B − 1` have `π(x) = π(y) = q`, but `π(4x) = 4q` and `π(4y) = 4q + ⌊4 − 4/B⌋ ≥ 4q + 2`. ∎
*Check (G2d):* `B ∈ {2,3,4,5,10,100,10³,10⁶}`.

**Consequence.** The hypothesised coarse-grained intertwining `π∘F = F_B∘π` fails for the floor projection. A coarse-grained dynamics must keep (part of) the inner coordinate, or restrict to the scale-preserving moves of Theorem 3. This is the precise sense in which the million-block outer level does *not* by itself carry the dynamics.

## 5. Distances across scales

**Corollary 5.1 — PROVED** (from Cor. 2.2): `d_G(Bu,Bv) ≤ d_G(u,v)`.

**Certified strictness — CERTIFIED (exact, untruncated).** Strict inequality occurs:
- `B = 2`: `d(1,2) = 5` but `d(2,4) ≤ 4`, via `2 →(+1) 8 →(+8) 81 →(−2) 18 →(−2) 4`.
- `B = 10`: `d(7,8) = 4` but `d(70,80) ≤ 3`, via `70 →(+35) 2592 →(−2) 576 →(−5) 80`.
Lower bounds `d(1,2) > 4` and `d(7,8) > 3` come from disjoint exact balls (`B₂(1) ∩ B₂(2) = ∅`, `B₂(7) ∩ B₁(8) = ∅`), computed without truncation; upper bounds are explicit legal paths (verified step by step).
Both witness paths leave the lattice (81 is odd; 2592 and 576 are not multiples of 10): the shortcuts are cross-scale.

**Observed frequency — EXPERIMENTAL (Gate 3).** Over successor and doubling pairs: stable-distance pairs where the scaled pair is strictly closer: `B=2`: 155/394; `B=3`: 120/394; `B=6`: 159/297; `B=10`: 128/295; `B=100`: 83/151. Observed gaps `d_base − d_scaled ∈ {0,1,2}`. No violation of Cor. 5.1 in any run. Base distances are truncation-stable (`L→4L`; the first 8 strict examples for `B = 2` and `B = 10` also re-evaluated at `L = 1.2·10⁷`, unchanged) but not certified in general.

## 6. Open questions (queued, not claims)

1. Exact law for `sup_n d(Bn, B(n+1))` as a function of `B` (compare `sup d(n,n+1) = 6` of frozen U1-BND).
2. Distribution of exits `ε_B(x)`: closed form in terms of prime factorisation of `B` and `x`; asymptotic mean as `B → ∞`.
3. Hierarchical nesting `10¹² = 10⁴·10⁴·10⁴`: do exit structures at consecutive levels compose (multiplicativity of the boundary law)?
4. Which UNNS operators other than SELECT-II commute with `S_B`? Scale compatibility must be settled grammar by grammar (an earlier note states `C(4)=8, C(8)=12` for the FIELD-I collective map, hence `C(2·4) ≠ 2·C(4)`; **not re-verified here**).
5. Complexity gate (Gate 4): whether scale structure lowers actual computational cost; not started, requires SCR-style baselines and nulls.
