# BATTELLI_CTRL_FREEZE.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 2  
**Control:** Battelli 2019 unsmoothed structural control  
**Status:** **FROZEN BEFORE STRUC EXECUTION**  
**Date:** 2026-10-05
**Revision:** v0.2 — STRUC-I parser-compatible grouped input

## 1. Role

This control follows the completed CEA_2017 VREF-I/B + STRUC bridge.

It does not reopen or alter:

```text
VREF-I/B = REFINEMENT-INDETERMINATE
STRUC_BRIDGE = ARCHITECTURE-PRESERVED
```

Its single purpose is to test whether the preserved ordered-ladder architecture is also visible in an **unsmoothed** connected-correlator measurement.

## 2. Source

N. Battelli and C. Bonati, *Color flux tubes in SU(3) Yang-Mills theory: an investigation with the connected correlator* (2019), arXiv:1903.10463v2.

Canonical local inputs:

```text
data/raw/battelli_2019/
├── arXiv-1903.10463v2.tar.gz
└── battelli_2019.pdf
```

Expected SHA-256:

```text
arXiv-1903.10463v2.tar.gz
e4ffd183a5d995862b19b2e4ce73e812f5cc102b67dad8174a7a6a8b1ba14b15

battelli_2019.pdf
796a3f24bc6369622750b72b54c01c2ec97a832c8974af26f2aa400341be81b0
```

Primary vector asset:

```text
el_withz.eps
SHA-256: a211dc25d56e68d7e03638a120ade1b76fbd77a752a29f3c85fe2dcc79acbc70
```

## 3. Why this source is a control rather than the VREF primary

The source uses stochastically exact multihit/multilevel measurements **without smoothing**.

The plotted quantity in `el_withz.eps` has had the linear divergence removed through `Z_L`, but the logarithmic multiplicative renormalization `Z_1(a,d_t)` is still missing.

For `d_t>0`, that missing factor is multiplicative and independent of `d_t` within each refinement. Therefore the **ordered amplitude geometry within one positive-`d_t` profile** is meaningful up to a positive scale factor, while absolute cross-refinement amplitudes are not treated as directly comparable.

This is exactly why this branch is a secondary structural control and not a replacement for CEA_2017 VREF-I/B.

## 4. The d_t = 0 point is excluded

The source explicitly distinguishes the logarithmic renormalization at:

```text
d_t = 0
d_t > 0
```

Accordingly, the `d_t=0` point is retained in `BATTELLI_POINTS.csv` for provenance but is **not admitted to the STRUC ladders**.

No point with `d_t>0` is removed.

## 5. Three admitted unsmoothed ladders

```text
B1_POS.csv   beta=6.0      d=4a   n=4
B2_POS.csv   beta=6.2601   d=6a   n=6
B3_POS.csv   beta=6.47466  d=8a   n=5
```

The physical quark-antiquark separation is approximately 0.37 fm at all three refinements.

The ladder values are the vector-recovered ordinates:

```text
Z_L(d,d_t,a) E_L(d,d_t) / 3   [fm^-2]
```

for `d_t>0`.

No normalization, rescaling, peak division, or synthetic completion is applied before the canonical chambers.

## 6. Deterministic vector extraction

The extractor reads the Grace vector geometry in `el_withz.eps`.

Frozen labelled-axis transform:

```text
X_plot 0.1976 -> d_t = 0.0 fm
X_plot 1.1500 -> d_t = 0.4 fm

Y_plot 0.2136 -> ordinate = 0
Y_plot 0.8500 -> ordinate = 20
```

Series mapping:

```text
Color1 -> beta 6.0
Color2 -> beta 6.2601
Color4 -> beta 6.47466
```

Expected recovered point counts including `d_t=0`:

```text
beta 6.0     : 5
beta 6.2601  : 7
beta 6.47466 : 6
```

Primary extraction output:

```text
data/derived/battelli_2019/BATTELLI_POINTS.csv
```

## 7. STRUC-I control run

Use canonical:

```text
STRUC-I v1.0.4
```

unchanged.

Load the single grouped CSV:

```text
BATTELLI_STRUC_I.csv
```

It contains exactly the same 4 + 6 + 5 admitted values, grouped as `B1`, `B2`, and `B3`.

This grouped wrapper is required only because canonical STRUC-I v1.0.4's single-column CSV fallback accepts a numeric column only when it sees more than five numeric rows. No ladder value is added, duplicated, removed, normalized, or altered. The chamber itself remains unchanged.

The individual files:

```text
B1_POS.csv
B2_POS.csv
B3_POS.csv
```

remain the canonical inputs for STRUC-PERC-I Batch Mode.

Freeze controls:

```text
MAX LADDER SIZE = 2000
MC RUNS          = 10000
kappa STEPS      = 40
kappa MIN        = 0.01
kappa MAX        = 1.0
DATASET FAMILY   = BATTELLI_2019
DATASET CLASS    = YM_UNSMOOTHED
```

Run once to completion.

Required exports:

```text
output/battelli_ctrl/struc_i/STRUC_I_BATTELLI.json
output/battelli_ctrl/struc_i/STRUC_I_BATTELLI.csv
```

## 8. STRUC-PERC-I control run

Use canonical:

```text
STRUC-PERC-I v2.5.0
```

unchanged, Batch Mode.

Load the same three ladders.

Freeze:

```text
kappa GRID POINTS = 17
kappa MIN         = 0.01
kappa MAX         = 1.0
DOMAIN ADAPTER    = Generic
BATCH DELAY       = 10 ms
MAX LADDERS       = 3
```

Required exports:

```text
output/battelli_ctrl/struc_perc_i/STRUC_PERC_BATTELLI.json
output/battelli_ctrl/struc_perc_i/STRUC_PERC_BATTELLI.csv
```

## 9. Very-short-ladder restriction

These ladders contain only 4, 6, and 5 admitted values.

Therefore **both** chamber outputs are treated as corroborative short-ladder diagnostics, and STRUC-PERC-I especially is labelled:

```text
VERY-SHORT-LADDER TOPOLOGY DIAGNOSTIC
```

No Battelli chamber tier alone may establish or falsify structural vacuum continuity.

## 10. Frozen control interpretation

Allowed control statuses:

```text
UNSMOOTHED-ARCHITECTURE-CONSISTENT
UNSMOOTHED-ARCHITECTURE-SPLIT
UNSMOOTHED-DIAGNOSTIC-INDETERMINATE
```

### UNSMOOTHED-ARCHITECTURE-CONSISTENT

All three Battelli refinements have the same STRUC-I regime, and their STRUC-PERC-I tiers are mutually consistent; that common architecture is compatible with the CEA control result of Geometric Persistence / Full Percolation.

### UNSMOOTHED-ARCHITECTURE-SPLIT

The unsmoothed refinements disagree materially in STRUC-I regime and/or STRUC-PERC-I tier, or the common unsmoothed architecture conflicts with the CEA structural result.

### UNSMOOTHED-DIAGNOSTIC-INDETERMINATE

The very short ladders produce mixed/boundary behavior insufficient for a coherent control classification.

## 11. Project-level scope

A consistent result would narrow the CEA VREF refinement mismatch further: preserved architecture would then be visible both in the smeared CEA representation and in an unsmoothed connected-correlator measurement.

It would **not** change the frozen VREF-I/B verdict by itself.

The next independent representation after this control remains the Yanagihara vacuum-subtracted EMT branch.
