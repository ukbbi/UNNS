# Reproducing the ESC-I admissibility results

Three levels, in increasing strength. Only level 3 can catch a bug that the original code shares with a rerun of itself.
Requirements: Python 3.8 or newer. No third-party packages.

## Level 1: same-code rerun (checks determinism, not correctness)
In a fresh folder copy `esc_i.py`, `admissibility.py` and `test_esc_i.py`, then:

```
python admissibility.py --out rerun
python -m unittest test_esc_i -v
```

Everything is seeded (seed 20261013; confirmation set seed 20261113) and all verdicts are decided in exact rational arithmetic.
`rerun/admissibility_report.json` must equal `output/admissibility_report.json` except for the two timestamps in the `order` block.
The unit tests assert the headline numbers: 0 disagreements in AR-1 and AR-2, 92 retained original AR-3 disagreements,
0 disagreements and 0 error-bound violations in the AR-3.1 confirmation, and the hash match.

## Level 2: check the pre-registration (shows rules were not edited after the results)
The hashes in `output/admissibility_rules.md` and in the report's `order` block are SHA-256 of the rules text plus the frozen parameters.

```python
import admissibility as A, json
print(A.sha((A.RULES_MD + json.dumps(A.P, sort_keys=True, default=str)).encode()))
```

Expected values:

| Item | SHA-256 |
|---|---|
| Frozen AR-1..3 text + parameters | `c32fa4fd2469fee5ab3654b91cb28843e23463d04f5c56b7d63c7df14ec19b54` |
| AR-3.1 text + confirmation parameters | `36d7bea38dd1b9217edc5a6654c7ca5020fd93d019ed49dba91d56097965da41` |
| Source of the amended rule function (recorded in the earlier run, compared inside the run) | `2cf5d68ae0b293fb2f06a37579e0dd216870ae3046efb0ec11cf6b9c713ff3f1` |

The report also records a hash of the predictions, taken before any exact comparison was run, and a source check that the rule functions never call the exact classifier.
These hashes show the rules were fixed before the comparison; they do not show the rules are correct.

## Level 3: independent re-implementation (the strongest check)
`independent_check_ar31.py` imports nothing from the module: its own random generator, its own quantizer, its own arithmetic. It tests the key claim of AR-3.1 directly:
at every step, the eigen-coordinate quantization error is at most kappa_inf(V) * |lambda| * 2^-k times the state norm. It also counts violations of the original, falsified bound (without |lambda|).

```
python independent_check_ar31.py              # seed 12345, 400 systems
python independent_check_ar31.py 777 1000     # any other seed and size
```

Result recorded when written (seed 12345, 16,000 steps): 0 violations of the corrected bound, 1,341 of the original bound, maximum observed/bound = 0.77.
The module's own run gave 0 and 1,359 with a maximum of 0.75, on a different fresh set. A correct claim gives 0 violations of the corrected bound for every seed; the script exits non-zero if it ever finds one.

The strongest form of level 3 is a second person writing this check from the AR-3.1 text in `admissibility_rules.md` alone, without reading either implementation, and comparing results.

## What reproduction does and does not establish
- Levels 1 and 2 show the run is deterministic and that the rules and predictions were fixed before the exact comparison.
- Level 3 shows the quantization bound is not an artifact of the module's code. It still uses the same reading of the rule, so a flaw in the rule's definition would carry over; a second reader is what would catch that.
- The audit of the original manuscript's s4 and s5 rests on the review summary, not the manuscript text (which was not available). A reader with the paper should check the formalization of the projection model against it.
- The rules restate established linear algebra and perturbation theory. Reproducing them does not show an independent UNNS law.

## PRD-1 (projection route dependence)
`python admissibility.py` also writes `output/prd1_rules.md` (frozen text, parameters and SHA-256; outcome appended) and `output/prd1_report.json` (rules hash, predictions hash, seed, timestamps). Level 1 and 2 checks apply as above. There is no independent re-implementation of PRD-1 yet, so it has not had a Level 3 check.
