# UNNS Color Confinement - Regime Synthesis Note

**Admissibility-by-closure, repair thresholds, and localized route geometry**  
**Status:** synthesis of three formal diagnostics, not a derivation of QCD confinement.  
**Date:** 2026-07-11

---

## 1. Purpose

This note combines the three formal diagnostics produced in the UNNS + color confinement investigation:

```
01 First Confinement Diagnostic
02 Repair-Threshold Analysis
03 Flux-Tube Separation Extension
```

The aim is to state what color confinement now adds to the UNNS regime-synthesis program, while preserving the boundary between a structural UNNS interpretation and a full QCD derivation.

---

## 2. Core synthesis

The current evidence supports treating color confinement as a physical benchmark for **admissibility-by-closure**:

> Colored constituents may be internally real, but isolated colored externalization is not the admissible output. The observable route is tensioned, localized, and repaired into color-neutral composite channels.

In UNNS terms, the extracted sequence is:

```
internal colored coordinate
-> attempted route extension
-> localized route tension
-> repair-threshold window
-> admissible color-neutral composite route
```

This gives the color-confinement work a precise role in the wider regime-synthesis program: it is a microphysical case where **external observability requires route closure**, and where attempted forbidden externalization is handled by **route tension and repair**, not by free primitive isolation.

---

## 3. Diagnostics synthesized

| Diagnostic | Main data object | UNNS object extracted | Boundary |
|---|---|---|---|
| First Confinement Diagnostic | static-source spectrum + single flux-tube profile | route-extension coordinate, boundary-pressure proxy, localized route geometry | V0,V1,V2 are model-reconstructed; first Baker profile is author-ancillary pointwise data |
| Repair-Threshold Analysis | reported r_c and r_cs windows + reconstructed gap behavior | repair-threshold markers and channel-competition window | thresholds are reported; gap behavior comes from model-reconstructed spectrum |
| Flux-Tube Separation Extension | Baker ancillary profiles across source separations | route-localization geometry tracked across separation | main trend uses only QC-accepted FULL/NP rows; special rows kept separate |

---

## 4. Diagnostic 01 - first confinement map

The first diagnostic established the basic mapping:

```
quark separation r
-> route-extension coordinate

static spectrum V0(r), V1(r), V2(r)
-> boundary-pressure / route-tension spectrum

string-breaking threshold
-> repair-threshold marker

flux-tube transverse profile Ex(xt)
-> localized route geometry
```

Key data status:

- Static-source energy rows: **57**.
- Static separation range: **0.7069-1.6065 fm**.
- Static data status: **MODEL_RECONSTRUCTION_FROM_REPORTED_PARAMETERS_NOT_RAW_DATA**.
- First flux-tube pointwise profile rows: **31**.
- First flux-tube source separation: **0.738309 fm**.
- Peak Ex FULL: **0.343135 GeV^2**.
- Peak Ex NP: **0.244566 GeV^2**.
- Estimated NP FWHM: **0.551469 fm**.

![UNNS confinement sequence](fig_unns_confinement_sequence.png)

---

## 5. Diagnostic 02 - repair-threshold window

The second diagnostic isolated the threshold-window object. The reported string-breaking markers are:

| Marker | Channel | r [fm] | nearest reconstructed r [fm] | gap V1-V0 [GeV] | gap V2-V1 [GeV] |
|---|---|---:|---:|---:|---:|
| r_c | light static-light threshold | 1.224 | 1.22094 | 0.08970 | 0.04594 |
| r_cs | strange static-strange threshold | 1.293 | 1.28520 | 0.08642 | 0.04639 |

The UNNS reading is not simply that energy increases. The important object is:

```
stretched color route
-> threshold-window approach
-> competing screened channel
-> repaired admissible color-neutral composite route
```

This is the first concrete repair-window object in the color-confinement track.

![Repair-threshold proximity map](fig_repair_threshold_proximity_map.png)

---

## 6. Diagnostic 03 - flux-tube separation extension

The Baker extension populated a multi-separation flux-tube dataset:

- Pointwise rows parsed/loaded: **1090**.
- Profiles represented: **41**.
- Source files represented: **10**.
- Missing files: **0**.

The fourth QC pass then established the trend-safe subset:

- Accepted for trend: **30** rows.
- Review separately: **9** rows.
- Excluded from trend: **2** rows.
- Trusted trend separation range: **0.723-1.060 fm**.

The trusted trend set contains ordinary FULL and NP profiles only. PAPER_DEFINED, large-distance, wide/outlier, and single-point summary rows remain outside the main trend.

### Trusted trend summary

| Component | rows | d range [fm] | peak range [GeV^2] | FWHM range [fm] | mean area [GeV^2 fm] |
|---|---:|---:|---:|---:|---:|
| FULL | 15 | 0.723-1.060 | 0.195-0.387 | 0.530-0.663 | 0.195 |
| NP | 15 | 0.723-1.060 | 0.126-0.274 | 0.544-0.723 | 0.152 |

