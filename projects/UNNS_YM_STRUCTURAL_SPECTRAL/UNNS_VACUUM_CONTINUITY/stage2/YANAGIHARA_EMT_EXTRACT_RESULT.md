# YANAGIHARA_EMT_EXTRACT_RESULT.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 2  
**Branch:** EMT-I — Yanagihara 2019  
**Extraction status:** **EXTRACTION-VALID**  
**Scientific EMT-I fit performed:** **NO**  
**Date:** 2026-10-05

## Source lock

```text
mid_separates.pdf
SHA-256: fe549266b6a2483aa0c0104835ddf3215a9b2d8812110aacb86ea2368aa10423
```

The admitted primary panel is:

```text
(b) R = 0.69 fm
```

## Deterministic vector recovery

The extraction reads vector marker and error-bar geometry directly from the PDF.

Recovered per component:

```text
epsilon      185 points
sigma_zz     185 points
sigma_rr     185 points
sigma_theta  185 points
```

Total long-format rows:

```text
740
```

All four components share **exactly the same 185 native transverse coordinates**.

Therefore:

```text
COMMON GRID: NATIVE
INTERPOLATION: NOT REQUIRED
PCHIP SENSITIVITY: NOT APPLICABLE
```

Measured support:

```text
r_min = 3.29759960626e-08 fm
r_max = 0.658002923403 fm
```

The frozen outer-tail cut is:

```text
r >= R/2 = 0.345 fm
```

and contains:

```text
127 common native coordinates
```

which is ample for the preregistered AICc tail comparison.

## Component sign convention

The source figure plots:

```text
-T44
-Tzz
 Trr
 Ttheta
```

The EMT-I physical vector is stored as:

```text
epsilon      = -T44
sigma_zz     = -Tzz
sigma_rr     = -Trr
sigma_theta  = -Ttheta
```

Both the plotted source value and the derived physical-component value are preserved in `YAN19_EMT_POINTS.csv`.

## Error bars

Each admitted marker has two vector-recovered cap positions.

Maximum marker/error-bar midpoint discrepancy:

```text
0.000259399 PDF points
```

No raster digitization or OCR was used.

## Outputs

```text
data/derived/yanagihara_2019/YAN19_EMT_POINTS.csv
SHA-256: 7370e8fb284ecaf2404ec4206b766f7880a780c071351678a65db73f40a35208

data/derived/yanagihara_2019/YAN19_EMT_COMMON.csv
SHA-256: a4d35526595601c5a9fb73ea4a8fef41df02a4b486c2d7dbb3f139eda5317f98

data/derived/yanagihara_2019/YAN19_EMT_EXTRACT.json
```

The next permitted action is the frozen EMT-I chamber build and first scientific run.
