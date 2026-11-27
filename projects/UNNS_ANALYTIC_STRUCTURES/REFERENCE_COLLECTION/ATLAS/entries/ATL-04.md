# ATL-04: Collective critical suppression

## Mathematical object

The negative moments $\mathbb E\,K_k^{-b}$ of the minimal source, the ratio $Z(X)/X^{\sigma_c}$ and the derivatives of $\mathcal G(s,1)$ at $\sigma_c$. Write $\beta=1/a$, and $\beta=1/\sigma_c$ at the critical exponent.

## Established structure

- **Depth.** For $a>1$ and large $k$, $ck^{\beta}/\log k\le-\log\mathbb E\,K_k^{-b}\le Ck^{\beta}$ (T23a, sharpening T23).
- **Counting.** $c(\log X)^{\beta}/\log\log X\le-\log\big(Z(X)/X^{\sigma_c}\big)\le C(\log X)^{\beta}$ (T24a, sharpening T24; second proof of one inequality in T24b).
- **Derivatives.** The $j$-th derivative magnitude $D_j$ satisfies $c^jj^{\sigma_cj}\le D_j\le(Cj\log j)^{\sigma_cj}$, so $\sigma_c$ is the infimal Gevrey order on the closed half-plane (T27).
- **First introductions.** The probability that every new prime among the first $k$ letters arrives only through $N+1$ has exact order $\exp(-\Theta(k^{\beta}/\log k))$ (T28a).

## What it reveals

The cost of admissibility at depth $k$ is stretched-exponential, with exponent fixed by the letter law. One quantity appears three times: as decay in depth, as a deficit in counting and as the growth of derivatives.

## Further structure

The two sides of the depth estimate have different sources. That the suppression is at least $ck^{\beta}/\log k$ comes from fresh primes. That it is at most $Ck^{\beta}$ comes from Jensen's inequality and a bound, for each prime, on the demand that can build up after the prime is first consumed.

## Open boundary

The exact order of the decay: the conjecture T28 states $-\log\mathbb E\,K_k^{-b}\asymp k^{\beta}/\log k$. T28a settles the first introductions only. Preventing harmful first introductions does not prevent depletion of primes met earlier, which is why T28a does not resolve T28. Membership at exactly the Gevrey order $\sigma_c$ is also open (T27).

## Reading across (interpretation)

The gap between T28a and T28 isolates repeated demands on small primes. The prime-resource questions of ATL-09 and ATL-11 have the same character in other settings.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS-T23a | Strengthened critical depth bounds | PROVED | V |
| ANS-T24a | Growth suppression without logarithms in the lower estimate | PROVED | V |
| ANS-T27 | Critical derivative growth; infimal Gevrey order sigma_c | PROVED | VQ |
| ANS-T28a | Exact order of the first-introduction event | PROVED | V |
| ANS-T28 | Exact order of the critical decay | CONJECTURE | N |

## Connected entries (cited dependencies)

- **Uses ATL-02** (Finite saturation and unbounded obstruction): ANS-T15, ANS-T17.
- **Uses ATL-03** (The characteristic exponent and its singular point): ANS-T21.
- **Used by ATL-02** (Finite saturation and unbounded obstruction): ANS-T26.
- **Used by ATL-03** (The characteristic exponent and its singular point): ANS-T22.
- **Used by ATL-05** (Generated populations and typical histories): ANS-T37a, ANS-T37b, ANS-T42a.
- **Used by ATL-09** (Collective growth at and below s = 1): ANS-T48.
- **Used by ATL-10** (Extended generation and prime-resource balance): ANS2-T02, ANS2-T03, ANS2-T04, ANS2-T07, ANS2-T09a.
- **Used by ATL-11** (Entropy and admissibility): ANS2N-T04b.

## Review boundary

Without a review verdict: ANS-T28 (N).

Qualified verdicts:

- ANS-T27: Valid for the infimal Gevrey order; membership at exactly that order is open.

## All results and proof sources

- **ANS-I v002:** ANS-T23, ANS-T24.
- **ANS-I v003:** ANS-T23a, ANS-T24a, ANS-T27, ANS-T28a, ANS-T28.
- **ANS-I v004:** ANS-T24b.
