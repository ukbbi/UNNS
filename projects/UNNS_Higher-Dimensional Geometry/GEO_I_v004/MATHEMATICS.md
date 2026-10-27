# GEO-I v004 — Mathematics

*Arithmetic obstructions and stable higher-dimensional geometry.*  Every statement carries one of four labels:

* **[P]** proved by hand in this file;
* **[C]** proved by an exact finite computation (all arithmetic in integers/rationals; the program is shipped and re-run by `verify.py`) — a *computer-assisted proof*, not a hand proof;
* **[O]** observed in exact data over a stated finite range, **not** proved;
* **[Open]** unresolved.

Nothing in v001–v003 or the Foundations manuscripts is modified (see §0).

---------------------------------------------------------------------------------------------------

## 0. Setting (unchanged from v003)

Primes `p_1..p_k`, modulus `b` coprime to all `p_i`, residues `r_i = p_i mod b`, orders `o_i = ord_b(r_i)`, `H = <r_1..r_k> ⊆ (Z/b)^×`.
Relation lattice `Λ = {α ∈ Z^k : Π r_i^{α_i} ≡ 1 (mod b)}`, index `[Z^k:Λ] = |H|`.  For a box `q ∈ N^k` the fibre is
`F_q = (Λ ∩ [0,q]) \ {0}`.  A *Graver move* is a conformally minimal nonzero element of `Λ` (Graver 1975); Lemma 0 of v003: `|g_i| ≤ o_i`.
A *cell* is a parallelotope `P(u;g_1..g_m) = u + Σ[0,1]g_i` with independent Graver generators and all `2^m` corners in `F_q`; `K_abs` is the (face-closed)
abstract complex of cells, `U` the union of the cells in `R^k` (the *geometric image*), and `K_emb` the exact subdivision of `U` when `K_abs` is *embedded*
(any two cells meet in a common face).  Three objects are kept distinct throughout: `K_abs`, `U`, `K_emb`.  **The topology of `U` is the principal invariant**; it depends on the
chosen parallelotope realization.  No claim is made about an intrinsic topology of UNNS occurrence structures.

## 1. Programme A — planar stabilization (k = 2)

### 1.1 Scaling reduction  **[P]**

**Proposition S1.**  Let `k=2`, `D = <r_1> ∩ <r_2>`, `d = |D|`, `a = o_1/d`, `c = o_2/d`.  Then there is `s ∈ (Z/d)^×` such that
`Λ = {(a i, c j) : j ≡ s·i (mod d)}`.  Consequently the map `(i,j) ↦ (a i, c j)` carries the pure lattice `Γ_{d,s} = {(i,j): j ≡ s i (mod d)}` onto `Λ`,
sends the fibre of `Γ` in the box `Q = (⌊q_1/a⌋, ⌊q_2/c⌋)` onto the fibre of `Λ` in `q`, Graver moves to Graver moves, cells to cells, and is an affine isomorphism of the ambient
planes.  Hence `K_abs`, `U`, `K_emb`, the embedded/not-embedded status and every Betti number are identical for `(Λ,q)` and `(Γ_{d,s},Q)`.

*Proof.*  If `r_1^{α_1} r_2^{α_2} = 1` then `r_1^{α_1} = r_2^{-α_2} ∈ D`.  `D` is the unique subgroup of order `d` of the cyclic group `<r_1>`, namely
`<r_1^{a}>`, and `r_1^{α_1} ∈ D ⇔ a | α_1`; likewise `c | α_2`.  Write `α = (a i, c j)`, `g_1 = r_1^{a}`, `g_2 = r_2^{c}` — both generators of the cyclic group `D`, so `g_1 = g_2^{σ}`
for a unit `σ`; the relation becomes `g_2^{σ i + j} = 1`, i.e. `j ≡ -σ i (mod d)`; put `s = -σ`.  The map is a diagonal positive linear map, so it preserves lattice
membership (by construction), the conformal order (coordinatewise comparison of absolute values and signs), convexity and parallelotopes, and the box conditions
`0 ≤ a i ≤ q_1 ⇔ 0 ≤ i ≤ ⌊q_1/a⌋`. ∎   (`d = 1` gives `Γ = Z^2`.)

So, for planar questions, the arithmetic enters only through the triple `(d, s, Q)`.  `verify.py` re-checks S1 on random `(b,p_1,p_2,q)`: `U`-Betti numbers *and* the embedded status agree between the
original lattice and the pure model.  `theory/stabilization.py::realize(o1,o2,d,s)` finds `(b, residues, prime representatives)` for any model.

