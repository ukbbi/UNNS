# TokaMark One-Shot Array Probe Report — Shot 12063

## 1. Purpose

This document records the first controlled array-level extraction from the public TokaMark/MAST source for the UNNS-H Mode project.

It belongs here:

```text
unns_hmode_project/
  docs/
    18_TOKAMARK_ONE_SHOT_ARRAY_PROBE_REPORT.md
```

It follows:

```text
docs/
  17_TOKAMARK_METADATA_CANDIDATE_SCAN_REPORT.md
```

The purpose of this step was narrow and technical:

> Verify that the top-ranked public TokaMark candidate shot can be read at array level and that the diagnostic families needed for a future time-resolved `m_edge(t)` probe are extractable.

This report does not claim that shot `12063` is physically a positive-corridor discharge. It establishes that the required public diagnostic arrays can be extracted and summarized.

---

## 2. Source and target

Target shot:

```text
shot_id: 12063
```

Public source:

```text
https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12063.zarr/
```

Metadata source:

```text
https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12063.zarr/.zmetadata
```

Shot `12063` was chosen because the metadata scan ranked it as a `FULL_PROFILE_EDGE_CANDIDATE`, meaning it had metadata support for power/density traces, D-alpha-like edge response, Thomson Te/ne profiles, soft-X activity, and equilibrium geometry.

---

## 3. Probe method

The probe used:

```text
components/
  tokamark_one_shot_array_probe.py
```

The script avoided the earlier `zarr/s3fs` route because that route caused Windows async/hanging problems. Instead, it used:

```text
HTTPS .zmetadata request
direct HTTPS chunk requests
numcodecs decompression
compact CSV / JSON / Markdown output
```

This confirms that the project can access TokaMark arrays without relying on a fragile local `zarr/s3fs` environment.

---

## 4. Output files produced

The successful run produced:

```text
outputs/reports/
  tokamark_shot_12063_signal_probe.csv
  tokamark_shot_12063_signal_probe.json
  tokamark_shot_12063_signal_probe.md
  tokamark_shot_12063_proxy_timeseries_preview.csv
```

Run result:

```text
loaded arrays: 16
failed arrays: 0
```

This is the main operational gain: all selected arrays loaded successfully.

---

## 5. Loaded diagnostic families

The loaded arrays were:

```text
summary_power_nbi
summary_ip
interferometer_n_e_line
dalpha_voltage
soft_x_lower
soft_x_upper
thomson_t_e
thomson_n_e
equilibrium_q95
equilibrium_elongation
equilibrium_triangularity_upper
equilibrium_triangularity_lower
equilibrium_minor_radius
equilibrium_beta_normal
equilibrium_beta_pol
equilibrium_whmd
```

No selected array failed to load.

This confirms that shot `12063` is not merely a metadata candidate. It is an array-readable public MAST/TokaMark discharge suitable for a controlled UNNS-H Mode time-resolved diagnostic prototype.

---

## 6. Signal-level summary

