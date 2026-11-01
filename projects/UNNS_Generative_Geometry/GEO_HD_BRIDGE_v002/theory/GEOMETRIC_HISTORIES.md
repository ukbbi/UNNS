# G2-A — Actual geometry of intermediate states and of whole histories

## 1. The state record (nothing manufactured)
For an integer `m` put `v_p=v_p(m)`, `q_p=floor(v_p/2)`, `P(m)={p: q_p>=1}`, `sigma(m)=prod p^{q_p}`, `k(m)=|P(m)|`.
`G(m)=(D, F, Lambda, cells, U, invariants)` is taken from the frozen GEO-I engine: `D(m)` = divisors `>=2` of `sigma`;
`F` = exponent box `prod[0,q_p]` minus the origin; `Lambda = Z^P` (denominator 1, so every prime is coprime to `b=1`);
Graver basis of `Z^P` = `{±e_p}`; cells = parallelotopes `P(u; e_S)` with all `2^|S|` vertices in `F`; `U` = union of cells.
If `P(m)` is empty, `D(m)` is empty and **every other component is reported undefined** (`state_record` returns `defined: False`).

## 2. Theorem B2-T1 (collapse and closed forms) — PROVED, CHECKED against the frozen engine
For an integer `m` with `k=k(m)>=1`:
1. `G(m)` is a function of `sigma(m)` alone, and `sigma(m)=max D(m)` recovers it; hence `m, m'` with the same `sigma` have identical records.
2. `K_axis = K_move`; `|F|=prod(q_p+1)-1=|D(m)|`; the number of cells is `prod(2q_p+1) - 2^k`; `chi = 1`; `d_aff = k` except `d_aff=0` for `k=1,q=1`.
3. `K(m)` is **contractible** (GF(2) Betti `(1,0,...,0)`, one component).
4. `K(m) ⊆ K(m')` (as cell complexes) ⇔ `D(m) ⊆ D(m')` ⇔ `q(m) <= q(m')` coordinatewise. In particular, for integers, persistence of occurrence vertices **does** imply persistence of Graver edges, cells and the realized region (the dissociation warned about in the spec needs `b>1`, §5).

*Proof.* Every nonzero conformally minimal vector of `Z^P` is a unit vector (a vector with two nonzero coordinates dominates a unit vector), so `K_axis=K_move`.
A cell with lex-minimal vertex `u` and generators `e_i, i∈S` has vertices `u+e_T, T⊆S`; all lie in `F` iff `u≠0` and `u+1_S<=q`. Counting pairs `(u,S)` with `u+1_S<=q`: per coordinate `p` there are `q_p+1` choices (`p∉S`) plus `q_p` (`p∈S`), i.e. `2q_p+1`; the pairs with `u=0` are the `2^k` subsets `S` (here `q_p>=1` is used). Euler characteristic: the full box complex has `chi=1` (product of intervals) and the `u=0` cells contribute `sum_S(-1)^{|S|}=0`.
Contractibility: let `B` be the box complex (contractible), `C=[0,1]^k` the closed star of the origin, `K=B∖openstar(0)`. Then `B=K∪C` and `K∩C` is the union of the facets `{x_i=1}` of `C`; these all contain the vertex `(1,..,1)`, so `K∩C` is a cone, contractible. `C` is contractible, so `K∩C→C` is a homotopy equivalence and therefore `K→B` is one; hence `K` is contractible.
(4): cells are determined by their vertices, `F ⊆ F'` iff the box of `q` fits in the box of `q'` (use the vertices `q_p e_p`), and `d=∏p^{α_p}` identifies `F` with `D`. ∎
*Checks.* 260 states vs the frozen `analyse` (f-vector, components, Betti over GF(2), `d²=0`): 0 violations (`results/GEOMETRY_STATES.json`); independent cubical homology on 50 boxes of up to 3 coordinates; 600 random persistence pairs; collapse on 245 same-`sigma` pairs (verifier Z1).

**Consequence (answer to "does geometry see more than occurrence counts?" for integers).** The complete GEO-I record of an integer state is *equivalent* to `D(m)`. All topological invariants are trivial; what varies is dimension `k`, the shape `q`, the f-vector, and the inclusion order. Any geometric law for integer states is therefore a law about `sigma` and `q`.

## 3. Theorem B2-T2 (transport of the box along a SELECT-II edge) — PROVED
For `m --N--> m'=m(N+1)^2/N` and a prime `p` with `n=v_p(N)`, `w=v_p(N+1)` (at most one is nonzero):
`q_p' = q_p + w` if `p∤N`; `q_p' = q_p − l_p` if `p|N`, with `l_p=floor(n/2)` when `v_p(m)` is odd and `ceil(n/2)` when it is even.
*Proof.* `v_p(m')=v_p(m)+2w−n`. For `p∤N` the change `2w` is even, so `floor` shifts by exactly `w`. For `p|N`, `floor((e−n)/2)` equals `floor(e/2)−floor(n/2)` for `e` odd and `floor(e/2)−ceil(n/2)` for `e` even. ∎ (checked on all 9 534 edges `m<=1300` by the verifier and 24 496 edges `m<=3000` by the builder). This is the finite-prime form of the square-root transport `sigma'=sigma(N+1)/c` of DEFINITIONS.md (`c=∏p^{l_p}`).

## 4. Theorem B2-T3 (gain–loss balance) — PROVED
For a history with labels `N_1..N_l` put `G_p=sum_i v_p(N_i+1)` (the *gain content*) and `Lambda_p=` total decrease of `q_p` over the steps with `p|N_i`. Then
`q_p(end) − q_p(start) = G_p − Lambda_p`.  Hence the **loss budget** `Lambda_p` is determined by the content (multiset of labels) and the endpoints — *not* by the order of the labels. (Telescoping of B2-T2.) For `4→65536`: route `1^7`: `G=(2:7)`, `Lambda=0`; route `(2,2,3,3,3,3)`: `G=(2:8,3:2)`, `Lambda=(2:1,3:2)`, both for every admissible ordering (`results/GEOMETRY_STATES.json`, `REWRITE_LAWS.json`).

## 5. What is *not* shown: rational states
For `x=a/b` with `b>1` the lattice `Lambda_b` is non-trivial and the Graver moves depend on `b`. In 7 464 random rational states (1 169 distinct fibres `D`) and 290 targeted ones, `|F|`, the cell counts per dimension, the number of components, the GF(2) Betti vector and `d_aff` were **functions of `D`** — but the number of region-Graver moves was not. No proof; **OPEN (O2-3)**. Along the FIELD-I orbits tried (1369/9, 225/2, 6845/36, 1369/3), the geometry at constant `D` did not change either (finite-exact observation, not a theorem).
