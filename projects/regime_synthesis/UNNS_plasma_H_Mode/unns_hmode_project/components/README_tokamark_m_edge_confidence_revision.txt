README_tokamark_m_edge_confidence_revision.txt

UNNS-H Mode Project
Component: tokamark_m_edge_confidence_revision.py

Purpose
-------
Add diagnostic confidence to the existing v0.1 TokaMark m_edge(t) outputs.

This follows:
  docs/24_DIAGNOSTIC_CONFIDENCE_REVISION_PLAN.md

It preserves:
  m_edge_raw(t)

and adds:
  Q_power
  Q_density
  Q_edge
  Q_profile
  Q_geometry
  Q_missing
  Q_diag
  P_missing_critical
  Q_capacity
  Q_fragmentation
  m_edge_conf
  m_edge_conf_state
  confidence_flag
  missing_critical_flags

Place
-----
  unns_hmode_project/components/tokamark_m_edge_confidence_revision.py
  unns_hmode_project/components/README_tokamark_m_edge_confidence_revision.txt

Run default five-shot panel
---------------------------
From project root:

  python components\tokamark_m_edge_confidence_revision.py --out-dir outputs\reports

Run one shot
------------
  python components\tokamark_m_edge_confidence_revision.py --shot-id 12063 --out-dir outputs\reports

Run custom panel
----------------
  python components\tokamark_m_edge_confidence_revision.py --shots 12063 11830 11876 11768 11776 --out-dir outputs\reports

Inputs
------
For each shot:

  outputs/reports/tokamark_shot_<SHOT>_m_edge_t_probe.csv
  outputs/reports/tokamark_shot_<SHOT>_signal_probe.json

Optional metadata:

  outputs/reports/tokamark_positive_corridor_metadata_candidates.csv

Outputs
-------
Per shot:

  outputs/reports/tokamark_shot_<SHOT>_m_edge_confidence_revision.csv
  outputs/reports/tokamark_shot_<SHOT>_m_edge_confidence_revision.json
  outputs/reports/tokamark_shot_<SHOT>_m_edge_confidence_revision.md

Panel:

  outputs/reports/tokamark_confidence_panel_comparison.csv
  outputs/reports/tokamark_confidence_panel_comparison.json
  outputs/reports/tokamark_confidence_panel_comparison.md

Next report
-----------
After running it, report the result as:

  docs/25_TOKAMARK_M_EDGE_CONFIDENCE_REVISION_RESULTS.md

Bounded claim
-------------
This is not physical H-mode validation. It tests whether the confidence correction
preserves the stronger structure of shot 12063 while suppressing incomplete
inflated cases such as 11776 and 11768.
