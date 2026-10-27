# GEO-I v001 — Finite Fibre Geometry and Modular Boundaries
Separate active research project. The published UNNS_MATH_FOUNDATIONS repository was used read-only (commit fefa7910c807a5fdac90980749a5d7993e3ec0ca) and is unchanged.

Contents
- GEO_I_v001_REPORT.md — research note (definitions, proofs, benchmarks, open problems)
- code/geo1lib.py — exact-arithmetic library written from the Volume I/II definitions (A0, A2, C)
- code/geo1_verify.py — verifier, 24 checks (runtime ~15-25 min; rational-orbit block is time-limited)
- code/geo1_figures.py — figures (projections of exact data)
- tests/test_benchmarks.py — fast smoke tests (seconds)
- data/verify_recorded.json, verify_run.json, verify_log.txt — recorded output (24/24 PASS); benchmark fibres, relation tables, orbit data
- figures/ — fig1..fig6 PNG
- MANIFEST.sha256 — integrity manifest

Run: `python3 -I tests/test_benchmarks.py` ; `python3 -I code/geo1_verify.py` ; `sha256sum -c MANIFEST.sha256`
Requires Python 3 (+ numpy, matplotlib for figures only).

Known limits (stated in the report): G>1 evidence for the layer-count law is one orbit (g=11) plus proof; 23 of 36 random rational seeds were undetected within the step/time bounds (not failures). Label fix: the text "320 steps" in D5 of the first recorded run was corrected to "220 steps" (the value actually used); no results changed.
