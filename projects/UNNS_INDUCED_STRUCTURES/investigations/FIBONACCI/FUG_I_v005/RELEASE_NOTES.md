# Release notes — FUG-I v005

**Title:** Unrestricted Structural Activation and History Classification  
**Date:** 20 November 2026  
**Status:** Locally produced, double-verified; user-side validation pending.

## What's new

- An exact and terminating all-label pair recursion for first new ancestry depth.
- Exact Lucas-squarefreeness criterion resolving the unrestricted first activation depth for all `(F_(12r),F_(24r))`, odd r.
- Proven infinite counterfamily to unrestricted depth-two for *every* odd r: r=7s, s odd.
- Infinite matched non-Fibonacci depth-two family showing the phenomenon is not uniquely Fibonacci-specific.
- Constructive unbounded multiplicity of distinct-content mergers at Fibonacci targets.
- Complete first-84 index-pair census reproduced by an independent word-set verifier; all output tables generated on demand.

## Compatibility

The release keeps the original `M ⟂ N` arithmetic and the SELECT-II integer transition unchanged. `FUG_I_v001` through `FUG_I_v004` are unmodified and referenced as frozen baselines. Only local files are produced. No GitHub operations, `.bat` launcher, dependencies or environment changes.

## Run and expected result

```powershell
py -3 scripts\run_p5.py
py -3 scripts\verify_p5.py
```

Expected final line: `FUG-I v005 VERIFY PASS`.

## Scope caution

The infinite delayed-first-depth-two statement from v004 remains true **only for its explicitly restricted alphabet**. Phase 5 gives the unrestricted gate but does not prove infinitely many odd r satisfy its squarefreeness condition. The new infinite obstruction disproves the unconditional unrestricted extension.
