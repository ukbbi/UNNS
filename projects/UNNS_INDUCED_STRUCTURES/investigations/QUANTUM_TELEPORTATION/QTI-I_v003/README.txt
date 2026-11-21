QTI-I v003 - Channel-conditioned analysis (research release, not a manuscript; Substrate unchanged; v001, v002 untouched).
Run (numpy, sympy; reads ../data/raw zips in place):
  python3 verification/qti_v003.py        # resumable (results/parts); rerun until it prints ALL PARTS DONE
  python3 verification/qti_v003_check.py  # exact structure checks S1-S6 + aggregation N0-N3, J1-J3 -> results/qti_v003_analysis.json (resumable, results/structure_cache.json)
