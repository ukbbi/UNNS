# VREF-I/A Calibration Report

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Branch:** VREF-I/A — refinement validation  
**Source:** `BAKER_2022_SU3`  
**Outcome:** **CALIBRATION-SENSITIVE**

> This is a representation-calibration result only. It is prohibited from being interpreted as `CONTINUITY-SUPPORTED` or `ISOLATION-SUPPORTED`.

## Source integrity

| Level | beta | rows | x_t>=0 rows | native support [fm] |
|---|---:|---:|---:|---|
| R1 | 6.240 | 33 | 17 | [-1.022434, 1.022434] |
| R2 | 6.544 | 25 | 13 | [-0.511477, 0.511477] |
| R3 | 6.769 | 33 | 17 | [-0.511238, 0.511238] |

All three admitted files passed the frozen SHA-256, finite-value, three-column, non-negative-error, mirror-symmetry, ordering, and common-support checks.

## Frozen executable geometry

- Reference length: d = 0.511 fm
- Dimensionless coordinate: u = x_t/d
- Common grid: u = [0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0]
- Window width: W = 0.5
- Window size: m = 5
- Primary interpolation: piecewise linear
- Sensitivity interpolation: PCHIP (Fritsch-Butland)
- Extrapolation: prohibited

## Primary cross-refinement metrics

| window | start u | R12 | R23 | R13 | C=R23/R12 | C class |
|---:|---:|---:|---:|---:|---:|:---:|
| 0 | 0.000 | 0.054917743 | 0.024674439 | 0.074719511 | 0.44929812 | <1 |
| 1 | 0.125 | 0.030721654 | 0.016784969 | 0.036930163 | 0.54635628 | <1 |
| 2 | 0.250 | 0.037878721 | 0.020140522 | 0.051200547 | 0.53171071 | <1 |
| 3 | 0.375 | 0.042382842 | 0.041820556 | 0.07569928 | 0.98673318 | <1 |
| 4 | 0.500 | 0.042954259 | 0.063790317 | 0.096997215 | 1.4850755 | >1 |

## Linear/PCHIP qualitative-sensitivity audit

- window 3 start_u=0.375: linear/PCHIP contraction classification differs
- window 3 start_u=0.375: linear/PCHIP refinement-distance ordering differs

## Leave-one-out diagnostic

The full deterministic leave-one-out table is written to:

`output/tables/VREF_A_LOO.csv`

This diagnostic is descriptive only and does not alter the frozen interpolation rule or the calibration outcome by itself.

## Outcome rule

`CALIBRATION-SENSITIVE` is assigned only if the frozen PCHIP sensitivity changes at least one qualitative representation property: profile sign classification, the direction signature of the D_RMS path, the C(s) classification relative to 1, or the ordering of R12/R23/R13 for any window.

Otherwise, after all mandatory integrity checks pass, the outcome is `CALIBRATION-VALID`.

## Scope restriction

VREF-I/A does not test whether D_struct approaches zero in an asymptotic vacuum-compatible region. The common three-resolution support ends at x_t≈0.511 fm. A separate preregistered VREF-I/B source is required for Structural Vacuum Accessibility.
