---
title: "ANS-I v009 --- The meromorphic domain of the depth-two function"
author: "UNNS Research Collective"
date: "27 November 2026"
---

Research notes. They continue ANS-I v008; notation is as there. All results concern the nesting grammar. New proofs are pending review; no claim of priority is made, and no comprehensive literature review has been done.

# 0. Review of v008

The owner's review found T34, T34a, T45, T42a, T43 and T44 valid. Three points of exposition have been addressed: the analytic nature of the sum--integral remainder and the last step of the block-frequency argument are now explicit in the v008 proofs, and the exactness of the pole order for restricted functions, which v008 stated in its register without proof, is supplied below.

## 0.1 Exact pole order for every restriction (ANS-T34b)

**Theorem.** For all $k\ge1$, $D\ge1$, the pole of $G_k(s;D)$ at $1/2$ has order exactly $k$, and $\lim_{s\to1/2}(2s-1)^kG_k(s;D)\ge1/D$.

*Proof (owner's review).* Since $N_1\mid K(w)$, all words with $D\mid N_1$ occur in $G_k(s;D)$, and $E(w)\le\prod(N_i+1)^2$. So for real $\sigma>1/2$,
$$G_k(\sigma;D)\ge\Big(\sum_{D\mid N}(N+1)^{-2\sigma}\Big)\big(\zeta(2\sigma)-1\big)^{k-1}.$$
Multiply by $(2\sigma-1)^k$ and let $\sigma\downarrow1/2$; the right side tends to $1/D$. The limit on the left exists by T34. $\square$

# 1. The natural boundary of $G_2$ (ANS-T45a)

Put $\mathcal P(s)=\prod_p(1+p^{-2s}+p^{-3s})$. Since $1+p^{-3s}/(1+p^{-2s})=(1+p^{-2s}+p^{-3s})/(1+p^{-2s})$ and $\prod_p(1+p^{-2s})=\zeta(2s)/\zeta(4s)$, T45 can be written
$$G_2(s)=\zeta(2s)\,\zeta(4s)\,\mathcal P(s)+\zeta(2s)\big(F_2(s)-1\big)+1.\qquad(1)$$

**Theorem.** $G_2$ is meromorphic on $\operatorname{Re}s>0$, and the line $\operatorname{Re}s=0$ is its natural boundary: it has no meromorphic continuation through any point of that line.

The statement and the method are the owner's.

## 1.1 The Euler product

Estermann (1928): for $h\in\mathbb Z[z]$ with $h(0)=1$, the product $\prod_ph(p^{-s})$ is meromorphic on $\operatorname{Re}s>0$; unless $h$ is a product of cyclotomic polynomials, $\operatorname{Re}s=0$ is its natural boundary. Here $h(z)=1+z^2+z^3$. As $h(-2)=-3$ and $h(-1)=1$, it has a root of modulus greater than $1$, so it is not a product of cyclotomic polynomials. Hence $\mathcal P$ has exactly this behaviour. With (1) and the holomorphy of $F_2$ on $\operatorname{Re}s>0$, $G_2$ is meromorphic there.

## 1.2 The additive term crosses the line

On $|\operatorname{Re}s|<1/16$ write
$$\zeta\big(2s,1+\tfrac1d\big)-\zeta(2s)=-\frac{2s\,\zeta(2s+1)}d+E(s,d).\qquad(2)$$
Here $E(s,d)=\sum_{m\ge1}\big[(m+\tfrac1d)^{-2s}-m^{-2s}+\tfrac{2s}d m^{-2s-1}\big]$ for $\operatorname{Re}s>0$ and $d\ge2$. By Taylor's theorem each term is $O_{\mathcal K}(d^{-2}m^{-2\sigma-2})$ uniformly for $s$ in a compact set $\mathcal K$ of $\operatorname{Re}s>-1/2$, so $E$ is holomorphic there and $O_{\mathcal K}(d^{-2})$. For $d=1$ the left side of (2) is $-1$, and $E(s,1)=-1+2s\zeta(2s+1)$ is holomorphic on the same half-plane. Therefore
$$F_2(s)=-2s\,\zeta(2s+1)\,\mathcal D(s)+\mathcal R(s),\qquad\mathcal D(s)=\sum_d\frac{J_s(d)}{d\,(d\rho(d))^{2s}},\quad\mathcal R(s)=\sum_d\frac{J_s(d)}{(d\rho(d))^{2s}}E(s,d).$$
For $|\sigma|<1/16$ one has $|J_s(d)|\le2^{\omega(d)}\max(d^\sigma,1)$ and $\rho(d)\le d$, so the terms of $\mathcal R$ are $O(2^{\omega(d)}d^{-7/4})$: $\mathcal R$ is holomorphic on the strip.

For $\sigma>0$, $\mathcal D$ has an Euler product with local factor
$$\mathcal D_p=1+a-b+O(p^{-3/2}),\qquad a=p^{-1-3s},\ b=p^{-1-4s},$$
the estimate being uniform on the strip. Then $\mathcal D_p(1-a)/(1-b)=1+O(p^{-3/2})$, so
$$\mathcal D(s)=\frac{\zeta(1+3s)}{\zeta(1+4s)}\,\mathcal V(s)$$
with $\mathcal V$ a normally convergent Euler product, holomorphic on the strip. Hence $F_2$ is meromorphic on $\operatorname{Re}s>-1/16$.

## 1.3 No cancellation

Suppose $G_2$ continued meromorphically to a disc $U$ about a point $i\tau_0$. By §1.2,
$$\mathcal P(s)=\frac{G_2(s)-\zeta(2s)(F_2(s)-1)-1}{\zeta(2s)\,\zeta(4s)}$$
would give a meromorphic continuation of $\mathcal P$ to a neighbourhood of $i\tau_0$ in $U$, contrary to Estermann. $\square$

# 2. Zeta factors and poles of $G_2$

## 2.1 Factorisation (ANS-T45b)

With $z=p^{-s}$ the local factor of $H$ is $1-(z^5+z^6)/(1+z^2)$, and as power series
$$1-\frac{z^5+z^6}{1+z^2}=(1-z^5)(1-z^6)(1-z^7)^{-1}(1-z^8)^{-1}(1-z^9)(1-z^{10})\,\big(1+O(z^{12})\big).$$
(Coefficients computed exactly.) Hence, with $H_{12}$ the Euler product of the last factor, absolutely convergent and holomorphic on $\operatorname{Re}s>1/12$,
$$H(s)=\frac{\zeta(7s)\,\zeta(8s)}{\zeta(5s)\,\zeta(6s)\,\zeta(9s)\,\zeta(10s)}\,H_{12}(s),$$
$$G_2(s)=\zeta(2s)^2\zeta(3s)\,H(s)+\zeta(2s)\big(F_2(s)-1\big)+1.\qquad(3)$$
The first two factors are those of the review, $H=\mathcal H_7/(\zeta(5s)\zeta(6s))$ on $\operatorname{Re}s>1/7$. In that half-plane a pole of $G_2$ at $\rho/5$ or $\rho/6$ would need $\operatorname{Re}\rho>5/7$. To reach the zeros on the critical line one must pass below $1/10$, which (3) does.

## 2.2 Real poles

**Theorem.** On the real segment $s>1/12$ the poles of $G_2$ are at $1/2$ (double) and at $1/3$, $1/7$, $1/8$ (simple).

*Proof.* In (3) the second part is holomorphic away from $1/2$. In $\zeta(2s)^2\zeta(3s)H(s)$ every zeta value at a real argument in $(0,1)\cup(1,\infty)$ is finite and non-zero, so only the arguments equal to $1$ matter: they give poles from $\zeta(2s)^2$, $\zeta(3s)$, $\zeta(7s)$, $\zeta(8s)$ and zeros from the denominator. Each local factor of $H_{12}$ is positive, because $1-(z^5+z^6)/(1+z^2)>0$ for $0<z<1$. $\square$

## 2.3 Poles at one fifth of the zeta zeros (ANS-T38a)

**Theorem.** Let $\rho=\tfrac12+i\gamma$ be a zero of $\zeta$ of multiplicity $m$ with $\zeta(n\rho/5)\ne0$ for $n=2,3,6,7,8,9$. Then $G_2$ has a pole of order exactly $m$ at $\rho/5$. Consequently the number of distinct poles of $G_2$ on $\operatorname{Re}s=1/10$ with $|\operatorname{Im}s|\le T$ is $\gg T\log T$.

*Proof.* Put $s_0=\rho/5$, with real part $1/10>1/12$. In (3), $\zeta(5s)^{-1}$ has a pole of order $m$ at $s_0$. The factors $\zeta(2s)$, $\zeta(3s)$, $\zeta(6s),\dots,\zeta(9s)$ are finite and non-zero there by assumption, and so is $\zeta(10s)$, since $10s_0=2\rho$ has real part $1$. It remains to see that $H_{12}(s_0)\ne0$. The local factor of $H$ equals $(1-z^3)(1+z^2+z^3)/(1+z^2)$, and no $1-z^n$ or $1+z^2$ vanishes for $|z|<1$. So a local factor of $H_{12}$ can vanish only if $1+z^2+z^3=0$, with $|z|=p^{-1/10}$. The real root has modulus $\beta>1$, where $\beta^3=\beta^2+1$; the other two have modulus $\beta^{-1/2}$. So $p=\beta^5=6.76\ldots$, which is not an integer. The product converges absolutely, so $H_{12}(s_0)\ne0$. The additive part of (3) is holomorphic at $s_0$.

For the count, Selberg's theorem gives $\gg U\log U$ distinct zeros $\tfrac12+i\gamma$ with $0<\gamma\le U$. For $n=6,\dots,9$, a zero at $n\rho/5$ has real part $n/10\ge0.6$ and height at most $2U$. For $n=2,3$, a zero at $n\rho/5$ reflects under $s\mapsto1-\bar s$ to a zero with real part at least $0.7$ at the same height. By the Bohr--Landau density theorem each of these sets has $O(U)$ elements. Take $U=5T$. $\square$

**Remarks.** This is unconditional, and it carries no information about the Riemann hypothesis: the zeros enter through the factorisation, as in Estermann's method. If the hypothesis holds, the assumption of the theorem is satisfied by every non-trivial zero, and $G_2$ has no non-real poles in $\operatorname{Re}s>1/10$. The theorem concerns $G_2$ only, not the complete function $\mathcal G$.

# 3. Depth three and higher at $1/3$ (ANS-T46)

Nothing is proved here. The following heuristic indicates what to expect, and it differs from the pattern suggested by $k=1,2$.

**Mechanism.** In the expansion $G_k=\sum_w\prod(N_i+1)^{-2s}g_i^s$, a prime $p$ linking a letter $i$ with $p\mid N_i+1$ to a later letter $j$ with $p\mid N_j$, both letters being of size about $p$, contributes $p^{s}\cdot p^{-2s}\cdot p^{-2s}=p^{-3s}$. Summed over $p$ this is a factor of the type $\zeta(3s)$. Links with different primes are independent if every letter is *either* a sender *or* a receiver: a sender attached to several primes has size about their product, and likewise a receiver. With senders $S$, receivers $R$ and all links $i<j$, the number of independent factors is the number of such pairs, at most $\lfloor k^2/4\rfloor$ (first half sending, second half receiving). A letter that both sends and receives lies in the progression $N\equiv0\ (P_{\rm in})$, $N\equiv-1\ (P_{\rm out})$, whose least element is generically of size $P_{\rm in}P_{\rm out}$; the resulting fluctuating term has mean zero if these least elements are equidistributed.

**Conjecture (ANS-T46b).** For $k\ge2$, $G_k$ has a pole at $s=1/3$ of order $\lfloor k^2/4\rfloor$.

This gives order $1$ at $k=2$ (proved, T45), order $2$ at $k=3$ and order $4$ at $k=4$. A proof needs (i) continuation past $1/3$, (ii) equidistribution, with a power saving, of the least elements above, which involves inverses modulo $P_{\rm out}$ and so estimates of Kloosterman type, and (iii) a non-vanishing check on the leading coefficient. The depth-three counts of v008 are compatible with order $2$ but do not test it.

# 4. Computations

Finite and floating-point checks only. Parameters and outputs are in `results/`.

- Factorisation: exact integer power series to order $30$ give exponents $c_5,\dots,c_{10}=-1,-1,1,1,-1,-1$ in $\prod(1-z^n)^{-c_n}$, with first discrepancy at order $12$.
- For the first $30$ zeros $\rho$, the smallest value of $|\zeta(n\rho/5)|$, $n\in\{2,3,6,\dots,10\}$, is $0.156$ in floating point, so the assumption of T38a holds numerically for them.
- $d^2|E(s,d)|$ stays bounded for $d$ up to $1000$ at four points of the strip.
- The facts used in §0.1 held on $13824$ words.

# 5. Open

- ANS-T46, T46a, T46b: depth three and higher at and beyond $1/3$; natural boundaries at higher depth.
- Zeros of $G_2$; poles of $G_2$ with $\operatorname{Re}s\le1/12$.
- The sharp second term of $A_2(X)$.
- ANS-T33, T39; ANS-T38 for the complete functions. Not addressed.
