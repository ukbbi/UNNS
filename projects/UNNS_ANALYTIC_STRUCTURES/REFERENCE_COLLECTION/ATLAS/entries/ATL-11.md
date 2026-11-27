# ATL-11: Entropy and admissibility

## Mathematical object

Probability laws $\pi$ on the letters, with entropy $H(\pi)$ and a resource functional $\Lambda(\pi)$ that charges the logarithm of the multiplier and the depletion of primes. A law is resource-neutral when no prime drift is negative. The dual variables are prime weights $\theta_p$ with optimum $\theta^\ast$, giving a candidate law $\nu^\ast$.

## Established structure

- **Variational principle.** For $a>1$, with the suprema taken over **finitely supported** probability laws $\pi$: $\log\rho=\sup_\pi[H-a\Lambda]$, also over resource-neutral laws, and for multipliers above one $\sigma^\ast=\sup_\pi H/\Lambda$; depletion is never optimal (T01, using weights controlled in T02). Attainment by a probability law on the complete alphabet is a separate result, subject to the criteria below.
- **Counting.** The three counting functions have the exponent $\sigma^\ast$ for any signs of the drifts (T04a, T04b). Certified example (T06).
- **Optimal law.** Finite optimal laws converge to $\nu^\ast$; criteria for attainment (T03, T07, T08) and a variational inequality (T09) lead to the depletion-surplus inequality: $\nu^\ast$ attains if it is neutral, and in particular if all weights are below one half (T10).
- **Shape of the weights.** They vanish identically or are supported on infinitely many primes (T05). Under negative drift, "all weights below one half" and "weights tend to zero" cannot both hold, in the setting of T11.
- **At the threshold.** Constraints on large weights (T12a, T12), the exceptional decay case (C12), bounds for the moment defect and its location at single primes (T13, T14), and a bound on average weight (T15).

## What it reveals

The exponent of a depleting grammar is an entropy rate under a balance condition at every prime. Whether the optimum is achieved by a law is a question about how weight behaves at individual primes.

## Further structure

Failure of attainment, if it occurs, requires a depleted prime with weight at least one half, on the boundary of the domain (T10) and visible in the mean divisibility of $N+1$ at that prime (T14).

## Open boundary

Whether the supremum is always attained; convergence and suppression at the abscissa; lower-order factors of the counts; decay of the weights; whether a weight can reach one half; and whether the logarithmic average of the weights vanishes (ANS2N-O1 to O6).

## Reading across (interpretation)

This principle is the broadest statement in the collection about balancing prime resources, and a natural frame for the questions of ATL-04 and ATL-09. It is a frame only: its hypotheses differ from theirs. It is also a candidate point of contact with generative information geometry.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS2N-T01 | Entropy-admissibility variational principle | PROVED | V |
| ANS2N-T03 | Optimal law and attainment criterion | PROVED | VQ |
| ANS2N-T10 | Depletion-surplus inequality | PROVED | V |
| ANS2N-T14 | Location of the defect | PROVED | VQ |

## Recorded open questions

- **ANS2N-O1:** Is the entropy supremum always attained?
- **ANS2N-O2:** Convergence of G at the abscissa, and suppression there.
- **ANS2N-O3:** Lower-order factors of the counting functions.
- **ANS2N-O4:** Decay of the optimal weights (remaining case: maximum exactly 1/2).
- **ANS2N-O5:** Can an optimal weight reach or exceed 1/2?
- **ANS2N-O6:** Is the logarithmic average of the optimal weights zero?

## Connected entries (cited dependencies)

- **Uses ATL-04** (Collective critical suppression): ANS-T24a.
- **Uses ATL-10** (Extended generation and prime-resource balance): ANS2-C16, ANS2-L1, ANS2-T16.

## Review boundary

Every result in this entry has a review verdict.

Qualified verdicts:

- ANS2N-T03: Convergence valid; attainment is open.
- ANS2N-T06: Method valid and stored result reviewed; no independent rerun.
- ANS2N-T07: Valid; its hypothesis is superseded by ANS2N-T10.
- ANS2N-T09: Valid; a proof clarification is recorded in ANS-II-ND v003.
- ANS2N-C12: Valid under its hypotheses.
- ANS2N-T14: Proof-writing clarification: in the final Fatou step use a limit superior for the drift difference, or a further convergent subsequence. The theorem is unaffected; the release file is not edited.

## All results and proof sources

- **ANS-II-ND v001:** ANS2N-T02, ANS2N-T01, ANS2N-T03, ANS2N-T04a, ANS2N-T04b, ANS2N-T05, ANS2N-T06.
- **ANS-II-ND v002:** ANS2N-T07, ANS2N-T08, ANS2N-T09, ANS2N-T10, ANS2N-T11.
- **ANS-II-ND v003:** ANS2N-T12a, ANS2N-T12, ANS2N-C12, ANS2N-T13, ANS2N-T14, ANS2N-T15.
