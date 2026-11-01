# Definitions and notation — scope-locked

Let `N,M` be positive integers and `x` a positive rational. Set `S_N(M)=M(N+1)^2/N`. The **discrete occurrence set** is `O={(N,M,S_N(M))}`, with section `O_x` at a fixed x. For reduced `x=a/b`, define

`D(x)={d>=2 : d^2 | a and d ≡ 1 (mod b)}`.

The map `O_x -> D(x)` sends `(N,M,x)` to `d=N+1`. Inverse: `N=d-1`, `M=a(d-1)/(b d^2)`. Define `s(a)=∏_p p^floor(v_p(a)/2)`. Integer fibre `D(m)` is the set of divisors >=2 of `s(m)`.

**Exponent-coordinate fibre:** for `P={p:p|s(a)}`, `E_x={ (α_p): 0<=α_p<=v_p(s(a)), ∏p^α_p>=2, ∏p^α_p ≡1(mod b) }`. This set is finite. Its ambient coordinate dimension is `|P|` (not a claim of intrinsic Euclidean geometry).

**Relation lattice:** `Λ_b={ z∈Z^P:∏ p^{z_p} ≡1(mod b) }`, defined when each active `p` is coprime to `b` (automatic for reduced x). The ordered cone and admissible cells are *additional geometric grammar*, not consequences of arithmetic alone.

**SELECT-II (A2):** for `m>=1`, divisor label `N|m`, `T_N(m)=m(N+1)^2/N`. An edge `m --N--> t` is not a fixed-index occurrence shift and not the collective FIELD-I map. Full nonnegative valuation vector `v(m)` belongs to `⊕_p Z_{>=0}` (finite support). Rational valuations belong to `⊕_p Z`.

**Square-root transport:** set `S=s(m)`, `S'=s(t)`, `g=gcd(S,S')`; for each `p|N`, write `n_p=v_p(N)` and `e_p=v_p(m)`, and put `ℓ_p=floor(n_p/2)` if `e_p` odd, else `ceil(n_p/2)`. Let `c=∏_{p|N}p^{ℓ_p}`. Then `S=g c`, `S'=g(N+1)` and `S'=S(N+1)/c`. All statements concern SELECT-II integer edges.

**History:** a finite source-rooted or fixed-start path of admissible SELECT-II label sequences, retaining the full vertex and edge lists. Endpoint + step count is not a faithful path identifier. Path-unfolding is a standard graph-theoretic construction; arithmetic-specific invariants remain open.

**Cell grammars:** in the trivial lattice `Z^k`, the Graver basis is `±e_i`; an admissible axis-aligned unit cell has all corners in the nonzero fibre. In a nontrivial lattice, use an explicitly declared Graver-generated construction. `src/cells.py` implements a *candidate full-rank parallelotope grammar* to explore, **not** an inherited Paper A/B theorem or an approved topological complex.

**FIELD-I (C):** for any realized rational x, `L=lcm D(x)`, `G=gcd{d-1:d∈D(x)}` and `C(x)=x+L^2/G`. Scope C depends on choosing this map; do not identify it with SELECT-II. In regime I (x integer divisible by 4), Vol. II Thm 2.4 gives eventual `x_{n+3}=4x_n`, with the entry time specified by its hypotheses.
