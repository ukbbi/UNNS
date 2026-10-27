# GEO-I v012 — Universal Planar Cap Closure

`GEO_I_v012.zip`: proof that `U_{d,s,Q} = conv(F_{d,s,Q})` for every `d>=2`, unit `s`, `Q1,Q2>=d`, `Q != (d,d)` (G12-T8, PROVED+CHECKED, conditional on the inherited G5-C1, G7-T1, G10-R1), built on the two proved gates G12-T1 (arithmetic strip inequality) and G12-T2 (uniform Graver steps), and a single cell family (G12-T3…T7) covering one-sided and mixed small boxes.
Contents: `VERIFICATION_STATUS.md` (what was and was not re-run), `MATHEMATICS.md` (all proofs), `ARITH_CAP.md`, `GRAVER_STRIP.md`, `MIXED_CAP.md`, `CERTIFICATION.md`, `REPORT.md`, `THEOREM_REGISTRY.tsv`, `PRIOR_ART.md`, `CONTEXT.md`; `theory/cap_cover.py`; `certificates/` (ARITH, CAPCOVER2, checker12); `tests/test_geo12.py`; `verify.py`; older documents in `docs_v006…docs_v011`.
Run: `python verify.py --smoke` (~10 min) or `python verify.py` (~15 min; inherited full v011/v010 gate NOT_RERUN - frozen baseline verified; add `--rerun-inherited-full` for the 2 h re-execution). Python 3.10+, gmpy2. `RUN_SMOKE.bat`, `RUN_FULL.bat`. Verify from a clean unzip.
v001–v011 are preserved (W2, universal rank 3); nothing in the frozen Foundations changed.
