# ANS-II v002 — register

PROVED means a written proof in `PROOFS.md`. COMPUTED means floating-point evaluation. Finite checks: `results/operator_checks.json`. Review: the UNNS Research Collective's independent mathematical review of v002 (recorded 26 November 2026) found T09-T16 valid (T15 with the boundedness qualification now in the text) and the proofs of T09a and T16 sound, conditional on the earlier minimal-source formula and prime-introduction estimates. The reviewer did not rerun the checks. The numerical interval was classed as computed, certification pending; novelty review is incomplete.

| ID | Result | Status | Origin | Review |
|---|---|---|---|---|
| ANS2-T09 | Drifts >= 0 (zero allowed): G(sigma_A, 1) finite and abscissa sigma_A | PROVED | UNNS Research Collective review note | reciprocal check: valid; UNNS Research Collective review: valid |
| ANS2-T09a | Drifts >= 0 at a > 1: -log E[K^-b] between orders k^beta / log k and k^beta (no sqrt k term) | PROVED | internal | UNNS Research Collective review: valid |
| ANS2-T10 | Divisibility pullback d divides n' iff D(d) divides n | PROVED | UNNS Research Collective review note | checked internally; UNNS Research Collective review: valid |
| ANS2-T11 | Nesting transfer operator | PROVED | UNNS Research Collective review note | checked internally; UNNS Research Collective review: valid |
| ANS2-T12 | Torsion carry operator, non-negative exponents | PROVED | UNNS Research Collective review note | checked internally; UNNS Research Collective review: valid |
| ANS2-T13 | Closed countable operator system, Re s > 1 | PROVED | UNNS Research Collective review note | checked internally; UNNS Research Collective review: valid |
| ANS2-T14 | One letter formula and operator for multipliers of any signs | PROVED | problem: UNNS Research Collective; proof: internal | UNNS Research Collective review: valid |
| ANS2-T15 | Realizations: uniform norm B_A(s); norm Phi_A(s, theta) on weighted l^1 | PROVED (these two spaces) | problem: UNNS Research Collective; proof: internal | UNNS Research Collective review: valid (boundedness qualified) |
| ANS2-T16 | lim G_k(a)^(1/k) = min over theta of Phi_A(a, theta); abscissa is the root; sharp drift dichotomy | PROVED | problem: UNNS Research Collective; statement and proof: internal | UNNS Research Collective review: valid |
| ANS2-C16 | 2/sqrt3: 2.06055 <= abscissa <= 2.06072 | COMPUTED (certified later, ANS2N-T06) | internal | UNNS Research Collective review: computed estimate |
| ANS2-O3 | Exact suppression order (log gap) | OPEN | | |
| ANS2-O5 | Convergence at the abscissa and suppression there under negative drift | OPEN | | |
| ANS2-O6 | Spectrum of the operators: compactness, eigenvalues, continuation, complex s | OPEN | | |
| ANS2-O7 | Does any extension have a drift exactly zero at sigma_A? | OPEN | | |
| ANS2-O8 | Counting functions under zero or negative drift | RESOLVED later at exponent level (ANS2N-T04a, T04b) | | |

Earlier open items: O1 (abscissa under negative drift) is answered by T16; O2 (zero drift) by T09 and T09a for abscissa and depth; O4 (coupled class operators) by T13 and T14.

**Dependencies:** ANS-I v001 Theorem 4.4; ANS-I v002 Lemma B and section 4; ANS-II v001 sections 2-4 (L1, L2, T00 and the depth inequalities).

**Novelty:** unreviewed. The minimum-of-the-transform form of T16 has a known analogue for exit probabilities of random walks from cones (Garbit and Raschel, see 07_REFERENCES/SOURCES.md); the upper bound and change-of-measure technique is standard. Here the walk has infinitely many prime coordinates and the weight is the minimal source. No claim of priority is made.
