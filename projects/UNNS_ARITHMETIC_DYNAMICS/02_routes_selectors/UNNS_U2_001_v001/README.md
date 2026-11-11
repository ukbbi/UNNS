# UNNS-U2-001 version 1.0 (v001)
**Intrinsic Generative Selectors: Finite Control, Arithmetic State, and Observational Realization** -- UNNS Research Collective, 8 November 2026.

## Results
- **U2.0** no state-only deterministic selector passes through 1,2,3,... in order (uses only d(n,n+1) >= 2).
- **U2.1** a deterministic selector with 43 control states, using exact integer arithmetic on the current state and no external input, passes through 1,2,3,... in order with at most 6 moves per successor (mean 4.9166 over 100,000 waypoints).
- **Doubling** sup_n d(n,2n) = 5 (attained at n = 1).

## Layout
- UNNS_U2_001_v001.pdf, manuscript/UNNS_U2_001_v001.tex (+ figures, tables)
- code/u2_selector.py (the selector), code/verify_u2_001.py (verifier W1-W8), code/build_u2.py, code/check_decode.py, code/run_selector.py, code/u1_bnd_lib.py (unchanged copy from U1-BND v001)
- reports/u2_001_verification_report.json (deterministic, no timestamps), reports/verifier_stdout.txt
- SHA256SUMS.txt

## Reproduce
From code/: python3 verify_u2_001.py --out ../reports/u2_001_verification_report.json --data ../data   (about 3 minutes; run without -I)

## Status
Symbolic checks use sympy (computer algebra, not a proof assistant). No formal certification and no literature originality review.
Observation maps are deliberately restricted (see Proposition 6.2 in the manuscript).

## Inherited, not re-run (NOT_RERUN)
- U1-BND v001 verification (exact distance table, search engines): zip sha256 912a068e2d26fb721c13d524f9bb18280e59a99fbafd79928781903c1c9d8e35
- u1_bnd_lib.py sha256 249e87d2bc636485231e053c9138e6a0c599afbf0470e17357a4be2c43f2e49c (identical to the U1-BND release copy)
- U0-001 and the frozen GIG collection (commit a115e4bc6b8ee734e6146b3b17a6b121e65d31c3): unchanged.
