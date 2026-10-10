# PREFLIGHT_v009 — Preregistration Closure Gate (SCR-III-B, Generative Admissibility / Physical Sufficiency)

Additive to `scr_iii_b/`. Nothing here freezes, ratifies or authorises anything; v005–v008 are read-only inputs; GitHub is untouched.

## Run (Ubuntu/WSL, project root; needs g++ and Python 3 with numpy)
```
python3 scr_iii_b/prereg_gate/validate_v009.py     # full gate (a few minutes), writes scr_iii_b/output/validation/v009/
python3 scr_iii_b/prereg_gate/test_v009.py         # fast unit tests
```
Exit code: 0 for PASS/PARTIAL, 1 for FAIL, 2 for BLOCKED.  Verdicts: `PREREG_CLOSURE_GATE_{PASS,PARTIAL,FAIL,BLOCKED}` — technical readiness only.

## Files
| file | role |
|---|---|
| `gate_common_v009.hpp` | shared: instance reader, tolerance hierarchy, common-E0 threshold, boundary cascade (scan → direct → binary128 → UNRESOLVED_BOUNDARY), outcome-blind guard, append-only invocation audit |
| `prereg_gate_v009.cpp` | B0, G1, G2, B1 (all take `--e0`), `cert_b0`/`cert_b1` (E0 certification), `nullgap` (Δ_null scan), `gcount`/`gscan` (grammar-only), `boundtest` |
| `e2_v009.cpp` | E2: certified remainder bound `H_R − B_O ≤ H ≤ H_R + B_O`, exact fallback |
| `seeds_v009.py` | deterministic seed derivation (identical to v006), null generation with full accounting |
| `tolerance_v009.py` | tolerance hierarchy, exact-rational oracle, preservation classification |
| `cost_audit_v009.py` | phase buckets, balanced interleaved timing protocol, paired-ratio uncertainty rule and its simulation |
| `validate_v009.py`, `test_v009.py` | the gate and the unit tests |

## Candidate orders (deterministic, outcome independent)
B0/E2: Gray code, step t flips spin ctz(t), exact resync every 256 steps. G1: ascending state id. G2: islands in first-appearance order over the vertex list, value 0 before 1, vertex checked when complete. B1: spin index order, lower-energy value first. E2 retained pairs: |K| descending, ties by pair index.

## Guard
Any `n>16` request with `W>0`, and the `nullgap` excitation-gap mode, is refused (exit 3) unless the post-freeze flag is given or the instance is flagged `--synthetic` and its FNV-1a fingerprint is absent from the protected list. Every invocation is appended to the audit log (`--audit` or `SCR_AUDIT_LOG`). v009 never uses the post-freeze flag.

## Cost accounting rules
See `E4` in `TESTS_v009.json` (`counting_rules`). Pair-operation counters equal an independent analytic model exactly.
