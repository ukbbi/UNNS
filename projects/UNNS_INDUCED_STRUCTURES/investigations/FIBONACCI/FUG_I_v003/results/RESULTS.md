# FUG-I Phase 3 — Exact history geometry results

**Date:** 2026-11-20. **Scope:** all full-depth incoming directed `T_N` histories of indexed Fibonacci targets `F_1` through `F_84`. The original `M ⟂ N` law is unchanged; `T_N` is the explicitly selected integer self-substitution continuation grammar.

## Primary exact results

| Metric | Exact value | Scope |
|---|---:|---|
| Fibonacci target layers | 84 | `1..84` |
| Complete history records (including each empty word) | 292 | `84+208` |
| Nonempty history records | 208 | Across all 84 indexed targets |
| Ordered Fibonacci index pairs satisfying word-set gcd identity | 7,056 | 84 x 84, exact |
| Ordered pairs with a nonempty common history | 206 | Includes diagonal pairs |
| Proper index-divisibility transport pairs `m|n, m<n` | 307 | `1..84` |
| No new histories under scale (`first_activation_depth=0`) | 193 | Of 307 |
| New immediate histories (`first_activation_depth=1`) | 108 | Of 307 |
| Delayed first activation at depth 2 | 6 | Of 307 |
| Same-source merger pairs | 122 | Unordered word pairs indexed by target layer |
| Permutation-equivalent merger pairs | 119 | Same label multiset |
| Different-content merger pairs | 3 | Different label multiset, all at `F72` |
| Prior v002 Fibonacci-to-Fibonacci endpoint paths | 8 | All reverified; no changes |

**Scale activation example:**

`P_F12(t)=1+5t+7t^2+3t^3`,

`P_F24(t)=1+5t+8t^2+8t^3+3t^4`,

`P_F24(t)-P_F12(t)=t^2+5t^3+3t^4`.

The one-step incoming labels do not change, although deeper histories do. The other five observed delayed-activation cases are recorded in `fib_transport_84.csv`.

## Different-content merger at Fibonacci index 72

At `s=1730743096803`, the four words

`(3,8,3)`, `(1,1,1,2)`, `(1,1,2,1)`, `(1,2,1,1)`

are all legal and end at `F72=498454011879264`.

`r_3^2*r_8 = r_1^3*r_2 = 288`, where `r_N=(N+1)^2/N`.

The first word has content `{3,3,8}`; the other three are permutations of `{1,1,1,2}`. This gives exactly three different-content pairs at F72. By the classical divisibility law `F72|F_(72k)`, every one of these histories lifts to every `F_(72k)` from the corresponding scaled source. Hence **infinitely many Fibonacci targets** admit different-content history mergers. The kernel relation was known in earlier GEO-HD research; its explicit Fibonacci realization is the Phase 3 contribution.

## Source-locked controls

| Input sequence, indexed 1..84 | Nonempty histories | Merger pairs | Different-content merger pairs |
|---|---:|---:|---:|
| Fibonacci | 208 | 122 | 3 |
| Lucas | 40 | 1 | 0 |
| Fibonacci+1 | 220 | 164 | 15 |

These are not matched statistical null models. The shifted Fibonacci control produces more different-content merger pairs in this window, so an exceptional-Fibonacci interpretation is **not** supported by these raw counts. `Fibonacci+1` preserves distinct index identities for equal values at indices 1 and 2.

## Reproducibility

- `fib_history_words_84.csv`: all 292 histories with source, full states, word, minimal admissible source and endpoint.
- `fib_history_profiles_84.csv`: 84 source/merge/spectrum summaries.
- `fib_mergers_84.csv`: every one of 122 source-locked merge pairs.
- `cross_content_witnesses.csv`: the three different-content pairs.
- `fib_transport_84.csv`: 307 transport checks and first activation depths.
- `controls_phase3.json`: exact control results, no significance claims.
- `summary.json`: exact machine-readable roll-up.

The independent verifier checks all recorded word actions, reconstructs minimal thresholds using a second prime-valuation calculation, independently computes route-count polynomials, tests the complete gcd-meet law, checks the 307 transports, and verifies the F72 witness and controls.

## Evidence categories

`PROVED`: general threshold, gcd-history meet, coefficientwise scale transport, merger equivalence, infinite F72-index family.

`VERIFIED-EXACT`: indexed first-84 census and control counts.

`OPEN`: universal classification of Fibonacci history kernels, matched null controls, novel physical laws, broader non-anchor nesting grammar.
