# GEO-I v008 — Programme B: the hollow box and hole disappearance

## 0. Results

| ID | Statement | Status |
|---|---|---|
| **G8-T1** | filling lemma: for `d ≥ 3`, every unit `s`, every `Q ≥ (d,d)`, `Q ≠ (d,d)`: `T1 ∪ T2 ⊂ U_{d,s,Q}` | **PROVED+CHECKED** (all units, `3≤d≤60` machine check of the explicit cells; independent exact leftover routine on test boxes) |
| **G8-K1** | corollary: both G7-T3 holes die at the first enlargement (`Q = (d,d+1)` or `(d+1,d)`) | **PROVED+CHECKED** |
| G8-T2 | `conv(F_{(d,d)}) ∖ U_{(d,d)} = int T1 ⊔ int T2` for `s ≢ −1` | **OPEN** in general; CHECKED `3≤d≤72` (v007 `3..50`, v008 `51..72`: 792 more unit classes, 0 violations) |
| G8-C2 | `β1(U_{(d,d)}) = 2` for `s ≢ −1` | **OPEN** in general (implied by G8-T2 + Alexander duality); CHECKED (Betti numbers `d ≤ 20`, inherited) |
| G8-T4 | hole-disappearance index along `Q=(d,h)`: first `h` with `T1,T2 ⊂ U` is `d+1` (G8-T1); first `h` with `β1 = 0` computed in `output/data/v8_hole_death.json` | G8-T1 part PROVED; `β1` part CHECKED on the shipped range |
| forced change (v007 corollary) | `β1 ≥ 2` at `h=d`, `β1 = 0` at `h=2d` ⇒ a drop occurs | PROVED (from G7-T1, G7-T3) — v008 sharpens: the drop of the two enclosed components happens at the *first* step |

## 1. Notation (v007, frozen)

`A=(0,d)`, `B=(d,0)`, `C=(d,d)`, `P_i=(i, s·i mod d)`. `T1 = tri(A, P_{d−t}, C)`, `T2 = tri(B, P_{d−1}, C)`, `P_{d−t} = (d−t, d−1)` (because `s(d−t) ≡ −1`), `P_{d−1} = (d−1, d−s)`; each has area `d/2`. G7-T3: `int T1, int T2` are disjoint from `U_{(d,d)}` with boundaries in `U`.

## 2. Proof of the filling lemma G8-T1

**Case `Q2 ≥ d+1`.** Put
* `R1 = P(A; (d−t,−1), (t,1))` with corners `A, P_{d−t}, (t,d+1), C` (`(t,d+1) = A + C − P_{d−t}`);
* `R2 = P((t,1); (0,d), (d−t,−1))` with corners `(t,1), (t,d+1), B, C`.

*Corners lie in `F`.* `s·t ≡ 1`, so `(t,1)` and `(t,d+1)` are in `Γ`; `s(d−t) ≡ −1`, so `P_{d−t} = (d−t,d−1) ∈ Γ`; all coordinates are within `[0,d]×[0,d+1] ⊂ [0,Q]`; none is `0`.
*Generators are Graver.* `(0,d)`: the vertical lattice vectors are the multiples of `(0,d)`. `(t,1)`: a lattice vector `(a,b)` with `0≤a≤t`, `0≤b≤1` is `(0,0)` or `(t,1)` (`b=0` forces `d|a`, `a<d`; `b=1` forces `a≡t`, `a≤t<d`). `(d−t,−1)`: identical argument with `b=−1`, `a≡−t`. *Independence.* `det((d−t,−1),(t,1)) = d`, `det((0,d),(d−t,−1)) = −d(d−t) ≠ 0` (`1 ≤ t ≤ d−1`).
*Containment.* `T1` has three of the four corners of `R1`, so `T1 ⊂ R1`. For `T2`: `B, C` are corners of `R2`; at `x = d−1` the parallelogram `R2` occupies `1/(d−t) ≤ y ≤ d + 1/(d−t)` (lower edge `(t,1)→B`, upper edge `(t,d+1)→C`), and `1/(d−t) ≤ 1 ≤ d−s ≤ d−1`, so `P_{d−1} = (d−1,d−s) ∈ R2`; by convexity `T2 = conv(B,C,P_{d−1}) ⊂ R2`.

**Case `Q1 ≥ d+1`.** Transposition `(i,j) ↦ (j,i)` maps `Γ_{d,s}` onto `Γ_{d,t}`, boxes to transposed boxes, Graver elements to Graver elements, cells to cells, and `T1(s) ↔ T2(t)`, `T2(s) ↔ T1(t)`. Apply the first case to `(d,t,Q^T)`. ∎

`theory/hollow.py:check_filling` verifies, in exact integers, for every `(d,s)` that the four cells (`R1,R2` and their transposes) have corners in `F` of the minimal enlarged box, Graver independent generators, and contain the vertices of the target triangle; run for all units `3 ≤ d ≤ 60` in the unit tests (and `3 ≤ d ≤ 150` in `verify.py` full). A second, independent path (`coverage.uncovered`, the v005 exact polygon-subtraction routine over *all* cells) shows the leftover of `H` is empty at `Q = (d,d+1), (d+1,d)` for the test types, including `s = −1` (`figures/fig5_hole_filling.png`).

## 3. Why this is not yet G8-C2/G8-T2

G8-T1 says the two *known* complement components are filled. G8-T2 asserts that these are the *only* complement of `U_{(d,d)}` in the hull; its proof needs the cell structure of the whole hollow box (no proof found; a continued-fraction induction on `(d,s)` is the natural route and was not completed). Approaches B1–B4 of the specification:
* **B1 (complement components):** reduces to showing that every point of `H ∖ (T1∪T2)` lies in a cell; the v007 certificate covers only the lower bound.
* **B2 (boundary chains):** `∂T1, ∂T2` are cycles of Graver edges (G7-T3) — used.
* **B3 (nerve/retraction):** not carried out.
* **B4 (small-box filling):** this is G8-T1 + G8-R1: if G8-T2 holds, `conv(F_{(d,d)}) ⊂ U_Q` for all larger `Q`.
`s = −1` is different: `β1 = d` (v005 Theorem H1, inherited) and the fan of Graver segments through the hull is not captured by two triangles; G8-T1 still holds for it (all units).

## 4. Hole-disappearance index (experiments/hole_death.py)

`hole_death.py` computes exact `β1(U_{(d,h)})` and the exact uncovered area of `conv(F)∖U` for `h = d..2d`, without assuming monotonicity, recording every increase. Shipped data (`output/data/v8_hole_death.json`, 40 unit classes, 3 ≤ d ≤ 11): β1 at h=d is d for s=−1 and 2 otherwise; **β1 = 0 and the uncovered area is 0 at every h ≥ d+1** (h_first_drop = h_zero = h_stay0 = d+1 in all 40 classes); **no increase of β1 occurs anywhere** in the window. This is CHECKED on the shipped range, not a theorem (G8-T4, β1 part).

## 5. Forced topological change, sharpened

From G7-T1 and G7-T3: along `Q=(d,h)`, `β1 ≥ 2` at `h=d` and `β1 = 0` at `h=2d`. G8-T1 locates the death of the two enclosed components exactly at `h = d+1`. Whether *additional* cycles (e.g. for `s=−1`, with `β1=d`) also die at `h=d+1` is part of the computed data, not a theorem (G8-T4 for `β1`).
