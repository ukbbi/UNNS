# GEO-I v005 — Programme B/C: obstruction atlases and essential obstruction dimension

Labels as in STABILIZATION.md. Inherited unchanged from v004 (frozen definitions): `Λ_b = ker(Z^k → (Z/b)^×)`, `F_q = (Λ ∩ [0,q]) ∖ {0}`, Graver moves, parallelotope cells `P(u;A)`, `K_abs` (face-closed), `U` (union of the cells), `K_emb` (exact subdivision). `K_abs`, `U`, `K_emb` stay distinct; the topology of `U` is the principal invariant. Theorem T-REL (a face-closed polyhedral family is embedded iff relative interiors of distinct cells are disjoint) and T-FIN (embedded ⇔ no forbidden template realized; the set of realization boxes of a template is an up-set) are used as proved in v004. In particular **embeddedness is a down-set in the box**.

## 0. Status table

| ID | Statement | Status |
|---|---|---|
| G5-T3 | `Obs(Γ_(d,−1)) = {(i, 2d+1−i) : 1 ≤ i ≤ 2d}`, i.e. embedded ⇔ `Q1+Q2 ≤ 2d` (for `Q1,Q2 ≥ 1`) | **PROVED+CHECKED**, all `d ≥ 2` |
| G5-T4 | `Obs(Γ_(d,1)) = {(1,2d),(2,d+1),(d,d),(d+1,2),(2d,1)}` for `d ≥ 3` (`d = 2` coincides with T3) | **PROVED+CHECKED**, all `d ≥ 3` |
| G5-C3 (weak) | every minimal obstruction box has a witness with `d_span ≤ 2` | **FALSE** — 14 certified lattice classes, simplest = 4D parity at `(1,1,1,1)`; **CORRECTED** to G5-C3′ below |
| G5-C3′ | every minimal obstruction box has a witness with `d_span ≤ 3` | **OPEN**; holds in all 919 minimal boxes of the census (k = 3, 4) |
| G5-C4 | irreducible witnesses are planar (`d_span ≤ 2`) | **FALSE** (irreducible witnesses with `d_span = 3` and `4` exist) |
| G5-T5 | essential higher-coordinate classification | **CHECKED** (exact tables for the mandatory families + bounded census); lifting lemma **PROVED** |
| G5-T6 | effective witness/rank certificates | **PROVED+CHECKED** (scheme + 46 independently verified certificates) |
| unrestricted `k = 4` atlas | all lattices, all boxes | **UNAVAILABLE** (bounded census only) |

## 1. Witness dimension — exact definitions

A *witness* of non-embeddedness at box `q` is a pair of distinct cells `c₁ = P(u;A)`, `c₂ = P(v;B)` of `K_abs(Λ,q)` with intersecting relative interiors, equivalently a forbidden template `T = (A,B,δ)`, `δ = v − u`, realized in `q` (T-REL/T-FIN). For a witness:
* `d_span(T) = rank_Q [A, B, δ]` (`δ` lies in the span of `A ∪ B` automatically);
* `d_support(T)` = number of coordinates `i` in which some generator or `δ` has a non-zero entry;
* `d_intersection(T) = dim(c₁ ∩ c₂) = |A| + |B| − d_span(T)` (the relative interiors meet, `δ` lies in the span, so the affine hulls meet in dimension `|A|+|B|−rank`).

A box `q` is an **essential coordinate obstruction** if `K_abs(Λ,q)` is non-embedded while `K_abs(Λ, q with q_i := 0)` is embedded for every `i` — computed from the actual restricted complexes with the independent polyhedral audit (`theory/witness_dimension.py::analyse_box_cells`). A *minimal obstruction box* is a minimal non-embedded box; its predecessors are embedded, so minimal boxes with all `q_i ≥ 1` are essential.

Complete enumeration (no cap): at a box, the witnesses are the non-face pairs of the cells *actually present* (`witnesses_from_cells`); the template route (`witnesses`) enumerates the forbidden templates realized in the box. The two routes agree (`canon`-equal witness sets) on every box compared (tests, and the 14 refutation boxes — `output/data/` + `tests/`), and a third criterion (the exact LP audit of v003) decides embeddedness when locating minimal boxes. Resource exhaustion raises `UNAVAILABLE`, never `embedded`.

