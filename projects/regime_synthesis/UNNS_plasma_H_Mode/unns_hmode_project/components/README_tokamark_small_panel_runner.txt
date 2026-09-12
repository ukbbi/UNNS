README_tokamark_small_panel_runner.txt

UNNS-H Mode Project
Component: tokamark_small_panel_runner.py

Purpose
-------
Run a small multi-shot TokaMark/MAST comparison panel using the same pipeline
already used for shot 12063.

This follows:
  docs/21_TOKAMARK_CROSS_SHOT_M_EDGE_COMPARISON.md

Default panel
-------------
  12063  FULL_PROFILE_EDGE_CANDIDATE        reference
  11830  PROFILE_DALPHA_CANDIDATE          profile/no-softX weaker control
  11876  CORE_DALPHA_GEOMETRY_CANDIDATE    core+softX/no-Thomson control
  11768  PARTIAL_DALPHA_CANDIDATE          partial candidate
  11776  LOW_PRIORITY                      stress-test / weak candidate

Place
-----
  unns_hmode_project/components/tokamark_small_panel_runner.py
  unns_hmode_project/components/README_tokamark_small_panel_runner.txt

Dependencies
------------
  python -m pip install requests numpy pandas numcodecs

Required existing components
----------------------------
The runner calls these scripts from the components folder:

  tokamark_one_shot_array_probe.py
  tokamark_m_edge_t_probe.py
  tokamark_m_edge_trace_inspector.py

Run
---
From project root:

  python components\tokamark_small_panel_runner.py --out-dir outputs\reports

Recompute everything:

  python components\tokamark_small_panel_runner.py --out-dir outputs\reports --force

Only aggregate existing outputs:

  python components\tokamark_small_panel_runner.py --out-dir outputs\reports --skip-run

Custom shots:

  python components\tokamark_small_panel_runner.py --shots 12063 11830 11876 11768 --out-dir outputs\reports

Outputs
-------
  outputs/reports/tokamark_small_panel_m_edge_comparison.csv
  outputs/reports/tokamark_small_panel_m_edge_comparison.json
  outputs/reports/tokamark_small_panel_m_edge_comparison.md
  outputs/reports/tokamark_small_panel_runner.log

Next document
-------------
After the run, report the result as:

  docs/22_TOKAMARK_SMALL_PANEL_M_EDGE_COMPARISON.md

Bounded claim
-------------
This is still not physical H-mode validation. It tests whether the normalized
UNNS-H Mode margin distinguishes the reference shot from several weaker public
TokaMark candidates.