### Descriptive trends inside trusted rows only

These are descriptive slopes across the accepted subset, not a fitted confinement law:

| Component | Quantity | slope vs d | correlation |
|---|---|---:|---:|
| FULL | peak | -0.4914 | -0.964 |
| FULL | FWHM | 0.3764 | 0.963 |
| FULL | area | -0.1898 | -0.969 |
| NP | peak | -0.2739 | -0.888 |
| NP | FWHM | 0.3963 | 0.900 |
| NP | area | -0.0813 | -0.654 |

The safe qualitative reading is:

```
within 0.723-1.060 fm,
trusted FULL/NP profiles show a localized route geometry;
peak tends to weaken with separation;
FWHM tends to increase modestly;
special large-distance rows must remain separate until conventions are resolved.
```

![Trusted Baker peak trend](fig_baker_qc_peak_trusted.png)

![Trusted Baker width trend](fig_baker_qc_width_trusted.png)

---

## 7. Review-separately boundary

The review pass decides how to treat the nine non-trend rows:

| Treatment | Meaning |
|---|---|
| KEEP_SEPARATE_QUALITATIVE_STRING_BREAKING | useful as qualitative/paper-defined control, not a trend row |
| KEEP_SEPARATE_LARGE_DISTANCE_CONTROL | useful as large-distance control, not part of trusted trend |
| EXCLUDE_FROM_TREND_KEEP_AS_OUTLIER_NOTE | preserve as an outlier note, do not use for route-broadening claims |
| NORMALIZE_LATER_QUALITATIVE_ONLY | potentially useful after normalization/source-convention review |

Thus the formal flux-tube interpretation is deliberately limited to the accepted FULL/NP subset. The special rows are not discarded; they are held for a later large-distance/control analysis.

---

## 8. What color confinement now adds to UNNS

Color confinement adds a compact, data-grounded benchmark for a UNNS principle:

```
internal reality != external admissibility
```

The investigation now has three empirical handles:

1. **Route-extension coordinate:** static-source separation r or d.
2. **Boundary-pressure / route-tension proxy:** static-source spectrum and level gaps.
3. **Localized route geometry:** transverse longitudinal chromoelectric flux-tube profile.

Together, these support a regime-synthesis interpretation:

```
separation
-> localized tension
-> channel competition
-> repair threshold
-> closed admissible composite route
```

The result is especially useful because it aligns with other UNNS themes without forcing identity between them:

- Charge Boundary-Route Preservation: the route, not only the scalar charge, must close.
- Sobra/Sobtra threshold repair: attempted forbidden externalization is rerouted into lawful composites.
- H-mode comparison track: confinement transitions can be compared at the level of boundary organization, while preserving distinct physical mechanisms.

---

## 9. What is supported now

Supported by the current diagnostics:

- Color confinement is a valid benchmark for admissibility-by-closure.
- Static-source separation can be used as a route-extension coordinate.
- Reported string-breaking thresholds can be treated as repair-threshold markers.
- Level gaps provide channel-competition indicators in the repair window.
- Baker flux-tube profiles provide localized route-geometry samples.
- Trusted FULL/NP profiles support cautious separation-dependent route-localization analysis over 0.723-1.060 fm.

---

## 10. What is not yet supported

Not yet supported:

- A derivation of QCD confinement from UNNS.
- A final quantitative UNNS confinement law.
- Raw measured GEVP V0(r), V1(r), V2(r) pointwise lattice tables.
- Full covariance/uncertainty propagation across the reconstructed spectrum.
- A clean monotonic large-distance broadening claim using the PAPER_DEFINED or large-distance profiles.
- A cross-system confinement law connecting QCD, H-mode, and other regimes.

---

## 11. Next work item

The next work item is **not another broad data import**. It is:

```text
UNNS Color Confinement - Regime Synthesis Step 2
Build a threshold-local boundary-pressure proxy.
```

Minimum requirements before that proxy becomes quantitative:

1. Obtain or digitize measured V0(r), V1(r), V2(r) near r_c and r_cs.
2. Preserve the current model-reconstructed table only as a controlled reconstruction.
3. Keep trusted Baker FULL/NP profiles separate from paper-defined large-distance rows.
4. Define a first proxy only over rows with explicit data status.

A provisional proxy can be drafted symbolically as:

```
B_color(r) = normalized route-tension spectrum + gap-compression term + localized-profile width/peak term
```

but it should not be fitted until measured/digitized static levels are available.

---

## 12. Final synthesis statement

Color confinement now contributes a grounded regime-synthesis benchmark to UNNS:

> A colored constituent can be internally real while remaining externally inadmissible as an isolated object. The admissible observable is produced by route closure. Attempted separation produces localized tension and threshold-channel competition; the continuation is repair into color-neutral composite routes, not free color externalization.

This is sufficient to include color confinement in the UNNS regime-synthesis program as a structured benchmark of **admissibility-by-closure**, while preserving the explicit boundary that UNNS has not derived QCD confinement.
