# SCR manuscript supplement record (v001): single-flip analysis and perturbation-bound inputs

**Status:** ADDITIVE, exact-arithmetic computation on frozen data. Not a Lean result. Not an optimization: nothing is minimized or enumerated over 2^40. No frozen file, verdict, prediction or certificate is changed. Reads only `GAP4_v010/output/real_4x4.txt` (sha256 `3d47ed1256da7620292a5fe4c64e0bc226b9836768ac87df0ff4fdbf91c5f7a2`) and `GAP4_v010/physical_energy_v005.py`.

## A. Single-island reversals of the certified ground witness (id 711243241830)
Couplings are used as exact dyadic rationals (the Lean encoding, kShift = 70). Every single flip leaves the grammar.
| Class | Islands | Gap above ground | Count |
|---|---|---|---|
| touches 1 constrained vertex, corner vertex | 6, 35, 39, 25, 36, 32, 30, 31 | 0.94592 kBT (8 values within 8562/2^70 = 7.1e-16 of the gap) | 8 |
| touches 1 constrained vertex, non-corner | 38, 14, 27, 34, 33, 37, 22, 29 | 1.04889 kBT | 8 |
| touches 2 constrained vertices | 24 islands | 1.78944 to 1.90986 kBT (4 / 8 / 4 / 8 at 1.78944 / 1.81136 / 1.88774 / 1.90986) | 24 |
- Island 6 gives exactly the certified gap numerator 12095447728404694790/2^70 A (id 711243241766).
- Island 39 gives id 161487427942, the frozen excluded value; it lies 928/2^70 A above island 6, exactly the certified correction. Island 35 lies 708/2^70 A above island 6.
- Decomposition of the energy cost of reversing island i: sum over partners j of -2 s_i s_j K_ij (exact). Island 6, in kBT: r = 0.707a (2 partners) +1.1746; r = a (2) -0.1911; r = 1.414a (1) +0.0192; r = 1.581a (3) -0.0873; r = 2a (2) +0.0176; all pairs beyond 2a, net +0.0129; total 0.9459. The lowest two-vertex island (island 2): r = 0.707a (4) +2.3492 (exactly twice island 6's nearest shell); r = a (3) -0.4942; r = 1.414a (2) +0.0383; r = 1.581a (6) -0.1745; r = 2a (3) +0.0505; beyond 2a net +0.0202; total 1.7894.
- Limits: single flips of one ground state only. The certificate fixes the global minimum of all excluded states; it does not give the minimum over excluded states whose violations are confined to a chosen vertex class. Whether the eight lowest values are symmetry-related in the ideal geometry (and split only by binary64 rounding of the couplings) is suggested by their 7e-16 spread but not verified here.

## B. Inputs for the perturbation bound |Delta' - Delta| <= 2 eps
- sum_{i<j} |K_ij| = 0.3159063 A; Delta = 0.01024524 A; Delta / sum|K| = 0.03243.
- Truncation to the nearest 126 pairs: removed sum |K| = 0.0416034 A (13.17%); 2 eps / Delta = 8.12 (the worst-case bound is uninformative).
- Island-dimension perturbations (A and K both re-evaluated from the frozen formulas at 792 K): for w or h scaled by (1+p) the Hamiltonian is a pure rescaling by (1+p)^2 (K is proportional to w h and A to l w h), residual at floating-point level; for l scaled by 1.01 and 1.05 the best rescaling lambda = 1.0225 and 1.1163 leaves a residual with 2 eps_R / (lambda Delta) = 0.0545 and 0.279.
- Persistence of the failure at W = 1 kBT under a general perturbation: guaranteed while eps <= 2.93e-4 A (0.0927% of sum |K|).
- The sign-inverted exploratory Hamiltonians are a different model; the bound gives no information about them.
- No perturbed model was solved.

## Files
`supplement_analysis_v001.py` (self-contained; `python3 supplement_analysis_v001.py <path to scr_iii_b>`), `supplement_analysis_v001_output.json` (full output), `SHA256SUMS.txt`.
