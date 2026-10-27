# GEO-I v008 — Programme A: small-box geometry (G8-C1)

## 0. Result in one paragraph

**G8-C1 (`U = conv(F)` for every `Q = (d+u, d+v)`, `0 ≤ u,v < d`, `(u,v) ≠ (0,0)`) is still OPEN: no proof, no counterexample.** Gate G2 is therefore met **only through the substantial new infinite-family theorems G8-T1 and G8-S below and the proved reduction G8-R1**, not through a proof of G8-C1; this is stated plainly in REPORT.md. What v008 adds: (i) the exact arithmetic description of the squareless zone (a staircase under the record minima of `s·i mod d`), which explains the number 29,890 of v007 as a closed formula; (ii) the filling lemma G8-T1 (both hollow-box holes are filled by explicit Graver parallelograms as soon as the box is enlarged in either direction), which removes the topological obstruction from every small box; (iii) the proved reduction G8-R1 (hollow-box structure ⇒ the whole square hull is covered in every larger box); (iv) an exhaustive exact sweep of the small-box region: exhaustive exact sweep, every unit s and every small box for 3 ≤ d ≤ 20: 26636 boxes, all covered, 0 failures, 0 staircase mismatches.

Frozen setting (v007, unchanged): `Γ = {(i,j): j ≡ s·i (mod d)}`, `t = s⁻¹ mod d`, `F = Γ ∩ [0,Q] ∖ {0}`, cells = points, Graver segments, parallelograms `P(u;g,h)` with independent Graver `g,h` and all four corners in `F`; `U` = union of cells, `H = conv(F)`. `Γ ∩ H = F`.

## 1. Partition of the small-box region

With `a_i := s·i mod d` and `m_s(u) := min_{1≤i≤u} a_i` (`m_s(0) := d`):

| class | definition | note |
|---|---|---|
| hollow | `(u,v) = (0,0)` | excluded from G8-C1; two holes (G7-T3) |
| bottom | `v = 0, u ≥ 1` | all boundary boxes are squareless |
| left | `u = 0, v ≥ 1` | likewise |
| interior | `u,v ≥ 1` | squareless iff `v < m_s(u)` |
| corner-adjacent | `u = 1` or `v = 1` | notational only; no separate theorem |

**Extension points over the hollow box.** `R_i = (d+i, a_i)` (`1≤i≤u`, the point `P_i` shifted right by `d`), `T_j = (c_j, d+j)` (`1≤j≤v`, `c_j = t·j mod d`, the point `(c_j,j)` shifted up by `d`), and `K = (d,d) + (Γ ∩ [1,u]×[1,v])`. (`theory/small_box.py:extension_points`.)

## 2. Theorem G8-S (squareless staircase) — PROVED + CHECKED

*For `u,v ≥ 1`: `Q` is squareless (v007 definition: `Γ ∩ [0,u]×[0,v] = {0}`) iff `v < m_s(u)`; boundary boxes (`u=0` or `v=0`) are always squareless. Hence the number of squareless small boxes of type `(d,s)` is*
`N_sq(d,s) = 2(d−1) + Σ_{u=1}^{d−1} (m_s(u) − 1)`.

*Proof.* A nonzero point `(i,j) ∈ Γ` with `0≤i≤u<d`, `0≤j≤v<d` has `i ≥ 1` (if `i=0` then `d | j`, `j<d` gives `j=0`) and `j = a_i`. Such a point exists iff `min_{1≤i≤u} a_i ≤ v`. For `u = 0` the box `[0,0]×[0,v]` contains only `(0,0)` (same argument); likewise `v = 0`. Counting: for each `u ≥ 1`, `v` ranges over `1..m_s(u)−1`; plus the two boundary rays (`u=0, v=1..d−1` and `v=0, u=1..d−1`). ∎

**Explaining 29,890.** `Σ_{d=3}^{32} Σ_{s unit} N_sq(d,s) = 29,890` exactly (computed by the formula; v007 enumerated the same boxes by brute force: records `v7_sqless_*`). The squareless zone of `(d,s)` is the region below the non-increasing step function `m_s`; its corners are the record minima of `s·i mod d`, i.e. the lower-left Pareto chain of `Γ ∩ (0,∞)²` (the convergents of `s/d`). `experiments/small_attack.py` re-checks the formula against the definition on every box it sweeps (`staircase_mismatch = 0`).

## 3. Filling lemma G8-T1 — PROVED + CHECKED (proof in HOLLOW.md §2)

For every `d ≥ 3`, unit `s`, `Q ≥ (d,d)`, `Q ≠ (d,d)`: `T1 ∪ T2 ⊂ U_{d,s,Q}`. Consequently the only complement of `U_{(d,d)}` inside `H_{(d,d)}` that G7-T3 produces (the two triangles, under G8-T2) is erased by *any* enlargement, in particular in every squareless boundary box.

## 4. Reduction G8-R1 — PROVED (conditional on G8-T2 for the type)

*If `conv(F_{(d,d)}) ∖ U_{(d,d)} = int T1 ∪ int T2` (G8-T2), then `conv(F_{(d,d)}) ⊂ U_Q` for every `Q ≥ (d,d)`, `Q ≠ (d,d)`.* Cells of `U_{(d,d)}` stay cells (corners remain in `F_Q ⊃ F_{(d,d)}`; Graver sets do not depend on `Q`), and `T1 ∪ T2 ⊂ U_Q` by G8-T1. ∎ So the remaining geometric content of G8-C1 is the **cap** `conv(F_Q) ∖ conv(F_{(d,d)})`, spanned by the extension points of §1.

## 5. Local filling lemmas G8-L1…L4 — PROPOSED, not established

These are *proposals* guiding the cap problem; none is claimed.
* **G8-L1 (right ribbon).** The cells `P(P_i; (1,δ_i),(d,0))` over consecutive `i ≤ u` cover the part of the cap right of `x = d`; missing: the cell at `i = 0` needs the origin (not in `F`).
* **G8-L2 (top ribbon).** Transposed version over the `T_j`.
* **G8-L3 (corner square).** For non-squareless `Q`, `K ≠ ∅` and `(d,d)+p` supplies square cells.
* **G8-L4 (origin repair).** The `i=0` strip is replaced by the primitive triangles `B,R_1,P_1` (and transposed), which are *not* cells; their coverage by larger cells (as in G8-T1) is the missing local lemma.
v007's finding stands: 1,014 of 1,586 squareless boxes (`3 ≤ d ≤ 13`) are covered by no strip/bridge/slanted family; the generic exact routine covers them all.

## 6. Evidence (exact; every record is a certificate-quality computation, not a theorem)

* Regenerated by `experiments/small_attack.py` (exact rational polygon subtraction against *all* cells): exhaustive exact sweep, every unit s and every small box for 3 ≤ d ≤ 20: 26636 boxes, all covered, 0 failures, 0 staircase mismatches.
* Inherited ranges (not re-counted as v008 checks): `d ≤ 30` complete base-window (v006), squareless zone `d ≤ 32` (v007, 29,890 boxes).
* Independent path: certificates `C1_cover.json` (14 boxes covering all region classes) verified by the standalone `checker8.py`, which recomputes `F`, Graver sets and the subdivision itself.
* No counterexample candidate and no unresolved box.

## 7. What a counterexample would have to look like

An exact `GAP` certificate (CERTIFICATION.md): a rational `z ∈ conv(F)` lying in no Graver segment and no Graver parallelogram with corners in `F`. By G8-T1 and G8-R1 (when G8-T2 holds) such `z` would lie in the cap `conv(F_Q) ∖ conv(F_{(d,d)})`.
