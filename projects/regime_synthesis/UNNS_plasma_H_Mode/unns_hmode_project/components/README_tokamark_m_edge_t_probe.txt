README_tokamark_m_edge_t_probe.txt

UNNS-H Mode Project
Component: tokamark_m_edge_t_probe.py

Purpose
-------
Compute the first normalized time-resolved UNNS-H Mode edge-admissibility margin
for one public TokaMark/MAST shot.

This component follows:
  tokamark_one_shot_array_probe.py

It computes first versions of:
  S_power_balance(t)
  S_transport(t)
  S_edge_response(t)
  C_edge_capacity(t)
  F_route_fragmentation(t)
  m_edge(t)

Placement
---------
Place the script here:

  unns_hmode_project/components/tokamark_m_edge_t_probe.py

Place this README here:

  unns_hmode_project/components/README_tokamark_m_edge_t_probe.txt

Install
-------
Run:

  python -m pip install requests numpy pandas numcodecs

The script intentionally avoids zarr/s3fs because that route caused Windows
hanging / async shutdown behavior in earlier tests.

Run
---
From project root:

  python components\tokamark_m_edge_t_probe.py --shot-id 12063 --out-dir outputs\reports

Optional controls:

  --dt 0.001
    Common time-grid spacing in seconds.

  --edge-fraction 0.20
    Outer fraction of Thomson profile indices used as crude edge proxy.

Outputs
-------
  outputs/reports/tokamark_shot_12063_m_edge_t_probe.csv
  outputs/reports/tokamark_shot_12063_m_edge_t_probe.json
  outputs/reports/tokamark_shot_12063_m_edge_t_probe.md

Formula v0.1
------------
S_power_balance(t):
  0.70 * normalized NBI pressure
  + 0.30 * density deviation pressure

S_transport(t):
  0.40 * Te profile-gradient pressure
  + 0.40 * ne profile-gradient pressure
  + 0.10 * Te edge/core deviation pressure
  + 0.10 * ne edge/core deviation pressure

S_edge_response(t):
  0.40 * D-alpha suppression/quiescence feature
  + 0.30 * soft-X activity feature
  + 0.30 * profile sharpening feature

C_edge_capacity(t):
  0.50 * S_edge_response(t)
  + 0.25 * density_support(t)
  + 0.25 * geometry_stability(t)

F_route_fragmentation(t):
  0.45 * S_power_balance(t)
  + 0.45 * S_transport(t)
  + 0.10 * missingness_pressure(t)

m_edge(t):
  C_edge_capacity(t) - F_route_fragmentation(t)

Important limitations
---------------------
This is a first normalized structural probe.

It does not prove H-mode.
It does not identify L-H transition time.
It does not classify shot 12063 physically.
It uses within-shot robust normalization.
It treats TokaMark arrays as preprocessed diagnostic signals, not raw units.
It uses a crude Thomson edge approximation: last 20 percent of profile indices.

Next document
-------------
After running, report the result as:

  docs/19_TOKAMARK_M_EDGE_T_PROBE_REPORT.md
