# UNNS-U2-SQ version 1.0 (v001)
**Squares and Power Sequences in the Reversible Square-Multiplication Graph** -- UNNS Research Collective, 9 November 2026.

## Results
- sup_n d(n^2,(n+1)^2) = 5 (24 certified path identities mod 24, <= 5 moves; lower bound d(23^2,24^2)=5, radius-2 balls of 97 and 562 vertices disjoint, two engines).
- Power lifting: d(x^k,y^k) <= k d(x,y); d(n^k,(n+1)^k) <= 6k. Square-specific route: d(n^2,(n+1)^2) <= 8.
- Finite-control selectors: direct (85 control states, <=5 moves per square), wrapper (45 states around the frozen U2-001 selector, <=8 moves), fixed powers (<=6k moves).

## Layout
- UNNS_U2_SQ_v001.pdf, manuscript/UNNS_U2_SQ_v001.tex (+ figures, tables)
- code/: u2sq_selector.py (selectors), verify_u2_sq.py (checks Q1-Q11), sqparam.py (identity search), sqsym.py (symbolic resolution and certification), sqscan.py, build_sq.py, u1_bnd_lib.py and u2_selector.py (unchanged copies)
- data/: square_identities.json (the 24 identities + 3 exceptional paths), square_distance_table.csv (exact, n <= 500), search_output_mod24.jsonl, resolved_identities_raw.json
- reports/: u2_sq_verification_report.json (deterministic), verifier_stdout.txt; SHA256SUMS.txt

## Reproduce
From code/: python3 verify_u2_sq.py --out ../reports/u2_sq_verification_report.json --csv ../data/square_distance_table.csv   (about nine minutes; run without -I)

## Status
Symbolic checks use sympy (computer algebra, not a proof assistant). No formal certification; no literature originality review. The lower bound is a computation. Infinite occurrence of distance 5 is open.

## Inherited, not re-run (NOT_RERUN)
- U1-BND v001 verification: zip sha256 912a068e2d26fb721c13d524f9bb18280e59a99fbafd79928781903c1c9d8e35
- U2-001 v001 verification: zip sha256 561a9558f713faa2905be18f2a6afc2d3aac6de955c58e73cace7051e057ca21
- u1_bnd_lib.py sha256 249e87d2bc636485231e053c9138e6a0c599afbf0470e17357a4be2c43f2e49c ; u2_selector.py sha256 8f0c9e06dd270e1b07e58b16b0ae55b689001715f6b7a0711fe3a1d70a7253ee (identical to the release copies)
- U0-001 and the frozen GIG collection (commit a115e4bc6b8ee734e6146b3b17a6b121e65d31c3): unchanged.
