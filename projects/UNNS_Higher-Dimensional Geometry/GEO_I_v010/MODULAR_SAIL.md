# GEO-I v010 — Programme A: the modular sail (G10-L1, G10-L2, G10-Z, G10-S1/S2)

**Result.** The hollow box `Q = (d,d)`, `d ≥ 5`, unit `s`, `2 ≤ s ≤ d−2`: the polygon `H0 = conv F` is covered by `T1 ∪ T2 ∪` Graver cells with all four corners in `F`. The cover is the zonogon on the steps of the lower-left hull chain of `F` plus one extra cell `K = P((d−t−1, d−s−1); (1,s), (t,1))`. Proof: `MATHEMATICS.md` §2 (Lemmas 1–4). It is not a Euclid-algorithm induction: the quantity that carries the proof is the *hull chain* (its first step is `(1, s−d)`, its last `(d−t, −1)`, steps are Graver, slopes monotone).

## Statements
* **G10-L1 (PROVED).** Consecutive F-points on the lower-left hull chain differ by Graver vectors; their zonogon is tiled by Graver cells with corners in `F`.
* **G10-Z (PROVED+CHECKED).** `H0 ⊆ Z ∪ T1 ∪ T2 ∪ K`. Exact check: every unit pair `5 ≤ d ≤ 150` (6560 pairs, max 127 cells, max 75 chain steps), 0 failures; v005/v009 engine agreement `d ≤ 32` (262 pairs).
* **G10-S1 (`d = sm+1`)**: cells `P((km, d−k); (1, s−d), (m, −1))`, `k = 0..s−1` and `K`. **G10-S2 (`d = sM−1`, `t = M`)**: four cells (three faces of the hexagon `A + [0,1](1,s−d) + [0,1](M−1,1−s) + [0,1](d−M,−1)`, and `K`). Direct or transposed (`s ↔ t`); 1276 pairs `d ≤ 150`. They are the closed forms of G10-Z for those arithmetic types.
* **G10-L2 (negative record).** Candidate Euclidean cell-transfer rules tested on the actual Graver cells of the frozen engine (`experiments/sail_attack.py`, 100 pairs `d ≤ 18`): R-SYM (transposition) holds; **R-MIR** (`|cells(d,s)| = |cells(d,d−s)|), **R-EUC** (naive one-step Euclid transfer of cell counts), **R-LAT** (generator sets map under the Euclid unimodular map) are **FALSE**; counterexamples are kept in `output/data/v10_sail_attack.json` (first: R-MIR at `(7,2)`; R-LAT at `(4,3)`).

## Files
`theory/modular_sail.py` (exact arithmetic), `experiments/sail_families.py`, `experiments/sail_attack.py`, `certificates/C8_boundary.json` (453 BOUNDARY certificates), `figures/fig7_transfer_rules.png`, `figures/fig8_sail_covers.png`.
