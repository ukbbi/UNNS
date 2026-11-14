# UNNS_PRIME_DYN_v003 — Autonomous Prime-Valuation Dynamics and Symbolic Complexity in the UNNS Substrate
Author: UNNS Research Collective. Manuscript Version 1.2 (`unns_prime_valuation_dynamics_v1_2.pdf`, LaTeX in `manuscript/`).

## Results
- Prime-fire reduction: primes >=5 fire finitely often; tail alphabet {2,3}; SPF and LPF eventually periodic (proved).
- MAXPP: for every x0>=2 the itinerary is not eventually periodic, with tail factor complexity exactly k+1 (irrational rotation by ln48/ln864 on a circle of length ln864); exact frequencies, discrepancy <1, Beatty-form valuations, growth 2.2747033 bits/step (proved).
- Composite branches: finite total prime support iff finitely many branch values (Stormer imported).
- Finite-guard selectors: |W_k| <= |Q| M^d c_d n_k^d, entropy 0 for finite codings of the branch/control itinerary only.
- Counter selector x_j=(m0+j)(m0+j)!/m0! with exponent-profile observable of entropy >= (2/pi^2) ln 2.

## Source provenance (GitHub reference alignment, Version 1.2)
- UNNS_U4_GEN_v001 is cited at commit 22d8c2e23f49fb98a5b04c6b7efe9ba0a3703808 of https://github.com/ukbbi/UNNS (projects/UNNS_ARITHMETIC_DYNAMICS/04_symbolic_dynamics/UNNS_U4_GEN_v001; proofs in docs/PROOFS_GEN.md). Its archive SHA-256 042eb5b0...e18df matches the collection's SOURCE_PROVENANCE.md.
- UNNS_U4_GEN_C_v001 and UNNS_U4_GEN_C_ORDER_v001 are NOT in that collection; they remain identified by release name and archive SHA-256 (inherited/INHERITED_ARCHIVE_SHA256SUMS.txt) and are cited as such. GEN-C3a is withdrawn (ORD-0, E1) and not used.
- UNNS_U4_SPEC_v001 was examined; its claim registry has no statement on prime-fire, MAXPP, composite branching or counters, so it is not cited.
- Appendix "Source provenance" now tabulates, per theorem family, the source release and whether the item is inherited (re-proved here), derived here, or recorded verification.

## Reproduce
`./run_all.sh` (verifier ~75 s, figures, tables, PDF). `reports/verification_report.json`: all checks pass.

## Disclosures
- The three U4 archives in `inherited/` are checked by hash only (NOT_RERUN); no proof relies on them.
- Computations illustrate proved statements; none proves an asymptotic claim. Non-periodicity of finite prefixes cannot be certified by data.
- Stormer's theorem, Euler's product and the classical hyperplane counts are credited, not re-proved (the latter two are proved in Appendix A).

## Changes from v001 (Version 1.0 -> 1.1; no theorem, proof or computation changed)
- Finite-guard scope kept consistent in Sec. 8 (after Cor. 8.6), Sec. 9.3 and Sec. 10.3-10.4: finite branch sets imply finite prime support; polynomial complexity and zero entropy need the finite-guard hypotheses.
- MINPP described as observed (2<=x0<=400), not proved, in Sec. 3.2.
- Log-cap example (Sec. 7.3) reports the observed runs only.
- Fig. 7 caption now lists panels (a)-(c) correctly; |7theta-4| = 0.0077; "generic" replaced by "every initial integer".

## Changes from Version 1.1 (UNNS_PRIME_DYN_v002, 25 pages)
- Bibliographic and provenance only: four commit-pinned/hash-identified bibliography entries (collection, U4-GEN, U4-GEN-C, U4-GEN-C-ORDER); citations in the summary theorem and one-line Source notes after Theorems A, SPF, LPF, B, C, D, E, the counter theorems and Prop. 9.x; provenance appendix extended with a location paragraph and a source-of-each-theorem-family table.
- Finite-guard scope unchanged and restated at Theorem E (finite branching alone is not sufficient); GEN-C3a not reintroduced.
- No theorem, proof, equation, figure, table, data or computation changed. PDF: 27 pages.
