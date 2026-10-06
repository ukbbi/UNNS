# VREF_B_EXTRACT.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Branch:** VREF-I/B  
**Protocol:** deterministic Grace/EPS vector extraction  
**Status:** **FROZEN**  
**Freeze date:** 2026-10-05

---

## 1. Input

Canonical archive:

```text
data/raw/cea_2017/arXiv-1702.06437v3.tar.gz
SHA-256: 38e899b4c9d83b78e8bca70a51fc3adb3fa4e8c278ce4c392b3b08cbc3de2c44
```

Canonical vector asset inside archive:

```text
E_physical_scaling_SU3.eps
SHA-256: bfa9e27a3d6e045e33977c277b8c473d1123067acac0c97955cd4fbee670a6fe
```

Expected EPS metadata:

```text
Creator: Grace-5.1.25
Title: E_physical_scaling_SU3.agr
```

No raster OCR or manual WebPlotDigitizer extraction is allowed for the primary branch.

---

## 2. Frozen graph transform

The EPS graph viewport is:

```text
X_plot: 0.1500 -> 0.8500
Y_plot: 0.1500 -> 0.8500
```

The corresponding physical world coordinates are:

```text
x_t: 0.0 -> 1.1 fm
E_l: 0.0 -> 0.5 GeV^2
```

The deterministic transforms are:

\[
x_t=
(X_{\rm plot}-0.1500)\frac{1.1}{0.7},
\]

\[
E_l=
(Y_{\rm plot}-0.1500)\frac{0.5}{0.7}.
\]

The extractor must verify the graph frame and source hash before applying these transforms.

---

## 3. Series identity

The Grace EPS uses:

```text
Color1 -> beta = 6.050
Color2 -> beta = 6.195
```

The legend assignment must be verified in the EPS text before output is written.

Expected primary point-marker geometry:

```text
EARC radius = 0.0050 x 0.0050
```

Expected count:

```text
11 beta=6.050 markers
11 beta=6.195 markers
```

Legend marker circles are excluded by drawing-order / graph-data-block validation and may not be mistaken for data points.

---

## 4. Point extraction

For every accepted marker:

1. read its Grace plot coordinates \((X,Y)\);
2. identify the two same-color vertical error-bar segments sharing the marker's \(X\);
3. recover \(Y_{\rm low}\) and \(Y_{\rm high}\);
4. convert the marker and error endpoints through the frozen graph transform.

The extracted central value is:

\[
E=
(Y-0.1500)\frac{0.5}{0.7}.
\]

The published symmetric error is:

\[
\sigma_{\rm published}
=
\frac{Y_{\rm high}-Y_{\rm low}}{2}
\frac{0.5}{0.7}.
\]

The error-bar midpoint must agree with the marker ordinate within the frozen EPS-coordinate tolerance.

---

## 5. EPS quantization tolerance

Grace coordinates are printed to four decimal places.

The conservative one-unit ordinate quantization scale is:

\[
\boxed{
\sigma_{\rm EPS}
=
10^{-4}\frac{0.5}{0.7}
=
7.142857\times10^{-5}\ {\rm GeV}^2
}.
\]

This is preserved separately from the published error and also combined in quadrature for later model fitting.

---

## 6. Native-coordinate integrity checks

For each series, the extractor must verify:

- 11 accepted markers;
- finite coordinates;
- strictly increasing \(x_t\);
- first coordinate consistent with zero within EPS quantization;
- approximately uniform native spacing;
- positive published errors;
- no accepted marker outside the graph viewport;
- no legend marker admitted;
- no smooth fit-curve vertex interpreted as a data marker.

The larger native spacing must correspond to the \(d=8a\) series and the smaller native spacing to the \(d=10a\) series.

---

## 7. Output schema

The extractor writes:

```text
data/derived/cea_2017/CEA17_VREF_B_POINTS.csv
data/derived/cea_2017/CEA17_VREF_B_EXTRACT.json
```

CSV columns:

```text
source_id
refinement
beta
color
point_index
X_plot
Y_plot
Y_low_plot
Y_high_plot
x_fm
E_GeV2
published_error_GeV2
eps_quant_GeV2
fit_sigma_GeV2
```

The JSON record contains:

- source/archive hash;
- EPS asset hash;
- graph transform;
- series mapping;
- parser version;
- output CSV hash;
- marker counts;
- native spacing summaries;
- extraction status.

---

## 8. No scientific calculation in extraction

The extraction step must **not**:

- fit an asymptotic model;
- compute AICc;
- classify continuity/isolation;
- normalize the profiles;
- discard points based on amplitude;
- interpolate either profile.

Extraction ends after the machine-readable native point table and provenance record are written.

---

## 9. Extraction verdict

Allowed extraction statuses are:

```text
EXTRACTION-VALID
EXTRACTION-INVALID
```

Only `EXTRACTION-VALID` permits the VREF-I/B chamber to be built and run.
