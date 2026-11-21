# Source provenance — FUG-I v004

## Internal references (local and read-only)

- `FUG_I_v003/results/summary.json` — Phase 3 totals: 84 indexed Fibonacci layers, 208 nonempty histories, 122 source-locked merger pairs, 307 transports.
- `FUG_I_v003/results/fib_history_words_84.csv` — all 292 indexed history instances, their source, ordered word, exact state path, minimum source K, minimum endpoint E.
- `FUG_I_v003/results/fib_transport_84.csv` — all 307 proper index-divisibility transports and first activation depths.
- `FUG_I_v003/results/fib_history_profiles_84.csv` — target-level ancestry depth and counts.
- `FUG_I_v003/results/controls_phase3.json` — earlier Lucas / shifted-Fibonacci control reference.
- `FUG_I_v003/results/cross_content_witnesses.csv` — same-source different-content merger witnesses at F72.
- `FUG_I_v003/scripts/arith.py` — reproduced unchanged as `scripts/arith.py` (certified factorization for values below 2^64).

These are copied into `baseline_v003` or `scripts/` so that the v004 release can be executed without modifying the earlier version. Checksums and sizes are recorded in `MANIFEST.json`.

## Prior mathematical records

- UNNS Mathematical Foundations / SELECT-II, FIELD-I: exact integer nesting and occurrence theory.
- GEO-HD-1 v002/v003/v004: labelled history admissibility thresholds, source requirements, and integer-kernel merger equivalences.
- FUG-I v003 T1–T5: minimal endpoint characterization, full-history gcd meet, coefficientwise scale transport, and the explicit F72 source witness.

## Classical independent mathematics used

- Fibonacci recurrence and strong divisibility `gcd(F_m,F_n)=F_gcd(m,n)`.
- Rank of apparition `z(q)` and divisibility of its index set.
- Fibonacci–Lucas doubling `F_(2n)=F_n L_n` and elementary modular recurrence.

These facts are not claimed as new. FUG-I v004 combines them with the **unchanged** UNNS nesting operation in a precisely scoped induced-ancestry investigation.

## Computational methods

- Pure integer arithmetic with exact fractions for original generation.
- Independent prime-valuation threshold verifier.
- Dynamic programming on strictly decreasing integer predecessors.
- Fast-doubling modular Fibonacci for extremely large indices; never materializes giant integers to establish the infinite-family witnesses.

## No physical claims

This is a mathematical Fibonacci overlay; it does not claim empirical physical mechanisms, universality of all mathematical structures, or applicability to unconstrained rational non-anchor compositions.
