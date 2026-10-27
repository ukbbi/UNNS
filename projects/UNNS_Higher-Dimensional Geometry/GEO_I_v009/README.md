# GEO-I v009 — Targeted Proof Closure of Modular Geometry

Baseline: GEO-I v008 (kept frozen; its documents are in `docs_v008/`, v007 in `docs_v007/`, v006 in `docs_v006/`; v008 figures in `figures_v008/`). Nothing earlier is rewritten; SELECT-I/II, FIELD-I and the Foundations volumes are untouched; no remote repository was modified.

## What this release does
A proof-closure attempt on three questions, with an honest report of which closed:

| Programme | Question | Outcome |
|---|---|---|
| **A — hollow box** | G9-C1/T1: is `H0 \ U0` exactly the two triangles for all `d ≥ 3`, `s ≢ −1`? | **OPEN.** Continued-fraction induction not completed; extended exact survey (all units `d = 46..50`; structured `s` for `d = 73..110`, `853` pairs) finds no counterexample |
| **B — cap** | G9-CAP/T2: is `H_Q \ H_0 ⊆ U_Q` for every nonexceptional small box? | **OPEN.** Survey `d = 3..22` (all boxes, all units): no counterexample |
| **C — nullity five** | G9-C2/T4: do all minimal non-embedded boxes with nullity 5 have `r_min = 3`? | **PROVED+CHECKED: yes.** 12 reduced orbits, all rank 3 |
| scope | G9-Z: zero parity columns | **PROVED+CHECKED**: never in a minimal box (v008 census scope closed) |
| corollary | G9-T5 | every non-embedded box of nullity `≤ 5` has `r_min = 3`; a universal counterexample would need nullity `≥ 6` |
| consolidation | G9-T3 (`U = H`) | **OPEN** (needs G9-T1 and G9-T2) |

**This release does not close the planar stabilization question**, and it does not call itself a closure release.

## Layout
* `MATHEMATICS.md` (registry, G9-Z proof, nullity-5 theorem; v008 mathematics reproduced as Section A), `HOLLOW.md`, `CAP.md`, `BINARY5.md`, `CERTIFICATION.md`, `PRIOR_ART.md`, `REPORT.md`.
* `theory/binary5.py` (new engine: codewords, circuits, cells, collisions, witness rank, orbit enumeration under `GL(k,2)`), all v005–v008 modules unchanged.
* `experiments/`: `orbits5.py`, `binary5_attack.py`, `binary5_crosscheck.py`, `zero_column.py`, `hollow_attack9.py`, `cap_attack.py`, `make_certificates_v9.py`, `figures_v9.py`; `tools/burnside5.c` (independent orbit count; needs a C compiler to re-run).
* `certificates/` (`C5_rank5.json` new), `tests/test_geo9.py`, `output/data/v9_*`, `figures/` (7 figures), `verify.py`, `RUN_SMOKE.bat`, `RUN_FULL.bat`, `MANIFEST.sha256`, `PROVENANCE.json`.

## Running (Windows-safe short paths, no sibling folders needed)
`RUN_SMOKE.bat` (a few minutes) or `RUN_FULL.bat`; or `python verify.py --smoke` / `python verify.py`. Python 3.10+, `gmpy2` for the inherited planar routines (`pip install gmpy2`); `matplotlib` only for figures. New v009 checks and inherited checks are reported separately.

## Standing disciplines
Exact arithmetic; counterexamples preserved; no fabricated references (see `PRIOR_ART.md`: nothing new was searched in v009); statuses limited to PROVED, PROVED+CHECKED, CHECKED, FALSE, CORRECTED, OPEN, UNAVAILABLE.
