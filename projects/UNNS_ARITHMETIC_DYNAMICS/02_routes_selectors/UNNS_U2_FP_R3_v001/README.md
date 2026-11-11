# UNNS-U2-FP-R3 v001 — Algebraic Parameter Recovery and the Generative Knowledge Audit

Separate research addendum. FP-SYM v001, FP v001, U2-SQ, U2-001, U1-BND are frozen and unchanged.

## Result summary
- R3' (fixed algebraic-monotone recovery) defined; alpha_eps strict monotonicity certified for 111 shifted states (t>=40); S5 re-run with alpha_eps, exact sign-safe radical comparisons.
- Fibonacci selector v2: explicit membership (5x^2+-4 square), mod-24 dispatch, 28-path small table (F_2..F_29), refusal of non-members. Verified k=2..899, 10^6 criterion cases, 607,409 domain cases.
- Knowledge audit (labels computable from state without recovery): Fibonacci 38/99, squares direct 87/105, squares wrapper 61/64. Ten Fibonacci labels (classes 1, 9; half-index) are unexplained by the tested vocabulary.
- Control states: 201 / 85 / 45. Max moves 12 / 5 / 8. External information: none.
- Bisection cost recorded separately from graph steps.

## Reproduce
    cd code
    python3 verify_u2_fp_r3.py --out ../reports/verification_report.json --data ../data
    python3 build_r3.py ../reports/verification_report.json ../manuscript ../data
    cd ../manuscript && pdflatex UNNS_U2_FP_R3_v001.tex && pdflatex UNNS_U2_FP_R3_v001.tex

## NOT_RERUN
Inherited route certificates and route searches (FP-SYM class_certificates.json, class_paths.json, small_fib_paths.json) are reused, not recomputed; frozen packages are copied under code/sq.
Inherited zip SHA-256:
- UNNS_U1_BND_v001.zip 912a068e2d26fb721c13d524f9bb18280e59a99fbafd79928781903c1c9d8e35
- UNNS_U2_001_v001.zip 561a9558f713faa2905be18f2a6afc2d3aac6de955c58e73cace7051e057ca21
- UNNS_U2_SQ_v001.zip c13a9be6c9a3d1d9299a009ab08844a9840a8ec24236dd5da171806e14691733
- UNNS_U2_FP_v001.zip c8469e88b76c66b248c827f00edf6da07cb9af0d4daf14ed2db935951e89ee91
- UNNS_U2_FP_SYM_v001.zip a614e196fa059bc58a7bea5bb3c616c8eaf0eead37945cb08bd56ecb982668c6

## Limits
Audit categories are exact fits checked at 26 sample points, not proved identities. "Not found" is not "necessary". Certificates are SymPy-based; no proof assistant. Costs are Python big-int counts. Whether R3' is the intended reading of Definition 2.1 is a programme decision. No literature priority search. No claim about primes. The small table dominates the Fibonacci control-state count (artefact of the b>=40 threshold).
