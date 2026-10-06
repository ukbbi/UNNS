# YANAGIHARA_EMT_BUILD_FREEZE.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 2  
**Branch:** EMT-I  
**Status:** **FROZEN AFTER VALID EXTRACTION, BEFORE FIRST SCIENTIFIC RUN**  
**Date:** 2026-10-05

## 1. Extraction gate

The chamber accepts only the exact deterministic common-native extraction:

```text
data/derived/yanagihara_2019/YAN19_EMT_COMMON.csv
```

Its SHA-256 is frozen in `EMT_I_CONFIG.json`.

The four EMT components share 185 identical native coordinates, so:

```text
INTERPOLATION = NONE
```

No linear/PCHIP branch is invoked.

## 2. Natural-unit distance

The source units are `GeV/fm^3`.

The dimensionless conversion is:

\[
D_{\rm EMT}
=
\frac{R_{\rm fm}^4}{\hbar c}
\sqrt{\frac{\varepsilon^2+\sigma_{zz}^2+\sigma_{rr}^2+\sigma_{\theta\theta}^2}{4}}.
\]

This follows because:

\[
({\rm GeV/fm^3})\,R_{\rm fm}^4/(\hbar c)
\]

is dimensionless.

Freeze:

```text
R = 0.69 fm
hbar*c = 0.1973269804 GeV fm
```

## 3. Norm uncertainty

With no published cross-component covariance matrix, use a deterministic independent-pointwise box envelope.

For each component:

\[
a_i=\max(|y_i|-\sigma_i,0),\qquad b_i=|y_i|+\sigma_i.
\]

Then:

\[
D_{\min}=S\sqrt{\frac14\sum_i a_i^2},
\qquad
D_{\max}=S\sqrt{\frac14\sum_i b_i^2},
\]

where \(S=R^4/(\hbar c)\).

The fit uncertainty is frozen as:

\[
\sigma_D=(D_{\max}-D_{\min})/2.
\]

The path reversal rule is material only if the next lower envelope exceeds the previous upper envelope.

## 4. Tail models

The frozen tail starts at:

```text
r >= 0.345 fm
```

The same exponential and `K0` families in `YANAGIHARA_EMT_FREEZE.md` are used.

AICc threshold:

```text
|Delta AICc| >= 6
```

The only sensitivity drops the first eligible tail coordinate.

## 5. Component cross-check

Each physical component is analyzed through its distance from zero:

```text
abs(component)
```

with the published component error bar retained.

Allowed component labels:

```text
VACUUM-DIRECTED
NONZERO-FLOOR
UNCERTAINTY-LIMITED
NONMONOTONE
```

A sign crossing is not itself a failure.

A decisive positive floor in any component blocks `EMT-CONTINUITY-CONSISTENT`.

## 6. Model-family disagreement

The frozen branch outcome list does not contain a separate `MODEL-SPLIT`.

Therefore exponential/K0 disagreement without a component-vs-vector contradiction maps to:

```text
EMT-UNCERTAINTY-LIMITED
```

`EMT-REPRESENTATION-SPLIT` is reserved for a material contradiction between the primary four-component norm and one or more individual EMT components.

## 7. First-run rule

The chamber has been built but **not scientifically executed** in this package.

The first permitted scientific operation is:

```text
RUN_EMT_I.bat
```

after this build is merged into the project containing the validated extraction.