| label                           | values_shape   | time_shape   |   finite_fraction |           median |             mean |              min |             max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|-----------------:|----------------:|--------------------:|-----------------:|
| summary_power_nbi               | (1712,)        | (1712,)      |          0.863902 |     -0.410069    |     -0.0143583   |     -1.58195     |     2.37293     |                   1 |                0 |
| summary_ip                      | (1712,)        | (1712,)      |          1        | 533124           | 422036           | -30424.3         |     1.09056e+06 |                   1 |                0 |
| interferometer_n_e_line         | (1712,)        | (1712,)      |          0.863902 |      5.17497e+19 |      4.2655e+19  |     -9.43505e+18 |     8.35795e+19 |                   1 |                0 |
| dalpha_voltage                  | (3, 21400)     | (21400,)     |          0.864439 |      0.136719    |      0.297777    |     -0.012207    |     1.85791     |                   4 |                0 |
| soft_x_lower                    | (18, 21400)    | (21400,)     |          0.864439 |      0.000152588 |      0.0122899   |     -0.00867844  |     0.181885    |                   8 |                0 |
| soft_x_upper                    | (18, 21400)    | (21400,)     |          0.864439 |      0.000610352 |      0.0088695   |     -0.0780869   |     0.154572    |                   8 |                0 |
| thomson_t_e                     | (120, 86)      | (86,)        |          0.421512 |    566.322       |    589.542       |      1.69646     |  1944.15        |                   1 |                0 |
| thomson_n_e                     | (120, 86)      | (86,)        |          0.421512 |      1.17177e+19 |      1.34884e+19 |      1.43788e+17 |     3.30007e+19 |                   1 |                0 |
| equilibrium_q95                 | (86,)          | (86,)        |          0.27907  |      7.33359     |      7.64875     |      6.60229     |    10.5101      |                   1 |                0 |
| equilibrium_elongation          | (86,)          | (86,)        |          0.27907  |      1.67092     |      1.72933     |      1.53669     |     1.97605     |                   1 |                0 |
| equilibrium_triangularity_upper | (86,)          | (86,)        |          0.27907  |      0.242472    |      0.255715    |      0.197949    |     0.366803    |                   1 |                0 |
| equilibrium_triangularity_lower | (86,)          | (86,)        |          0.27907  |      0.242472    |      0.252487    |      0.197949    |     0.331861    |                   1 |                0 |
| equilibrium_minor_radius        | (86,)          | (86,)        |          0.27907  |      0.465046    |      0.482708    |      0.434919    |     0.547053    |                   1 |                0 |
| equilibrium_beta_normal         | (86,)          | (86,)        |          0.27907  |      0.00356961  |      0.00371898  |      0.0015782   |     0.00837878  |                   1 |                0 |
| equilibrium_beta_pol            | (86,)          | (86,)        |          0.27907  |      0.0808708   |      0.0887838   |      0.0528466   |     0.188386    |                   1 |                0 |
| equilibrium_whmd                | (86,)          | (86,)        |          0.27907  |  51204.7         |  53787.6         |  22087.8         | 95270.6         |                   1 |                0 |

Key extracted shapes:

```text
D-alpha-like edge response:
  dalpha_voltage shape = (3, 21400)
  time shape           = (21400,)
  finite fraction      = 0.8644392523364486

Soft-X lower:
  shape                = (18, 21400)
  finite fraction      = 0.8644392523364486

Soft-X upper:
  shape                = (18, 21400)
  finite fraction      = 0.8644392523364486

Thomson Te:
  shape                = (120, 86)
  finite fraction      = 0.42151162790697677

Thomson ne:
  shape                = (120, 86)
  finite fraction      = 0.42151162790697677
```

The high-time-resolution D-alpha-like and soft-X signals cover approximately `-0.068 s` to `0.360 s`. Thomson and equilibrium signals provide coarser profile/equilibrium support over nearly the same interval.

---

## 7. Raw proxy summaries

| proxy                               |   finite_fraction |        median |          mean |          min |           max |           std |
|:------------------------------------|------------------:|--------------:|--------------:|-------------:|--------------:|--------------:|
| dalpha_median_across_channels       |          0.864439 |   0.090332    |   0.130248    | -0.00732422  |   1.44043     |   0.127262    |
| soft_x_lower_median_across_channels |          0.864439 |   0.00144958  |   0.00248548  | -0.00535965  |   0.0226784   |   0.00347418  |
| soft_x_upper_median_across_channels |          0.864439 |   0.00106812  |   0.00324847  | -0.00400543  |   0.0244904   |   0.00521353  |
| thomson_t_e_edge_median             |          0.360465 | 177.316       | 194.526       |  7.81743     | 590.428       | 128.163       |
| thomson_t_e_core_median             |          0.651163 | 391.699       | 415.271       | 21.3805      | 660.595       | 135.642       |
| thomson_t_e_edge_core_ratio         |          0.348837 |   0.378018    |   0.468726    |  0.0242326   |   1.49959     |   0.307893    |
| thomson_t_e_profile_gradient_proxy  |          0.662791 |  14.1349      |  14.5933      |  1.95986     |  30.6255      |   5.87292     |
| thomson_n_e_edge_median             |          0.360465 |   4.87797e+18 |   4.71113e+18 |  1.61641e+17 |   1.09487e+19 |   2.62166e+18 |
| thomson_n_e_core_median             |          0.651163 |   9.85051e+18 |   1.06473e+19 |  3.22478e+18 |   1.65401e+19 |   2.6315e+18  |
| thomson_n_e_edge_core_ratio         |          0.348837 |   0.551535    |   0.512369    |  0.0119414   |   1.03498     |   0.253777    |
| thomson_n_e_profile_gradient_proxy  |          0.662791 |   3.194e+17   |   3.13318e+17 |  7.95609e+16 |   6.2905e+17  |   1.66276e+17 |

The probe computed first-pass proxy summaries for D-alpha, soft-X, and Thomson profile-derived quantities. These are not final physics claims. They are raw diagnostic summaries used to determine whether the next `m_edge(t)` component has enough material to proceed.

