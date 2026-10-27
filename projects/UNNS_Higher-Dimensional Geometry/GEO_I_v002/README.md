# GEO-I v002 — Intrinsic Arithmetic Geometry, Modular Lattice Moves, and Cell Complexes
Separate research release. GEO-I v001 and the published UNNS_MATH_FOUNDATIONS archive are unchanged (GitHub read-only, commit fefa7910c807a5fdac90980749a5d7993e3ec0ca).

Start with REPORT.md, then MATHEMATICS.md.
- verify.py            full verifier (26 checks, ~25 s); `--smoke` is a quick subset
- tests/test_geo2.py   fast deterministic tests
- geometry/geo2lib.py  exact engine (fibres, cubical cells, Graver region moves, homology mod p); geo1lib.py is a copy of the v001 arithmetic library
- geometry/*/          exported benchmark data, certified cells, Graver moves, corpus CSV and witnesses
- dynamics/            C-orbit geometry CSV, SELECT-II geometry-change summary
- experiments/         make_figures.py, export_data.py
- figures/, output/    figures; verifier JSON (verify_full.json, verify_smoke.json) and CSV exports
- RUN_SMOKE.bat / RUN_FULL.bat   Windows launchers (need Python 3; figures need numpy + matplotlib)
- MANIFEST.sha256      integrity: `sha256sum -c MANIFEST.sha256`

Limits (also in the report): M1 (b1 vs Graver relation rank) is a conjecture with recorded counterexamples; topology depends on the cell definition; no claim on composite/even g; literature references quoted from memory.
