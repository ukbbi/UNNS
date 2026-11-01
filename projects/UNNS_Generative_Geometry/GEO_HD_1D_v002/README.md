# GEO-HD-1D v002 -- threshold theory of swap classes
Builds on GEO_HD_1D_v001 (untouched; its builder modules are copied byte-identically and pinned in results/V001_PINS.json).
Read `theory/THEOREMS_V002.md`. Verify: `python RUN_VERIFY.py --fast` (stages W0..W6, W2b) or `--full`; `RUN_WINDOWS.bat`; `python -m pytest -q tests`.
New code: src/thresholds.py (K(w), induced graphs, lcm-closure, connection thresholds), src/build_v002.py (census), src/verify_v002.py (independent verifier).
Scope: histories from a FIXED source; complete histories need a squarefree source. C3 not claimed.
