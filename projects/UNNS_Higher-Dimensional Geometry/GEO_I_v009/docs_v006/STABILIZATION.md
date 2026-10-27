# GEO-I v006 — Programme A: uniform stabilization for every unit s (G6-C1, G6-C2)

Labels: **PROVED**, **PROVED+CHECKED**, **CHECKED** (exact finite computation, not a proof for all parameters), **FALSE**, **OPEN**, **CORRECTED**, **UNAVAILABLE**.
Frozen conventions (v004/v005, unchanged): `Γ_(d,s) = {(i,j) ∈ Z² : j ≡ s·i (mod d)}`, `gcd(s,d)=1`, `t = s⁻¹ mod d`; box `Q = (Q1,Q2) ≥ (d,d)`; `F = (Γ ∩ [0,Q]) ∖ {0}`; Graver vectors = conformally minimal vectors of `Γ`; cells = points, segments, parallelograms `P(u;g,h)` with independent Graver `g,h` and all four corners in `F`; `U` = union of the cells; `H = conv(F)`; always `U ⊆ H`. Transposition `(d,s,Q) ↦ (d,t,Qᵀ)` is a symmetry, so only `s ≤ t` is run.

## 0. Status table

| ID | Statement | Status |
|---|---|---|
| G5-C1 (s = ±1) | `U = conv(F)`, all `d`, all `Q ≥ (d,d)`, `Q ≠ (d,d)` | **PROVED+CHECKED** (v005, inherited, regression-tested) |
| **G6-C1** (all units) | `U = conv(F)` for every unit `s`, all `Q ≥ (d,d)`, `Q ≠ (d,d)` | **CHECKED for every (d,s) with 2 ≤ d ≤ 30** (complete base window, exact) — **OPEN** for `d > 30`. No counterexample. Not proved for all `d` |
| G6-C1-thick/thin | the same for boxes with `max(Q1,Q2) ≥ 2d` | an explicit cell family (squares + corner sails + chain cells, §2) covers `conv(F)` exactly in every instance run: **CHECKED** (3021 boxes of 9 types completely; every window box for every `d ≤ 30`; random audits for 15 ≤ d ≤ 36). A written proof of the covering step for all `(d,s)` is **not** claimed (§3) |
| G6-C1-small | the `d²−1` boxes `Q = (d+r₁,d+r₂)`, `Q ≠ (d,d)` | **CHECKED** by the sufficient-family test (§4) for every `(d,s)` with `d ≤ 30`, and for `15 ≤ d ≤ 36` in the extended run; **OPEN** in general |
| **G6-C2** (hollow box, s ≢ −1) | `β₁(U_(d,d)) = 2`, `d ≥ 3` | `conv(F)∖U = int T₁ ∪ int T₂` with `T₁ = tri((0,d),(d−t,d−1),(d,d))`, `T₂ = tri((d,0),(d−1,d−s),(d,d))`, total area `d`: **CHECKED** (exact) for every unit `s ≢ −1`, `3 ≤ d ≤ 45`; `β₁ = 2` from the full chain complex: **CHECKED** for `d ≤ 20`. The boundary `∂Tᵢ ⊂ U` is **PROVED** (§5), hence `β₁ ≥ 2` follows from `int Tᵢ ∩ U = ∅` (CHECKED) |
| G5-C2 (s = −1, s = +1) | `β₁ = d`, resp. `2` (d ≥ 3) | **PROVED+CHECKED** (v005, inherited) |
| Stabilization search beyond 21 | `d = 22..30` | see §6 |

## 1. Reduction to a finite window

**Lemma S4 (v004, PROVED, inherited; re-checked in the regression suite).** If `Q1 ≥ 2d` every lattice row of the box contains ≥ 2 fibre points, so a translation by `(d,0)` (resp. `(0,d)`) identifies the box with a smaller one and `U = H` for `Q` follows from `U = H` for the base window `[d,3d−1]² ∖ {(d,d)}`. Therefore **`U = conv(F)` for all `Q ≠ (d,d)` holds for a given `(d,s)` iff it holds on the window** — a finite check of `(2d)² − 1` boxes (≈ half after transposition symmetry when `s = t`).

Within the window we distinguish
* *thick*: `Q1,Q2 ≥ 2d`; *thin*: exactly one of `Q1,Q2` in `[d,2d)`; *small*: both in `[d,2d)`, `Q = (d+r₁,d+r₂)`.

## 2. The cell families (`theory/modular_layers.py`)

For a box `Q` the following cells are built **by explicit rules**, each checked to be a legitimate cell (corners in `F`, generators in the Graver set computed by brute force, independent) and then the exact union is compared with `H` by rational polygon clipping.

1. **Squares** `P(u;(d,0),(0,d))`, `u ∈ Γ∖0`, `u + (d,d) ≤ Q`. (`(d,0),(0,d)` are Graver for every `s`; all corners are in `Γ` and nonzero since `u ≠ 0`.)
2. **Corner sails.** At each of the four corners of the box take the fibre points that are Pareto-minimal for the corner's coordinates `m₀,…,m_k` (the Hilbert basis of the corner coset quadrant), ordered along the sail. *Lemma P (argument, instances verified):* (a) every Pareto-minimal point lies on the sail (a Pareto-minimal point strictly inside the sail would give, by reflection through the midpoint of two neighbours, a smaller Pareto point); (b) consecutive differences `gᵢ = m_{i+1} − mᵢ` are Graver and `(mᵢ, m_{i+1})` is a lattice basis of `Γ` (`det = d`). The cell `P(mᵢ; gᵢ, completion)`, completion `(0,±d)`, covers the staircase triangle between the sail and the Pareto staircase.
3. **Chain cells (thin boxes, `Q1 < 2d`).** `P(Bₖ; B_{k+1}−Bₖ, (0,d))` over the lowest points `Bₖ` of the columns `x = k`, and the analogous cells below the highest points; the generators `(1,s)`, `(1,s−d)` are Graver (column bridges); for `Q2 < 2d` the transposed construction with row bridges `(t,1)`, `(t−d,1)`.

