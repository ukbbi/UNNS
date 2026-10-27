# GEO-I v010 — Modular Boundary Geometry and Obstruction-Rank Universality

Baseline: GEO-I v009 (documents in `docs_v009/`, figures in `figures_v009/`; v008, v007, v006 in `docs_v008/`, `docs_v007/`, `docs_v006/`). Nothing earlier is rewritten; SELECT-I/II, FIELD-I and the Foundations volumes are untouched; no remote repository was modified.

## Outcome

| Programme | Question | Outcome |
|---|---|---|
| **A — modular sail / hollow box** | G10-T1: `H0 ∖ U0 = int T1 ⊔ int T2`? | **PROVED+CHECKED** for all `d ≥ 5`, units `2 ≤ s ≤ d−2` (zonogon theorem G10-Z); `β1(U0) = 2` (G10-T1H). Exact check: all 6560 unit pairs `d ≤ 150`. G8-R1 becomes unconditional (G10-R1). |
| **B — cap** | G10-T2: `C_Q ⊆ U_Q` for nonexceptional small boxes? | **OPEN.** No proof; v009 evidence only. |
| consolidation | G10-T3: `U = H` | **OPEN** — needs only G10-T2 now. |
| **C — binary universality** | G10-C1: `r_min = 3` for every minimal box? | **OPEN**, with: G10-E1 (partition criterion), G10-F1 (full support: closes G8-C3), G10-A1, rigidity, and G10-T4: nullity six fully classified (215 minimal classes, all rank 3, all W2). A rank-4 box needs nullity ≥ 7; none found. |
| **D — certification** | new BOUNDARY and RANK6 certificates, standalone `checker10.py` | **PROVED+CHECKED** (453 + 222 certificates, tamper tests) |

Planar stabilization is therefore **half closed**: the hollow-box complement is a theorem; the cap is not. The universal rank-three statement is **not** proved; it is reduced to one concrete combinatorial property (W2).

## Layout
`MATHEMATICS.md` (registry and proofs), `REPORT.md`, `MODULAR_SAIL.md`, `HOLLOW.md`, `CAP.md`, `BINARY6.md`, `RANK_UNIVERSAL.md`, `CERTIFICATION.md`, `PRIOR_ART.md`, `THEOREM_REGISTRY.tsv`, `CONTEXT.md`; `theory/` (`modular_sail.py`, `binary6.py`, `binary5.py`, inherited modules), `experiments/`, `certificates/` (`checker10.py` standalone), `tests/test_geo10.py`, `figures/` (8), `output/data`, `output/reports`, `tools/` (C programs), `verify.py`, `RUN_SMOKE.bat`, `RUN_FULL.bat`, `MANIFEST.sha256`, `PROVENANCE.json`.

## Running
`RUN_SMOKE.bat` or `python verify.py --smoke` (minutes); `RUN_FULL.bat` or `python verify.py` (long). Python 3.10+, `gmpy2` for inherited planar routines, `matplotlib` for figures, optional `gcc` for the Burnside programs. New v010 checks and inherited checks are reported separately; `output/reports/verify_smoke.json` and `verify_full.json` are v010's own.

## Standing disciplines
Exact arithmetic; counterexamples preserved (FALSE transfer rules R-MIR, R-EUC, R-LAT); no fabricated references; statuses limited to PROVED, PROVED+CHECKED, CHECKED, FALSE, CORRECTED, OPEN, UNAVAILABLE.
