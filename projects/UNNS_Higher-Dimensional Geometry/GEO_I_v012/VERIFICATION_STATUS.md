# GEO-I v012 — what was and was not re-run (accurate record)

| Item | Status |
|---|---|
| Clean-unzip smoke (`verify.py --smoke`), earlier v012 build | PASS: v012 25/25 new checks; inherited v011 gate 33/33 (v010 125/125 inside) |
| New v012 checks in a full-mode run (earlier build) | PASS: all v012 checks (unit tests 13/13, T1 regeneration, structure lemmas, cell cover, certificates 984 ARITH + 2,130 CAPCOVER2 + inherited formats, tamper rejection, documentation) |
| Inherited v011/v010 FULL gate (about 2 h) | **NOT_RERUN - FROZEN BASELINE VERIFIED** (not PASS). Baseline reports of the v011 release preserved in `output/baseline_v011/` (v011 33/33, v010 132/132); v001-v011 files sha-256-checked unchanged by `verify.py`. A partial attempt was stopped by the operator and is not counted. |
| Standalone sweep d=13..30 | **PARTIAL** (interrupted; no range claimed; unused) — `output/data/v12_sweep_13_30_PARTIAL.json` |
| Completed exact cover run | d<=22 (29,206 boxes), structure d<=16, 19,731 adversarial boxes to d=399, 3,000 random: 0 failures — `output/data/v12_cap.json` |
| Final `verify.py` after the portability fix, smoke mode | **PASS, executed end to end on two systems.** (1) Windows PowerShell on the author's machine, clean extraction (reports generated 2026-10-26 23:08 UTC): v012 25/25 new checks, 27/27 in the file; inherited v011 gate 33/33; v010 125/125; 618 s. (2) Linux clean unzip with a sibling release folder present and no `sha256sum` on PATH: v012 25/25, v011 33/33, v010 125/125, 498 s. Records archived in `output/records_v012/` (`WINDOWS_verify_*_smoke_final.json`, `LINUX_clean_unzip_smoke_final.log`). Default full mode (v012 checks + smoke-mode gate, inherited 2 h gate NOT_RERUN) and `--rerun-inherited-full` were not executed in the final package. |

## Portability fix after the Windows smoke (v010 gate 124/125, v011 gate 32/33)
* Failing check (from `output/reports/verify_inherited_smoke.json` on the Windows run): *G1: v005 regression suite ... passes completely* — `FileNotFoundError: [WinError 2]` inside `subprocess`.
* Cause: **environment / verification-script portability, not a mathematical regression.** The frozen `regression_v005.py` runs the external program `sha256sum -c MANIFEST.sha256` for optional sibling releases `GEO_I_v001..v004` when they sit next to the release folder (they do on the Windows disk, not in the clean container); `sha256sum` does not exist on Windows, so the whole suite aborted. All 52 core v005 checks are unaffected.
* Reproduced exactly in a clean unzip with a sibling folder present and no `sha256sum` on PATH (same exception); with the fix the suite gives CORE 52/52 and the sibling is reported `PASS (optional)`.
* Fix: `tools/run_regression_v005.py` (new) runs the byte-identical `regression_v005.py` with a pure-Python `sha256sum -c` equivalent; `verify_v010.py` line 44 calls it. No frozen file or result changed, no check suppressed (a non-verifying sibling is still reported). Provenance: key `portability_patch_v012`.

## Note on a transient error
A Windows run started while the archive was still being extracted failed with `ModuleNotFoundError: cap_cells` (`verify.py` is extracted before `theory/`). The extracted tree was then verified intact (356/356 manifest entries) and the later smoke run above passed. Not a package defect; run the verifier only after extraction completes.
