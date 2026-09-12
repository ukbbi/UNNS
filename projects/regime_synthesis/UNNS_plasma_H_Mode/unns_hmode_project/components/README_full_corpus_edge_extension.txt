README.txt
UNNS-H Mode Project — Full 92-Event TCV Extension Pack

Purpose
-------
This pack extends the event-level UNNS-H Mode score from the nine manually reviewed
suspect shots to the full 92-row TCV canonical event corpus.

It also performs:
1. first full-corpus corridor/state summary;
2. first comparison against standard plasma variables;
3. first residual check of the UNNS margin;
4. inventory/probe of available time-resolved traces in LH_DATA.h5.

Important
---------
The previous 9-shot model used fragment-family tags from the chamber mapping stage.
The full-corpus extension cannot rely on such tags for every row. Therefore this
extension uses a tag-free numeric generalization of m_edge_event.

This means the full-corpus scores are not identical to the earlier 9-shot validation
scores. Treat this as v0.2 generalization, not as a replacement for the validated
9-shot v0.1 model.

Files produced
--------------
components/full_corpus_edge_event_extension.py
  Script to run the full-corpus score, residual comparison, and time-resolved inventory.

outputs/reports/tcv_full_corpus_edge_event_scores.csv
  One row per TCV event with computed m_edge_event, component scores, corridor, and state.

outputs/reports/tcv_full_corpus_state_summary.csv
  Summary by negative / ambiguous / positive margin state.

outputs/reports/tcv_full_corpus_corridor_summary.csv
  Summary by formal corridor.

outputs/reports/tcv_full_corpus_standard_vs_unns_comparison.csv
  Leave-one-out ridge comparison of standard-variable models and UNNS margin models.

outputs/reports/tcv_full_corpus_residual_analysis.csv
  Checks how much m_edge_event is explainable from standard variables.

outputs/reports/tcv_full_corpus_single_variable_auc.csv
  Single-variable ILH association ranking.

outputs/reports/tcv_time_resolved_corridor_inventory.csv
  Inventory and first edge-profile probe of available LH_DATA.h5 time-resolved traces.

docs/15_FULL_CORPUS_EDGE_EVENT_EXTENSION_REPORT.md
  Human-readable synthesis.

Run command
-----------
From project root:

PowerShell:
  python components\full_corpus_edge_event_extension.py --canonical data\processed\tcv_lh_events_canonical.csv --lh-data data\raw\tcv_zenodo_14996664\LH_DATA.h5 --out-dir outputs\reports

macOS / Linux:
  python components/full_corpus_edge_event_extension.py --canonical data/processed/tcv_lh_events_canonical.csv --lh-data data/raw/tcv_zenodo_14996664/LH_DATA.h5 --out-dir outputs/reports

Recommended placement
---------------------
Put the script here:
  unns_hmode_project/components/full_corpus_edge_event_extension.py

Put the report here:
  unns_hmode_project/docs/15_FULL_CORPUS_EDGE_EVENT_EXTENSION_REPORT.md

Keep CSV/JSON outputs here:
  unns_hmode_project/outputs/reports/

What this can claim
-------------------
This extension shows that m_edge_event can now be computed for the full 92-row
TCV event corpus without manual fragment tags.

What this cannot claim
----------------------
It does not prove the physical origin of H-mode.
It does not establish time-dependent m_edge(t).
It does not prove cross-machine generality.
It does not yet supply one time-resolved discharge per corridor if the available
LH_DATA.h5 traces do not cover all three states.
