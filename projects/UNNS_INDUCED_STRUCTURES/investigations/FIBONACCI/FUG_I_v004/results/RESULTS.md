# FUG-I Phase 4 — Exact results

**Date:** 2026-11-20. **Scope:** all 84 indexed Fibonacci targets from frozen v003; new proofs about infinite index families are independent of the finite census.

## Central answer

Every labelled word w has a minimal legal endpoint E(w). Its Fibonacci appearance schedule is exactly the infinite index set

`{n>=1: z(E(w)) divides n}`.

The resulting history polynomial is `P_n(t)=sum_w [z(E(w))|n] t^|w|`. It does **not** require a numerical search at each new n to determine membership of a *known* history word.

## Verified finite results

- 84 Fibonacci index layers; 292 Phase 3 records, of which 208 are nonempty indexed histories.
- 83 **distinct** nonempty words observed among the 84 layers (some appear at several indices).
- All 307 index-divisibility transports reconstructed using only activation ranks; first-new-depth categories 193 unchanged / 108 depth 1 / 6 depth 2.
- All 7,056 ordered gcd-meet checks and 4,164 eligible first-index joint-rank checks pass.

### First appearances of distinct words

| First Fibonacci index | Newly appearing nonempty words |
|---:|---:|
| 6 | 1 |
| 12 | 14 |
| 24 | 9 |
| 25 | 2 |
| 36 | 6 |
| 48 | 25 |
| 56 | 3 |
| 60 | 13 |
| 72 | 10 |

## Exact selected different-content merger gate

For label words `a=(3,8,3)` and `b=(1,1,1,2)`, the rational multiplier is 288 for both. The minimum admissible sources are 3 and 1; their minimum common source is 3 and their minimum common endpoint is **864**.

`3 --3-->16 --8-->162 --3-->864`

`3 --1-->12 --1-->48 --1-->192 --2-->864`

Since `z(864)=72`, these two words merge from one source at Fibonacci target F_n **if and only if 72|n**. The first target is `F_72=498454011879264`. This exact iff statement concerns the named word pair.

## Infinite delayed activation (restricted grammar)

Fix `A={1,2,3,5,7,11}`. For **every odd r>=1** the one-step incoming label sets in this alphabet agree at `F_(12r)` and `F_(24r)`, and both are `{1,2,3,5,11}`. Yet `(7,2)` is a new legal history in `F_(24r)` and absent from `F_(12r)`. Thus first new history depth in A is **2**, for infinitely many pairs.

Proof uses modulo-64 Fibonacci periodicity, `F_12|F_(12r)`, and the exact threshold `E(7,2)=288`. The **unrestricted** first depth for every odd r is not established.

## Unbounded ancestry growth

For every t>=0, `v2(F_(6*4^t))=3+2t` and the longest valid history consisting exclusively of label 1 has length exactly **t+1**. Thus there are Fibonacci targets of arbitrarily large full ancestry depth, though the actual maximum mixed-label depth is not classified.

## Control outcomes (not matched statistical nulls)

| Index sequence | Transport inclusion failures / 307 | First-appearance periodicity violations (distinct words) |
|---|---:|---:|
| Fibonacci | 0 | 0 |
| Lucas | 37 | 4 |
| Fibonacci_plus_1 | 55 | 35 |

## Files and verification

- `word_activation_84.csv`: 84 distinct word ranks and minimal endpoints.
- `index_activation_84.csv`: history counts and newly activated words per index.
- `transport_activation_84.csv`: 307 rank-predicted transport deltas.
- `merger_gate.json`: exact source-locked first-appearance gate.
- `delayed_family_witnesses.csv`: nine odd-r examples supporting the algebraic infinite-family proof.
- `unbounded_depth_spine.csv`: twelve modular checks of the explicit unbounded-depth family.
- `control_activation_84.json`: detailed descriptive controls.
- `summary.json`: machine-readable result register.

Run `py -3 scripts\run_p4.py` and `py -3 scripts\verify_p4.py` locally from the release root. All arithmetic is exact and no network or third-party packages are needed. Full statements and limitations are in `theory/THEOREMS.md` and `theory/LIMITS.md`.
