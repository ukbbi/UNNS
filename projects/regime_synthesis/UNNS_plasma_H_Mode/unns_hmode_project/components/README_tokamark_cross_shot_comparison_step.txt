README_tokamark_cross_shot_comparison_step.txt

UNNS-H Mode Project
Next step after docs/20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md

Files in this pack
------------------
1. tokamark_comparison_candidate_selector.py
2. tokamark_cross_shot_m_edge_comparator.py
3. README_tokamark_cross_shot_comparison_step.txt

Purpose
-------
Select one weaker / comparison TokaMark shot and compare it against reference
shot 12063 after running the same pipeline.

Recommended first weaker candidate
----------------------------------
Run the selector:

  python components\tokamark_comparison_candidate_selector.py --out-dir outputs\reports

On the current 200-shot scan, the expected recommendation is:

  shot 11830
  PROFILE_DALPHA_CANDIDATE
  core 8/8
  Thomson profiles 2/2
  soft-X 0/2

Why 11830?
----------
It is weaker than 12063 but still usable:
- keeps core required signals;
- keeps Thomson Te/ne profiles;
- lacks soft-X edge-activity support.

That makes it better than a LOW_PRIORITY shot for the first comparison, because
a very incomplete shot would mainly test missingness rather than structural
specificity.

Run the comparison-shot pipeline
--------------------------------
After selecting the shot, run:

  python components\tokamark_one_shot_array_probe.py --shot-id 11830 --out-dir outputs\reports

  python components\tokamark_m_edge_t_probe.py --shot-id 11830 --out-dir outputs\reports

  python components\tokamark_m_edge_trace_inspector.py --input outputs\reports\tokamark_shot_11830_m_edge_t_probe.csv --shot-id 11830 --out-dir outputs\reports

Then compare against 12063:

  python components\tokamark_cross_shot_m_edge_comparator.py --reference-shot 12063 --comparison-shot 11830 --out-dir outputs\reports

Expected outputs
----------------
Selector:
  outputs/reports/tokamark_comparison_candidate_selection.csv
  outputs/reports/tokamark_comparison_candidate_selection.json
  outputs/reports/tokamark_comparison_candidate_selection.md

Comparator:
  outputs/reports/tokamark_cross_shot_m_edge_comparison.csv
  outputs/reports/tokamark_cross_shot_m_edge_comparison.json
  outputs/reports/tokamark_cross_shot_m_edge_comparison.md

Decision logic
--------------
If the comparison shot reproduces the same coherent positive-window pattern as
shot 12063, v0.1 may be overbroad.

If the comparison shot lacks coherent positive windows or shows stronger
fragmentation/missingness, shot 12063 becomes structurally more meaningful.

Bounded claim
-------------
This is still not physical H-mode validation. It is a cross-shot structural
specificity test.
