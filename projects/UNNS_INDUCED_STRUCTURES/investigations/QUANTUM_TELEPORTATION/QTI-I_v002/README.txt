QTI-I v002 - QTI-I/A on all raw channels (research release, not a manuscript; Substrate unchanged).
Run (needs numpy, sympy; reads ../data/raw zips in place):
  python3 verification/qti_v002.py        # resumable: rerun until it prints the summary (parts cached in results/parts)
  python3 verification/qti_v002_check.py  # C1-C5 checks, writes results/qti_v002_analysis.json
results/parts/ = per-stream cache; verification/run.log = log of an interrupted first attempt (kept; deletion is off on the device).