### 1.2 The v003 guess is false  **[P] for the family s = -1, [C] in general**

*v003 observation O1:* "`q_i > o_i` for both `i` ⇒ `β_1(U) = 0`."  **This is false.**

**Proposition S2 (hollow box).**  For `d ≥ 2` and `Q = (d,d)` the image `U` of `Γ_{d,s}` is not `conv(F)`; for `s = -1` it is a planar graph with `β_1(U) = d`.
For every other `s` the exact computation gives `β_1(U) = 2` (all `(d,s)` with `d ≤ 12`, including composite `d`; the data up to `d = 13` partially).

*Proof for `s = -1`.*  `Γ = {(i,j): i+j ≡ 0 (d)}`.  In `[0,d]^2` minus the origin, the fibre is `F = {(i, d-i): 0 ≤ i ≤ d} ∪ {(d,d)}` (the `d+1` points of the antidiagonal and the corner).
A vector `(a,b) ≥ 0` of `Γ` below `(d-i, i)` has `a+b ≡ 0 (d)` and `0 < a+b ≤ d`, so `a+b = d`, i.e. it equals `(d-i,i)`: hence `(d-i,i)` is a Graver move for `0<i<d`, as is `(1,-1)`, `(d,0)`, `(0,d)`.
Edges of `K_abs`: the `d` antidiagonal steps `(1,-1)`, and the `d+1` spokes from `(d,d)` to every antidiagonal point (moves `(d-i,i)`, `(d,0)`, `(0,d)`); the spokes meet only at `(d,d)` and the spokes are not collinear with the chain.
No 2-cell exists: a parallelogram needs four corners in `F`, and any four points of `F` containing two independent Graver differences would have to include two points off the antidiagonal, but only `(d,d)` is.
So `U` is a connected planar graph with `V = d+2`, `E = 2d+1`, `β_1 = E - V + 1 = d`. ∎

*The hand computation for `d = 2, s = 1` (the simplest hollow box):* `Γ = {j ≡ i (2)}`, `F = {(2,0),(1,1),(0,2),(2,2)}`; moves `(1,1),(2,0),(0,2)`; edges `(1,1)–(2,2)`, `(1,1)–(2,0)`, `(1,1)–(0,2)`, `(0,2)–(2,2)`, `(2,0)–(2,2)`; no parallelogram; `V=4, E=5`, `β_1 = 2`.

**Transfer to actual primes.**  `q_i > o_i = a_i d` allows `Q = (d,d)` as soon as `a_i ≥ 2` (take `q_i = a_i d + 1 ≤ a_i d + a_i - 1`).  Example **[C]**: `b=15`, `p=(2,7)` (orders 4,4; `d=2, a=c=2, s=1`),
`q=(5,5)` (so `x = 2^{10} 7^{10}/15 = 289254654976/15` in the v002 convention `q_i = ⌊e_i/2⌋`): the fibre has 4 points, `K_abs` is embedded, `β(U) = β(K_abs) = (1,2,0)`.  `experiments/counterexample_search.py` certifies 13 such counterexamples
(`d ≤ 5`, `a,c ≤ 3`) through three independent exact routes — the v003 geometric pipeline (planar arrangement, Betti over `Q`), the pure model, and the nerve of the maximal-cell cover over `Q`
(convex cover ⇒ nerve theorem) — which agree in every case and equal the predicted `B(d,s)`.

### 1.3 The corrected statement

Define `B(d,s) = d` if `s ≡ -1 (mod d)`, and `B(d,s) = 2` otherwise.

> **Stabilization statement (corrected G4-C1).**  Let `d ≥ 2`, `Q_1,Q_2 ≥ d`.  (i) If `Q ≠ (d,d)` then `U = conv(F)`; in particular `U` is contractible, `β_1(U) = 0`.
> (ii) If `Q = (d,d)` then `U ≠ conv(F)`, `U` is hollow, and `β_1(U) = B(d,s)`.  For `d = 1` `U` is always contractible.
>
> In terms of primes: `β_1(U_x) = 0` whenever `⌊q_1/a⌋ ≥ d`, `⌊q_2/c⌋ ≥ d` (equivalently `q_1 ≥ o_1`, `q_2 ≥ o_2`) and `(⌊q_1/a⌋,⌊q_2/c⌋) ≠ (d,d)`.

