# Baker REVIEW_SEPARATELY Row Inspection

Fifth diagnostic for the UNNS + color confinement investigation.

This report inspects the rows previously marked `REVIEW_SEPARATELY` by the Baker flux-tube QC pass. It decides whether each row may be used in the formal flux-tube extension report, must be kept as a separate evidence class, should be normalized later, or should be excluded from interpretation for now.

## 1. Input boundary

Input files inspected:

```
04_baker_flux_extension_qc.md
03_flux_tube_separation_extension.md
baker_flux_profile_qc_table.csv
baker2024_extended_flux_profiles_long.csv
Ex_NP_d1.0fm_scaling_normfact.agr
beta7.158dist13.agr
beta6.3942dist789.agr
QCD_large_distances.agr
```

The QC pass had already separated ordinary trusted FULL/NP rows from `PAPER_DEFINED`, large-distance, wide/outlier, and single-point rows. This inspection does not override that separation; it refines the decision for the reviewed rows.

## 2. Review decisions

- `KEEP_SEPARATE_QUALITATIVE_STRING_BREAKING`: 3
- `EXCLUDE_FROM_INTERPRETATION_FOR_NOW`: 2
- `NORMALIZE_LATER_QUALITATIVE_ONLY`: 2
- `KEEP_SEPARATE_LARGE_DISTANCE_CONTROL`: 1
- `EXCLUDE_FROM_TREND_KEEP_AS_OUTLIER_NOTE`: 1

The ordinary trend set should remain restricted to accepted FULL/NP rows from the QC pass. The rows below are not to be mixed into the main peak/width trend.

## 3. Row-level decisions

| source file | component | d [fm] | n | peak | peak SNR | FWHM [fm] | decision | rationale |
|---|---|---:|---:|---:|---:|---:|---|---|
| `beta7.158dist13.agr` | PAPER_DEFINED | 0.960 | 31 | 0.292766 | 16.86 | 0.645 | `KEEP_SEPARATE_QUALITATIVE_STRING_BREAKING` | clean paper-defined string-breaking profile; single source convention distinct from scaling_normfact profiles. |
| `Ex_NP_d1.0fm_scaling_normfact.agr` | NP | 1.033 | 37 | 0.439904 | 2.12 | 2.458 | `EXCLUDE_FROM_TREND_KEEP_AS_OUTLIER_NOTE` | ordinary NP/scaling file, but profile has wide FWHM, high edge floor, and low peak significance; do not interpret as route broadening. |
| `beta6.3942dist789.agr` | PAPER_DEFINED | 1.064 | 29 | 0.27671 | 58.84 | 0.663 | `KEEP_SEPARATE_QUALITATIVE_STRING_BREAKING` | paper-defined qualitative string-breaking profile with central peak; separate from trusted scaling profiles. |
| `QCD_large_distances.agr` | PAPER_DEFINED | 1.216 | 29 | 0.140815 | 3.67 | 0.708 | `KEEP_SEPARATE_LARGE_DISTANCE_CONTROL` | large-distance normalized profile with central peak, but separate source convention and larger errors. |
| `beta6.3942dist789.agr` | PAPER_DEFINED | 1.216 | 29 | 0.181792 | 3.67 | 0.708 | `KEEP_SEPARATE_QUALITATIVE_STRING_BREAKING` | paper-defined qualitative string-breaking profile with central peak; separate from trusted scaling profiles. |
| `QCD_large_distances.agr` | PAPER_DEFINED | 1.235 | 28 | 0.562076 | 1.63 | 0.538 | `NORMALIZE_LATER_QUALITATIVE_ONLY` | large-distance normalized profile but low signal-to-noise and unstable width; not usable in current trend. |
| `QCD_large_distances.agr` | PAPER_DEFINED | 1.267 | 29 | 0.441594 | 1.57 | 1.272 | `NORMALIZE_LATER_QUALITATIVE_ONLY` | large-distance normalized profile but low signal-to-noise and unstable width; not usable in current trend. |
| `QCD_large_distances.agr` | PAPER_DEFINED | 1.368 | 29 | 0.196347 | 0.65 | 4.171 | `EXCLUDE_FROM_INTERPRETATION_FOR_NOW` | maximum occurs at boundary with very large errors; FWHM estimate is a parsing/noise artifact. |
| `beta6.3942dist789.agr` | PAPER_DEFINED | 1.368 | 29 | 0.253483 | 0.65 | 4.171 | `EXCLUDE_FROM_INTERPRETATION_FOR_NOW` | maximum occurs at boundary with very large errors; FWHM estimate is a parsing/noise artifact. |


