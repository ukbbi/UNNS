# Repair-Threshold Analysis

Second diagnostic for the UNNS + color confinement investigation.

This report focuses only on the reported string-breaking thresholds and the reconstructed static-source gap behavior around them. It does not claim that UNNS derives QCD confinement.

## 1. Data boundary

The static-source levels used here are `MODEL_RECONSTRUCTION_FROM_REPORTED_PARAMETERS_NOT_RAW_DATA`. They are useful for a controlled structural diagnostic, but they are not raw measured GEVP lattice points.

- Static rows total: 57
- Static separation range: 0.70686 to 1.6065 fm
- Rows inside threshold-analysis window: 17

## 2. Reported repair-threshold markers

| symbol | channel | reported r [fm] | nearest reconstructed r [fm] | gap V1-V0 [GeV] | gap V2-V1 [GeV] |
|---|---|---:|---:|---:|---:|
| r_c | light_static_light_threshold | 1.224 | 1.22094 | 0.0897 | 0.0459369 |
| r_cs | strange_static_strange_threshold | 1.293 | 1.2852 | 0.0864175 | 0.0463905 |

The two reported thresholds mark the light and strange screening channels. In UNNS language they are treated as repair-threshold markers, not as free-color externalization points.

## 3. Figures

### Repair-threshold energy-level window

![Repair-threshold energy levels](fig_repair_threshold_energy_levels_zoom.png)

### Repair-threshold gap window

![Repair-threshold gaps](fig_repair_threshold_gaps_zoom.png)

### UNNS repair-window marker

![Repair-threshold proximity map](fig_repair_threshold_proximity_map.png)

## 4. Diagnostic finding

The reconstructed spectrum places both reported string-breaking thresholds inside a region where the low-lying static-source gaps are compressed relative to the smaller-separation side. This makes the region suitable as the first UNNS repair-window object:

```
stretched color route
-> threshold-window approach
-> competing screened channel
-> repaired admissible color-neutral composite route
```

The relevant diagnostic is not simply that an energy rises. The relevant diagnostic is that the route-extension coordinate enters a channel-reorganization window where the forbidden output is not an isolated colored constituent but a screened/color-neutral composite channel.

## 5. UNNS object extracted

| Physics item | UNNS interpretation |
|---|---|
| separation r | route-extension coordinate |
| V0,V1,V2 static spectrum | boundary-pressure / route-tension spectrum |
| V1-V0 and V2-V1 gaps | channel-competition / repair-window indicators |
| r_c | light-channel repair-threshold marker |
| r_cs | strange-channel repair-threshold marker |
| screened two-meson channel | repaired admissible composite route |

## 6. What is supported

Supported by the current diagnostic:

- a concrete repair-threshold window around the reported light and strange string-breaking distances;
- a gap-based channel-competition diagnostic in that window;
- a clean UNNS mapping from route extension to threshold repair;
- preservation of the internal/external distinction: colored constituents remain internal coordinates, while external admissibility appears through color-neutral screened channels.

## 7. What is not yet supported

Not yet supported:

- a full measured-point analysis of V0(r), V1(r), V2(r);
- covariance/uncertainty propagation for the reconstructed spectrum;
- a fitted UNNS boundary-pressure law;
- a derivation of QCD confinement from UNNS.

## 8. Next required data/action

```
1. Obtain author or digitized measured V0,V1,V2 points around r_c and r_cs.
2. Extend Baker flux-tube profiles across separations approaching the onset of string breaking.
3. Build the first threshold-local boundary-pressure proxy only after measured/digitized static points are available.
```

## 9. Files produced

```
reports/repair_threshold_window_static_gaps.csv
reports/02_repair_threshold_analysis_metrics.json
reports/fig_repair_threshold_energy_levels_zoom.png
reports/fig_repair_threshold_gaps_zoom.png
reports/fig_repair_threshold_proximity_map.png
```