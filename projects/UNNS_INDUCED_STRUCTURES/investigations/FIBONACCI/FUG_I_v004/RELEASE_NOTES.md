# FUG-I v004 — Phase 4 release notes

**Date:** 2026-11-20. **Status:** package built and independently verified; local user validation pending.

## Research additions

- Rank-of-apparition activation as an explicit iff law for every selected UNNS history word in Fibonacci.
- Full activation table for all 84 distinct observed words, including 83 nonempty words.
- Reconstruction of all 208 nonempty occurrences and 307 proper divisibility transports from activation ranks alone.
- Exact minimum common-source endpoint `864` for a distinct-content merger; first admissible Fibonacci layer exactly `F72`, with occurrence at every `F_(72k)`.
- Infinite delayed activation at depth 2 for the specified finite alphabet `A={1,2,3,5,7,11}` along `(F_(12r),F_(24r))` for all odd `r`; explicitly **not generalized** to the unrestricted first-activation depth.
- Unbounded family of provable all-label-1 ancestry lengths `t+1` along `F_(6*4^t)`.
- Control diagnostics about index-divisibility transport and first-appearance periodicity for Lucas and shifted Fibonacci.

## Existing reference preservation

- FUG-I v001, v002, v003 unchanged.
- Six selected v003 reference files copied into `baseline_v003/`; checked against the v003 release before packaging.
- No remote files modified.

## Verification gates

`run_p4.py`: exact calculations and baseline cross-checks.

`verify_p4.py`: independent prime-valuation thresholds; independent Fibonacci modular ranks; ancestry reconstruction; 307 transport checks; 7,056 gcd-meets; 4,164 two-word joint-rank checks; explicit merger and infinite-family arithmetic; independent controls. No import from `run_p4.py`.

## Open obligations

1. Determine exact unrestricted first-activation depth across infinite Fibonacci index families, or prove a limiting obstruction.
2. Classify the first-appearance ranks of all different-content kernel relations, not just the selected pair.
3. Find stronger controls matching valuation and size while respecting independent recurrences.
4. Extend beyond integer self-substitution only after a separate, explicit rational nesting grammar is specified.
