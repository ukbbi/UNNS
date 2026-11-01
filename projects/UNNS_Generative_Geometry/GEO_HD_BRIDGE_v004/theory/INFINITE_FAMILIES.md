# A4-T1 / A4-T2 — the activation family

**Data.** `k≥2`; prime ℓ with `k | ℓ−1`; `c` of exact order `k` mod ℓ; distinct primes `p_1..p_k ≡ c (ℓ)`; prime `q ≡ c⁻¹ (ℓ)`, `q∉{p_i}`; `P=∏p_i`. Existence of infinitely many such `(p_i), q` is Dirichlet's theorem. `x=P²/ℓ`, `y=(Pq)²/ℓ` (both reduced: ℓ∤P q since `c,c⁻¹≢0`).

## A4-T1 (PROVED)
`D(x)={P}` and `D(y)={P, p_1q, …, p_kq}`; `e_i−e_j` (i≠j) is a primitive relation at both states; it is dormant at `x` and active at `y`.

*Proof.* `a=P²` is square of a squarefree number, so `d²|a ⇔ d | P`; `d=∏_{i∈S}p_i ≡ c^{|S|}`, which is `1 (ℓ)` iff `k | |S|`; with `0<|S|≤k` only `S=[k]`. Hence `D(x)={P}`. For `y` the admissible `d` are `∏_{S}p_i·q^t` (t∈{0,1}), residue `c^{|S|−t}`; `=1` iff `|S|≡t (k)`: `t=0 ⇒ |S|=k`; `t=1 ⇒ |S|=1` (since `k≥2`, `|S|=k+1` is impossible). So `D(y)` is as stated. Primitivity of `e_i−e_j`: in the lattice (`c^{1−1}=1`), entries `±1`; a proper conformal sub-vector has one non-zero entry `±e_i`, residue `c^{±1}≠1`. At `x` no two elements of `D(x)` exist so `E_g(x)=∅`; at `y`, `p_iq/p_jq` realises `e_i−e_j`. ∎ (Congruence alone does **not** prove primitivity — the argument above uses the full lattice and conformal order.)

**Activation, not creation.** `e_i−e_j ∈ Gr(x)` in the common embedding (coordinates `p_1..p_k`, box `1^k`, lattice `Σg_i ≡ 0 (k)`): `Gr(x)={±1^k}∪{e_i−e_j}`, size `k(k−1)+2` (proved: sum-zero vectors in `{−1,0,1}^k` dominate some `e_i−e_j`; sum `±k` forces `±1^k`). The mechanism is new *occurrence vertices* (`p_iq`, from the new prime `q`), not new relations.

## A4-T2 (PROVED + machine-confirmed)
`K_move(y)` is the complete graph `K_{k+1}` with **no** 2-cells, hence `β₁=k(k−1)/2`, `β_j=0` for `j≥2`; `K_axis(y)` is `k+1` isolated points; `K_move(x)` is a point.

*Proof.* Vertices = `F(y)↔D(y)`: `v_0=P=(1^k;0)`, `v_i=p_iq=(e_i;1)` in coordinates `(p_1..p_k;q)`. **Edges** (hull rule, v003): the hull box of `v_i,v_j` has `x_q=1`, `x_l=0` (l∉{i,j}), `x_i,x_j∈{0,1}`; its points `e_q, e_i+e_j+e_q` have `Σ_{[k]}−x_q = −1, +1 ≢ 0 (k)` so are not in `F`. Hull of `v_0,v_i` contains no other point of `F∪{0}` (a point with `x_i=1` in `F` is `v_0` or `v_i`). So all `C(k+1,2)` pairs are edges. **2-cells** need four vertices with `w_1+w_4=w_2+w_3`; sums `v_i+v_j=(e_i+e_j;2)` and `v_0+v_i=(1^k+e_i;1)` are pairwise distinct, so no parallelogram, hence no cells of dimension ≥2. **Axis:** the vertices pairwise differ in ≥2 coordinates. Euler count: `β₁=C(k+1,2)−(k+1)+1`. ∎

Machine checks (frozen engine in the builder; independent code in verifier Z1): B4-1 `ℓ=3, p=(5,11), q=17`: `x=3025/3, y=874225/3`, `D(y)={55,85,187}`, triangle, `β₁=1`; `k=2,3,4,5` with `(ℓ,primes,q)=(3,[5,11],17), (7,[23,37,79],11), (5,[7,17,37,47],3), (11,[37,59,103,191,257],3)`, plus 7 further instances (ℓ=7,13,19) and 51 further `k=2` members: all confirmed; `|Gr(y)|=(k+1)(k+2)` FINITE-EXACT for k=2..5 (not needed for the proofs). **Scope:** this is `K_move`; no statement about `K_real` beyond equality with the frozen move complex.
