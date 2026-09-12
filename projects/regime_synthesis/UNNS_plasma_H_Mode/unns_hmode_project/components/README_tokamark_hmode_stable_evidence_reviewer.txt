README_tokamark_hmode_stable_evidence_reviewer.txt

UNNS-H Mode Project
Component: tokamark_hmode_stable_evidence_reviewer.py

Purpose
-------
Generate a focused evidence review for excluded H_MODE_STABLE candidate windows.

This follows:
  docs/32_H_MODE_STABLE_EVIDENCE_RECOVERY_PLAN.md

Place
-----
  unns_hmode_project/components/tokamark_hmode_stable_evidence_reviewer.py
  unns_hmode_project/components/README_tokamark_hmode_stable_evidence_reviewer.txt

Run
---
From project root:

  python components\tokamark_hmode_stable_evidence_reviewer.py --out-dir outputs\reports

Inputs
------
  outputs/reports/tokamark_physical_window_labels_HARDENED_v0_1.csv
  outputs/reports/tokamark_physical_window_label_candidate_markers.csv
  outputs/reports/tokamark_physical_window_label_preview_shot_<SHOT>.csv
  outputs/reports/tokamark_shot_<SHOT>_m_edge_confidence_revision.csv

Outputs
-------
  outputs/reports/tokamark_hmode_stable_evidence_review.csv
  outputs/reports/tokamark_hmode_stable_evidence_review.md
  outputs/reports/tokamark_hmode_stable_evidence_review_summary.json

Important
---------
This script does NOT auto-accept H_MODE_STABLE labels.
UNNS audit columns are included only for later comparison.

Manual next step
----------------
Edit:

  outputs/reports/tokamark_hmode_stable_evidence_review.csv

Then create:

  outputs/reports/tokamark_physical_window_labels_HARDENED_v0_2.csv

Next report
-----------
  docs/33_H_MODE_STABLE_EVIDENCE_RECOVERY_RESULTS.md
