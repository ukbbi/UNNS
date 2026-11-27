# ANS-I v002 — Critical admissibility and analytic singularities

**State:** working research notes. T22-T24 and T26 passed the UNNS Research Collective's mathematical review (26 November 2026); sharper bounds are in v003. No report or manuscript. v001 is unchanged.

## Run
    python critical_checks.py      (Python 3.8+ with sympy; reads ../v001; about 15 s)

## Core statements
- G_k(sigma_c) = E[K_k^-sigma_c] under the critical letter law.
- K_k -> infinity: the complete alphabet keeps introducing prime requirements.
- How fast: G_k(sigma_c) = exp(-k^(1/sigma_c + o(1))). Hence G(sigma_c,1) is finite, with all derivatives.
- Counting: X^sigma_c exp(-(log X)^(1/sigma_c + o(1))).
- Every finite alphabet instead retains a positive limit c_M, and c_M -> 0.

Files: PROOFS.md, THEOREMS.md, critical_checks.py, results/.

Pending from v001 before freezing it: run `RUN_WINDOWS.bat` on Windows.
