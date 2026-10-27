# GEO-I v003 — Abstract and Embedded Geometry of the Modular-Move Complex

v003 asks which parts of the higher-dimensional UNNS fibre geometry are **forced by the arithmetic** and which depend on how the cells are drawn. It separates three objects: the abstract complex `K_abs` (v002), its geometric image `U_x` in exponent space, and (where it exists) an exact embedded subdivision `K_emb`.

* `REPORT.md` — findings, data tables, figures, gate status.
* `MATHEMATICS.md` — definitions, theorems and proofs, open problems.
* `PRIOR_ART.md` — sources, what was verified, what is not claimed.

## Run
Python 3.9+ with `matplotlib` (figures only) and `gmpy2` (optional speed-up; falls back to `fractions`).

    python verify.py --smoke            # about a minute or two
    python verify.py                    # full verifier
    python verify.py --orbits-exhaustive   # also recompute every cached orbit state (hours)
    python figures/make_figures.py      # regenerate the figures

Windows: `RUN_SMOKE.bat`, `RUN_FULL.bat`. Exit code 0 only if every check passes. Results go to `output/reports/verify_<mode>.json`; data tables to `output/data/`, certificates to `output/certificates/`.

## Layout
`geometry/` exact intersections, LP, realization, subdivision, validation, Graver arithmetic · `topology/` chain complexes (exact rank over Q), Betti comparison (abstract / nerve / clique) · `experiments/` E1–E10 · `frozen/` the v002 arithmetic libraries, byte-identical (SHA-256 checked) · `tests/` unit tests · `MANIFEST.sha256` file hashes.

## Honest limits
Everything is exact (integers / rationals), but the orbit data (E9) are cached records produced by the same code; the verifier recomputes a deterministic sample (all with `--orbits-exhaustive`). Where a computation exceeded its budget the record says `UNAVAILABLE` and the case is not counted as a success. Open questions are listed in `MATHEMATICS.md` §8.