## 2. Planar atlases (Programme C)

Throughout `Γ = Γ_(d,s)`, `Obs` = antichain of minimal non-embedded boxes with `Q1, Q2 ≥ 1` (axis boxes are 1-dimensional and embedded). By the down-set property: *`Obs = X` iff (W) each `x ∈ X` is non-embedded, (M) every box that dominates no element of `X` is embedded.* For (M) it suffices to exhibit the finitely many *maximal* boxes dominating no element of `X` and prove those embedded.

### Theorem T3 (s = −1)  [PROVED+CHECKED]
`Γ = {i+j ≡ 0 (d)}`, `S = i + j`, Graver set from Lemma G (STABILIZATION.md). *(M)* If `Q1 + Q2 ≤ 2d` it suffices to treat `Q1+Q2 = 2d`. Then `F ⊂ {S = d} ∪ {p}`, `p = (Q1,Q2)` (the only point of the box with `S = 2d`). Edges: the steps `(1,−1)` between consecutive points of the segment `{S = d}`, and one spoke `p − x = (a,d−a)` (Graver) to each `x` on the segment. A 2-cell needs a non-degenerate parallelogram, but any 4 points of `F` contain ≥ 3 collinear points of the segment; so the complex is a path plus a fan from `p` over a line not through `p`: spokes meet pairwise only at `p`, a spoke meets the line only at its end point. Embedded. *(W)* For `0 ≤ a ≤ d` the box `Q = (a+1, 2d−a)` contains the parallelogram `P(u;(1,−1),(a,d−a))`, `u = (0,d)`, whose four corners are `(0,d),(1,d−1),(a,2d−a),(a+1,2d−a−1)`; for `a ≥ 1` the diagonal `(1,d−1)→(a,2d−a)` has the Graver vector `(a−1, d−a+1)` and is an edge (for `a = 0` use the other diagonal `(0,d)→(1,2d−1)`, vector `(1,d−1)`). A diagonal edge is not a face of its parallelogram, so by T-REL the box is non-embedded; the transposed configuration gives `(2d−a, a+1)`. Together `Q1 ∈ {1,…,d+1} ∪ {d,…,2d}`. Every `Q` with `Q1,Q2 ≥ 1` and `Q1+Q2 ≥ 2d+1` dominates `(min(Q1,2d), 2d+1−min(Q1,2d))`. ∎
`theory/symbolic_atlas.py::check_T3(d)` re-derives (W) with explicit corner/chord data, (M) with the independent exact planar test, and the staircase combinatorics, for **every `2 ≤ d ≤ 40`**, plus the brute-force antichain for `d ≤ 8`: all pass (`output/data/atlas_s_pm1.json`). The planar test (`theory/planar_embed.py`) shares no code with the template machinery and agrees with it on 2851 boxes (`d ≤ 7`, all `s`).

### Theorem T4 (s = +1, d ≥ 3)  [PROVED+CHECKED]
`Γ = {i ≡ j (d)}`, `X = {(1,2d),(2,d+1),(d,d),(d+1,2),(2d,1)}`. *(W)*
* `(1,2d)`: cell `P((0,d); (0,d), (1,1−d))` (corners `(0,d),(0,2d),(1,1),(1,d+1)`) contains the diagonal edge `(0,d)→(1,d+1)`, Graver `(1,1)`; `(2d,1)` is its transpose.
* `(2,d+1)`: cell `P((1,1); (1,1), (−1,d−1))` (corners `(1,1),(2,2),(0,d),(1,d+1)`) contains the diagonal edge `(1,1)→(1,d+1)`, vector `(0,d)`; `(d+1,2)` is its transpose.
* `(d,d)`: cell `P((0,d); (1,1−d), (d−1,−1))` (corners `(0,d),(1,1),(d−1,d−1),(d,0)`) whose long diagonal `(1,1)→(d−1,d−1)` is the union of the edges `(i,i)→(i+1,i+1)`; each is a non-face of the cell.

