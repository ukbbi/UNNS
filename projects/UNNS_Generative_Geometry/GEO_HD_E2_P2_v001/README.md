# GEO_HD_E2_P2_v001 — Arithmetic criteria for geometric transport between non-trivial relation lattices
Start with `results/P2_REPORT.md`; proofs in `theory/THEOREMS.md`; verdicts in `STATUS.json`.
Verify: `python RUN_VERIFY.py` (full) or `--fast`; tests: `python -m unittest discover -s tests`. Python ≥ 3.8, standard library only (figures need matplotlib: `python src/make_figures.py`).
Rebuild data: `python src/build_p2.py --out DIR` (~2.5 min).
Extract into `GEO_HD_1_PROJECT`: everything is new files; `ERRATA/E2_P1_ADDENDUM_001/002.md` record the two E2-P1 precision corrections. No E2-P1, HD-0 or frozen GEO-I file is modified.
Extra files beyond the requested tree: `src/inherited/` (byte-identical E2-P1 engine, `cell_transport.py` renamed `e1_cell_transport.py`), `ERRATA/`, `SPEC/E2_P1_ASSESSMENT_RECEIVED.md`, `theory/` additions as specified.
