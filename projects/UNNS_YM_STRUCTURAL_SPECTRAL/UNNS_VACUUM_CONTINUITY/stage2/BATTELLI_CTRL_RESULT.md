# BATTELLI_CTRL_RESULT.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 2  
**Control:** Battelli 2019 unsmoothed structural control  
**Status:** **FROZEN — COMPLETE**  
**Frozen control verdict:** **UNSMOOTHED-ARCHITECTURE-CONSISTENT**  
**Date:** 2026-10-05

---

## 1. Purpose

This control tested whether the structural architecture observed in the CEA_2017 branch survives removal of the CEA smoothing construction.

It does not reopen or alter:

```text
VREF-I/B = REFINEMENT-INDETERMINATE
CEA STRUC bridge = ARCHITECTURE-PRESERVED
```

The Battelli branch is corroborative only.

---

## 2. Canonical STRUC-I run

Chamber:

```text
STRUC-I v1.0.4
```

Frozen executable settings actually achieved:

```text
MC RUNS       = 10000
kappa STEPS   = 40
kappa MIN     = 0.01
kappa MAX     = 1.0
```

Input wrapper:

```text
BATTELLI_STRUC_I.csv
```

The wrapper contains three independent unsmoothed positive-transverse-distance ladders:

```text
B1  n=4
B2  n=6
B3  n=5
```

The `d_t=0` point was excluded before chamber ingestion under the frozen renormalization rule.

### STRUC-I results

| Ladder | Regime | State | mean A_k | min A_k | max rho |
|---|---|---|---:|---:|---:|
| B1 | Geometric Persistence | Stable Structure | 0.999962 | 0.9986 | 0.3457 |
| B2 | Geometric Persistence | Stable Structure | 0.999965 | 0.9988 | 0.3728 |
| B3 | Geometric Persistence | Stable Structure | 0.999992 | 0.9997 | 0.28685 |

All three unsmoothed refinements therefore occupy the same canonical STRUC-I regime.

The export left:

```text
dataset.family = null
dataset.class  = null
```

although the preregistered descriptive labels were:

```text
BATTELLI_2019
YM_UNSMOOTHED
```

These fields are export metadata only. They are not chamber inputs to the structural calculation and have no numerical effect.

No rerun is required for metadata alone.

---

## 3. STRUC-PERC-I result

Canonical chamber:

```text
STRUC-PERC-I v2.5.0
```

All three Battelli ladders returned:

```text
FULL_PERCOLATION
```

with:

```text
giant ratio = 1.0
isolated vertices = 0
tail dominance = 0
```

The observed connectivity scales were:

```text
B1  kappa_connect = 2.0
B2  kappa_connect = 1.0
B3  kappa_connect = 2.0
```

Values beyond the initial `kappa <= 1` grid arise from the canonical chamber's adaptive extension and are retained exactly as returned.

Because the ladders contain only 4–6 values, these STRUC-PERC outcomes remain:

```text
VERY-SHORT-LADDER TOPOLOGY DIAGNOSTICS
```

They are not promoted to a vacuum-continuity theorem.

---

## 4. Frozen synthesis

The result is:

```text
UNSMOOTHED-ARCHITECTURE-CONSISTENT
```

Reason:

1. all three unsmoothed refinements occupy the same STRUC-I regime;
2. all three are classified as Stable Structure;
3. all three return Full Percolation in STRUC-PERC-I;
4. there is no refinement-induced regime split;
5. the common unsmoothed architecture is compatible with the CEA structural result.

Thus the preservation of ordered amplitude-ladder architecture seen in the CEA branch is not restricted to the CEA smoothing construction.

---

## 5. Project-level meaning

The combined Stage-2 pattern is now:

```text
CEA_2017 VREF-I/B:
REFINEMENT-INDETERMINATE

CEA_2017 STRUC bridge:
ARCHITECTURE-PRESERVED

Battelli_2019 unsmoothed control:
UNSMOOTHED-ARCHITECTURE-CONSISTENT
```

This narrows the CEA refinement mismatch.

The mismatch is observed in absolute profile amplitude, while ordered structural architecture remains stable across:

- the CEA physical refinements;
- common-support interpolation variants;
- an independent unsmoothed connected-correlator measurement.

This does **not** convert the VREF-I/B verdict into `CONTINUITY-SUPPORTED`.

It does establish that the available evidence for indeterminacy is not accompanied by a detected ordered-structure break.

---

## 6. Next branch

The next frozen Stage-2 branch is:

```text
YANAGIHARA_2019_EMT
```

Its purpose is stronger than the Battelli control: it changes the physical representation itself, from connected chromoelectric-field amplitudes to the vacuum-subtracted continuum energy-momentum tensor.

That branch is preregistered separately in:

```text
stage2/YANAGIHARA_EMT_FREEZE.md
```
