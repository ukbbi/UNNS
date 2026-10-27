# GEO-I v004 — Arithmetic Obstructions and Stable Higher-Dimensional Geometry

A theorem-development release following GEO-I v003.  It attacks two questions about the geometric image `U_x` of the UNNS modular-move complex:
**(A)** does sufficient arithmetic depth (`q_i > o_i`) make the planar image acyclic? — **(B)** can embedding / obstruction in dimension 3 and 4 be decided by a finite criterion from the arithmetic relation lattice?

**Headline results** (details and honest status labels in `REPORT.md` / `MATHEMATICS.md`):

* The v003 guess "`q_i > o_i` ⇒ `β_1(U)=0`" is **false** (13 certified counterexamples with explicit primes, e.g. `x = 2^10·7^10/15`).  The corrected statement — `U = conv(F)` exactly when both scaled exponents are `≥ d` and not both equal `d` — is reduced by a proved translation lemma to a finite window per arithmetic type `(d,s)` and **certified for every type with `d ≤ 13`**; it is **open** for general `d`.
* A **finite template criterion** (T-REL / T-FIN) decides embeddedness of `K_abs` in any dimension, with proofs in both directions and an exact algorithm; it agrees with the exhaustive polyhedral audit on 10 852 + 1 450 (residues, box) cases.
* **Klein-four classification** in dimension 3 (two lattices, nine / seven minimal obstruction boxes, all of the "diagonal inside a 2-cell" type in a non-coordinate plane), the **O2 case** `b=5, (2,3), q=(4,4)` explained, a **genuinely 4D obstruction** `(1,1,1,1)` for the parity lattice, and a negative/nuanced answer to *essential dimensionality*: a residue-1 prime does not change the classification but does lower thresholds.
* Not achieved (and reported as such): a proof of stabilization for all `d`, closed-form atlases for all `(d,s)` and all `k`, a `k = 4` template atlas (UNAVAILABLE: too large).

## Run
Python 3.10+, `gmpy2` (exact rationals; `pip install gmpy2`), `matplotlib` (figures only).

    python3 verify.py --smoke     # a few minutes
    python3 verify.py             # full verification
    python3 experiments/figures.py

Windows: `RUN_SMOKE.bat`, `RUN_FULL.bat`.  Exit code 0 only if every **core** check passes.  Core checks use only files inside this folder, so the count is the same after a clean unzip; checks of sibling releases `GEO_I_v001..v003` (if present beside this folder) are *optional* and reported separately.
Reports: `output/reports/verify_full.json` (smoke: `output/smoke/`).

## Layout
* `REPORT.md` findings and gate status · `MATHEMATICS.md` definitions, theorems, proofs with **[P]/[C]/[O]/[Open]** labels · `PRIOR_ART.md` sources (verified / carried / unverified).
* `theory/` — `lattice_model.py` (scaling model `Lat(o1,o2,d,s)`), `coverage.py` (exact test `U = conv(F)`), `stabilization.py` (Programme A statement, prime realization), `obstruction_templates.py` (T-FIN engine), `arithmetic_criteria.py`.
* `experiments/` — `stabilization_certificate.py` (base-window certificates), `planar_stabilization.py` (window scans), `counterexample_search.py`, `validate_templates.py` / `obstruction_atlas.py` (template vs audit), `k2_atlas.py`, `klein_four.py`, `obstruction_kinds.py`, `essential_dimension.py`, `high_dimensional.py`, `benchmarks.py`, `figures.py`.
* `geometry/`, `topology/` — v003 exact machinery, unchanged · `frozen/` — v001/v002 arithmetic libraries, byte-identical (SHA-256 checked) · `tests/` — `test_geo3.py` (24, inherited), `test_geo4.py` (72).
* `output/data/` shipped exact data (certificates, atlases, validation runs) · `figures/` · `MANIFEST.sha256` (regenerate with `make_manifest.py`).

## Scope
v001–v003 and the Foundations manuscripts are neither modified nor re-released here; v003's non-sharp Klein-four threshold is recorded as an *erratum in this release*.  The topology of `U_x` refers to the parallelotope realization defined in v003; nothing here asserts an intrinsic topology of UNNS structures or any physical interpretation.
