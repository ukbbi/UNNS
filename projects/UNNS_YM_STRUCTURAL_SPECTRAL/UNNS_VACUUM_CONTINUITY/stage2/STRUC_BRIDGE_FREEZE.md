# STRUC_BRIDGE_FREEZE.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 2  
**Bridge:** VREF-I/B → STRUC-I / STRUC-PERC-I  
**Status:** **FROZEN BEFORE STRUC EXECUTION**  
**Date:** 2026-10-05

## 1. Purpose

This bridge asks whether the refinement disagreement found by VREF-I/B changes the **internal ordered-ladder architecture** of the measured field amplitudes.

It does **not** replace VREF-I/B.

The three instruments answer different questions:

- **VREF-I/B:** Does the physical radial profile approach the vacuum locus or a positive asymptotic floor?
- **STRUC-I v1.0.4:** Is the ordered amplitude ladder admissible under the chamber's perturbation grammar?
- **STRUC-PERC-I v2.5.0:** What is the connectivity/percolation topology of the gap-vulnerability graph?

Because both STRUC chambers sort scalar ladder values internally, they do **not** preserve the radial direction \(x_t\to\infty\). Their outputs are therefore structural diagnostics of the amplitude ladder, not independent tests of radial vacuum accessibility.

## 2. Canonical chambers

Use the existing canonical chambers **unchanged**:

```text
STRUC-I v1.0.4
STRUC-PERC-I v2.5.0
```

No code, thresholds, adapters, graph definitions, or regime rules may be modified for this project.

## 3. Frozen numerical source

All bridge ladders are generated only from:

```text
data/derived/cea_2017/CEA17_VREF_B_POINTS.csv
```

Expected SHA-256:

```text
a2a83c9a6d601b43ed6a51798192897b575fcf25b5b60f1ae5e015a3a2035d54
```

No value is re-digitized and no value is taken from the plotted figures a second time.

## 4. Ladder representations

Five representations are frozen.

### R1_NATIVE

The 11 native CEA 2017 field amplitudes at:

```text
beta = 6.050
d = 8a
```

### R2_NATIVE

The 11 native CEA 2017 field amplitudes at:

```text
beta = 6.195
d = 10a
```

### R1_COMMON

R1 native amplitudes restricted to the VREF-I/B two-resolution common support:

```text
0 <= x_t <= 0.761985714 fm
```

This gives 9 scalar amplitudes.

### R2_COMMON_LIN

R2 mapped to the exact R1 common-grid coordinates by the already-frozen piecewise-linear VREF interpolation.

This gives 9 scalar amplitudes.

### R2_COMMON_PCHIP

R2 mapped to the same R1 common-grid coordinates by the already-frozen PCHIP sensitivity interpolation.

This gives 9 scalar amplitudes.

## 5. Amplitude handling

The bridge preserves the extracted \(E_l\) values in GeV².

Prohibited:

- peak normalization;
- min-max normalization;
- unit-interval rescaling;
- subtraction of the terminal value;
- division by R1 or R2 central amplitude;
- deletion of low-amplitude tail points;
- adding synthetic points.

The canonical chambers may internally sort the values because that behavior is part of their frozen grammar.

## 6. STRUC-I v1.0.4 run

Load all five ladder CSVs simultaneously into the five upload slots.

Freeze:

```text
MAX LADDER SIZE = 2000
MC RUNS          = 10000
kappa STEPS      = 40
kappa MIN        = 0.01
kappa MAX        = 1.0
DATASET FAMILY   = CEA_2017
DATASET CLASS    = YM_VACUUM
```

Run exactly one completed canonical chamber session.

The chamber uses `Math.random()` internally. Exact Monte Carlo numbers are therefore not bitwise reproducible. The high run count is frozen to reduce sampling noise.

Do not repeat a completed run merely because a classification is inconvenient. A rerun is permitted only if the first session is interrupted, crashes, or fails to export.

Export both:

```text
JSON
CSV
```

Place/rename them as:

