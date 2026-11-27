# ATL-07: Depth two: an arithmetic singularity hierarchy

## Mathematical object

$G_2(s)=\sum_{a,b\ge1}\big[\gcd((a+1)^2,b)/((a+1)^2(b+1)^2)\big]^s$ and the integer exponents $e_n$ obtained by expanding its Euler factor in powers of $p^{-s}$.

## Established structure

- **First continuation.** A Hurwitz-zeta representation gives continuation to $\operatorname{Re}s>1/3$ and the double pole at $1/2$, with $A_2(X)\sim(\kappa/2)\sqrt X\log X$ (T05, T13).
- **Factorization.** $G_2$ is meromorphic on $\operatorname{Re}s>1/5$ with a simple pole at $1/3$ (T45), and on $\operatorname{Re}s>0$, where the line $\operatorname{Re}s=0$ is a natural boundary (T45a).
- **Pole divisor.** On the positive real axis the poles are at $1/n$ with $e_n>0$, of order $e_n$ (T45d). Examples: orders $2,1,1,1$ at $1/2,1/3,1/7,1/8$ (T45b) and order two at $1/12$ (T45c).
- **Exponents.** $nc_n=-2R^n\cos n\theta+O(\tau(n)R^{n/2})$ for the stated algebraic $R>1$ and $\theta$, each sign of $e_n$ has density one half (T45e), and the normalized exponents follow an arcsine law (T45f).
- **Zeta zeros.** For $e_n<0$, all but a small set of critical-line zeros $\rho$ give poles at $\rho/n$ (T38d; cases T38a, T38b), with lower bounds (T38c) and asymptotic populations on the lines $\operatorname{Re}s=1/(2n)$ (T38e).

The description of **all** non-real poles in the second corollary of T45d assumes the Riemann hypothesis. The other statements listed here are recorded without it.

## What it reveals

A single coupling between two letters produces an unbounded hierarchy of singularities, accumulating on a natural boundary, with orders governed by one cubic polynomial.

## Further structure

The signs of the exponents decide whether a given $n$ contributes poles on the real axis or poles at rescaled zeta zeros.

## Open boundary

The maximal meromorphic domain and the pole divisor are established. Two questions about depth two remain unresolved: the classification of the zeros of $G_2$ (ANS-G2Z), and a rigorous sharp, unsmoothed secondary counting term of order $X^{1/3}$ in $A_2(X)$ (ANS-A2S). They are preserved as mathematical questions, not active investigations. The corresponding hierarchy at higher depth is also open (ATL-08).

## Reading across (interpretation)

The natural boundary is a candidate point of contact with structural obstruction theory. The poles at rescaled zeta zeros reflect zeta factors in the formula; they carry no information about where those zeros lie.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS-T45 | Depth two to Re s > 1/5 with a simple pole at 1/3 | PROVED | V |
| ANS-T45a | Depth two: meromorphic on Re s > 0 with natural boundary | PROVED | V |
| ANS-T45d | Depth two: exact pole divisor on Re s > 0 | PROVED | V |
| ANS-T45e | Depth two: asymptotics and sign densities of the Euler exponents | PROVED | V |
| ANS-T38d | Depth two: vertical pole family for every negative exponent | PROVED | V |
| ANS-T38e | Depth two: pole populations on the lines Re s = 1/(2n) | PROVED | V |

## Recorded open questions

- **ANS-G2Z:** Classification of the zeros of G_2 (the maximal meromorphic domain and the pole divisor are established). ID is a label of this collection.
- **ANS-A2S:** Rigorous sharp, unsmoothed secondary counting term of order X^(1/3) in A_2(X) (recorded as not proved in ANS-I v008; a smoothed form holds). ID is a label of this collection.

## Connected entries (cited dependencies)

- **Uses ATL-01** (Exact admissible composition): ANS-T03.
- **Uses ATL-06** (Fixed-depth singularity architecture): ANS-T34.
- **Used by ATL-08** (The mechanism at one third): ANS-T46b, ANS-T46h-i, ANS-T46k, ANS-T46s.

## Review boundary

Every result in this entry has a review verdict.

## All results and proof sources

- **ANS-I v001:** ANS-T13, ANS-T05.
- **ANS-I v008:** ANS-T45.
- **ANS-I v009:** ANS-T45a, ANS-T45b, ANS-T38a.
- **ANS-I v010:** ANS-T45d, ANS-T45c, ANS-T45e, ANS-T38d, ANS-T38b, ANS-T38c.
- **ANS-I v011:** ANS-T45f, ANS-T38e.
