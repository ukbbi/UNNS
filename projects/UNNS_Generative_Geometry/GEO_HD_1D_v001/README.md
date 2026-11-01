# GEO-HD-1D v001 -- Generative Histories and Global Route Geometry (D0-D2)
Start: `python RUN_VERIFY.py --fast` (stages V0..V9, seconds each), `python RUN_VERIFY.py --full`, `RUN_WINDOWS.bat`, `python -m pytest -q tests`.
Read first: `results/HD1D_REPORT.md`, then `theory/THEOREMS.md`, `results/OPEN_PROBLEMS.md`.
Layout: SPEC/ (the specification), theory/, src/ (builder modules + independent verifier `verify_hd1d.py`), data/ (D_B1..D_B5), results/, figures/, tests/.
Rules kept: exact integer arithmetic; frozen baselines untouched; bounded searches labelled BOUNDED; C3 not claimed; no novelty claim.
