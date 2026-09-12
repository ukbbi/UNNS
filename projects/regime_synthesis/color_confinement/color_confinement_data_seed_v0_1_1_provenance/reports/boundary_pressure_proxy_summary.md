# Boundary-Pressure Proxy Computation Summary

**Script:** compute_boundary_pressure_proxy.py  
**Version:** 0.3.0_STATIC_ONLY_EXACT_COLUMNS  
**Mode:** STATIC_ONLY_EXACT_COLUMNS  
**Status:** computed structural diagnostic proxy, not a fitted physical law

## Inputs

```text
static: C:\Users\igorc\Desktop\UNNS_SUBSTRATE(desktop)\TRANSFER\Bulk_2\REGIME_SYNTHESIS\Color confinement\color_confinement_data_seed_v0_1_1_provenance\reports\repair_threshold_window_static_gaps.csv
flux:   REMOVED_NOT_READ
```

## Exact columns used

```json
{
  "r": "r_fm",
  "gap01": "gap01_GeV",
  "gap12": "gap12_GeV",
  "slope01": "d_gap01_GeV_d_r_GeV_per_fm",
  "slope12": "d_gap12_GeV_d_r_GeV_per_fm"
}
```

## Outputs

```text
C:\Users\igorc\Desktop\UNNS_SUBSTRATE(desktop)\TRANSFER\Bulk_2\REGIME_SYNTHESIS\Color confinement\color_confinement_data_seed_v0_1_1_provenance\reports\boundary_pressure_proxy_table.csv
C:\Users\igorc\Desktop\UNNS_SUBSTRATE(desktop)\TRANSFER\Bulk_2\REGIME_SYNTHESIS\Color confinement\color_confinement_data_seed_v0_1_1_provenance\chamber_inputs\boundary_pressure_proxy_ladder.csv
```

## Threshold markers

```text
r_c  = 1.224 fm
r_cs = 1.293 fm
```

## Effective normalized weights

```json
{
  "gap": 0.4117647058823529,
  "threshold": 0.35294117647058826,
  "slope": 0.23529411764705885
}
```

## Proxy range

```text
rows: 17
min Pi_boundary_available: 0.2775715262695271
max Pi_boundary_available: 0.7657322066594006
mean Pi_boundary_available: 0.5462697703862975
min at r_fm: 1.12455
max at r_fm: 1.22094
max band: HIGH_BOUNDARY_PRESSURE_NEAR_REPAIR
```

## Band counts

```json
{
  "MILD_BOUNDARY_TENSION": 7,
  "ACTIVE_REPAIR_WINDOW_PRESSURE": 9,
  "HIGH_BOUNDARY_PRESSURE_NEAR_REPAIR": 1
}
```

## Boundary

This table is a structural UNNS diagnostic. It is not a QCD potential, not a
derivation of confinement, and not a universal fitted law.
