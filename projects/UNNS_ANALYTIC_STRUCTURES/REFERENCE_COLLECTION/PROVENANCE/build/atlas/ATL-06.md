title: Fixed-depth singularity architecture
principal: T12 T32 T34 T34a T34b
entries: T12 T32 C1 T32a T34 T34a T34b
open: ANS-T38
---
## Mathematical object

$G_k(s)$ for a fixed depth $k$, its restrictions to words whose source is divisible by $D$, and the counting function $A_k(X)$.

## Established structure

- **Region of convergence.** The weighted sum over words of length $k$ converges exactly in the stated region; in particular $G_k$ has abscissa $1/2$ at every depth (T12).
- **Counting.** $A_k(X)\sim\kappa_k\sqrt X(\log X)^{k-1}/(2^{k-1}(k-1)!)$, with $\kappa_k$ an Euler product (T32); as a corollary, $(2\sigma-1)^kG_k(\sigma)\to\kappa_k$ at $1/2$ (C1). The local factors have the expansion $1+\binom k2p^{-3/2}+\binom k3p^{-2}+O_k(p^{-5/2})$ (T32a).
- **Continuation.** Every $G_k$ is meromorphic on $\operatorname{Re}s>1/3$, with a single pole there, at $1/2$, of order exactly $k$ (T34), also for every source restriction (T34b).
- **Full main term.** $A_k(X)=\sqrt X\,P_{k-1}(\log X)$ with a power saving (T34a).

## What it reveals

At fixed depth $k$, the principal pole has order $k$, one order per letter position. Arithmetic coupling changes its leading coefficient and generates additional singularity structures.

## Further structure

To the left of $1/3$ the picture depends on depth: ATL-07 treats depth two and ATL-08 the singularity at one third.

## Open boundary

Zeros and poles of the complete functions (ANS-T38). Continuation of general $G_k$ to $1/3$ and beyond is part of ATL-08.

## Reading across (interpretation)

The abscissae $1/2$ at fixed depth and $\sigma_c$ for the whole series show that the infinite sum over depths creates a singularity that no single depth has.
