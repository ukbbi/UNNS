README_tokamark_physical_label_hardening_template.txt

UNNS-H Mode Project
Component: tokamark_physical_label_hardening_template.py

Purpose
-------
Create a hardening review CSV and markdown review sheet for provisional
physical-window labels.

This follows:
  docs/30_PHYSICAL_WINDOW_LABEL_HARDENING_PLAN.md

Place
-----
  unns_hmode_project/components/tokamark_physical_label_hardening_template.py
  unns_hmode_project/components/README_tokamark_physical_label_hardening_template.txt

Run
---
From project root:

  python components\tokamark_physical_label_hardening_template.py --out-dir outputs\reports

Inputs
------
  outputs/reports/tokamark_physical_window_label_template_EDITED.csv
  outputs/reports/tokamark_physical_window_label_analysis.csv
  outputs/reports/tokamark_physical_window_label_candidate_markers.csv

Outputs
-------
  outputs/reports/tokamark_physical_window_labels_HARDENING_REVIEW.csv
  outputs/reports/tokamark_physical_window_labels_HARDENING_REVIEW.md
  outputs/reports/tokamark_physical_window_labels_HARDENING_REVIEW_summary.json

Reviewer output
---------------
After manual review/editing, save:

  outputs/reports/tokamark_physical_window_labels_HARDENED_v0_1.csv

Then rerun:

  python components\tokamark_physical_window_label_analyzer.py --labels outputs\reports\tokamark_physical_window_labels_HARDENED_v0_1.csv --out-dir outputs\reports --prefix tokamark_physical_window_label_analysis_HARDENED_v0_1

Next report
-----------
  docs/31_PHYSICAL_WINDOW_LABEL_HARDENING_RESULTS.md

Important
---------
The UNNS margin columns are audit-only. They must not be used to decide the
physical label.
