# TokaMark Public Metadata Candidate Scan Report

## 1. Purpose

This report records the first successful public-source reconnaissance for a time-resolved MAST/TokaMark discharge suitable for the UNNS-H Mode positive-corridor validation gap.

The immediate project problem was:

```text
The TCV time-resolved probe covered boundary-ambiguous and negative-leakage cases,
but had no positive-boundary / edge-response time-resolved discharge.
```

The purpose of the TokaMark metadata scan was not to compute `m_edge(t)` yet.  
It was to answer a narrower source-acquisition question:

> Does a public TokaMark/MAST source contain shots with the signal families required for a future positive-corridor time-resolved UNNS-H Mode probe?

The answer is yes.

---

## 2. Scan input

The scan used:

```text
TokaMark_temporal_data_splits.csv
```

The scanner was:

```text
components/tokamark_metadata_candidate_scanner.py
```

The scanner queried public TokaMark shot metadata through HTTP requests to:

```text
https://s3.echo.stfc.ac.uk/mast/tokamark/v1/<shot_id>.zarr/.zmetadata
```

Only `.zmetadata` files were fetched.  
No full diagnostic arrays were downloaded.

This was deliberately chosen because the direct `zarr/s3fs` opening route caused Windows async/hanging issues, while the HTTP metadata route completed cleanly.

---

## 3. Scan scope

The first reconnaissance scan was intentionally small:

```text
scanned shots:               200
successful metadata fetches: 200
failed metadata fetches:     0
campaign filter:             none
split filter:                none
max shots:                   200
```

This was the correct scope.  
A full 11,188-shot survey is not needed at this stage.

The aim was simply to find whether viable candidates exist.

---

## 4. Target signal logic

The scanner ranked shots by the presence of signal families needed for a future UNNS-H Mode edge-response probe.

### 4.1 Core required signals

```text
summary-power_nbi
interferometer-n_e_line
spectrometer_visible-filter_spectrometer_dalpha_voltage
equilibrium-q95
equilibrium-elongation
equilibrium-triangularity_upper
equilibrium-triangularity_lower
equilibrium-minor_radius
```

These provide:

```text
power drive
line density
D-alpha-like edge response
equilibrium / geometry context
```

### 4.2 Preferred profile signals

```text
thomson_scattering-t_e
thomson_scattering-n_e
```

These are essential for edge/profile evolution and future `m_edge(t)` construction.

### 4.3 Preferred edge-activity signals

```text
soft_x_rays-horizontal_cam_lower
soft_x_rays-horizontal_cam_upper
```

These provide additional high-time-resolution edge/MHD response proxies.

### 4.4 Supporting signals

The scanner also tracked supporting signals such as:

```text
summary-ip
magnetics-ip
equilibrium-whmd
equilibrium-beta_normal
equilibrium-beta_pol
equilibrium-psi
equilibrium-q
pf_active-coil_current
pf_active-solenoid_current
magnetics-b_field_pol_probe_obr_field
```

These are useful for later context, but were not required for the first candidate classification.

---

## 5. Candidate-class result

The 200-shot scan returned:

```text
CORE_DALPHA_GEOMETRY_CANDIDATE: 110
FULL_PROFILE_EDGE_CANDIDATE:    45
LOW_PRIORITY:                   6
PARTIAL_DALPHA_CANDIDATE:       38
PROFILE_DALPHA_CANDIDATE:       1
```

The key result is:

```text
FULL_PROFILE_EDGE_CANDIDATE: 45
```

That means the scan found multiple shots containing the full required combination:

```text
power + density + D-alpha-like signal + equilibrium geometry
+ Thomson Te/ne profiles
+ soft-X-ray edge/activity signals
```

This confirms that TokaMark is a viable public source for the missing positive-corridor time-resolved search.

---

## 6. Top candidates

|   rank |   shot_id | campaign   | split_membership   |   candidate_score | candidate_class             |   core_required_present |   profile_preferred_present |   edge_activity_present |   supporting_present |
|-------:|----------:|:-----------|:-------------------|------------------:|:----------------------------|------------------------:|----------------------------:|------------------------:|---------------------:|
|      1 |     12063 | M5         | val                |            97.143 | FULL_PROFILE_EDGE_CANDIDATE |                       8 |                           2 |                       2 |                   10 |
|      2 |     12065 | M5         | train              |            97.143 | FULL_PROFILE_EDGE_CANDIDATE |                       8 |                           2 |                       2 |                   10 |
|      3 |     12069 | M5         | train              |            97.143 | FULL_PROFILE_EDGE_CANDIDATE |                       8 |                           2 |                       2 |                   10 |
|      4 |     12075 | M5         | train              |            97.143 | FULL_PROFILE_EDGE_CANDIDATE |                       8 |                           2 |                       2 |                   10 |
|      5 |     12076 | M5         | val                |            97.143 | FULL_PROFILE_EDGE_CANDIDATE |                       8 |                           2 |                       2 |                   10 |
|      6 |     12077 | M5         | train              |            97.143 | FULL_PROFILE_EDGE_CANDIDATE |                       8 |                           2 |                       2 |                   10 |
|      7 |     11823 | M5         | train              |            96.429 | FULL_PROFILE_EDGE_CANDIDATE |                       8 |                           2 |                       2 |                    9 |
|      8 |     11824 | M5         | val                |            96.429 | FULL_PROFILE_EDGE_CANDIDATE |                       8 |                           2 |                       2 |                    9 |
|      9 |     11825 | M5         | train              |            96.429 | FULL_PROFILE_EDGE_CANDIDATE |                       8 |                           2 |                       2 |                    9 |
|     10 |     11826 | M5         | train              |            96.429 | FULL_PROFILE_EDGE_CANDIDATE |                       8 |                           2 |                       2 |                    9 |

