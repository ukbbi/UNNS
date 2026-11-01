# GEO-HD-1B / E2-P3 v001 — Realized Geometric Transport

Extract this ZIP into `GEO_HD_1_PROJECT/` (it creates `GEO_HD_E2_P3_v001/`; nothing existing is overwritten).
Run `RUN_WINDOWS.bat` (or `python -I RUN_VERIFY.py --fast`).  `--full` re-derives every row; `python src/build_p3.py --out DIR` rebuilds (deterministic).

Read first: `results/P3_REPORT.md`, then `theory/THEOREMS.md`, `results/P3_THEOREM_AUDIT.md`, `theory/COUNTEREXAMPLES.md`, `ERRATA/`.

Organizing principle: Coverage-Gap Reduction U ⊆ U′ ⇔ U ∩ (H′∖U′) = ∅.

Extra files beyond the specification tree: `ERRATA/` (append-only addenda for E2-P2), `SPEC/E2_P2_ASSESSMENT_RECEIVED.md`, `src/audit_p3.py`, `src/certificate_check.py`,
`src/finalize_p3.py`, `src/p2/` (hash-pinned E2-P2 modules), `data/E2P2_SEARCH_CORPUS_REFERENCE.json`, `tests/_path.py`.
