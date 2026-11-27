---
title: "ANS-I v010 --- Arithmetic singularity hierarchies"
author: "UNNS Research Collective"
date: "27 November 2026"
---

Research notes. They continue ANS-I v009; notation is as there. All results concern the nesting grammar. New proofs are pending review; no claim of priority is made, and no comprehensive literature review has been done.

# 0. Review of v009

The owner's review found T34b, T45a, T45b and T38a valid. It proposed T45c, T38b and the passage to simple poles, which are treated in §§1--2.

**Sharper bound.** In v009 §2.1, within $\operatorname{Re}s>1/7$ a pole at $\rho/5$ needs $\operatorname{Re}\rho>5/7$, and one at $\rho/6$ needs $\operatorname{Re}\rho>6/7$.

## 0.1 An exact non-vanishing argument (owner's review)

Let $\beta>1$ be the real root of $x^3-x^2-1$, so that $-\beta$ is the real root of $1+z^2+z^3$ and the other two roots of the latter have modulus $\beta^{-1/2}$.

**Lemma.** $\beta^j\notin\mathbb Z$ for every integer $j\ge1$.

*Proof.* $x^3-x^2-1$ has no rational root, so it is irreducible; its other roots have modulus $\beta^{-1/2}<1$. If $\beta^j=n\in\mathbb Z$, an embedding sending $\beta$ to a conjugate $\beta'$ gives $\beta'^j=n=\beta^j$, but $|\beta'^j|<1<\beta^j$. $\square$

Consequently $1+p^{-2s}+p^{-3s}\ne0$ for every prime $p$ on each line $\operatorname{Re}s=1/(2j)$, since a zero there would need $p=\beta^j$. This replaces the numerical step $\beta^5=6.76\ldots$ in v009 §2.3.

# 1. The pole divisor of $G_2$ (ANS-T45d)

Let $h(z)=1-(z^5+z^6)/(1+z^2)=(1-z^3)(1+z^2+z^3)/(1+z^2)$ be the local factor of $H$, and define integers $c_n$ by
$$h(z)=\prod_{n\ge1}(1-z^n)^{-c_n}.\qquad(1)$$
Put $e_2=c_2+2$, $e_3=c_3+1$ and $e_n=c_n$ otherwise. Since $c_1=\dots=c_4=0$ we have $e_1=e_4=0$, $e_2=2$, $e_3=1$. For $M\ge4$ let $H_{M+1}=H\prod_{n\le M}\zeta(ns)^{-c_n}$. Its local factor $h(z)\prod_{n\le M}(1-z^n)^{c_n}$ is analytic in $|z|<1$ and equals $1+O(z^{M+1})$, so the product converges absolutely and locally uniformly on $\operatorname{Re}s>1/(M+1)$. There, by v009 (3),
$$G_2(s)=\mathcal M(s)+\mathcal A(s),\qquad\mathcal M=\prod_{2\le n\le M}\zeta(ns)^{e_n}\,H_{M+1},\qquad\mathcal A=\zeta(2s)(F_2-1)+1,\qquad(2)$$
and $\mathcal A$ is holomorphic on $\operatorname{Re}s>0$ apart from a simple pole at $1/2$.

For a complex number $w$ let $\mu(w)$ be the multiplicity of $w$ as a zero of $\zeta$ ($0$ if $\zeta(w)\ne0$). For $s_0$ with $\operatorname{Re}s_0>0$ let $\delta(s_0)=1$ if $1+p^{-2s_0}+p^{-3s_0}=0$ for some prime $p$, and $0$ otherwise.

**Theorem.** (i) The poles of $G_2$ on the half-line $s>0$ are exactly the points $1/n$ with $e_n>0$, and the order at $1/n$ is $e_n$.

(ii) For non-real $s_0$ with $\sigma_0=\operatorname{Re}s_0>0$, the order of the pole of $G_2$ at $s_0$ is $\max(0,-\nu(s_0))$, where
$$\nu(s_0)=\sum_{2\le n<1/\sigma_0}e_n\,\mu(ns_0)+\delta(s_0).$$

