# GEO_HD_E2_P1_v001 — Geometric transport under a changing relation lattice

Read `results/E2_REPORT.md` first. Proofs: `theory/`. Verify: `python RUN_VERIFY.py` (full, ~35 s) or `--fast`; tests: `python -m unittest discover -s tests`.
Needs Python ≥ 3.8 (stdlib only). Figures need matplotlib + numpy (`python src/make_figures.py`; not needed for verification).

Extract into the existing `GEO_HD_1_PROJECT` directory: the package lives in its own folder `GEO_HD_E2_P1_v001/` and touches nothing else.

Gates: **EXACT_PASS** (29/29) · scientific: **COUNTEREXAMPLE** (L1–L5), **THEOREM_PASS** scoped, **OPEN** general law, **UNAVAILABLE** (4-D union topology, 3-D K_emb, interactive viewer). See `STATUS.json`.

Files beyond the requested tree: `src/build_e2.py` (generates data/ and results/E2_TRANSPORT.json, E2_COUNTEREXAMPLES.json; `--out DIR`) and `src/make_figures.py`.
No HD-0 or frozen GEO-I file is modified; STATUS.md, CHANGELOG.md and MANIFEST.json of the project are untouched.
