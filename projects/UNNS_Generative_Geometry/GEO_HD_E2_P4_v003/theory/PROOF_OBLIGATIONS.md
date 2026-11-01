# E2-P4 proof obligations
| ID | Statement | Status | Where |
|---|---|---|---|
| O-A | FIELD-I arithmetic of P4-F110 for all m | DISCHARGED (P4-A) | THEOREMS.md |
| O-L | Lattice formulas, nonrectangularity | DISCHARGED (P4-L) | THEOREMS.md |
| O-T1 | U(E_3,[0,n]^3)=H' for even n>=4 | DISCHARGED (cube tiling + exact corner certificate n=4 + cell monotonicity) | RUN_VERIFY S3,S4 |
| O-T2 | P4-F110 containment for all m | DISCHARGED (m=1 direct; m>=2 via T1) | RUN_VERIFY S2,S3 |
| O-DIRECT-m2 | independent direct engine run m=2 | OPT-IN stage `m2` (build) and `--m2` (verify S4); result recorded if run | results/P4_GEOMETRY.json |
| O-DIRECT-m3 | direct engine m>=3 | UNAVAILABLE_COST | data/SEARCH_LIMITS.json |
| O-CP3A | residual planar CP3-A | OPEN (P4-E3 not started) | results/P4_PLANAR.json |
| O-T3 | parameter-family classification for other coupled pairs | OPEN (not started) | - |
| O-T4 | essentially 3D coupled-target obstruction theory | OPEN (not started) | - |
| O-NOV | prior-art audit for C3 | PARTIAL (overlap table only; no C3 claim) | SOURCE_OVERLAP.md |
| O-P3ADD | E2-P3 infinite (2,7,13) family, rectangular target | DISCHARGED as addendum (proof + 8 instances) | ERRATA/E2_P3_ADDENDUM_004 |
