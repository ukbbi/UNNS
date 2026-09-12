README_reproduce_hardened_v0_1_from_review.txt

UNNS-H Mode Project
Component: reproduce_hardened_v0_1_from_review.py

Purpose
-------
Deterministically reproduce:

  outputs/reports/tokamark_physical_window_labels_HARDENED_v0_1.csv

from:

  outputs/reports/tokamark_physical_window_labels_HARDENING_REVIEW.csv

using the conservative v0.1 hardening rule documented in:

  docs/31A_REPRODUCIBILITY_PROTOCOL_HARDENED_LABELS.md

Place
-----
  unns_hmode_project/components/reproduce_hardened_v0_1_from_review.py
  unns_hmode_project/docs/31A_REPRODUCIBILITY_PROTOCOL_HARDENED_LABELS.md

Run
---
From project root:

  python components\reproduce_hardened_v0_1_from_review.py --review outputs\reports\tokamark_physical_window_labels_HARDENING_REVIEW.csv --out-dir outputs\reports

Expected outputs
----------------
  outputs/reports/tokamark_physical_window_labels_HARDENED_v0_1.csv
  outputs/reports/tokamark_physical_window_labels_HARDENED_v0_1_summary.json
  outputs/reports/tokamark_physical_window_labels_HARDENED_v0_1_SUMMARY.md

Important
---------
This reproduces the conservative hardened artifact. It does not provide
independent physical H-mode validation.
