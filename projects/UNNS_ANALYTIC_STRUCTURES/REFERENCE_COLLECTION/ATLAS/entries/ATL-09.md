# ATL-09: Collective growth at and below s = 1

## Mathematical object

$G_k(s)^{1/k}$ for real $s>1/2$, with particular attention to $1/2<s\le1$ and the window near $1$. For $s\le1$ one has $B(s)=\infty$ and the radius of convergence of $\sum_kG_k(s)t^k$ is zero. For $s\le1/2$ the fixed-depth sums already diverge.

## Established structure

- At $s=1$ the growth has exact order $\log k$: $\log k-\log\log k+O(1)\le G_k(1)^{1/k}\le(e^{\gamma}\zeta(2)+o(1))\log k$, and for $1/2<s<1$ it is at least $c_sk^{1-s}$ (T48).
- The constants are sharpened on both sides (T49 below, T48a above):
$$\boxed{1.107910\ldots\le\liminf_{k\to\infty}\frac{G_k(1)^{1/k}}{\log k}\le\limsup_{k\to\infty}\frac{G_k(1)^{1/k}}{\log k}\le e^{\gamma}}$$
- Under growth constants $0<c_-\le c_+<\infty$, the exponential generating function $\sum_kG_k(1)t^k/k!$ is entire of order one and infinite type, with matching maximum-modulus bounds (T48b).
- Two-sided bounds hold in the window $s=1+\tau/\log k$ for every fixed real $\tau$ as $k\to\infty$ (T50). No uniform statement for a growing parameter $\tau=\tau(k)$ is established.

## What it reveals

Without admissibility the value at $s=1$ would be infinite. With it, the growth rate is finite and of size $\log k$, which is also the total weight of the letters up to a fixed power of $k$.

## Further structure

The lower constant above one uses letters beyond the base range whose prime factors are small, counted with the Dickman function (T49).

## Open boundary

Existence and value of $\lim G_k(1)^{1/k}/\log k$ (ANS-LIM), including whether the upper limit is strictly below $e^{\gamma}$. A heuristic recorded in v015, which assumes an equidistribution that is not proved, suggests a value below $e^{\gamma}$.

## Reading across (interpretation)

The constraint here is a balance between primes supplied by $N+1$ and consumed by $N$, the same bookkeeping as in ATL-10. The variational principle of ATL-11 gives a broader context for this reading. No theorem in the collection carries it over to $s=1$: those results assume $a>1$ in the extended grammar.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS-T48 | Growth of G_k at s = 1 of exact order log k | PROVED | V |
| ANS-T48a | Upper constant e^gamma | PROVED | V |
| ANS-T49 | Lower constant 1.1079 | PROVED | V |
| ANS-T50 | Growth bounds in the window around s = 1 | PROVED | VQ |

## Recorded open questions

- **ANS-LIM:** Existence and value of lim G_k(1)^(1/k)/log k. A heuristic (v015, unproved) suggests a value below e^gamma. No separate ID in the releases; ANS-LIM is a label of this collection.

## Connected entries (cited dependencies)

- **Uses ATL-04** (Collective critical suppression): ANS-T23, ANS-T23a.

## Review boundary

Every result in this entry has a review verdict.

Qualified verdicts:

- ANS-T48b: The bounding constants satisfy 0 < c_- <= c_+ < infinity.
- ANS-T50: Fixed real tau as k tends to infinity; no uniform statement for tau = tau(k).

## All results and proof sources

- **ANS-I v014:** ANS-T48.
- **ANS-I v015:** ANS-T48a, ANS-T48b, ANS-T49, ANS-T50.