The threshold is *not* `q_i > o_i`: it is `q_i ≥ o_i` *plus* leaving the single hollow box `Q = (d,d)`, i.e. `q ∈ [o_1, o_1 + a - 1] × [o_2, o_2 + c - 1]`; for `a = c = 1` (e.g. `b = 5, (2,3)`) the hollow box is `q = o`, i.e. `q_i > o_i` already excludes it, which is why the v003 data looked like a theorem.
Outside `Q ≥ (d,d)` there are many boxes with `β_1 ≠ 0` (`figures/fig4_phase_map_b5.png`); the statement is only about the quadrant `Q ≥ d`.

**Status.**  d = 1 **[P]** (see §1.5).  The statement for a **fixed** `(d,s)` is reduced to a finite computation by Lemma S4; it is **[C]** for all `(d,s)`, `2 ≤ d ≤ 13`
(`output/data/stabilization_certificates.jsonl`: 42 lattice classes up to the symmetry `s ↔ s^{-1}`, 15 048 boxes, zero violations, every `(d,d)` hollow).  For general `d` it is **[Open]**; `B(d,s) = 2` for `s ≠ -1` is **[C]**
for `d ≤ 12` and **[Open]** in general.

### 1.4 Reduction of "all boxes" to a finite window  **[P]**

**Lemma S4 (translation).**  Fix `(d,s)`, `d ≥ 2`.  Suppose `U_Q = conv(F_Q)` for every `Q` in the *base window* `W = [d,3d-1]^2 \ {(d,d)}`.  Then `U_Q = conv(F_Q)` for every `Q ≥ (d,d)`, `Q ≠ (d,d)`.

*Proof.*  `U_Q ⊆ conv(F_Q)` always.  Induct on `Q_1 + Q_2`.  Let `Q ∉ W`, `Q ≥ (d,d)`; say `Q_1 ≥ 3d` (the case `Q_2 ≥ 3d` is symmetric using `(0,d)` and vertical chords).  Put `Q' = (Q_1 - d, Q_2)`, so `Q'_1 ≥ 2d`, `Q' ≠ (d,d)`, and by induction `U_{Q'} = conv(F_{Q'}) =: P`.
`(d,0) ∈ Γ` (since `0 ≡ s·d`), so translating by `(d,0)` maps fibre points of `Q'` to fibre points of `Q`, and cells to cells (same generators), giving `U_Q ⊇ P ∪ (P + (d,0))`.
Every point `(i,j) ∈ F_Q` lies in `F_{Q'}` (if `i ≤ Q_1 - d`) or in `F_{Q'} + (d,0)` (if `i > Q_1 - d ≥ 2d`: then `(i-d,j) ∈ Γ ∩ [0,Q'] ` is nonzero because `i - d > d`).
Hence `conv(F_Q) = conv(P ∪ (P + (d,0))) = P + [0,(d,0)]`.  This equals `P ∪ (P+(d,0))` iff every horizontal chord of `P` has length `≥ d`.
Each row `y = j` (`0 ≤ j ≤ Q_2`) of the box `[0,Q'_1]` contains the points `i ≡ s^{-1} j (mod d)`; since `Q'_1 ≥ 2d` there are at least two (for `j = 0` the points `d, 2d,...`, the origin being excluded), spaced `d` apart, so the chord of `P` at integer height `j` has length `≥ d`.
For a non-integer height `y` between `j` and `j+1`, the slice of the convex set `P` contains the corresponding convex combination of the two intervals, of length `≥ d`.  So `P ∪ (P+(d,0))` is convex, `= conv(F_Q)`, and `U_Q = conv(F_Q)`. ∎

So for each `(d,s)`, statement (i) is equivalent to a computation on the `(2d)^2 - 1` boxes of `W`.  `theory/coverage.py` decides `U = conv(F)` exactly: it subtracts, in rational arithmetic, every 2-cell of `K_abs` (as a convex polygon, by half-plane clipping) from the convex hull; the difference is empty iff `U = conv(F)`.  It was validated against the full exact planar-arrangement homology: 0 disagreements on 102 boxes (and again on 40 in `verify.py`).
(Since `U` is a planar compact set, `β_2 = 0` and `β_1` = number of bounded complementary components; `U = conv(F)` implies contractible because `conv(F)` is convex.)

### 1.5 The case d = 1  **[P]**

