# R3-A  What the occurrence inventory fails to describe

## 1. The record and its three kinds of move
For a reduced rational `x=a/b` the frozen record is `(D, F, Lambda_b, region-Graver set Gr, cells, invariants)`. Write `k` for the number of active primes, `F ⊂ B ⊂ Z^k`.  
Every `g ∈ Gr` falls in exactly one class:
* **positive-primitive**: `g ∈ F` (or `-g ∈ F`), minimal for `<=` in `F`;
* **edge-realised**: `g = v-u` with `u,v ∈ F`;
* **dormant**: neither.  A dormant move is a relation of the lattice inside the box that no pair of occurrence indices witnesses.

## 2. Theorem R3-T1a (realised geometry is a function of D) — PROVED
For reduced rational `x`: `F` is determined by `D` (recover `alpha` from `d` by factorisation), and the positive-primitive and edge-realised moves, the cell complexes `K_axis(x)`, `K_move(x)`, their boundary maps, components and homology are functions of `F`, hence of `D`.  
*Proof.* `K_axis`: its cells are unit cubes with all vertices in `F`. `K_move`: a cell `P(u;g_1..g_j)` needs `g_i ∈ Gr` and all vertices in `F`. Fix `u,u+g ∈ F`. Then `g ∈ Lambda_b ∩ [-q,q]`. `g` is conformally minimal iff no `h ∈ Lambda_b`, `h ≠ 0,g`, `h ⊑ g`. Such `h` has each `h_i` between `0` and `g_i`, so `w=u+h` lies in the coordinate hull of `{u,u+g}`, hence in `B`, and in `Lambda_b` (since `u,h` are); so `w ∈ F ∪ {0}`, `w ≠ u, u+g`. Conversely any such `w` gives `h=w-u ⊑ g`. So *g is minimal iff the hull box of u,u+g contains no point of F ∪ {0} besides u,u+g*, a property of `F`. For `g ≥ 0`, `g ∈ F`, the same argument shows minimality iff `g` is `<=`-minimal in `F`. ∎  
*Checks.* 631 constructed states (323 with `|F|>=2`, 96 with dormant moves): moves rebuilt from `F` alone = frozen engine's (0 violations); independent implementation (verifier Z4): 159 states, plus K_move homology compared with the rebuilt moves.  
**Consequence.** For rational states the *realised* geometry has no information beyond `D`. Information beyond `D` lives in (i) dormant moves, (ii) the box and the dead coordinates (primes with `q>=1` that occur in no element of `D`), (iii) `b` itself. Compare B2-T1: for integers everything is a function of `sigma`; here the realised part is a function of `D` but is **not** contractible in general (§4).

## 3. Theorem R3-T1 (occurrence-incompleteness, infinite families) — PROVED (uses Dirichlet's theorem)
**Family k=2.** For every prime `r ≡ 5 (mod 8)`, `r>=13`:  `x_r = 25 r²/(5r-1)`, `y_r = 25 r²/8`.
1. *Domain.* Both are reduced (`5r-1` is prime to `5r`; `8` is prime to `5r`); `v_5=v_r=2` so the active primes are `{5,r}` with `q=(1,1)` for both (same primes, same order, same box).
2. *D.* `F ⊆ {(1,0),(0,1),(1,1)}`. mod `5r-1`: `5 ≢ 1` (`5r-1>4`), `r ≢ 1` (`0<r-1<5r-1`), `5r ≡ 1` ✓. mod 8: `5 ≢ 1`, `r ≡ 5 ≢ 1`, `5r ≡ 25 ≡ 1` ✓. So `F={(1,1)}`, `D(x_r)=D(y_r)={5r}`.
3. *Lattices in the box.* `(1,-1) ∈ Lambda_b ⇔ 5 ≡ r (mod b)`: for `b=5r-1`, `0<r-5<5r-1` ⇒ no; for `b=8`, `r ≡ 5` ⇒ yes. So `Lambda ∩ [-1,1]² = {0, ±(1,1)}` for `x_r` and `{0, ±(1,1), ±(1,-1)}` for `y_r`.
4. *Graver sets.* `Gr(x_r)={±(1,1)}` (size 2); `Gr(y_r)={±(1,1), ±(1,-1)}` (size 4; the two pairs have different sign patterns so neither dominates the other).
5. *Not an artefact.* Fractions are reduced; coordinates, box and order of primes coincide; `Gr` is a lattice-intrinsic set (a coordinate permutation maps `±(1,-1)` to itself). The lattices differ (`Lambda_{5r-1}` and `Lambda_8` have different indices).
6. *Realised geometry.* `F` is one point for both: `K_axis=K_move=` a point; identical. The difference is **not** topological and, by R3-T1a, no equal-`D` pair can differ in realised cells or homology. The extra vector `(1,-1)` is dormant.
Infinitely many such `r` by Dirichlet; verified for the first 15 (Z1) and 12 (builder).

**Family k (all dimensions).** Fix `k>=2`, a prime `ell ≡ 1 (mod k)`, `c ∈ (Z/ell)*` of exact order `k`, distinct primes `p_1..p_k ≡ c (mod ell)` (Dirichlet), `P=prod p_i`. Then `ell | P-1`, and  
`x = P²/(P-1)`, `y = P²/ell` have `q=(1^k)`, `D(x)=D(y)={P}`, `Gr(x)={±1^k}`, `Gr(y)={±1^k} ∪ {e_i - e_j : i≠j}`: sizes `2` and `k(k-1)+2`.  
*Proof.* x: `p_T ≡ 1 (mod P-1)` for `T ≠ ∅` iff `T=[k]` (for proper `T`, `0<p_T-1<P-1`). A vector `1_{T+}-1_{T-}` with both parts non-empty needs `p_{T+} ≡ p_{T-} (mod P-1)`; both are `<= P/2 < P-1` so they would be equal, impossible for disjoint non-empty sets. y: `p_T ≡ c^{|T|}`, so `1_{T+}-1_{T-} ∈ Lambda` iff `k | |T+|-|T-|`; since `|T+|+|T-|<=k` this means `|T+|=|T-|` or `±1^k`. `F={1^k}`. Conformally minimal: `±1^k` and, for `|T+|=|T-|>=1`, only the pairs `e_i-e_j`. ∎  
The dormant set is the root system `A_{k-1}`: its size is quadratic in `k`, which is a property of the lattice, not of the number of coordinates. Verified k=2..5 (Z2) with explicit primes.

## 4. Rational states are not contractible
Unlike B2-T1, realised complexes of rational states can have non-trivial homology: the `ell=11` tower (`COLLECTIVE`/`GEOMETRIC_TRANSITIONS`) has `K_move` with GF(2) Betti vector `(1,6,0)` at `x=S_0²/11` and `(1,8,17,7)` at k=11. So the "additional geometry beyond the integer collapse" exists, is a function of `D`, and is generated by the arithmetic of the congruence `d ≡ 1 (mod b)`.
