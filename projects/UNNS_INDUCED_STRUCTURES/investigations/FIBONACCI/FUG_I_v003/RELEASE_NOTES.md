# FUG-I v003 — Phase 3 release notes

**Title:** Generative Ancestry Geometry and History Invariants

**Status:** locally runnable; exact primary run and independent verification PASS.

**Baseline:** v002 files copied to `baseline_v002/` without changing the source release. The four pair / eight route census from v002 is source-locked and unchanged.

## Added in v003

1. Minimal admissible endpoint `E(w)` for complete labelled words, verified using independent rational and prime-valuation calculations.
2. Complete-history word-set meet theorem `W(gcd(x,y))=W(x)∩W(y)` and its exact Fibonacci consequence.
3. Coefficientwise history-polynomial transport and first-new-depth classification; explicit depth-2 activation between F12 and F24.
4. All 122 same-source merger pairs in first 84 Fibonacci layers, classified into 119 permutation and 3 different-content pairs.
5. F72 exact different-content kernel witness from common source and **proved infinite family** at all `F_(72k)`.
6. Controls for Lucas and `F_n+1`, including negative evidence against claiming Fibonacci exceptionality from merger counts.
7. Two portable vector figures and all CSV/JSON outputs.

## Windows workflow

Open this `FUG_I_v003` folder in Explorer and type `powershell` in the address bar. Then run:

```
py -3 scripts\run_p3.py
py -3 scripts\verify_p3.py
```

If `py -3` is unavailable, use `python` instead. No `.bat`, `.ps1`, elevated privileges, or network access are needed.

## Scope constraints

- Integer self-substitution is explicitly chosen; original UNNS occurrence arithmetic is not redefined.
- The finite census covers Fibonacci indices 1..84 only. The infinite family follows from a separate exact theorem, not extrapolated statistics.
- No physical or universal interpretation is claimed.
- No GitHub writes; all development is local.
