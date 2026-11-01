# P4 theorem audit (P4-E5, partial)
| Claim | Status | Basis | Novelty |
|---|---|---|---|
| P4-A arithmetic of P4-F110 | PROVED | closed-form divisor analysis; exact enumeration m=1..12; engine and brute-force cross-check m=1..3 | elementary |
| P4-L lattices, nonrectangularity | PROVED | orders and subgroup sizes | elementary |
| P4-T1 hull theorem for E_3, n even >= 4 | PROVED | cube tiling + exact n=4 certificate (independent replay) + cell monotonicity (Graver set stable; checked 4<6<8) | elementary; planar analogue G12-T8 |
| P4-T2 F110 containment, all m | PROVED (scoped) | m=1 direct; m>=2 via T1 and U subset conv F subset conv F' | elementary specialisation |
| P4-C1 predictor for sublattices of E_3 | PROVED | T1 | elementary |
| CP3-A residual planar | OPEN | - | - |
| P4-T3/T4/T5 (general) | NOT STARTED | - | - |
Adversarial review: only the built-in falsification checks (tamper tests, independent re-derivation, direct m=2 cross-check).  No external review.  C3 NOT claimed.