*(M)* The boxes with `Q1,Q2 ≥ 1` dominating no element of `X` lie below one of `(1,2d−1)`, `(d−1,d)`, `(d,d−1)`, `(2d−1,1)` (staircase, checked for every `d`). These four are embedded: `(1,2d−1)` has the three points `(0,d),(1,1),(1,d+1)` (a triangle); `(d−1,d)` has the collinear points `(i,i)`, `1 ≤ i ≤ d−1`, and the apex `(0,d)`, joined by the Graver vectors `(i,i−d)` — a fan over a line not through the apex, no 2-cell (any 4 of the points contain 3 collinear); the other two are transposes. Minimality of each box of `X` follows because its predecessors lie below those four boxes. ∎ Checked for every `3 ≤ d ≤ 40` as for T3.

These are the two planar atlases observed in v004 for `d ≤ 7` (conjecture there), now theorems for all `d`. They also explain the coupling noted in v004: for `s = +1` the minimal box `(d,d)` is exactly the hollow box of STABILIZATION.md.

**Not claimed:** general `s`. The data of v004 (`d ≤ 7`) show antichains whose size grows with the continued fraction of `s/d`; no formula is asserted.

## 3. G5-C3 is false: certified counterexamples

**Parity lattice `Λ = {α ∈ Z⁴ : Σα_i even}` (b = 3, residues (2,2,2,2)), box `q = (1,1,1,1)`.** `F` = the six vectors of weight 2 (vertices of a regular octahedron in the hyperplane `Σx = 2`) and `(1,1,1,1)`. The Graver moves in the box are `e_i ± e_j`. The 2-cells are the three *equatorial squares* of the octahedron (one for each pair of antipodal axes), e.g. `P((0,0,1,1); e₂−e₃, e₁−e₄)`. Any two of them meet exactly along the common axis, a segment through the centre which is a *diagonal* of both squares and not an edge of the complex (`(1,1,−1,−1)` is not Graver). So there are exactly **3 witnesses**, each a pair of 2-cells with `d_intersection = 1`, hence **`d_span = 3`**, `d_support = 4`; their faces form no non-face pair, so each witness is irreducible. All four coordinate restrictions `q_i := 0` are embedded, and every smaller box is embedded: `(1,1,1,1)` is a minimal, essential obstruction box, and **no witness has `d_span ≤ 2`**. Verified by two enumerations of the witnesses (cells route, template route) and by the exact LP audit; certificate `output/certificates/witness_certificates.json`.

**13 further lattice classes** (k = 4, census of §5):

| `b` | residues | orders | box | witnesses | `d_span` / support | mechanism |
|---|---|---|---|---|---|---|
| 3 | (2,2,2,2) | (2,2,2,2) | (1,1,1,1) | 3 | 3 / 4 | octahedron: two squares meet along a diagonal |
| 5 | (2,2,2,3) | (4,4,4,4) | (1,1,1,2) | 3 | 3 / 4 | same |
| 5 | (2,4,4,4) | (4,2,2,2) | (2,1,1,1) | 3 | 3 / 4 | same |
| 7 | (2,2,2,4) | (3,3,3,3) | (1,1,1,2) | 3 | 3 / 4 | same |
| 7 | (2,2,3,4) | (3,3,6,3) | (1,1,2,2) | 3 | 3 / 4 | same |
| 7 | (3,3,3,5) | (6,6,6,6) | (1,1,1,2) | 3 | 3 / 4 | same |
| 11 | (3,3,3,4) | (5,5,5,5) | (1,1,1,2) | 3 | 3 / 4 | same |
| 11 | (3,3,4,5) | (5,5,5,5) | (1,1,2,2) | 3 | 3 / 4 | same |
| 15 | (2,4,4,7) | (4,2,2,4) | (2,1,1,2) | 3 | 3 / 4 | same |
| 21 | (2,4,5,16) | (6,3,6,3) | (2,1,2,2) | 3 | 3 / 4 | same |
| 21 | (2,5,16,19) | (6,6,3,6) | (2,2,2,2) | 3 | 3 / 4 | same |
| 24 | (5,7,11,13) | (2,2,2,2) | (2,2,2,2) | 9 | 3 / 3 | lattice point at the centre of a 3-cube cell lifted off the origin |
| 40 | (3,7,9,13) | (4,4,2,4) | (2,2,1,2) | 3 | 3 / 4 | octahedron |
| 40 | (3,7,13,33) | (4,4,4,4) | (2,2,2,2) | 3 | 3 / 4 | octahedron |

