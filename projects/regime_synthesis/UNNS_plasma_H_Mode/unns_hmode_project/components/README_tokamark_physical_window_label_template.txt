README_tokamark_physical_window_label_template.txt

UNNS-H Mode Project
Component: tokamark_physical_window_label_template.py

Purpose
-------
Generate independent physical-window labeling templates after the v0.2
diagnostic-confidence method passed the moderate TokaMark panel.

This follows:
  docs/28_PHYSICAL_WINDOW_LABELING_REQUIREMENTS.md

Place
-----
  unns_hmode_project/components/tokamark_physical_window_label_template.py
  unns_hmode_project/components/README_tokamark_physical_window_label_template.txt

Run
---
From project root:

  python components\tokamark_physical_window_label_template.py --out-dir outputs\reports

Custom shots:

  python components\tokamark_physical_window_label_template.py --shots 12046 11941 12055 12007 12017 12063 11768 11776 --out-dir outputs\reports

Default shots
-------------
  12046
  11941
  12055
  12007
  12017
  12063
  11768
  11776

Outputs
-------
  outputs/reports/tokamark_physical_window_label_template.csv
  outputs/reports/tokamark_physical_window_label_candidate_markers.csv
  outputs/reports/tokamark_physical_window_label_review.md
  outputs/reports/tokamark_physical_window_label_summary.json
  outputs/reports/tokamark_physical_window_label_preview_shot_<SHOT>.csv

Important
---------
This script does NOT assign final physical labels.
It only creates candidate review windows and an editable label template.

Physical labels must be assigned independently of UNNS columns.

Allowed labels
--------------
  L_MODE
  LH_TRANSITION
  H_MODE_STABLE
  PRE_ELM
  POST_ELM
  HL_BACK_TRANSITION
  AMBIGUOUS
  UNLABELABLE

Next report
-----------
After manual labels are filled:

  docs/29_PHYSICAL_WINDOW_LABELING_RESULTS.md