---

## 8. Meaning for the UNNS-H Mode project

Before this step, the project had:

```text
TCV event-level model validation
TCV full-corpus extension
TCV time-resolved probe with no positive-boundary trace
TokaMark metadata evidence for possible candidate shots
```

After this step, the project has:

```text
a public MAST/TokaMark shot with extractable arrays
D-alpha-like edge-response signal available
soft-X activity signals available
Thomson Te/ne profiles available
equilibrium geometry available
power / density / current context available
```

This directly addresses the previous source gap. The project no longer lacks a public source candidate for the missing positive-boundary time-resolved probe.

---

## 9. What this establishes

This probe establishes five things.

### 9.1 Public array-level access works

Selected Zarr arrays were read successfully through direct HTTPS chunk requests.

### 9.2 Shot `12063` is technically usable

The shot contains all selected diagnostic families needed for the first time-resolved UNNS-H Mode prototype.

### 9.3 Edge-response diagnostics are present

The D-alpha-like and soft-X signals loaded with high time resolution, which is essential because the positive corridor is expected to involve edge-response dominance.

### 9.4 Profile diagnostics are present

Thomson Te and ne profiles loaded as two-dimensional profile/time arrays, allowing a first crude edge/profile evolution proxy.

### 9.5 Geometry diagnostics are present

q95, elongation, triangularity, minor radius, beta, and stored-energy-like equilibrium variables loaded successfully.

---

## 10. What this does not establish

This probe does not establish that shot `12063` is physically positive-corridor.

It does not identify:

```text
L-H transition time
D-alpha collapse time
pedestal formation interval
edge-gradient sharpening interval
soft-X event timing
m_edge(t)
```

It does not prove H-mode access, compare against negative or boundary-ambiguous MAST cases, or align all signals onto a common time base.

It also does not yet use explicit Thomson radial / flux coordinates. The current edge proxy assumes that the outer edge corresponds to the last 20% of profile indices, which is acceptable only as a raw first-pass probe.

---

## 11. Caution about units and preprocessing

Some extracted signals appear preprocessed or normalized rather than raw physical values. For example, `summary_power_nbi` includes negative values and `interferometer_n_e_line` includes negative values.

For the next step, treat these arrays as:

```text
TokaMark-preprocessed diagnostic signals
```

not automatically as raw engineering units.

This does not prevent `m_edge(t)` construction, but the first model should use robust normalized signal features rather than absolute physical thresholds.

---

## 12. Recommended next component

The next component should be:

```text
components/
  tokamark_m_edge_t_probe.py
```

Its task should be to align selected signals onto a common time base and compute the first MAST/TokaMark time-resolved UNNS-H Mode margin:

```text
S_power_balance(t)
S_transport(t)
S_edge_response(t)
C_edge_capacity(t)
F_route_fragmentation(t)
m_edge(t)
```

Recommended first target:

```text
shot_id = 12063
```

Recommended outputs:

```text
outputs/reports/
  tokamark_shot_12063_m_edge_t_probe.csv
  tokamark_shot_12063_m_edge_t_probe.json
  tokamark_shot_12063_m_edge_t_probe.md
```

The first `m_edge(t)` version should remain cautious and normalized:

```text
use robust percentile / z-score normalization
avoid absolute-unit threshold claims
treat D-alpha / soft-X / Thomson changes as structural proxies
report uncertainty and NaN coverage explicitly
```

---

## 13. Updated project status

```text
TokaMark diagnostic vocabulary:          confirmed
TokaMark shot split metadata:            confirmed
TokaMark public HTTP metadata access:    confirmed
TokaMark batch metadata scanning:        confirmed
Full diagnostic candidate shots:         found
Top target shot:                         12063
Array-level extraction for 12063:        complete
Failed selected arrays:                  0
Physical positive-corridor validation:   not yet
m_edge(t) construction:                  next
```

---

## 14. Final synthesis statement

The one-shot TokaMark array probe succeeded.

Shot `12063` is now confirmed as an array-readable public MAST/TokaMark discharge containing the diagnostic families needed for a future time-resolved UNNS-H Mode edge-margin prototype: power, current, line density, D-alpha-like edge response, soft-X activity, Thomson Te/ne profiles, and equilibrium geometry.

This does not yet prove that the shot is a positive-corridor discharge. It establishes the technical prerequisite for testing that claim.

The next decisive step is to construct a first normalized `m_edge(t)` probe for shot `12063`.
