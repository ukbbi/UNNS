# CIB-I v001 — Computed comparative results

All results refer to binary periodic dielectric **first-order material Fourier coupling** on a fixed 2pi domain. These are analytical model comparisons, not physical observations.

## Primary fixed-window comparison (m,m′ ≤512)

| Duty D | UNNS nonzero / 301 | Maxwell all-pair background | UNNS enrichment | Near− fraction | Near+ fraction | Square fraction |
|---|---:|---:|---:|---:|---:|---:|
| 1/2 | 155 / 301 | 0.501 | 1.028 | 0.181 | 0.190 | 0.336 |
| 1/3 | 97 / 301 | 0.668 | 0.482 | 0.689 | 0.498 | 0.193 |
| 1/5 | 248 / 301 | 0.802 | 1.028 | 0.524 | 0.745 | 0.648 |
| 2/5 | 248 / 301 | 0.802 | 1.028 | 0.524 | 0.745 | 0.648 |
| 1/7 | 189 / 301 | 0.859 | 0.731 | 0.875 | 0.842 | 0.794 |
| 1/11 | 281 / 301 | 0.911 | 1.025 | 0.926 | 0.915 | 0.904 |
| 1/13 | 248 / 301 | 0.925 | 0.891 | 0.875 | 0.939 | 0.927 |
| 2/17 | 289 / 301 | 0.943 | 1.018 | 0.886 | 0.955 | 0.950 |

The source-scrambled UNNS control preserves every q increment and has exactly the same nonzero counts, average normalized Fourier power, and enrichment for every profile. Hence these one-edge statistics do not identify UNNS uniquely.

## Equal-endpoint UNNS diamond under untuned profiles

| Duty D | A 2→8→36 shifts (6,28) | B 2→9→36 shifts (7,27) |
|---|---|---|
| 1/2 | both matrix elements zero | both nonzero |
| 1/3 | first zero, second nonzero | first nonzero, second zero |
| 1/5 | both nonzero | both nonzero |

These are first-order matrix-entry results, **not** whole-history Maxwell evolution or physical realization of T_N.

## Post-protocol exploratory topology

| Duty D | UNNS two-step routes | UNNS 2-route merger pairs | q-scramble two-step routes | q-scramble merger pairs |
|---|---:|---:|---:|---:|
| 1/2 | 42 | 0 | 22 | 0 |
| 1/3 | 15 | 0 | 6 | 0 |
| 1/5 | 173 | 28 | 42 | 0 |
| 1/7 | 80 | 12 | 21 | 0 |

These different motif counts show that q-matching controls do **not** preserve graph topology. No dynamical mode amplitudes were calculated for those specific paths and the scramble is not degree-matched.

## Prime theorem examples

| Prime p | Suppressed label residues N mod p (all t) |
|---:|---|
| 3 | 1 |
| 7 | 2, 4 |
| 13 | 3, 9 |
| 19 | 7, 11 |
| 2, 5, 11, 17 | none |

## Verdict

**Established:** exact infinite UNNS label-family Fourier suppression in rational binary profiles; mathematically distinct selected nesting subgraphs; an exact first-order q-only identifiability limit; cross-equation nonuniqueness.

**Not established:** unique physical preference for UNNS, improved predictive accuracy on independent measurements, all-orders mode blockade or full-field UNNS dynamics.

Programs and source controls are in README, THEOREMS and REGISTER.
