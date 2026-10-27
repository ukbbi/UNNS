# GEO-I v009 — Programme A: the exact hollow-box complement (G9-C1 / G9-T1 / G9-T1H)

**Status: OPEN (A-OPEN).** No proof, no counterexample. This document records the question, the reductions that were used, the exact surveys (including the mandatory falsification attempts), and the precise reason the continued-fraction induction was not completed. A larger finite survey is *not* presented as a proof.

## 1. The statement
`Γ = {(i,j) : j ≡ s·i mod d}`, `s` a unit, `s ≢ −1`, `d ≥ 3`; `F = Γ ∩ [0,d]² \ 0`; `H0 = conv F`; `U0` = union of Graver cells with all four corners in `F`. With `t = s⁻¹`: `T1 = tri((0,d),(d−t,d−1),(d,d))`, `T2 = tri((d,0),(d−1,d−s),(d,d))` (area `d/2` each).

**G9-C1.** `H0 \ U0 = int T1 ⊔ int T2`.  **G9-T1H.** Consequently `β1(U0) = 2`. The case `s ≡ −1` is separate (`β1 = d`) and is not part of the statement.

Known: `⊇` (G7-T3). Open: `⊆`, i.e. *no additional hole*.

## 2. Reductions (elementary; no new theorem is claimed)
* **Origin-free cells.** Every cell of the complex has all corners in `F`, so none has `0` as a corner (`0 ∉ F`); a point of `H0` is in `U0` iff it lies in a parallelogram `P(u;g,h)`, `g,h` independent Graver vectors, with four corners in `F`, or on a Graver segment with endpoints in `F`.
* **Central inversion.** `p ↦ (d,d) − p` preserves `Γ ∩ [0,d]²` and exchanges `0 ↔ C`, `A ↔ B`, `P_i ↔ P_{d−i}`; cells through `C` correspond to cells through `0`.
* **Sail.** Consecutive record minima `v_k, v_{k+1}` of `s·i mod d` (`i = 0..d`) are a basis of `Γ` (`det = d`, primitive triangle with the origin); `∂H0` is the sail `A → B` plus `B → C → A`. (Plotted for Fibonacci-type, large-first-quotient and long-chain pairs in Figure 2.)
* **Gap criterion.** A counterexample to G9-C1 is an exact rational point `z ∈ H0` outside `U0 ∪ T1° ∪ T2°`, certified by a `GAP` certificate (the checker recomputes all Graver segments and parallelograms with corners in `F`). None exists in any tested case.

## 3. Why the induction was not closed
The plan was A1 (primitive boundary directions) → A2 (sail decomposition into exact rational polygons respecting the punctured origin) → A3 (an induction step with explicit invariance obligations) → A4 (no-additional-hole lemma) → A5 (`β1 = 2`). Only A1 is standard. For A2 the obstruction is quantitative: the residual convex pieces left after successive subtraction of the cells are the fragments of `T1 ∪ T2`, whose number grows with `d` (6, 10, 13, 18 for `s = 2`, `d = 7, 9, 11, 13`), and for general `s` the covering cells are not uniformly describable by the first few partial quotients. A valid induction step would have to show that the Euclid step `(d, s) → (s, d mod s)` maps the exact complement of the hollow box to that of the smaller hollow box; no such map between the *cell complexes* (as opposed to the lattices) was found, and replacing the Graver-cell complex by another triangulation is not allowed in this programme. Nothing here is a partial theorem: **A-PARTIAL was not reached.**

## 4. Mandatory falsification (CHECKED within scope — not a proof)
| Survey | scope | result |
|---|---|---|
| inherited (v006–v008) | all units `s ≠ d−1`, `d = 3..45` and `51..72` | exact complement `= T1 ∪ T2` |
| `v9_hollow_46_50.json` | all units, `d = 46..50` (closes the gap in the inherited ranges) | 141 exact pairs, 0 violations |
| `v9_hollow_attack_p0/p1.json` | `d = 73..110`, composite and prime `d`, `s` with large partial quotients (up to `54`), `s = 2..6`, `d−2..d−4`, `(d±1)/2`, `(d±1)/3`, `d/2±1`, `≈ d/k` and inverses; `853` exact pairs | no counterexample |

Method (path 1): `experiments/hollow_check.py` — v005 all-cells exact rational polygon subtraction; uncovered area (twice) must equal `2d`, and its intersection with `T1 ∪ T2` must equal all of it. Outcome labels: **no counterexample within the completed scope**; **search incomplete** outside it; **general theorem not proved**.

## 5. What would close it
(a) An explicit cell cover of `H0 \ (T1 ∪ T2)` indexed by the sail edges, with a uniform proof that the pieces glue along the punctured origin; or (b) an inductive map between consecutive Euclid levels that is compatible with the Graver parallelogram structure. `G8-R1` (proved, conditional on G9-C1) then gives full square-hull coverage for every enlarged box.