## 4. Interpretation of the reviewed classes

### 4.1 `KEEP_SEPARATE_QUALITATIVE_STRING_BREAKING`

These profiles are real transverse profiles, but they come from `ANALISI_QUALITATIVA_STRING-BREAKING` source paths and are `PAPER_DEFINED` rather than the ordinary `FULL`/`NP` scaling-normalized class. They should be used in a separate qualitative string-breaking section, not in the main trusted trend.

Rows:

```
beta7.158dist13.agr       d = 0.960 fm
beta6.3942dist789.agr     d = 1.064 fm
beta6.3942dist789.agr     d = 1.216 fm
```

### 4.2 `KEEP_SEPARATE_LARGE_DISTANCE_CONTROL`

This row is a large-distance normalized profile with a central peak, but it belongs to the large-distance/string-breaking convention and has larger errors than the trusted scaling set. It may be used as a separate control point, not as part of the main fitted trend.

Row:

```
QCD_large_distances.agr   d = 1.216 fm
```

### 4.3 `NORMALIZE_LATER_QUALITATIVE_ONLY`

These large-distance profiles are potentially informative, but their signal-to-noise is low and the width estimates are unstable. They should be retained only as qualitative evidence until source conventions and normalization are inspected more carefully.

Rows:

```
QCD_large_distances.agr   d = 1.235 fm
QCD_large_distances.agr   d = 1.267 fm
```

### 4.4 `EXCLUDE_FROM_TREND_KEEP_AS_OUTLIER_NOTE`

This row comes from an ordinary NP scaling file, but it is an outlier relative to its group: wide FWHM, high edge floor, and low peak significance. It should not be interpreted as route broadening.

Row:

```
Ex_NP_d1.0fm_scaling_normfact.agr   d = 1.033 fm
```

### 4.5 `EXCLUDE_FROM_INTERPRETATION_FOR_NOW`

These rows are dominated by boundary/noise behavior. The maximum occurs at the boundary, and the FWHM value is therefore not a physical route-width estimate. They should be excluded from the current interpretation.

Rows:

```
QCD_large_distances.agr   d = 1.368 fm
beta6.3942dist789.agr     d = 1.368 fm
```

## 5. Practical decision for the formal flux-tube report

Use the following evidence structure:

```
Main trend:
  ACCEPT_FOR_TREND rows from QC only
  ordinary FULL / NP profiles
  d = 0.723–1.060 fm

Separate qualitative section:
  beta7.158dist13.agr
  beta6.3942dist789.agr at d = 1.064 and 1.216 fm

Separate large-distance control:
  QCD_large_distances.agr at d = 1.216 fm

Qualitative only / normalize later:
  QCD_large_distances.agr at d = 1.235 and 1.267 fm

Excluded from current interpretation:
  Ex_NP_d1.0fm_scaling_normfact.agr at d = 1.033 fm
  QCD_large_distances.agr at d = 1.368 fm
  beta6.3942dist789.agr at d = 1.368 fm
```

## 6. UNNS interpretation boundary

This inspection supports a clean next report, but it does not establish a route-broadening law.

The defensible UNNS conclusion is:

> The trusted Baker FULL/NP profiles provide a controlled localized-route geometry over d = 0.723–1.060 fm. The additional reviewed profiles indicate a possible large-distance/string-breaking evidence class, but those rows must remain separate until their normalization and source conventions are fully reconciled.

## 7. Files produced

```
reports/05_baker_review_separately_rows.md
reports/baker_review_separately_decisions.csv
reports/fig_baker_review_profiles_overlay.png
reports/fig_baker_review_snr.png
reports/fig_baker_review_width_flags.png
```