The highest-ranked candidate is:

```text
shot_id:          12063
campaign:         M5
split membership: val
candidate score:  97.143
candidate class:  FULL_PROFILE_EDGE_CANDIDATE
core:             8/8
profile:          2/2
soft-X:           2/2
support:          10/14
```

This is currently the best target for a controlled one-shot array probe.

---

## 7. Why shot 12063 matters

Shot `12063` contains all major diagnostic families required for the next step:

```text
summary-power_nbi
interferometer-n_e_line
spectrometer_visible-filter_spectrometer_dalpha_voltage
equilibrium-q95
equilibrium-elongation
equilibrium-triangularity_upper
equilibrium-triangularity_lower
equilibrium-minor_radius
thomson_scattering-t_e
thomson_scattering-n_e
soft_x_rays-horizontal_cam_lower
soft_x_rays-horizontal_cam_upper
```

The metadata shapes indicate usable time/profile coverage:

```text
summary-power_nbi:                                  [1712]
interferometer-n_e_line:                            [1712]
spectrometer_visible-filter_spectrometer_dalpha_voltage: [3, 21400]
equilibrium-q95:                                    [86]
thomson_scattering-t_e:                             [120, 86]
thomson_scattering-n_e:                             [120, 86]
soft_x_rays-horizontal_cam_lower:                   [18, 21400]
soft_x_rays-horizontal_cam_upper:                   [18, 21400]
```

This is enough to justify building a one-shot diagnostic probe.

---

## 8. What this establishes

This scan establishes four things.

### 8.1 Public metadata access works

The earlier HTTP metadata smoke test showed that the public TokaMark endpoint is reachable.  
This candidate scan confirms the same behavior at batch level: all 200 metadata fetches succeeded.

### 8.2 TokaMark contains full diagnostic candidates

The source is not merely a metadata listing.  
It contains shots with the complete signal families needed for a profile-resolved edge-response probe.

### 8.3 A positive-corridor source path now exists

The previous TCV source lacked positive-boundary time-resolved coverage.  
TokaMark now supplies candidate shots that can be tested for positive edge-response behavior.

### 8.4 The next step can be narrow

We do not need a full 11,188-shot scan.

The next technical step should focus on one top-ranked shot, starting with `12063`.

---

## 9. What this does not establish

This scan does not yet prove that shot `12063` is physically a positive-corridor discharge.

It only proves that shot `12063` has the required diagnostic coverage to test that question.

The scan does not compute:

```text
m_edge(t)
S_power_balance(t)
S_transport(t)
S_edge_response(t)
C_edge_capacity(t)
F_route_fragmentation(t)
```

It does not yet identify an L-H transition time.

It does not yet show D-alpha collapse, pedestal formation, edge-gradient sharpening, or soft-X response behavior.

Therefore, the correct claim is:

> TokaMark contains full-profile edge-response candidate shots suitable for a future positive-corridor probe.

not:

> TokaMark has already validated the positive corridor.

---

## 10. Recommended next component

The next component should be:

```text
components/
  tokamark_one_shot_array_probe.py
```

Its target should be:

```text
shot_id = 12063
```

Its job should be narrow:

```text
1. Fetch only selected arrays for shot 12063.
2. Save compact local summaries.
3. Extract time bases and value shapes.
4. Compute first raw proxies:
   - NBI power trace
   - line-density trace
   - D-alpha trace
   - soft-X activity trace
   - Thomson edge Te/ne profile evolution
   - equilibrium geometry traces
5. Do not yet compute final m_edge(t).
```

Expected outputs:

```text
outputs/reports/
  tokamark_shot_12063_signal_probe.csv
  tokamark_shot_12063_signal_probe.json
  tokamark_shot_12063_signal_probe.md
```

---

## 11. Project status update

```text
TokaMark diagnostic vocabulary:          confirmed
TokaMark shot split metadata:            confirmed
TokaMark public HTTP metadata access:    confirmed
TokaMark batch metadata scanning:        confirmed
Full diagnostic candidate shots:         found
Top target shot:                         12063
Physical positive-corridor validation:   not yet
One-shot array probe:                    next
m_edge(t) construction:                  after one-shot probe
```

---

## 12. Final synthesis statement

The TokaMark metadata candidate scan succeeded.

It found 45 `FULL_PROFILE_EDGE_CANDIDATE` shots in the first 200 scanned MAST shots, with zero failed metadata fetches.

The highest-ranked shot, `12063`, contains the full signal family needed for a future UNNS-H Mode time-resolved positive-corridor probe: power, density, D-alpha-like edge response, Thomson Te/ne profiles, soft-X-ray activity, and equilibrium geometry.

This does not yet validate a positive corridor physically.  
It does, however, solve the immediate source-acquisition problem:

> A public MAST/TokaMark source exists that can supply a candidate discharge for the missing positive-boundary time-resolved validation step.