(all 14: every witness of the box has `d_span = 3`; all predecessors embedded; the first 10 rows were additionally cross-checked by the independent template route (`output/data/crosscheck_span3.jsonl`, 10/10 equal); the template route for the remaining 4 rows did not finish in the time budget and is **UNAVAILABLE**, not passed — those 4 rest on the cells route + exact LP audit.) The remaining 441 non-direct `k = 4` classes of the census and all 221 `k = 3` classes have a witness with `d_span = 2` in every minimal box. Hence the *weak* conjecture is false, but the failures are rare (14/455) and have a clean structure.

**Corrected conjecture G5-C3′ [OPEN].** *For every `k` and every minimal obstruction box some witness has `d_span ≤ 3`.* Evidence: all 919 minimal boxes of the census (k = 3: 239 boxes, all with a witness of `d_span = 2`; k = 4: 680 boxes, minimum `d_span ∈ {2,3}`). The maximal `d_span` over *all* witnesses of a minimal box is 4. No claim is made for `k ≥ 5`.

## 4. Support dimension versus span dimension; irreducible witnesses

The pair (min support, min span) takes the values (2,2), (3,2), (4,2), (3,3), (4,3) over the minimal obstruction boxes of the census (`figures/v5_fig6_support_vs_span.png`):

| family | boxes | `(d_support, d_span)` | essential? |
|---|---|---|---|
| Klein-four `(a,b,ab)`, `b = 8, (3,5,7)` | 9 (perms of (1,1,4),(1,2,3)) | (3,2) | all 9 |
| Klein-four `(a,a,b)`, `b = 8, (3,3,5)` | 7: (1,4,0),(2,3,0),(3,2,0),(4,1,0),(1,3,2),(3,1,2),(2,2,2) | (2,2) | the last 3 (support 2, **three** coordinates needed) |
| parity `n = 3`, `b = 3` | 9 within bound 3 | (3,2) for (1,1,2)-type; (2,2) for the 2D ones | (1,1,2)-type |
| parity `n = 4`, `b = 3` | 25 within bound 3 | (3,2) ×12, (2,2) ×12, **(4,3) ×1 = (1,1,1,1)** | only (1,1,1,1) |
| `b = 24, (5,7,13,23)` (all coordinates of equal parity) | 16: the 12 permutations of (3,2,1,1) and the 4 of (4,1,1,1) | **(4,2)** — one witness, an edge inside a 2-cell, using all four coordinates | all 16 |

* **Answer to the v004 question** — *can an obstruction require four independent arithmetic coordinates while its intersecting cells lie in an affine 2-plane?* **Yes**: the sixteen `b = 24` boxes have a single witness (O-D: a Graver edge that is a chord of a 2-cell) with `d_span = 2` and `d_support = 4`, and the box is essential (every 3-coordinate restriction is embedded). Conversely **the converse also happens**: span 3 with support 4 (parity `(1,1,1,1)`) and support 3 with span 3 (`b = 24, (5,7,11,13)`, box `(2,2,2,2)`).
* **Lifting lemma [PROVED].** Let `T` be a witness realized at base `u` in box `m`, `S = supp(T)`. All corners have the same coordinate `u_i` for `i ∉ S`. If the configuration can be realized with `u_i = 0` for all `i ∉ S` then `T` is already realized in the box with `m_i = 0` for `i ∉ S`. Hence in a minimal box, `m_i > 0` for some `i ∉ S` only if every realization has `u_i > 0` for some such `i`, i.e. the `S`-projection of the configuration touches the excluded origin (a corner with all `S`-coordinates 0) or lattice membership forces it. This is the *origin-avoidance lift*; it is the mechanism of the (2,2)-essential Klein-four `(a,a,b)` boxes and of `b = 24, (5,7,11,13)` (the 3-cube `[0,2]³` has a corner at the origin; the cell is lifted by `(0,0,0,2)` because `(0,0,0,1) ∉ Λ`). So *essential coordinate* ≠ *support coordinate*, and the support dimension of an obstruction is not a topological invariant of the lattice alone.
* **G5-C4 is false.** Definition: a witness `(c₁,c₂)` is *irreducible* if no other pair of faces `(f₁ ≤ c₁, f₂ ≤ c₂)` is itself a witness (decided inside the complete witness list of the box; `theory/witness_dimension.py::irreducibility`). Irreducible witnesses with `d_span = 3` exist at the minimal box above (3 of 3 witnesses), and with **`d_span = 4`** in `Λ_5 = {Σα_i even} ⊂ Z⁵` at `(1,1,1,1,1)` (90 witnesses, all irreducible: 75 with `d_span = 3`, 15 with `d_span = 4`, all pairs of 2-cells, support 4) and in `Λ_4` at `(2,2,2,2)` (6169 irreducible of 32 743 witnesses: `d_span` 2/3/4 = 107/1298/4764) — `output/data/irreducible_stats.json`, `figures/v5_fig7_irreducible_spans.png`. Planarity is not a property of irreducible witnesses.

