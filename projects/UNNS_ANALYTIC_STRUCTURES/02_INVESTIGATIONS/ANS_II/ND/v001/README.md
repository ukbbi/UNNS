# ANS-II-ND v001 — Negative drift: entropy, resource neutrality, counting

**State:** working research notes of the negative-drift investigation. T01 and T04a were proposed in the UNNS Research Collective review of ANS-II v002; the other results await review. No report or manuscript.

## Run
    python nd_checks.py      (Python 3.8+ with numpy, sympy and gmpy2; uses ../../v002; about 20 s)

## Where things stand
- The abscissa is the largest entropy per unit of effective endpoint cost (UNNS Research Collective's principle).
- At the optimum the resource term vanishes: it suffices to use letter laws with no negative drift, and any law with a deficit is strictly worse.
- Consequently every fixed source has the same counting exponent as all minimal histories.
- If some unweighted drift is negative, the optimal weights occupy infinitely many primes (the UNNS Research Collective's working term: induced prime-coordinate redistribution). The theorem concerns the weights; their pattern and size are open.
- The interval for 2/sqrt3 is certified with directed rounding.

## What the checks cover
Floating point, finite alphabets (four extensions, M = 12, 60, 400): agreement of orthant and cube optima, neutrality of the optimal law, the entropy identity. Exact exponent arithmetic: 40 sampled histories (k <= 16000) realised from the state 1 after the preparation word. Numerical illustration of the inequality in Theorem 5 for a one-prime weight. Directed rounding: the interval.
Not covered numerically: the passage to the infinite alphabet in Theorems 1 and 3. In the 400-letter run for {8/7, 9/8} the largest weight (0.307) exceeds the sufficient bound of Theorem 3 (about 0.299), so that criterion should not be expected to cover every extension.

Files: PROOFS.md, THEOREMS.md, nd_checks.py, certify.py, results/, ANS_II_ND_v001_working_notes.pdf.