Machine check: `modular_layers.verify_box` on all 3021 boxes `d ≤ Q ≤ 3d` with `max ≥ 2d` of the types `(5,2),(7,2),(7,3),(8,3),(9,2),(11,3),(11,4),(13,5),(10,3)`: 0 failures; every window box of every class with `d ≤ 30` (`output/data/window_full_*.jsonl`, `via_proof_cells`).

## 3. What is and is not proved for thick/thin boxes

**Proved in this document:** the legitimacy of the squares (item 1) and of the column/row bridges (item 3: `(1,s)` and `(1,s−d)` are the only vectors of their sign pattern with first coordinate 1 and second coordinate `≤ d` in absolute value, so no smaller vector of `Γ` is conformally below them); Lemma P(b) for adjacent Pareto points (two lattice points spanning a parallelogram with no further lattice point of the quadrant below the sail have `det = d`, because the area of a fundamental domain of `Γ` is `d`).

**Not proved:** that squares ∪ sails ∪ chains cover `H` for *all* `(d,s,Q)`. The heuristic reason is that every point of `H` at distance ≥ `d` from the box boundary lies in a square (a `d×d` window of integers contains exactly `d` points of `Γ`), and the boundary strips are tiled by sail cells whose completion `(0,±d)` fits in the box when `max(Q) ≥ 2d`; the fit condition is `a·b ≤ a·h_y + b·h_x`. The *fit condition for every sail step* fails for `Q` with a coordinate equal to `d` (see `HYP-LL` in `REPORT.md` §4: false when `r₁ = 0` or `r₂ = 0`), which is why the small boxes need their own family. A rigorous all-parameter proof requires controlling the continued-fraction pattern of `s/d` along each of the four sails; **we do not have it**. The claim is therefore **CHECKED**, window by window.

## 4. Small boxes (`theory/small_boxes.py`)

`family(d,s,Q)` = squares + sail cells with completions `(0,d)` and `(d,0)` at all four corners (using *all* Pareto points `m_j`) + chain cells in both directions, filtered by `legit`. `certify_box` accepts a box if the exact union of the *true cells in the family* covers `H` (**sufficient-family certificate**: any subfamily of true cells covering `H` proves `U = H`); otherwise it falls back to the full v005 test `coverage.uncovered(Lat(d,d,d,s), Q)`. Soundness check: at the hollow box `Q = (d,d)` the family leaves positive uncovered area and the generic test gives exactly `d`.

Results: `d ≤ 14` all classes (general_s_d2_14.jsonl); `15 ≤ d ≤ 36` (general_s_d15_70.jsonl; the run was stopped at `d = 36`, **70 was not reached: UNAVAILABLE**); complete windows `22 ≤ d ≤ 30` (window_full_d22_30_s*.jsonl). The fallback was needed in 37 (of 143,228 small boxes in the 15 ≤ d ≤ 37 run; 0 of the 47,769 small and 142,828 thick/thin window boxes for 22 ≤ d ≤ 30) boxes.

## 5. The hollow box `Q = (d,d)`, `s ≢ −1`

Let `t = s⁻¹`. `F ∩ [0,d]²` consists of the points of `Γ` in the closed square without the origin; the corner points `(0,d),(d,0),(d,d)` are always present.

**Lemma H1 (PROVED).** For `s ≢ −1` and `d ≥ 3`, the three sides of `T₁ = tri((0,d),(d−t,d−1),(d,d))` are Graver segments between points of `F` (vectors `(d−t,−1)`, `(t,1)`, `(d,0)`), hence lie in `U`; likewise for `T₂ = tri((d,0),(d−1,d−s),(d,d))` with `(−1,d−s)`, `(1,s)`, `(0,d)`. *Proof.* `(d−t,−1)`: `−1 − s(d−t) ≡ −1 + st ≡ 0 (mod d)`; it is conformally minimal since the only vector of `Γ` with sign pattern `(+,−)` and `|second| ≤ 1`, `|first| ≤ d−t` is itself. The same computation gives the others. ∎ Each triangle has area `d/2` (`det((d−t,−1),(d,0)) = d`), and `z ↦ (d,d) − z` swaps `T₁` and `T₂`.

**Theorem H2 (CHECKED).** `conv(F)∖U = int T₁ ∪ int T₂` (area `d`) for every unit `s ≢ −1`, `3 ≤ d ≤ 45`, `β₁(U) = 2` for `d ≤ 20`. Method: exact uncovered region of the v005 test, compared with the triangles by exact polygon clipping (`experiments/hollow_check.py`, data `output/data/hollow_general_s.json`); the Betti number from the v005 planar arrangement chain complex (independent of the clipping).

**Consequence.** If `int Tᵢ ∩ U = ∅` then `Tᵢ` is a bounded component of `R²∖U` whose boundary lies in `U` (Lemma H1), so `β₁(U) ≥ 2` by Alexander duality; the upper bound `β₁ ≤ 2` is the CHECKED part. For `s ≡ −1` the structure is different (`β₁ = d`, v005, PROVED).

## 6. Beyond d = 21

v005's search stopped at `D* = 21` (2.2 h for `d = 14..21`). With the explicit certificates the complete window for `d = 22 … 30` was certified exactly (`83` unit classes, `190,597` boxes, 0 unresolved). **Result: no counterexample; `D*` is now 30 (CHECKED).** For `d > 30`: **UNAVAILABLE** (not run).
