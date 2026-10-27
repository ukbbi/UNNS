# GEO-I v009 — Programme D: certificates, validation paths, adversarial verification

Four reviews are kept **separate**: (1) *proof review* — the arguments in MATHEMATICS/BINARY5, read by a human; (2) *exact recomputation* — `theory/` and `experiments/` regenerate data in exact integer/rational arithmetic; (3) *certificate verification* — `certificates/checker8.py`, a standalone program (standard library only, imports nothing from this release, run with `python3 -I`); (4) *integrity checking* — `MANIFEST.sha256` and `PROVENANCE.json`. A passing certificate check never validates a universal proof.

## 1. Certificates (checker8.py, unchanged from v008)
| Kind | Files | Status in v009 |
|---|---|---|
| COVER, GAP, HOMOLOGY, RANK | `C1_cover.json`, `C2_gap.json`, `C3_homology.json`, `C4_rank.json` (v008, 40 certificates) | inherited, still accepted |
| D1_coverage, D2_rank, D3_hollow | v007 files (19 records; v008 documents stated 20 — the files contain 19) | inherited, still accepted |
| **RANK (new)** | `C5_rank5.json` — the 12 minimal nullity-5 boxes: columns, `min_rank = 3`, `nullity = 5`, reduced support | **new in v009**: all 12 accepted; tampered `min_rank`, `nullity`, or a dropped column are rejected (`tests/test_geo9.py`) |
No new COVER or GAP certificates are needed: no new planar theorem was proved and no planar counterexample exists (a valid GAP outside `T1 ∪ T2` would be one).

## 2. Two independent validation paths
| Result | Path 1 | Path 2 |
|---|---|---|
| nullity-5 classification | `theory/binary5.py` (own codeword, circuit, cell and rank code) | v006/v008 stack: `binary_01`, `centre_collisions`, `rank_reduction` (785 supports, 0 disagreements) |
| orbit completeness (k=5) | python orbit generator (1371 non-empty orbits) | Burnside over all of `GL(5,2)`, `tools/burnside5.c` (1372 including `∅`) |
| minimal boxes' rank | `binary5.min_rank` | `checker8.check_RANK` (independent recomputation inside the standalone checker) |
| G9-Z | proof (MATHEMATICS §1) | exhaustive recomputation: all 6,763 matrices with a zero column, `m ≤ 3, n ≤ 8` (`zero_column.py`) |
| planar surveys | v005 all-cells exact polygon subtraction | the `GAP`/`COVER` certificate kinds of the checker (inherited sample) |
Supports with `> 16` points are classified by path 1 only (541 supports); this is a single-path result for non-minimal supports.

## 3. Outcome vocabulary
*Counterexample found* — none in any programme. *No counterexample within completed scope* — hollow and cap surveys (ranges in HOLLOW.md, CAP.md). *Search incomplete* — everything beyond these ranges; nullity `≥ 6`. *General theorem proved* — G9-Z, G9-T4, G9-T5 only. Computations exceeding limits are reported UNAVAILABLE, never PASS.

## 4. Failure behaviour and reproducibility
Rejected with a reason: a RANK with wrong `min_rank`/`nullity`, or an embedded/non-minimal box. Deterministic: no random seeds in v009 code; `verify.py` samples (v008/v007 parts) use fixed seeds. `RUN_SMOKE.bat` / `RUN_FULL.bat` call `verify.py`; names say REGENERATED or SHIPPED. New and inherited checks are reported separately (`output/*/verify_*.json`).

## 5. Cost (build machine, 2 cores, illustrative)
`output/data/v9_cost.json`. The orbit generator for `k=5` takes about 40 s; the scan of the 1326 supports 8 s; the Burnside C program a few seconds; the hollow survey `d=73..110` and the cap extension are the long steps.

## 6. Not certified
G9-Z and G9-T4/T5 are proofs with finite computations; the checker validates only finite instances. The planar surveys are searches, not proofs.
