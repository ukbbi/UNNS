# GEO-I v011 — Cap Closure and Circuit-Partition Universality

**Headline.** (1) **W2 is proved**: every minimal non-embedded binary box has ≥ 2 (for `p ≥ 9`, ≥ `p−1`) two-circuit partitions of the all-ones word, hence **universal minimum witness rank 3** (G11-T3/T4); a rank-4 minimal box does not exist. (2) **The planar cap is not closed**: the one-sided cap has an explicit verified cell family (CHECKED, reduced to an arithmetic lemma), the mixed case and G11-T1/T2 remain OPEN.

Start with `REPORT.md`, then `MATHEMATICS.md` (§1 proofs), `CIRCUIT_PARTITIONS.md`, `CAP.md`, `RANK_UNIVERSAL.md`, `CERTIFICATION.md`, `PRIOR_ART.md`, `THEOREM_REGISTRY.tsv`, `CONTEXT.md`. v010 documents are archived unchanged in `docs_v010/`.

## Run
Python ≥ 3.10, `gmpy2` (pip install gmpy2); matplotlib only for figures.
* `RUN_SMOKE.bat` / `python verify.py --smoke` — several minutes.
* `RUN_FULL.bat` / `python verify.py` — ≈ 2 h (includes the full inherited v010 gate).
* `python tests/test_geo11.py` — new unit tests.
* `python -I certificates/checker11.py certificates/C9_partition.json certificates/C10_capcover.json` — standalone certificate check.
* `python experiments/w2_attack.py [--k5]`, `python experiments/cap_attack11.py` regenerate `output/data/v11_w2.json`, `v11_cap.json`.

Frozen: v001–v010 records and both Mathematical Foundations volumes. Inherited vs new files: `PROVENANCE.json`.
