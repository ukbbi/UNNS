README_tokamark_confidence_panel_selector.txt

UNNS-H Mode Project
Component: tokamark_confidence_panel_selector.py

Purpose
-------
Select a balanced moderate TokaMark panel for the v0.2 diagnostic-confidence
UNNS-H Mode test.

This follows:
  docs/26_TOKAMARK_MODERATE_CONFIDENCE_PANEL_PLAN.md

Place
-----
  unns_hmode_project/components/tokamark_confidence_panel_selector.py
  unns_hmode_project/components/README_tokamark_confidence_panel_selector.txt

Run
---
From project root:

  python components\tokamark_confidence_panel_selector.py --metadata outputs\reports\tokamark_positive_corridor_metadata_candidates.csv --per-class 6 --out-dir outputs\reports

Optional total panel size:

  python components\tokamark_confidence_panel_selector.py --panel-size 30 --out-dir outputs\reports

Outputs
-------
  outputs/reports/tokamark_moderate_confidence_panel_selection.csv
  outputs/reports/tokamark_moderate_confidence_panel_selection.json
  outputs/reports/tokamark_moderate_confidence_panel_selection.md

Default target
--------------
  6 FULL_PROFILE_EDGE_CANDIDATE
  6 PROFILE_DALPHA_CANDIDATE
  6 CORE_DALPHA_GEOMETRY_CANDIDATE
  6 PARTIAL_DALPHA_CANDIDATE
  6 LOW_PRIORITY

Always include anchors when available:
  12063
  11830
  11876
  11768
  11776

Next
----
Use the selected shot list to run the existing array/probe/confidence pipeline,
then report as:

  docs/27_TOKAMARK_MODERATE_CONFIDENCE_PANEL_RESULTS.md

Bounded claim
-------------
This selector only creates a balanced test panel. It does not validate H-mode
and does not rank physical success.
