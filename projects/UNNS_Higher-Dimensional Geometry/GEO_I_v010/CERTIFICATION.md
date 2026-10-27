# GEO-I v010 — Programme D: certificates, validation paths, verification

Four reviews are kept separate: proof review (human), exact recomputation (`theory/`, `experiments/`), certificate verification (standalone `certificates/checker10.py`, standard library only, run with `python3 -I`), integrity (`MANIFEST.sha256`, `PROVENANCE.json`). A passing certificate check never validates a theorem, only a finite instance.

## Certificates
| Kind | Files | Status |
|---|---|---|
| COVER, GAP, HOMOLOGY, RANK | `C1`–`C4` (v008, 40 certificates), `C5_rank5.json` (v009, 12) | inherited, still accepted by `checker8.py` |
| D1–D3 (certificates), D4–D5 (records) | v007 files | inherited; D1–D3 hold **19** certificates (the v008 documents said 20 — kept as a correction) |
| **RANK6 (new)** | `C6_rank6.json` (215 nullity-6 classes), `C7_k2t.json` (`K_{2,t}`, `t = 2..8`) | accepted by `checker10.py`; tampered `min_rank`, `S = T`, base `x` inside `span S`, a dropped or added support point are rejected |
| **BOUNDARY (new)** | `C8_boundary.json`: 453 certificates (zonogon cover for every unit pair `5 ≤ d ≤ 40`; samples `d = 61, 100, 151, 199`) | accepted; `d ≤ 48`: `checker10.py` recomputes all Graver vectors, segments and cells and checks `conv F ∖ U0 = int T1 ∪ int T2`; larger `d`: cover-only (disjointness is G7-T3). Rejected: a removed cell, a changed generator, a different `s`, cells of another pair |

## Statuses
PROVED, PROVED+CHECKED, CHECKED, FALSE, CORRECTED, OPEN, UNAVAILABLE. Resource exhaustion is UNAVAILABLE, never PASS.

## Two independent paths
See `MATHEMATICS.md` §5. Single-path items: orbits of nullity 6 are counted by two programs (python, C) but the *classification* uses two engines that share the code-to-circuit routine in `binary5.py` for the cell path.

## Reproducibility and a lesson
Deterministic code; `verify.py` writes its **own** `output/reports/verify_smoke.json` and `verify_full.json`. In v009 the shipped `verify_full.json` was a stale v008 file; v010 regenerates both and checks that their `release` field is `v010`.
