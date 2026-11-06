# GIG-I v001 — Proofs

All statements are about the frozen SELECT-II operator `T_N(m) = m(N+1)²/N`, `N | m`. "Edge" means a single step.

## §1 GIG-T1 (reverse edges, finiteness, nonemptiness)
**(1)** Suppose `m —N→ t`. Then `N | m`; write `m = kN`. Then `t = kN(N+1)²/N = k(N+1)²`, so `(N+1)² | t`, `k = t/(N+1)²` and `m = Nk = N t/(N+1)²`. Conversely, if `(N+1)² | t` put `k = t/(N+1)²` and `m = Nk`; then `N | m` and `T_N(m) = k(N+1)² = t`. ∎
**(2)** `t/m = (N+1)²/N = N + 2 + 1/N`, and `N + 1/N ≥ 2` (AM–GM) with equality iff `N = 1`. ∎
**(3)** By (1) the reverse edges correspond to integers `d = N+1 ≥ 2` with `d² | t`. Write `d = ∏ p^{b_p}`; `d² | t ⇔ 2b_p ≤ v_p(t) ⇔ b_p ≤ ⌊v_p(t)/2⌋` for all `p` ⇔ `d | s(t)`. The divisors `d ≥ 2` of `s(t)` number `τ(s(t)) − 1`. ∎
**(4)** Each step multiplies the state by at least 4 (by (2)), so a history of length `ℓ` from `m0` ends at `t ≥ 4^ℓ m0`, i.e. `ℓ ≤ log_4(t/m0)`. For fixed `m0`, `t` the set of histories is therefore a finite union of finite sets (each state has finitely many labels). For complete histories, sources are squarefree integers `≤ t/4^ℓ ≤ t`, so only finitely many sources occur. ∎
**(5)** `m` has a reverse edge iff some `d ≥ 2` has `d² | m` (by (3)) iff `m` is not squarefree. Existence of a complete history of `t`, by strong induction: if `t` is squarefree, `(t; ())` is one; otherwise pick a reverse edge `m —N→ t` (`m < t` by (2)); a complete history of `m` extended by `N` is a complete history of `t`. `|F_t| = 1 ⇔ A(t) = 0` is immediate. ∎

## §2 GIG-T2 (hierarchy and decomposition)
*Key arithmetic fact.* A legal swap replaces `(…,a,b,…)` by `(…,b,a,…)`, same source, same multiset of labels, and the endpoint `m0 ∏ R(N_i)` is unchanged. Hence swap-connected histories have equal `(M,Q)`, so `(M,Q)` is a function of the class `C`; `C` is a function of `W`; and `T` is a function of `(M,Q)`.
*Chain rule* (standard): if `X = f(Y)` then `H(Y|Z) = H(X|Z) + H(Y|X,Z)`. Apply with `Z = T` successively to `X = (M,Q)`, `X = C`, `X = W` (the last is trivial), and split `H(M,Q|T) = H(M|T) + H(Q|M,T)`. Since `C` determines `(M,Q)`, `H(W|M,Q,C,T) = H(W|C,T)` and `H(C|T) = H(M,Q|T) + H(C|M,Q,T)`. ∎

## §3 GIG-T3
Gibbs' inequality gives `H(p) ≤ log2 N` with equality iff `p` is uniform (strict concavity of log); `H ≥ 0` with equality iff `p` is a point mass. The path `p_s = (1−s)δ + s·u` (`δ` point mass, `u` uniform) has continuous entropy from `0` to `log2 N`; the intermediate value theorem gives every value in between. For `p = (1−ε, ε/(N−1), …)` entropy `→ 0` as `ε → 0`. ∎

