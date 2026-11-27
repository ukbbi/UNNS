# ATL-03: The characteristic exponent and its singular point

## Mathematical object

The full history series $\mathcal G(s,1)=\sum_kG_k(s)$ and the counting functions $N_x(X)$, $A(X)$, $C(X)$.

## Established structure

- **Growth in depth** is $G_k(\sigma)^{1/k}\to B(\sigma)$ for $\sigma>1$ and infinite for $0\le\sigma\le1$, so the abscissa is $\sigma_c$ (T09; a sufficient criterion is T07).
- **Counting.** For every fixed source, and for the other two counts, $\log Z(X)/\log X\to\sigma_c$ (T10).
- **Probability form.** $G_k(a)/B(a)^k=\mathbb E\,K_k^{-a}$ (T16). At $\sigma_c$ the depth terms tend to zero although their $k$-th roots tend to one (T19).
- **Below a pure power.** $Z(X)=o(X^{\sigma_c})$ (T21).
- **The singular point.** $\mathcal G(s,1)$ has no meromorphic continuation through $\sigma_c$ (T20), yet converges on the whole critical surface under the stated condition and is infinitely differentiable up to the line $\operatorname{Re}s=\sigma_c$ (T22).
- **The rest of the line is regular.** The function continues holomorphically across every point $\sigma_c+i\tau$ with $\tau\ne0$; the line is not a natural boundary (T31).

## What it reveals

The exponent is the one that independent letters would give, $B(\sigma_c)=1$: admissibility does not move it. Admissibility changes the nature of the singularity and pushes the counts below the pure power. The singularity is smooth from the right and still not meromorphic.

## Further structure

The continuation of T31 comes from cancellation inside each $G_k$; the word series itself does not converge absolutely to the left of the line.

## Open boundary

The nature of the singularity at $\sigma_c$, including whether continuations above and below it agree to its left (ANS-T33), and the analogous theory for higher-degree and other nesting grammars (ANS-T25).

## Reading across (interpretation)

A smooth non-meromorphic singularity is a second kind of obstruction, different in nature from the natural boundary of ATL-07.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS-T09 | Growth in depth and the sharp boundary sigma_c | PROVED | V |
| ANS-T10 | Growth exponent of every counting function | PROVED | V |
| ANS-T20 | No meromorphic continuation through sigma_c | PROVED | V |
| ANS-T22 | Convergence on the critical surface; smooth singularity | PROVED | V |
| ANS-T31 | Holomorphic continuation across the critical line away from sigma_c | PROVED | V |
| ANS-T21 | Strict growth suppression | PROVED | V |

## Recorded open questions

- **ANS-T33:** Nature of the singularity at sigma_c; whether the continuations above and below agree to its left.
- **ANS-T25:** Higher-degree and other nesting grammars.

## Connected entries (cited dependencies)

- **Uses ATL-02** (Finite saturation and unbounded obstruction): ANS-T15, ANS-T18.
- **Uses ATL-04** (Collective critical suppression): ANS-T23.
- **Used by ATL-01** (Exact admissible composition): ANS-T14.
- **Used by ATL-02** (Finite saturation and unbounded obstruction): ANS-T11.
- **Used by ATL-04** (Collective critical suppression): ANS-T24.
- **Used by ATL-05** (Generated populations and typical histories): ANS-T35, ANS-T36, ANS-T37, ANS-T37a, ANS-T40.

## Review boundary

Every result in this entry has a review verdict.

## All results and proof sources

- **ANS-I v001:** ANS-T07, ANS-T09, ANS-T10.
- **ANS-I v002:** ANS-T16, ANS-T19, ANS-T20, ANS-T21, ANS-T22.
- **ANS-I v005:** ANS-T31.
