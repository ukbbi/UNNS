README_tokamark_physical_window_label_analyzer.txt

UNNS-H Mode Project
Component: tokamark_physical_window_label_analyzer.py

Purpose
-------
Analyze manually edited physical-window labels against the v0.2
diagnostic-confidence UNNS-H Mode traces.

This follows:
  docs/28_PHYSICAL_WINDOW_LABELING_REQUIREMENTS.md

It produces source evidence for:
  docs/29_PHYSICAL_WINDOW_LABELING_RESULTS.md

Place
-----
  unns_hmode_project/components/tokamark_physical_window_label_analyzer.py
  unns_hmode_project/components/README_tokamark_physical_window_label_analyzer.txt

Run
---
From project root:

  python components\tokamark_physical_window_label_analyzer.py --out-dir outputs\reports

Custom labels:

  python components\tokamark_physical_window_label_analyzer.py --labels outputs\reports\tokamark_physical_window_label_template_EDITED.csv --out-dir outputs\reports

Inputs
------
  outputs/reports/tokamark_physical_window_label_template_EDITED.csv
  outputs/reports/tokamark_shot_<SHOT>_m_edge_confidence_revision.csv

Outputs
-------
  outputs/reports/tokamark_physical_window_label_analysis.csv
  outputs/reports/tokamark_physical_window_label_analysis_by_label.csv
  outputs/reports/tokamark_physical_window_label_analysis_transition_pairs.csv
  outputs/reports/tokamark_physical_window_label_analysis.json
  outputs/reports/tokamark_physical_window_label_analysis.md

Important
---------
This script does not assign labels. It tests labels that were already edited.

The result is not broad physical H-mode validation. It is the first physical-window
alignment test.
