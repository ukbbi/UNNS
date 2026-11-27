title: Entropy and admissibility
principal: ANS2N-T01 ANS2N-T03 ANS2N-T10 ANS2N-T14
entries: ANS2N-T02 ANS2N-T01 ANS2N-T03 ANS2N-T04a ANS2N-T04b ANS2N-T05 ANS2N-T06 ANS2N-T07 ANS2N-T08 ANS2N-T09 ANS2N-T10 ANS2N-T11 ANS2N-T12a ANS2N-T12 ANS2N-C12 ANS2N-T13 ANS2N-T14 ANS2N-T15
open: ANS2N-O1 ANS2N-O2 ANS2N-O3 ANS2N-O4 ANS2N-O5 ANS2N-O6
---
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