```text
output/struc_bridge/struc_i/STRUC_I_CEA17.json
output/struc_bridge/struc_i/STRUC_I_CEA17.csv
```

## 7. STRUC-PERC-I v2.5.0 run

Use **BATCH MODE** and load the same five CSVs.

Freeze the visible chamber controls before batch execution:

```text
kappa GRID POINTS = 17
kappa MIN         = 0.01
kappa MAX         = 1.0
DOMAIN ADAPTER    = Generic
BATCH DELAY       = 10 ms
MAX LADDERS       = 5
```

Run the complete five-ladder batch once.

Export:

```text
BATCH CSV
BATCH JSON
```

Place/rename them as:

```text
output/struc_bridge/struc_perc_i/STRUC_PERC_CEA17.csv
output/struc_bridge/struc_perc_i/STRUC_PERC_CEA17.json
```

If desired, individual full JSON exports may also be retained, but the batch CSV/JSON are the required bridge records.

## 8. Short-ladder restriction

These ladders contain only 9 or 11 field values.

Therefore all STRUC-PERC-I results are explicitly labelled:

```text
SHORT-LADDER STRUCTURAL DIAGNOSTIC
```

A chamber tier is recorded faithfully, but it is not promoted by itself to a project-level theorem about the Yang-Mills vacuum.

In particular:

- `FULL_PERCOLATION` or `GIANT_COMPONENT_PERCOLATION` does not prove admissibility.
- STRUC-I remains the independent admissibility chamber.
- Any `HARD_FRAGMENTATION` result is recorded, but its project-level physical interpretation remains subordinate to the VREF representation and the short-ladder limitation.

## 9. Frozen cross-chamber interpretation

After both chambers finish, the bridge synthesis uses these comparisons.

### A. Native refinement comparison

```text
R1_NATIVE ↔ R2_NATIVE
```

Question: does the physical refinement change the ladder regime/topology?

### B. Common-support comparison

```text
R1_COMMON ↔ R2_COMMON_LIN
```

Question: after enforcing the same physical support, does the structural architecture remain aligned?

### C. Interpolation sensitivity

```text
R2_COMMON_LIN ↔ R2_COMMON_PCHIP
```

Question: can the interpolation choice change the STRUC-I regime or STRUC-PERC tier?

## 10. Bridge synthesis statuses

The later synthesis record may assign only one of:

```text
ARCHITECTURE-PRESERVED
ARCHITECTURE-SPLIT
INTERPOLATION-SENSITIVE
DIAGNOSTIC-INDETERMINATE
```

### ARCHITECTURE-PRESERVED

Native and common-support R1/R2 comparisons agree in STRUC-I regime and STRUC-PERC tier, and linear/PCHIP sensitivity does not change either classification.

### ARCHITECTURE-SPLIT

R1 and R2 differ materially in STRUC-I regime and/or STRUC-PERC tier under the like-for-like comparison.

### INTERPOLATION-SENSITIVE

R2 common-linear and R2 common-PCHIP produce different STRUC-I regime or STRUC-PERC tier.

### DIAGNOSTIC-INDETERMINATE

Outputs are internally mixed, incomplete, or too close to chamber boundaries for a coherent bridge-level assignment.

No bridge status alters the frozen VREF-I/B result:

```text
REFINEMENT-INDETERMINATE
```

## 11. Interpretation target

The most informative possible pattern would be:

```text
VREF-I/B: REFINEMENT-INDETERMINATE in absolute amplitude
STRUC-I: same structural regime across refinements
STRUC-PERC-I: same topology tier across refinements
```

That combination would support the narrower interpretation that the CEA refinement mismatch is largely an amplitude/calibration/discretization issue while ordered structural architecture is preserved.

Conversely, a STRUC regime/topology split would show that the refinement mismatch changes the ladder architecture itself.

## 12. Freeze statement

The bridge files, run matrix, chamber settings, and synthesis logic above are frozen before either canonical STRUC chamber is run on these CEA ladders.
