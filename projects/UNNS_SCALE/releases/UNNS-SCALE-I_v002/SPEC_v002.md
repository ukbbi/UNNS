# UNNS-SCALE-I v002 — Specification

**Title.** Boundary Arithmetic and Hierarchical Composition.
**Relation to v001.** v001 (`../UNNS-SCALE-I`, `../SHA256SUMS.txt`) is frozen and is only read. v002 reuses an identical copy of `scale_lib.py` (sha-256 recorded in the report) so that v001 is never imported or written to.

## Questions
1. Exact formula and growth law for the number of cross-scale exits `ε_B(x)`.
2. How exit counts compose across nested scales; how they distribute over levels.
3. How much of the inner coordinate any faithful outer-coordinate model must retain.
4. How the infinite-graph boundary counts differ from counts inside a finite window such as `[1, 10¹²]`.

## Parts
| Part | Content | Script | Status |
|---|---|---|---|
| A | prime-factor law (A1–A3), mean number of exits (A4) | `run_A_boundary.py` | PASS |
| B | additivity (B1), level stratification (B2), 10¹² decompositions | `run_B_composition.py` | PASS |
| C | resolution by horizon, minimal inner information (C1–C3) | `run_C_information.py` | PASS |
| W | finite-window edge classes, trillion-window table | `run_W_window.py` | PASS |
| D (next) | `D_B = sup_n d_G(Bn, B(n+1))`, certified values for small B | — | not started |
| Gate 4 | computational benefit | — | deferred |

## Acceptance rules (unchanged from v001, plus)
- Every proved statement has an independent finite check that does not call the formula being proved.
- Asymptotic statements are accompanied by exact-sieve measurements and a stated error rate.
- Infinite-graph counts and finite-window counts are always labelled as such.
- v001 files are never modified; `verify_all_v002.py` hashes them against `../SHA256SUMS.txt` and reports any difference.

## Proposed next part (D)
Determine `D_B`. Known: `D_B ≤ 6` (Scaling Lemma + frozen U1-BND) and `d(1,2) = 5`, `d(2,4) ≤ 4`, `d(7,8) = 4`, `d(70,80) ≤ 3` from v001. Plan: exact (untruncated) distance values for successor pairs `n ≤ N₀` for `B ∈ {2,3,4,5,6,10}` by exact ball intersections with certified lower bounds; search for path identities in residue classes of `n` modulo a period depending on `B`, in the style of U1-BND; certify a candidate constant for each `B`.