## §4 GIG-T4 (the histories of 72) — derivation
`72 = 2³3²`: `d ∈ {2,3,6}` ⇒ reverse edges `(N,m) = (1,18), (2,16), (5,10)`.
* `10` is squarefree ⇒ history `(10;5)`.
* `18 = 2·3²`: `d = 3` ⇒ `(2,4)`. `4`: `d = 2` ⇒ `(1,1)`; `1` squarefree. History `(1;1,2,1)`.
* `16 = 2⁴`: `d = 2` ⇒ `(1,4)`, `d = 4` ⇒ `(3,3)`. `3` squarefree ⇒ `(3;3,2)`; `4 → 1` ⇒ `(1;1,1,2)`.
So `|F_72| = 4`. The words `(1,1,2)` and `(1,2,1)` from source 1 differ by one adjacent swap of the distinct labels 1,2 at state 4; both are admissible (states 1,4,16,72 and 1,4,18,72), so they form one class. The histories from sources 3 and 10 have different sources, hence no swap joins them to anything. Uniform model: class probabilities `(1/2,1/4,1/4)` ⇒ `H(C|T) = 1.5`; `H(W|C,T) = ½ log2 2 = 0.5`; sources `(1,1,3,10)` ⇒ `H(M|T) = 1.5`; each source carries one content ⇒ `H(Q|M,T) = 0`. ∎ (Computation: `E1_72.py`; test `test_E1_decomposition`.)

## §5 GIG-T5
Fix `r ≥ 1`. For `S ⊆ {1,…,2r}`, `|S| = r`, let `w_S = 1^r · u` with `u ∈ {1,2}^{2r}`, `u_i = 2` iff `i ∈ S`. From source 1 the state after the prefix is `4^r = 2^{2r}`. Track the 2-adic valuation: label 1 adds 2 to `v_2` (`Δ_2(1) = 2v_2(2) − 0 = 2`), label 2 subtracts 1 (`Δ_2(2) = 2v_2(3) − v_2(2) = −1`) and needs `v_2 ≥ 1`. During the tail at most `r` labels 2 occur, so `v_2 ≥ 2r − r = r ≥ 1` throughout; label 1 is always admissible; so every `w_S` is admissible from 1. Labels used: `1` appears `r + r = 2r` times, `2` appears `r` times, so the endpoint is `R(1)^{2r}R(2)^r = 4^{2r}(9/2)^r = 72^r`. The source 1 is squarefree, so each `(1; w_S)` is a complete history of `72^r`; different `S` give different words. Hence `|F_{72^r}| ≥ C(2r,r)`. ∎ Exact counts: memoised DP `count(t) = Σ_{reverse edges} count(m)` (`count = 1` at squarefree `t`), validated against full enumeration for r ≤ 4 and against the frozen engine.

## §6 GIG-T6
The component sizes are the masses of the partition `C`; `H(C|T=t)` is the Shannon entropy of a distribution on `k` points, hence `≤ log2 k` with equality iff uniform, i.e. iff all `n_i/N` are equal. `H(W|C,T=t) = Σ P(C=i) H(W|C=i)` with `H(W|C=i) = log2 n_i` under the uniform model, so it equals `Σ (n_i/N) log2 n_i ≤ log2 n_max`. Adding, `A(t) = log2 N = H(C|T) + H(W|C,T)` by the chain rule. ∎

## §7 GIG-T7
(a) By definition `Σ_w log2 |B_r(w)| = log2 ∏_w |B_r(w)|`. Equal `N` and equal `I_r` ⇔ equal `log2 P_r` ⇔ equal integers `P_r`.
(b) `B_0(w) = {w}`, so `I_0 = 0`; `B_r(w) ⊆ B_{r+1}(w)`.
(c) `B_{r+1}(w) = B_r(w)` iff there is no vertex at distance exactly `r+1` from `w`, iff the component of `w` is contained in `B_r(w)`, iff `r ≥ ecc(w)`. Therefore `I_{r+1} − I_r = (1/N) Σ_w log2(|B_{r+1}(w)|/|B_r(w)|)` is `> 0` iff some `w` has `ecc(w) > r`, i.e. iff `r < ρ := max ecc`. For `r ≥ ρ`, balls are full components and `I_r` is constant.
(d) For `r ≥ ρ`, `I_r = (1/N) Σ_w log2 n_{C(w)} = Σ_i (n_i/N) log2 n_i = H(W|C,T=t)`. For `r < ρ` some ball is a proper subset of its component, so the sum is strictly smaller. ∎
(e) `|B_r|` of a vertex is computed inside its own piece (edges never leave a piece), so `Σ_w log2 |B_r(w)|` splits over pieces; divide by `N`. Betti numbers of a disjoint union of complexes add.
(f) The graph is simple, so `|B_1(w)| = 1 + deg(w)`. Jensen for the concave `log2`: `(1/N) Σ log2(1+deg) ≤ log2((1/N) Σ (1+deg)) = log2(1 + 2E/N)`, equality iff all `1+deg` equal. The cycle space of a finite graph has dimension `E − N + β0`, so `E = N − β0 + β1(G)` and `1 + 2E/N = 3 + 2(β1(G) − β0)/N`. If `G` is a forest, `β1(G) = 0` and the value is `3 − 2β0/N < 3`. Solving the inequality for `β1(G)` gives the quantitative form. ∎
(g) 2-cells can only kill 1-cycles: `β1(K_A) ≤ β1(G)`.