*Proof.* Take $M\ge\max(4,1/\sigma_0)$ with $\sigma_0=\operatorname{Re}s_0$. (i) For real $s_0>0$ the local factors of $H_{M+1}$ are positive, because $h(z)>0$ on $(0,1)$; hence $H_{M+1}(s_0)>0$. A real zeta value at an argument in $(0,1)\cup(1,\infty)$ is finite and non-zero. So $\mathcal M$ has a pole or zero at $s_0$ only if $s_0=1/n$, and then its order there is that of $\zeta(ns)^{e_n}$. For $n=2$ the pole of order $2$ cannot be cancelled by the simple pole of $\mathcal A$.

(ii) $\nu(s_0)$ is the order of $\mathcal M$ at $s_0$: for $n\sigma_0\ge1$ the value $\zeta(ns_0)$ is finite and non-zero, and for $n\sigma_0<1$ the factor contributes $e_n\mu(ns_0)$. A local factor of $H_{M+1}$ vanishes only if $1+z^2+z^3=0$ with $|z|=p^{-\sigma_0}$, which forces $|z|=\beta^{-1/2}$ and so determines $p$; the zero is simple. $\mathcal A$ is holomorphic at $s_0$. $\square$

**Corollary 1 (ANS-T45c, owner's review).** $G_2$ has a pole of order exactly two at $1/12$: $c_{12}=2$.

The first real poles and their orders are:

| $n$ | 2 | 3 | 7 | 8 | 12 | 13 | 17 | 18 | 21 | 22 | 23 | 26 | 27 | 28 |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| order at $1/n$ | 2 | 1 | 1 | 1 | 2 | 1 | 3 | 2 | 1 | 6 | 2 | 4 | 13 | 3 |

**Corollary 2.** Assume the Riemann hypothesis. The non-real poles of $G_2$ in $\operatorname{Re}s>0$ are exactly the points $\rho/n$, with $\rho$ a non-trivial zero and $e_n<0$, and the order is $|e_n|\mu(\rho)$.

*Proof.* A non-zero term $\mu(ns_0)$ needs $\operatorname{Re}ns_0=1/2$, so only $n=1/(2\sigma_0)$ can contribute. At such a point $\delta=0$ by the lemma; elsewhere, if no term contributes, $\nu\ge0$. $\square$

# 2. Vertical pole families (ANS-T38b, T38c, T38d)

**Theorem.** Let $n\ge2$ with $e_n<0$. For all but $O_n(U)$ zeros $\rho=\tfrac12+i\gamma$, $0<\gamma\le U$, the point $\rho/n$ is a pole of $G_2$ of order exactly $|e_n|\,\mu(\rho)$.

*Proof.* Apply T45d(ii) at $s_0=\rho/n$, where $1/\sigma_0=2n$. By the lemma $\delta=0$. Exclude the $\rho$ with $\zeta(k\rho/n)=0$ for some $2\le k<2n$, $k\ne n$. For $k>n$ such a zero has real part $k/(2n)\ge\tfrac12+\tfrac1{2n}$; for $k<n$ its reflection under $w\mapsto1-\bar w$ has that property. Heights are at most $2U$. By the Bohr--Landau theorem there are $O_n(U)$ exceptions. For the others $\nu=e_n\mu(\rho)$. $\square$

The cases $n=5$ (T38a) and $n=6$ (T38b, owner's review) have $e_n=-1$.

**Corollary (ANS-T38c; the method is the owner's).** The number of poles of $G_2$ of order exactly $|e_n|$ on $\operatorname{Re}s=1/(2n)$ with $0<\operatorname{Im}s\le T$ is at least $\big(\tfrac{n}{5\pi}+o(1)\big)T\log T$. In particular $\rho/5$ and $\rho/6$ give at least $(1/\pi+o(1))T\log T$ and $(6/(5\pi)+o(1))T\log T$ **simple** poles.

*Proof.* By Conrey (1989) at least $\tfrac25$ of the zeros are simple and on the critical line. Up to height $U=nT$ that is at least $(\tfrac25+o(1))\frac{nT}{2\pi}\log T$ zeros, of which $O_n(T)$ are excluded. $\square$

# 3. The exponents (ANS-T45e)

Let $\alpha$ be a non-real root of $x^3+x+1$, put $R=|\alpha|=\beta^{1/2}=1.2106\ldots$ and $\theta=\arg\alpha$, and let $p_N$ be the sum of the $N$-th powers of the three roots.

**Theorem.** (i) $n\,c_n=\sum_{d\mid n}\mu_{\rm M}(n/d)\,A_d$, where $\mu_{\rm M}$ is the Möbius function and
$$A_N=-p_N-3\,[3\mid N]+2(-1)^{N/2}[2\mid N].$$
(ii) $n\,c_n=-2R^n\cos n\theta+O(\tau(n)R^{n/2})$.

(iii) The sets $\{n:e_n<0\}$ and $\{n:e_n>0\}$ both have natural density $\tfrac12$.

*Proof.* (i) From (1), $\log h(z)=\sum_N\frac{z^N}N\sum_{n\mid N}nc_n$. From the factorisation of $h$, with $1+z^2+z^3=\prod(1-\alpha_iz)$ over the roots $\alpha_i$ of $x^3+x+1$, the coefficient of $z^N/N$ is $A_N$. Invert.

(ii) The real root has modulus $\beta^{-1}<1$, so $p_N=2R^N\cos N\theta+O(1)$. The divisors $d<n$ satisfy $d\le n/2$ and contribute $O(\tau(n)R^{n/2})$.

(iii) $\theta/\pi$ is irrational. Otherwise $\alpha^m=\bar\alpha^m$ for some $m\ge1$. The discriminant of $x^3+x+1$ is $-31$, not a square, so the Galois group is $S_3$, and some automorphism fixes $\alpha$ and sends $\bar\alpha$ to the real root $r$. Then $\alpha^m=r^m$, impossible since $|\alpha|>1>|r|$. By Weyl's theorem $n\theta$ is equidistributed modulo $2\pi$. For fixed $\eta>0$, for large $n$ with $|\cos n\theta|>\eta$ the sign of $c_n$ is opposite to that of $\cos n\theta$; each sign occurs on a set of density tending to $\tfrac12$ as $\eta\to0$. $\square$

**Consequences.** $G_2$ has real poles at $1/n$ for a set of $n$ of density $\tfrac12$, and for another set of density $\tfrac12$ the line $\operatorname{Re}s=1/(2n)$ carries $\gg_nT\log T$ poles. In both cases the orders are unbounded: they exceed $\eta R^n/n$ on sets of density close to $\tfrac12$. The mechanism, a factorisation of an Euler product into zeta values with Möbius-determined exponents, is classical (it underlies Estermann's theorem); what is specific is the polynomial supplied by the grammar.

# 4. Depth three: a letter linked on both sides (ANS-T46c)

## 4.1 The model

In the mechanism of v009 §3, a middle letter $M$ may receive a prime $q$ from the first letter ($q\mid M$) and send a prime $r$ to the last ($r\mid M+1$). The weights are about $q^{-s}$ and $r^{-s}$. This leads to the series
$$U(s)=\sum_{M\ge1}M^{-2s}\sigma_{-s}(M)\,\sigma_{-s}(M+1),\qquad\sigma_{-s}(M)=\sum_{d\mid M}d^{-s},$$
absolutely convergent for $\operatorname{Re}s>1/2$. It is a **model**: $G_3$ also contains Möbius corrections, the link from the first letter to the last, and the interaction of the three gcds. Counting each link separately suggests two factors $\zeta(3s)$.

**Theorem.** $U$ is meromorphic on $\operatorname{Re}s>3/10$. Its poles there are simple poles at $1/2$ and $1/3$, and
$$\operatorname{Res}_{s=1/3}U=\frac{2\,\zeta(2/3)\,\zeta(4/3)}{3\,\zeta(2)}\ne0.$$

So two links through one letter produce a pole of order one at $1/3$, not two. $U$ is a shifted divisor sum of the kind studied by Ingham and Estermann; no novelty is claimed for the theorem. Its use here is that it tests the step on which the conjecture T46b depends, in the simplest case.

## 4.2 Decomposition

Since $(M,M+1)=1$, summing over $q\mid M$, $r\mid M+1$ with $(q,r)=1$ gives
$$U(s)=\sum_{(q,r)=1}(qr)^{-3s}\,\zeta\big(2s,\alpha(q,r)\big),\qquad\alpha(q,r)=\frac{M_0}{qr},$$
where $M_0\in[1,qr]$ is the least element of the progression. The term $q=r=1$ is $\zeta(2s)$; otherwise $q<r$ or $q>r$. For an integer $x$ let $\langle x\rangle_q\in\{1,\dots,q\}$ be its residue, and $\bar u$ an inverse of $u$ modulo $q$.

*Case $q>r$.* Write $q=mr+v$ with $m\ge1$, $1\le v\le r$, $(v,r)=1$. Then $\alpha=\langle-\bar v\rangle_r/r$.

*Case $q<r$.* Write $r=mq+u$ with $m\ge1$, $1\le u\le q$, $(u,q)=1$. Then $M_0=ry-1$ with $y=\langle\bar u\rangle_q$, so $\alpha=y/q-1/(qr)$.

Put $f(a)=\zeta(2s,a)$, $g(x)=\zeta(3s,1+x)$ and
$$T_q^\pm=\sum_{u\le q,\,(u,q)=1}f\Big(\frac{\langle\pm\bar u\rangle_q}q\Big)\,g\Big(\frac uq\Big).$$
Replacing $\alpha$ by $y/q$ in the case $q<r$, both cases become exact sums, and
$$U(s)=\zeta(2s)+\mathcal E(s)+\sum_{q\ge1}q^{-6s}\big(T_q^++T_q^-\big),\qquad(3)$$
$$\mathcal E(s)=\sum_qq^{-3s}\sum_u\sum_{m\ge1}r^{-3s}\Big[f\Big(\frac yq-\frac1{qr}\Big)-f\Big(\frac yq\Big)\Big],\quad r=mq+u.$$

**The correction $\mathcal E$.** Here $r\ge2$, so the segment between the two arguments lies above $y/(2q)$. As $\partial_af=-2s\,\zeta(2s+1,a)$, on a compact subset of $\operatorname{Re}s>0$ the bracket is $O((qr)^{-1}(q/y)^{2\sigma+1})$. Summing $r^{-3\sigma-1}$ over $m$ gives $O(q^{-3\sigma-1})$, and $\sum_yy^{-2\sigma-1}$ is bounded. The total for given $q$ is $O(q^{-4\sigma-1})$. Hence $\mathcal E$ is holomorphic on $\operatorname{Re}s>0$.

## 4.3 The main sums

Write $g=\zeta(3s)+k$ with $k(x)=\zeta(3s,1+x)-\zeta(3s)$; $k$ and $\partial_xk$ are bounded on $[0,1]$, locally uniformly in $\operatorname{Re}s>0$. By Möbius inversion,
$$\sum_{(j,q)=1,\,j\le q}\zeta\Big(2s,\frac jq\Big)=\zeta(2s)\,J_{2s}(q),\qquad J_w(q)=\sum_{d\mid q}\mu_{\rm M}(d)(q/d)^w,$$
and $\sum_qJ_{2s}(q)q^{-6s}=\zeta(4s)/\zeta(6s)$. Therefore (3) reads
$$U(s)=\zeta(2s)+\frac{2\,\zeta(2s)\,\zeta(3s)\,\zeta(4s)}{\zeta(6s)}+\mathcal E(s)+\sum_qq^{-6s}\big(R_q^++R_q^-\big),\qquad(4)$$
$$R_q^\pm=\sum_uf\Big(\frac{\langle\pm\bar u\rangle_q}q\Big)\,k\Big(\frac uq\Big).$$

## 4.4 The bound for $R_q$

We use the classical equidistribution of modular inverses, a consequence of the Weil--Estermann bound for Kloosterman sums (see Shparlinski's survey, equation (10) and Theorem 13): uniformly for $a,b\in[0,1]$,
$$\#\Big\{u:\ (u,q)=1,\ \frac uq\le a,\ \frac{\langle\pm\bar u\rangle_q}q\le b\Big\}=\varphi(q)\,ab+O\big(q^{1/2+o(1)}\big).\qquad(5)$$

**Proposition.** On compact subsets of $0<\operatorname{Re}s<1/2$, $R_q^\pm=O\big(q^{1/2+\sigma+o(1)}\big)$.

*Proof.* Write $y_u=\langle\pm\bar u\rangle_q/q$ and $x_u=u/q$, and let $\eta=q^{-1/2}$. We have $|f(a)|\ll a^{-2\sigma}$ and $|f'(a)|\ll a^{-2\sigma-1}$ on $(0,1]$.

*Small $y_u$.* The $y_u$ are distinct, so the terms with $y_u<\eta$ are at most $\sum_{j<\eta q}O((q/j)^{2\sigma})=O(q\,\eta^{1-2\sigma})$.

*Large $y_u$.* Expand $k(x)=k(1)-\int_0^1k'(a)\,1_{x\le a}\,da$ and, for $y\ge\eta$, $f(y)=f(1)-\int_\eta^1f'(b)\,1_{y\le b}\,db$. Each resulting count is a difference of counts as in (5). Hence
$$\sum_{y_u\ge\eta}k(x_u)f(y_u)=\varphi(q)\int_0^1k\int_\eta^1f+O\Big(q^{1/2+o(1)}\Big(1+\int_\eta^1|f'|\Big)\Big),$$
and the error is $O(q^{1/2+o(1)}\eta^{-2\sigma})$.

*The main term.* For $\operatorname{Re}w<1$,
$$\int_0^1\zeta(w,a)\,da=\int_0^1a^{-w}da+\int_1^2\zeta(w,x)\,dx=\frac1{1-w}+\frac{\zeta(w-1,2)-\zeta(w-1)}{1-w}=0.$$
So $\int_\eta^1f=-\int_0^\eta f=O(\eta^{1-2\sigma})$. With $\eta=q^{-1/2}$ all three contributions are $O(q^{1/2+\sigma+o(1)})$. $\square$

The vanishing of this integral is the *mean-zero* property noted in v009 §3.

## 4.5 Conclusion

On $3/10<\sigma\le2/5$ the proposition gives $q^{-6\sigma}|R_q|\ll q^{-5\sigma+1/2+o(1)}$, summable since $5\sigma-1/2>1$. For $\sigma>1/3$ the trivial bound $|(2s-1)R_q|\ll q^{\max(1,2\sigma)+o(1)}$ also suffices. So $(2s-1)\sum_qq^{-6s}R_q^\pm$ is holomorphic on $\operatorname{Re}s>3/10$. In (4), $\zeta(4s)/\zeta(6s)$ is holomorphic on $\operatorname{Re}s>3/10$. The only poles are therefore at $1/2$ (from $\zeta(2s)$ and the last sum, at most simple, and genuine because the terms of $U$ are positive and at least $M^{-2s}$) and at $1/3$ (from $\zeta(3s)$), with the stated residue. $\square$

**Check against the classical theory.** The residue corresponds to the secondary term $\frac{2C}{1-s}X^{1-s}$, $C=\zeta(1-s)\zeta(1+s)/\zeta(2)$, of $\sum_{M\le X}\sigma_{-s}(M)\sigma_{-s}(M+1)$ at $s=1/3$.

# 5. Computations

Finite and floating-point checks only. Parameters and outputs are in `results/`.

- Exact integer arithmetic to order $80$: the coefficients of $h\prod_{n\le11}(1-z^n)^{c_n}$ at $z^{12},\dots,z^{15}$ are $2,1,-2,-2$, as in the review; the formula T45e(i) holds for all $n\le80$; $|nc_n+p_n|/R^{n/2}\le2.82$ for $2\le n\le80$; $e_n=0$ for $n=1,4,11,16,33$ in this range.
- For $30$ zeros, $\min|\zeta(k\rho/6)|$ over $2\le k\le12$, $k\ne6$, is at least $0.103$.
- The two formulas for $M_0$ agree with direct search for all $2202$ coprime pairs $(q,r)\ne(1,1)$ with $q,r\le60$.
- At $s=0.8$, formula (3) summed to $q\le400$ gives $5.041370$; the direct series with a tail correction gives $5.041373$.
- At $s=1/3$ and nearby, $|R_q^\pm|/q^{1/2+s}$ stays below $1.17$ for the sampled $q\le30011$.
- $\sum_{M\le X}\sigma_{-1/3}(M)\sigma_{-1/3}(M+1)$: the secondary term divided by $X^{2/3}$ is $-16.056$ at $X=2\cdot10^7$; predicted $-16.074$.

# 6. Open

- ANS-T46b (conjecture): the pole order of $G_3$ at $1/3$. Still needed: continuation of $G_3$ itself past $1/3$; the configuration with all three links; the leading coefficient.
- ANS-T46, T46a: higher depth beyond $1/3$.
- Zeros of $G_2$.
- The sharp second term of $A_2(X)$.
- ANS-T33, T39; ANS-T38 for the complete functions. Not addressed.
