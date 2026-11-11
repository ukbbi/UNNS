# UNNS-U2-FP version 1.0 (v001)
**Fibonacci Numbers and Primes in the Reversible Square-Multiplication Graph: Structure, Distances and Selector Restrictions** -- UNNS Research Collective, 9 November 2026.

## Results
- Prime neighbour rigidity Nbr(p) = {4p, (p+1)^2}; path ends (+1 or +p first, -1 or -q last); reduction d(p,q) = 2 + min d(u,v).
- Certified d(61,67) = 7 and d(661,673) = 8 (disjoint balls, two engines for the first, explicit paths).
- Exact tables: 195 consecutive primes < 1200 (distances 4..8), 30 consecutive Fibonacci pairs (distances 2..6), generic controls.
- Fibonacci two-parameter path identities for k = 4, 7, 10 (mod 12), lengths 5, 7, 7: validated on exact pairs for k < 1800; NOT symbolically certified. No identity found in the vocabulary for the other nine classes.
- Predeclared selector restrictions (Definition 2.1). No selector for Fibonacci numbers or primes is constructed here.

## Layout
UNNS_U2_FP_v001.pdf, manuscript/UNNS_U2_FP_v001.tex (+ figures, tables); code/ (verify_u2_fp.py, mitm.py, fibparam.py, fibsym.py, fibsanity.py, fibcover.py, fibvalidate.py, fib_table.py, primescan.py, build_fp.py, u1_bnd_lib.py); data/ (tables, identities, search outputs); reports/ (u2_fp_verification_report.json, search_sanity.json, verifier_stdout.txt); SHA256SUMS.txt

## Reproduce
From code/: python3 verify_u2_fp.py --out ../reports/u2_fp_verification_report.json --data ../data   (about ten minutes; run without -I). fibsym.py regenerates data/fibonacci_identities_raw.json; fibsanity.py regenerates reports/search_sanity.json.

## Status
Lower bounds on distances are computations. Fibonacci families are numerically validated, not proved. No formal certification; no literature originality review. Unresolved in the time limit: Fibonacci pairs k = 31, 33, 34, 35; four ratio-matched control pairs.

## Inherited, not re-run (NOT_RERUN)
U1-BND zip sha256 912a068e2d26fb721c13d524f9bb18280e59a99fbafd79928781903c1c9d8e35 ; U2-001 zip sha256 561a9558f713faa2905be18f2a6afc2d3aac6de955c58e73cace7051e057ca21 ; U2-SQ zip sha256 c13a9be6c9a3d1d9299a009ab08844a9840a8ec24236dd5da171806e14691733 ; u1_bnd_lib.py sha256 249e87d2bc636485231e053c9138e6a0c599afbf0470e17357a4be2c43f2e49c (identical to the release copy). U0-001 and the frozen GIG collection (commit a115e4bc6b8ee734e6146b3b17a6b121e65d31c3) unchanged.