## §8 GIG-T8 (radius-2 formula)
*Setting.* The Cayley graph of `S_k` w.r.t. adjacent transpositions `s_1..s_{k-1}` is the 1-skeleton of the permutohedron `P_k`; it is bipartite (sign), so induced subgraphs are triangle-free.
*Claim A.* Two distinct vertices `v, z` of `P_k` at distance 2 have either exactly one common neighbour or exactly two, and two exactly when `z = v s_i s_j` with `|i−j| ≥ 2`.
*Proof.* `z = v s_a s_b` with `a ≠ b`. A common neighbour is `v s_c` with `s_c s_d = s_a s_b` for some `d`. If `|a−b| ≥ 2`, `s_a s_b` is a product of two disjoint transpositions and equals `s_c s_d` iff `{c,d} = {a,b}`: two solutions `(a,b),(b,a)`. If `|a−b| = 1`, `s_a s_b` is a 3-cycle whose only factorisation of the form `s_c s_d` is `(c,d) = (a,b)` (the other order gives the inverse 3-cycle). ∎
*Claim B.* If two vertices of `A` at distance 2 in `G` have two common neighbours in `A`, their four vertices form a square face of `P_k` (commuting swaps), all in `A`, hence a face of `K_A`. Conversely every square face of `K_A` gives such a configuration. (Immediate from Claim A and the definition of faces.)
*Formula.* In a triangle-free graph the walks `v–x–z` with `z ≠ v` end at distance-2 vertices only; their number is `Σ_{x~v}(d(x) − 1) = Σ_{z∈S_2(v)} c(z)` with `c(z)` common neighbours. By Claim A, `c(z) ∈ {1,2}`, so `|S_2(v)| = Σ_x(d(x)−1) − #{z: c(z)=2} = Σ_x(d(x)−1) − q(v)`, with `q(v)` the number of squares through `v` (distinct squares through `v` have distinct opposite vertices, since `c ≤ 2`). Add `|B_0| + |S_1| = 1 + d(v)`. ∎
*Square count.* Summing over `v`: `Σ_v q(v) = N + 2E + Σ_x d(x)(d(x)−1) − Σ_v |B_2(v)|` (each `x` appears `d(x)` times as a neighbour). Each square has 4 vertices, so `Q = Σ_v q(v) / 4`. ∎
*Interpretation (not part of the theorem).* Hexagonal faces are boundaries of 6-cycles (braid relations `(s_i s_{i+1})³ = e`); they influence `|B_3|` and beyond, never `|B_2|`. The certificates W5/W6 (T9) realise this exactly: equal `(N,E,Q)` and equal fine radius-≤2 statistics, one hexagon of difference, Betti numbers different.

## §9 GIG-T9, GIG-T10 (existence statements)
These are existence statements with explicit finite witnesses; the proof is an exact integer computation:
1. build the admissible arrangement set `A` of the piece by **simulating** the SELECT-II step for every permutation (and cross-check against the threshold law `K(w) | m`);
2. build the induced permutohedron graph, its components, BFS ball sizes, `P_r`, and the fine signature;
3. build the full subcomplex `K_A` from the face list of `P_k` and compute GF(2) Betti numbers by exact rank over bitsets; check `χ = Σ(−1)^i f_i = Σ(−1)^i β_i`.
Two independent implementations agree: this package, and (read-only) the frozen GEO-HD-1D v004 engine (`RESULTS/crosscheck_frozen.json`; 2 129 sets for k=4, 300 random sets for k=5, the complete-history lists for all `t ≤ 2500`). The tests `test_certificates` and `test_complete_history_loop` re-derive every number quoted in `THEOREMS.md`. No floating-point arithmetic enters any equality: signatures are compared as integers/tuples; entropies are reported at 50-digit precision.