## 5. Bounded census (reproducible `k = 3, 4` search)

`experiments/span_two_search.py`: all non-direct classes `Λ = ker(Z^k → (Z/b)^×)` up to coordinate permutation with `b ≤ 48`, orders `≤ 8` (k = 3, bound 3) / `≤ 6` (k = 4, bound 2). Minimal boxes are located with the independent LP audit; every minimal box gets its complete witness table.
* `k = 3`: 221 classes, 239 minimal boxes. `(min d_support, min d_span)`: (3,2) ×196, (2,2) ×43; essential (3,2) ×196, (2,2) ×10 (206 essential). **No box has `min d_span ≥ 3`**; 3 boxes contain some witness of span 3 (max span 3). 0 UNAVAILABLE.
* `k = 4`: 455 classes, 680 minimal boxes. `(min d_support, min d_span)`: (3,2) ×449, (4,2) ×178, (2,2) ×39, **(4,3) ×13, (3,3) ×1**; essential: 325 of the 680 (by type (4,3) ×13, (3,2) ×114, (4,2) ×178, (2,2) ×19, (3,3) ×1). Max `d_span` over all witnesses of a box: 2 in 578 boxes, 3 in 90, 4 in 12. 0 UNAVAILABLE; 14 classes with `min d_span ≥ 3`.
This is a *bounded* census, complete inside the stated scope; it is **not** the unrestricted `k = 4` atlas, which stays **UNAVAILABLE**.

## 6. G5-T6 — effective certificates  [PROVED+CHECKED]

A certificate `(res,b,q,u,A,v,B,t,l)` (`theory/certificates.py`) lists two cells and rationals `t_i, l_j ∈ (0,1)` with `u + Σ t_i g_i = v + Σ l_j h_j`. Verification needs only: membership `∏ r_i^{α_i} ≡ 1 (b)`; box/origin conditions on the `2^r + 2^s` corners; a brute-force Graver test of each generator; independence by rank over `Q`; distinctness of the cells; exact rational equality. If it passes, `K_abs(Λ,q)` is not embedded (T-REL), and `d_span`, `d_support`, `d_intersection` are read off. `output/certificates/witness_certificates.json` holds all 48 witnesses of the 14 refuting boxes (with predecessor-embeddedness flags from the exact audit) and one minimum-span witness of each of 32 essential boxes of the mandatory families; all are re-verified in `verify.py`. Negative tests (tampered box, coefficient 1, non-Graver generator) are rejected.

## 7. Mandatory families — summary

Klein-four (both types), parity `n = 3, 4` (and 5 at `(1^5)`), `b = 24` reproducing `(3,2,1,1)` and `(4,1,1,1)` with all 16 permutations, the non-direct 4-coordinate classes (455) and the 14 refuting lattices: see tables above and `output/data/four_dimensional_families.json`.

## 8. Reproduction
```
python experiments/atlas_families.py 40 8 out.json         # T3/T4 proof ingredients
python experiments/four_dimensional.py out.json            # mandatory families (witness tables)
python experiments/span_two_search.py K BMAX BOUND out.jsonl [ORDMAX]
python experiments/irreducible_stats.py out.json
python experiments/make_certificates.py out.json
python verify.py [--smoke]
```
