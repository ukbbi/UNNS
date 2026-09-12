README_tokamark_m_edge_trace_inspector.txt

Purpose
-------
Inspect the generated m_edge(t) trace for TokaMark shot 12063 and decide whether
positive and negative margin intervals have interpretable diagnostic structure.

Place:
  unns_hmode_project/components/tokamark_m_edge_trace_inspector.py

Install:
  python -m pip install numpy pandas

Run:
  python components\tokamark_m_edge_trace_inspector.py --input outputs\reports\tokamark_shot_12063_m_edge_t_probe.csv --out-dir outputs\reports

Outputs:
  outputs/reports/tokamark_shot_12063_m_edge_trace_inspection_windows.csv
  outputs/reports/tokamark_shot_12063_m_edge_trace_inspection_summary.json
  outputs/reports/tokamark_shot_12063_m_edge_trace_inspection.md

This component does not prove H-mode, identify L-H transition time, or revise
the v0.1 formula. It is trace-level triage before cross-shot comparison or
formula adjustment.