`Γ = Z^2`, Graver moves are `±e_1, ±e_2`, `F` the box minus the origin, cells are unit squares (and unit edges) avoiding the origin.  For `Q_1,Q_2 ≥ 2`, `U` is the union of all unit squares of the box except the corner square `[0,1]^2`, together with the two edges `(1,0)–(1,1)` and `(0,1)–(1,1)` of that square (they are edges of the neighbouring squares); this is an L-shaped region and deformation retracts to a point.
For `Q_1 = 1` or `Q_2 = 1` it is a strip or an arc.  So `U` is always contractible.  (Not `conv(F)`: the triangle `(1,0),(0,1),(1,1)` of the hull near the origin is not covered, which is why S1 requires `d ≥ 2` for statement (i).)

### 1.6 What remains open  **[Open]**

A uniform proof for all `(d,s)`.  The window computation scales as `d^2` boxes each costing `O(d^4)`; we certified every `(d,s)` for `d ≤ 13` and the runs for `d = 14` were stopped for time, not because of a failure.
`B(d,s) = 2` for `s ≠ -1`: at the hollow box the fibre is the set `Γ ∩ [0,d]^2 \ {0}`, a small planar configuration, and the computation shows two independent cycles for every `(d,s)` tested, but a proof for all `d` was not completed.  Nothing in this release assumes stabilization beyond `d ≤ 13`.

---------------------------------------------------------------------------------------------------

## 2. Programme B — finite obstruction criteria

### 2.1 Relative-interior criterion  **[P]**

**Theorem T-REL.**  A face-closed finite family `K` of convex polytopes is an embedded polyhedral complex (any two members meet in a common face, possibly empty) iff the relative interiors of distinct members are pairwise disjoint.

*Proof.*  (⇒) If `x ∈ relint P ∩ relint Q`, then `P ∩ Q` is a face of both containing a relative-interior point of `P`; the only such face of `P` is `P` itself; likewise for `Q`; so `P = Q`.
(⇐) Let `P ∩ Q ≠ ∅` and choose `x ∈ relint(P ∩ Q)`.  `x` lies in the relative interior of a unique face `P'` of `P` and a unique face `Q'` of `Q`; both are members of `K` (face-closed) whose relative interiors share `x`; by hypothesis `P' = Q' =: F`.
`F ⊆ P ∩ Q`.  For `y ∈ P ∩ Q`, the segment `[y, x]` extends slightly beyond `x` inside the convex set `P ∩ Q` (as `x` is relatively interior in it), hence inside `P`; a face of `P` containing a relative-interior point of a segment of `P` contains the whole segment, so `y ∈ F`.
Thus `P ∩ Q = F`, a common face. ∎

`K_abs` is face-closed (all subsets of generators give cells whose corners are corners of the larger cell).  Distinct cells are distinct point sets (the edge directions of a parallelotope determine its generators up to sign; we use lex-positive generators and the base `u`).

### 2.2 The finite template criterion  **[P] (theory) + [C] (algorithms)**

A **template** is `(A, B, δ)`: `A, B` are independent tuples of lex-positive Graver vectors of `Λ` (sizes `r, s ≥ 1`), and `δ ∈ Λ` lies in the **open zonotope**
`Z(A,B) = { Σ t_i g_i − Σ l_j h_j : 0 < t_i, l_j < 1 }`, with `(A,δ) ≠ (B,0)` (the two cells are distinct; for `A = B` we identify `δ ~ -δ`).
It is **realized in `q`** if there is `u ∈ Λ` with all corners of `P(u;A)` and `P(u+δ;B)` in `[0,q] \ {0}`.

