README_tokamark_moderate_confidence_panel_runner.txt

UNNS-H Mode Project
Component: tokamark_moderate_confidence_panel_runner.py

Purpose
-------
Run the moderate selected TokaMark confidence panel through the existing v0.2
pipeline.

This follows:
  docs/26_TOKAMARK_MODERATE_CONFIDENCE_PANEL_PLAN.md

Place
-----
  unns_hmode_project/components/tokamark_moderate_confidence_panel_runner.py
  unns_hmode_project/components/README_tokamark_moderate_confidence_panel_runner.txt

Required existing components
----------------------------
  components/tokamark_one_shot_array_probe.py
  components/tokamark_m_edge_t_probe.py
  components/tokamark_m_edge_trace_inspector.py
  components/tokamark_m_edge_confidence_revision.py

Run
---
From project root:

  python components\tokamark_moderate_confidence_panel_runner.py --selection outputs\reports\tokamark_moderate_confidence_panel_selection.csv --out-dir outputs\reports

Recompute all per-shot stages:

  python components\tokamark_moderate_confidence_panel_runner.py --selection outputs\reports\tokamark_moderate_confidence_panel_selection.csv --out-dir outputs\reports --force

Only aggregate existing outputs:

  python components\tokamark_moderate_confidence_panel_runner.py --selection outputs\reports\tokamark_moderate_confidence_panel_selection.csv --out-dir outputs\reports --skip-run

Outputs
-------
  outputs/reports/tokamark_moderate_confidence_panel_results.csv
  outputs/reports/tokamark_moderate_confidence_panel_results.json
  outputs/reports/tokamark_moderate_confidence_panel_results.md
  outputs/reports/tokamark_moderate_confidence_panel_runner.log

It also snapshots the generic confidence-revision panel outputs as:

  outputs/reports/tokamark_moderate_confidence_panel_results__raw_confidence_panel.csv
  outputs/reports/tokamark_moderate_confidence_panel_results__raw_confidence_panel.json
  outputs/reports/tokamark_moderate_confidence_panel_results__raw_confidence_panel.md

Next report
-----------
After running, report as:

  docs/27_TOKAMARK_MODERATE_CONFIDENCE_PANEL_RESULTS.md

Bounded claim
-------------
This runner does not validate H-mode physically. It tests whether v0.2 remains
methodologically stable across a controlled moderate panel.
