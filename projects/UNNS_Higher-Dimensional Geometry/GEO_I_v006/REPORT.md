# GEO-I v006 — Report

Labels: **PROVED**, **PROVED+CHECKED**, **CHECKED**, **FALSE**, **OPEN**, **CORRECTED**, **UNAVAILABLE**.

## 1. Gates

| Gate | Result |
|---|---|
| G1 v005 regressions (80 witness certificates, 4D parity (1,1,1,1) min span 3, 5D parity, b=24 (5,7,13,23) planar witness, s = ±1 theorems, d ≤ 21 certificates) | **PASS** — the unmodified v005 verifier runs inside v006 (`regression_v005.py`; smoke 52/52, full full 52/52) |
| G2 stabilization beyond 21 | **PASS (CHECKED)** — complete windows for d = 22..30 (83 unit classes, 190,597 boxes, 0 unresolved); not claimed for d > 30 |
| G3 general-s theorem / counterexample | **no theorem for all d; no counterexample.** Result recorded as CHECKED with an explicit, partly unproved covering family (STABILIZATION.md §3) |
| G4 hollow box | **CHECKED** (exact two-triangle structure, d ≤ 45; β₁ = 2, d ≤ 20); boundary lemma PROVED |
| G5 obstruction rank | G6-C3 **OPEN**; exhaustive binary 0/1 census n ≤ 6, partial n = 7, 8: all minimum spans 3 |
| G6 certification | finite reduction + explicit covers + centre criterion; complexity measured (CERTIFICATION.md) |
| G7 independent verification | two paths per claim (MATHEMATICS.md §4); 0/1 engine vs v005 engine: 180 + 15 lattices and parity 4/5/6, **0 mismatches** |
| G8 clean-unzip smoke and full | **PASS** — clean unzip into an empty folder: `verify.py --smoke` 20/20 core checks (2 min), `verify.py` 25/25 (6.5 min); each includes the inherited v005 regression suite (52/52). Python 3.10, no sibling releases present |
| G9 preservation | v001–v005, SELECT, FIELD, Foundations untouched; frozen libraries and inherited modules hash-checked; no remote GitHub access or modification |

## 2. Programme A in one paragraph
Lemma S4 (v004) reduces every box to a finite window; thick/thin boxes are covered by an explicit cell list, small boxes by a sufficient-family test with the v005 generic test as a fallback. The covering was verified exactly, box by box, for every unit class with `d ≤ 30`. The expected hand proof for all `(d,s)` — controlling the four corner sails through the continued fraction of `s/d` — is not complete; the claim stays CHECKED/OPEN, not PROVED.

## 3. Programme B in one paragraph
For binary relation lattices the 0/1 box is governed by the circuits of a binary matroid: cells are disjoint-circuit parallelotopes and two cells fail to meet in a common face iff they share a centre (PROVED). Enumerating all binary column multisets found 1, 3, 50 minimal boxes for n = 4, 5, 6 (complete), 2983 for n = 7 (code dimension ≥ 3) and 7 for n = 8 (code dimension ≥ 5), all with minimum witness span 3. For parity lattices the *individual* witness spans reach 4 (n = 5), 6 (n = 6): this separates the minimum from the maximum span and does not refute G6-C3.

## 4. Failed or false sub-hypotheses (recorded)
* **HYP-LL** (every step of the corner sail has a valid completion among `(0,d),(d,0),mᵢ,m_{i+1}`) — **FALSE** for boxes with `r₁ = 0` or `r₂ = 0`; other cell types are needed there. This is why small boxes use the broader family and the generic fallback. The failure does not falsify G6-C1.
* The small-box family test is only a *sufficient* test: at the hollow box it leaves more uncovered area than the true holes, and the generic test must be used to read off the exact holes.
* My first witness count for parity 6 (1710) counted cell pairs, not witnesses up to translation (1440 = v005); fixed by reporting both (`n_cell_pairs`, `n_witnesses`).

## 5. UNAVAILABLE / not done
* d > 30 for the complete window; the extended random-audit run stopped at d = 36 (target 70).
* Exhaustive non-binary or mixed-modulus search at k = 5, 6 (v005 engine too slow); binary n = 7 with code dimension ≤ 2 and n = 8 with code dimension ≤ 4.
* Any proof of G6-C3; a general arithmetic certificate (G6-C4).
* GitHub was not accessed (not needed).
* Independent external proof certification and equivalence-based literature review (PRIOR_ART.md).

## 6. Suggested next steps
(1) Prove the sail-cover lemma by induction on the Euclidean algorithm of `(d,s)`; (2) extend the window run to d = 31..40 (~minutes per class); (3) for G6-C3, a structure theorem for binary matroids: does every minimal 0/1 box contain a centre with three cells whose generators span rank 3? (4) lattices of exponent 3 / mixed modulus with the fast centre-type criterion.