**Theorem T-FIN (G4-T3).**  `K_abs(Λ,q)` is embedded iff no template is realized in `q`.  The set of boxes in which a fixed template is realized is an up-set of `N^k`; its minimal elements form a finite antichain
(Dickson's lemma and the explicit window below), and the set of templates is finite.  Hence there is a finite antichain `Obs(Λ) ⊂ N^k` of **minimal obstruction boxes** with
`K_abs(Λ,q)` embedded ⇔ `q` does not dominate any element of `Obs(Λ)`.

*Proof.*  (Template ⇒ non-face intersection.)  If realized, `P(u;A)` and `P(u+δ;B)` are cells of `K_abs`; they are distinct, and `u + Σt_i g_i = u + δ + Σ l_j h_j` is a common point of their relative interiors.  By T-REL `K_abs` is not embedded.
(Non-face intersection ⇒ template.)  If `K_abs` is not embedded, T-REL gives distinct cells `P(u;A), P(v;B)` with `x ∈ relint ∩ relint`; so `v - u = Σ t_i g_i − Σ l_j h_j` with all `t_i, l_j ∈ (0,1)`; `δ = v − u ∈ Λ`; the corners lie in `F_q ⊆ [0,q]\{0}`; so the template `(A,B,δ)` is realized.  Finiteness of the templates: the Graver basis is finite, and `δ` ranges over the lattice points of a bounded box containing `Z(A,B)`.
Monotonicity in `q` is obvious.  *Window for the minimal boxes:* the smallest box containing the corners for a given `u` is the coordinatewise maximum of the corners; if some `u_i + min-corner_i ≥ 2 o_i` then `u − o_i e_i ∈ Λ` is also admissible (no corner can land on the origin because that corner has coordinate `i` at least `o_i ≥ 1`) and gives a strictly smaller box; hence minimal boxes are attained with `u_i + min-corner_i < 2 o_i`.  `min_boxes` searches three periods per coordinate. ∎

**Algorithm and validation.**  `theory/obstruction_templates.py` enumerates the templates (exact rational solve for independent generators, exact LP for dependent ones) and computes `Obs(Λ)`.  It shares no code with the geometric audit of v003 (`geometry/validation.py`: exact polyhedral intersection by LP).
`verify.py` and the shipped runs compare the two on every box of a range: `output/data/validation_k2_templates.jsonl`: 233 residue classes (b ≤ 14), 10 852 (residues, box) cases (3 431 non-embedded); `validation_k3_templates.jsonl`: 15 classes (b ≤ 5), 1 450 cases; **0 disagreements**.
Direct-product lattices (v003 T2a) have an empty atlas (checked).

### 2.3 Hierarchy of obstructions  **[P] for the definitions, [C] for the censuses**

For a template `(A,B,δ)` with `|A| ≤ |B|`:

| kind | meaning | v003 name |
|---|---|---|
| **O-E** | `|A|=|B|=1`, two non-parallel edges cross at an interior point | pairwise edge crossing (the only thing an edge audit can see) |
| **O-D** | an edge `[x,x+g]` of the complex, **both** of whose endpoints are corners of a higher cell `Q`, so the edge is a chord (diagonal) of `Q` | Proposition D |
| **O-T** | an edge from a corner of a cell `Q` to a lattice point strictly inside `Q`/on its interior (the edge "goes through" the cell without being a chord) | the v003 case O2 |
| **O-C** | two cells of dimension ≥ 2 whose relative interiors meet | — |

Edge audits detect O-E only; O-D, O-T, O-C are invisible to them.  That is exactly the Klein-four phenomenon.

### 2.4 k = 2: the planar atlas  **[C] and [O]**

By S1 it suffices to compute `Obs` for the pure lattices `Γ_{d,s}` (in `Q`-units).  `output/data/k2_atlas_pure.jsonl` lists `Obs(Γ_{d,s})` for all `d ≤ 7` and all `s`.  Observed **[O]** (for `d ≤ 7`, not proved):

* `s = 1`:  `Obs = {(1,2d), (2,d+1), (d,d), (d+1,2), (2d,1)}` for `3 ≤ d ≤ 7` (for `d = 2` the box `(2,2)` is embedded and the antichain is `{(1,4),(2,3),(3,2),(4,1)}`, which is also the `s = -1` formula);
* `s = -1`:  `Obs = {(i, 2d+1-i) : 1 ≤ i ≤ 2d}` (non-embedded iff `Q_1 + Q_2 ≥ 2d+1`).
* other `s`: irregular staircases with more corners (see `figures/fig3`).  `(1,2d)` and `(2d,1)` are always present.
* `d = 1` (direct product): `Obs = ∅` (consistent with v003 T2).

The two exceptional families of boxes — hollow `(d,d)` (Programme A) and the minimal obstruction boxes — are different sets, but for `s = 1` they share the box `(d,d)`; for `b = 5, (2,3)` both are the O2 case (§2.6).

### 2.5 G4-T4: the Klein-four classification (k = 3)  **[C]**

`Λ` depends on the residues only through the homomorphism `Z^3 → H`.  `H = Z/2 × Z/2` with three non-trivial images generating `H` gives exactly two lattices up to permuting coordinates and `Aut(H)`:

* **type (a,b,ab)** (pairwise distinct images, e.g. `b = 8`, `p ≡ 3,5,7`): `Λ = {α_1 ≡ α_2 ≡ α_3 (mod 2)}` ("all coordinates of the same parity").
  `Obs` = the 9 boxes that are the coordinate permutations of `(1,1,4)` and `(1,2,3)`; **every one is O-D**, realized by a single 2-cell with generators `(0,0,2)` and `(1,1,-1)` whose long diagonal `(1,1,1)` is itself an edge (e.g. at `q = (1,1,4)`: points `(0,0,2),(0,0,4),(1,1,1),(1,1,3)`).
  `(2,2,2)` is **not** an obstruction; `(3,2,1)`, `(4,1,1)`, ... are.  The atlas is identical for every modulus and residue triple tested (`b ∈ {8,15,24}`, 11 triples).
* **type (a,a,b)** (one repeated image): `Obs = {(1,3,2),(3,1,2),(2,2,2)} ∪ {(1,4,0),(2,3,0),(3,2,0),(4,1,0)}`, the last four lying in the coordinate plane `q_3 = 0` (they are the k=2 obstructions of the repeated pair).  `(2,2,2)` is O-T.
* Two-direction audit: for type (a,b,ab), each of the 9 minimal boxes is non-embedded and every box one unit lower is embedded, by the exhaustive polyhedral audit (an independent code path) — `verify.py`.

**Erratum recorded for v003 (v003 itself is untouched).**  v003 reported the Klein-four class `(3,5,7) mod 8` as non-embedded "from `q ≥ (3,3,2)`" — true but not sharp: `(3,3,2) ≥ (3,2,1)`, and the sharp threshold is the 9-box antichain.

In all of the censuses computed, **every minimal obstruction has span dimension 2** (a 2-plane), while its *support* (set of coordinates used) is 2 or 3: for type (a,b,ab) the obstruction lives in a non-coordinate 2-plane spanned by `(0,0,2)` and `(1,1,-1)` and uses all three coordinates (`output/data/obstruction_kinds.json`).

### 2.6 G4-T5: the O2 case  **[P]**

`b = 5`, residues `(2,3)`, `q = (4,4)`.  Then `Λ = {(i,j): i ≡ j (mod 4)}` (`2·3 = 6 ≡ 1`), `d=4, s=1`, and the fibre has 6 points.
The Graver vectors `g = (1,-3)`, `h = (3,-1)` and `m = (2,-2) = (g+h)/2` give the cell `P((0,4); g, h)` with corners `(0,4),(1,1),(3,3),(4,0)` (all in `Λ`: `3^4 = 81`, `2·3`, `2^3 3^3 = 216`, `2^4 = 16`, all `≡ 1 mod 5`)
and the lattice point `c = (2,2) = (0,4) + m ∈ Λ` at its centre (`2^2 3^2 = 36 ≡ 1`).  `m` is a Graver move (no `(1,-1)` in `Λ`: `2·3^{-1} = 4 ≠ 1`), so `[(0,4),(2,2)]` is an edge of `K_abs`; its relative interior lies in the interior of the 2-cell and it is not a chord: an **O-T** obstruction with no crossing of edges.
The box is minimal: the corners force `q ≥ (4,4)` (the base corner `(0,4)` and the far corner `(4,0)`), and the exhaustive search over `u` in the window shows no smaller `u` works; `(3,4)` and `(4,3)` are embedded (audit).  Full atlas: `Obs = {(1,8),(2,5),(4,4),(5,2),(8,1)}`; `(2,5)` and `(5,2)` are the v003 crossing (82944/5 has `q=(5,2)`).
`verify.py` check BM-9 re-derives all of this.

### 2.7 G4-T6: essential dimensionality  **[C] + [P] partial**

*Adjoining a prime with residue 1 mod b* appends a unit axis `e_{k+1} ∈ Λ'` (`Λ' = Λ ⊕ Z e_{k+1}`, `o_{k+1} = 1`).

* **(a) persistence [P].** `F_q × {0} ⊆ F'_{(q,t)}` and cells of `K_abs(Λ,q)` are cells of `K_abs(Λ',(q,t))` (generators with last coordinate 0), so every obstruction persists: `Obs(Λ) × {0}` is dominated by `Obs(Λ')`.
* **(b) classification invariance.**  For `k = 2 → 3` [P]: `Λ` direct product ⇒ `Λ'` direct product (`|H|` and `Π o_i` unchanged) ⇒ embedded for all boxes (v003 T2a); `Λ` non-direct ⇒ non-embedded for large `q` ⇒ `Λ'` non-embedded by (a).  So "embedded for all boxes" is unchanged by a residue-1 prime.
  [C] on every class `b ≤ 12` of the shipped run (`essential_dimension.py`, `output/data/essential_dimension_k2.jsonl`): the atlas is empty for `Λ` iff it is empty for `Λ'`.
* **(c) thresholds are lowered [C].**  The fibre excludes only the origin; with a unit axis the vertices `(0,t)`, `t ≥ 1`, re-enter, so the "origin-excluded" corner constraint of a template can be avoided one level up.  In `b = 5, (2,3)`: `Obs(Λ) = {(1,8),(2,5),(4,4),(5,2),(8,1)}` but
  `Obs(Λ') = {(1,8,0),(2,5,0),(4,4,0),(5,2,0),(8,1,0)} ∪ {(1,5,1),(5,1,1)}` — **new, smaller obstruction boxes at height `q_3 = 1`**.  This occurs in **every** non-direct class of the shipped run (88 of 88, `b ≤ 12`, `output/data/essential_dimension_k2.jsonl`; the 14 direct-product classes have empty atlases both before and after), and the new boxes are always at height exactly 1.
  Hence a residue-1 prime is **not essential for the classification** but **it is not inert for the thresholds**: the stated expectation "adjoining a residue-1 prime is not essential" is true for classification and false for thresholds.
* **(d) support versus span [C].**  In every atlas computed (k = 2, k = 3: b=5 (2,3); Klein-four; parity `Σα even`) every minimal obstruction has span dimension 2, and support dimension 2 or 3.  The parity lattices and type (a,b,ab) need all three coordinates although their obstructions are planar.

### 2.8 Genuinely four-dimensional obstructions  **[C] audits; templates for k=4 are UNAVAILABLE**

The full template atlas for `k = 4` exceeded the compute budget (the `k = 3` parity atlas has 22 864 templates and takes 48 s; `k=4` is much larger) and is reported **UNAVAILABLE**.  Exhaustive audits of the polyhedral realization (independent code path) were run instead:

* parity lattice `Λ_4 = {Σ α_i even}` (`b = 3`, residues `(2,2,2,2)`): all boxes with a zero coordinate agree with `Λ_3`, and **`(1,1,1,1)` is a new non-embedded box** that dominates no 3D obstruction box (`(1,1,1,0)` is embedded); `Λ_3 = {Σ α_i even}`: first obstruction at `(2,1,1)` (full support), `(1,1,1)` embedded.
* the 4D example `b = 24`, residues `(5,7,13,23)` (`H = (Z/24)^× ≅ (Z/2)^3`, orders `(2,2,2,2)`, `|H| = 8 < 16`; `Λ = {α: all α_i same parity}`): every box with `max q ≤ 2` is embedded; over `[0,4]^4` (up to permutation) the minimal non-embedded boxes are `(3,2,1,1)` and `(4,1,1,1)`; no edges cross in any of them.  So the 4D complexes in this class are embedded in all boxes `≤ (2,2,2,2)`, and the obstruction is again a diagonal/higher-cell overlap, invisible to edges.

### 2.9 What is **not** established

* No hand proof for the closed forms of §2.4 or the `Klein-four` atlases; they are exact finite computations (T-FIN gives a decision procedure, so each `Obs` is a *computer-assisted theorem* for the lattice computed, but the infinite families in `d` are conjectural).
* No classification of `Obs` for general `k`, no bound on the span dimension of minimal obstructions (observed 2), no `k = 4` atlas.
* No topological statement for `k ≥ 3` (the planar Alexander-duality argument is two-dimensional).

---------------------------------------------------------------------------------------------------

## 3. Reproducibility and exactness

All decisions use `fractions.Fraction` / `gmpy2.mpq` / integers.  Betti numbers are over `Q` (exact rank).  For planar `U` degrees `≥ 2` vanish by Alexander duality; for the nerve route only degrees certified trusted are compared.  Resource-limited cases are reported UNAVAILABLE (never counted as PASS).
`python3 verify.py --smoke` and `python3 verify.py` re-run the checks listed in `README.md`; the sibling-release integrity checks are optional and reported separately.
