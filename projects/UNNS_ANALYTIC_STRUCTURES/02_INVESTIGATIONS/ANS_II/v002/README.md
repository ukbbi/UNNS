# ANS-II v002 — Divisibility-resolved analytic transfer operators

**State:** working research notes, reviewed by the UNNS Research Collective (26 November 2026). T09 and T10-T13 were proposed in the UNNS Research Collective review of v001; the other results await review. No report or manuscript.

## Run
    python operator_checks.py      (Python 3.8+ with numpy, sympy and mpmath; uses ../v001; about 2 minutes)

## Where things stand
- The class series, resolved by source divisibility d, satisfy an exact closed linear recursion for Re s > 1; one formula covers all letters, with exponents of any sign.
- On uniformly bounded sequences the operator has norm B_A(s) and does not see the drifts. On the space of measures weighted by prime powers it has norm Phi_A(s, theta).
- The depth growth rate is exactly the minimum of Phi_A over theta in [0,1]^primes. The abscissa is the root of that minimum = 1.
- The abscissa equals the characteristic root sigma_A exactly when no drift is negative there.
- With all drifts >= 0 (zero allowed) the depth law has orders k^beta / log k to k^beta.
- For 2/sqrt3 the abscissa is computed to lie in [2.06055, 2.06072] (sigma_A = 2.100608); the minimising weight involves many primes besides 3.

## What the checks cover
Exact: the one-letter formula and pullback on random words; the operator recursion against enumeration (depth <= 3, N <= 6, s = 2). Floating point: the weighted one-step bound and its equality case; the upper bound G_k <= C Phi^k on a finite alphabet (N <= 8, k <= 20); the two-sided computation for 2/sqrt3.
Not covered numerically: T09 and T09a (no zero-drift example is known); the lower bound of T16. In the finite-alphabet run G_k^(1/k) is still far below the limit at k = 20 (0.70 against 0.94 at a = 2), so it is recorded as an observation and is not evidence of convergence.

Files: PROOFS.md, THEOREMS.md, operator_checks.py, rate.py, results/.
