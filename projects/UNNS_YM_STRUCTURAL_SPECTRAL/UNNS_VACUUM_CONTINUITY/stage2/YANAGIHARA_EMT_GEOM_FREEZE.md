# YANAGIHARA_EMT_GEOM_FREEZE.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 2  
**Branch:** EMT-I secondary geometry checks  
**Status:** **FROZEN BEFORE SECONDARY SCIENTIFIC RUN**  
**Date:** 2026-10-05

## 1. Purpose

The primary Yanagihara EMT-I branch at `R=0.69 fm` is closed as:

```text
EMT-UNCERTAINTY-LIMITED
```

This secondary branch asks only whether its qualitative structural behavior is stable under the two already-published neighboring source separations:

```text
R = 0.46 fm
R = 0.92 fm
```

It does not change the primary verdict.

## 2. Source and extraction

Source:

```text
data/raw/yanagihara_2019/mid_separates.pdf
SHA-256: fe549266b6a2483aa0c0104835ddf3215a9b2d8812110aacb86ea2368aa10423
```

Deterministic vector extraction recovered, for **each** secondary geometry:

```text
epsilon      185 native points
sigma_zz     185 native points
sigma_rr     185 native points
sigma_theta  185 native points
```

The four components share the exact same native coordinate grid in each panel.

Therefore:

```text
INTERPOLATION = NONE
```

Secondary support:

```text
R=0.46: r <= 0.658002718 fm
R=0.92: r <= 0.658002757 fm
```

## 3. Exact reuse of primary rules

No scientific rule is changed except for the geometry-dependent quantities forced by `R`.

For each geometry use:

\[
D_{EMT}(r)
=
rac{R^4}{\hbar c}
\sqrt{rac{arepsilon^2+\sigma_{zz}^2+\sigma_{rr}^2+\sigma_	heta^2}{4}}
\]

with:

```text
hbar*c = 0.1973269804 GeV fm
```

Tail cuts are fixed geometrically:

```text
R=0.46 -> r >= 0.230 fm
R=0.92 -> r >= 0.460 fm
```

Tail point counts:

```text
R=0.46 -> 156
R=0.92 -> 88
```

The only tail sensitivity remains:

```text
drop the first eligible tail coordinate
```

Model families remain:

```text
exponential
K0
```

and each compares:

```text
zero floor
positive common floor
```

with:

```text
|Delta AICc| >= 6
```

as the decisive threshold.

## 4. Component rule

All four physical component distances from zero are checked exactly as in primary EMT-I.

A sign crossing is not a failure.

A decisive positive component floor is a material contradiction.

## 5. Per-geometry outcomes

Allowed per-geometry outcomes are unchanged:

```text
EMT-CONTINUITY-CONSISTENT
EMT-POSITIVE-FLOOR
EMT-REPRESENTATION-SPLIT
EMT-UNCERTAINTY-LIMITED
EMT-DATA-LIMITED
```

## 6. Secondary synthesis status

Allowed combined geometry statuses:

```text
GEOMETRY-ROBUST-NO-FLOOR
GEOMETRY-POSITIVE-FLOOR
GEOMETRY-SPLIT
GEOMETRY-UNCERTAINTY-LIMITED
```

### GEOMETRY-ROBUST-NO-FLOOR

Both secondary four-component norm paths are vacuum-directed, neither secondary geometry yields `EMT-POSITIVE-FLOOR`, and no secondary component yields a decisive `NONZERO-FLOOR`.

This status does **not** require both secondary geometries to reach `EMT-CONTINUITY-CONSISTENT`; uncertainty-limited zero-floor evidence is allowed.

### GEOMETRY-POSITIVE-FLOOR

Both secondary geometries decisively support a positive structural floor under the unchanged primary rules.

### GEOMETRY-SPLIT

The two secondary source separations give materially incompatible structural topology, including a decisive positive-floor result in only one geometry or a representation split not shared by the other.

### GEOMETRY-UNCERTAINTY-LIMITED

The secondary evidence cannot be assigned coherently to the statuses above.

## 7. Interpretation

A `GEOMETRY-ROBUST-NO-FLOOR` result would mean:

> the independent continuum EMT representation is vacuum-directed without a detected positive structural floor across all three published source separations, while the primary `R=0.69 fm` branch remains formally uncertainty-limited.

It still does not imply closure of the Yang-Mills Hamiltonian mass gap.

## 8. No-retuning rule

After this freeze:

- do not change either secondary `R`;
- do not shift either tail cut;
- do not alter the four-component norm;
- do not normalize profiles;
- do not change the model families;
- do not change `|Delta AICc|=6`;
- do not use secondary results to rewrite the primary `R=0.69 fm` verdict.
