---
title: "ANS-I v011 --- An exact decomposition of the depth-three function"
author: "UNNS Research Collective"
date: "27 November 2026"
---

Research notes. They continue ANS-I v010; notation is as there. All results concern the nesting grammar. New proofs are pending review; no claim of priority is made, and no comprehensive literature review has been done.

# 0. Review of v010

The owner's review found T45c, T45d, T45e, T38b, T38c, T38d and T46c valid. It proposed two consequences and a second residue, treated in §1. It also qualified v010 §4.1: T46c supports the proposed mechanism of dependence between links; it does not directly confirm the formula $\lfloor k^2/4\rfloor$. That reading is adopted.

# 1. Consequences proposed in the review

## 1.1 Limit law of the exponents (ANS-T45f)

**Theorem.** Put $Y_n=ne_n/(2R^n)$. For $-1\le a<b\le1$,
$$\lim_{N\to\infty}\frac1N\#\{n\le N:\ a\le Y_n\le b\}=\frac{\arcsin b-\arcsin a}\pi.$$
In particular the set where $|e_n|>R^n/n$ has density $\tfrac23$, split equally between the two signs.

*Proof.* By T45e(ii), $Y_n=-\cos n\theta+o(1)$, and $n\theta$ is equidistributed modulo $2\pi$. The distribution of $-\cos$ of a uniform angle is the arcsine law, which has no atoms. For the last statement take $|Y_n|>\tfrac12$. $\square$

## 1.2 Populations of the vertical lines (ANS-T38e)

Let $N_0^*(T)$ count the distinct zeros $\tfrac12+i\gamma$ of $\zeta$ with $0<\gamma\le T$, and $P_n(T)$ the distinct poles of $G_2$ on $\operatorname{Re}s=1/(2n)$ with $0<\operatorname{Im}s\le T$.

**Theorem.** For each fixed $n\ge1$,
$$P_n(T)=\begin{cases}N_0^*(nT)+O_n(T),&e_n<0,\\O_n(T),&e_n\ge0.\end{cases}$$
Hence $P_n(T)\asymp_nT\log T$ when $e_n<0$.

*Proof.* By T45d(ii) a pole $s_0$ on this line has $\nu(s_0)<0$, so $\mu(ks_0)\ne0$ for some $k<2n$ with $e_k<0$. For $k\ne n$ the real part of $ks_0$ differs from $\tfrac12$ by at least $1/(2n)$; by Bohr--Landau and the reflection used in v010 §2, such points number $O_n(T)$. If $e_n\ge0$ nothing else remains. If $e_n<0$, every $s_0=\rho/n$ with $\rho$ on the critical line satisfies $\delta(s_0)=0$ and, apart from $O_n(T)$ coincidences, $\nu(s_0)=e_n\mu(\rho)<0$. The last statement uses Selberg's theorem. $\square$

The estimates are for fixed $n$; nothing uniform in $n$ is claimed.

## 1.3 The residue of the model at $1/2$ (ANS-T46f)

**Theorem.** $\operatorname{Res}_{s=1/2}U=\zeta(3/2)^2/(2\zeta(3))$.

*Proof (owner's method; convergence supplied).* We show that $\sum_{(q,r)=1}(qr)^{-3s}(2s-1)\zeta(2s,\alpha(q,r))$ converges normally on compact subsets of $\operatorname{Re}s>1/3$. There $|(2s-1)\zeta(2s,a)|\ll a^{-2\sigma}+1$ on $(0,1]$. If $q>r$, then $\alpha=j/r$ with distinct $j$ as $q$ runs through the classes modulo $r$, and $\sum_{q>r,\,q\equiv v}q^{-3\sigma}\ll r^{-3\sigma}$; so the terms with given $r$ total $O(r^{\max(1,2\sigma)-6\sigma}\log r)$. If $q<r$, then $\alpha\ge y/(2q)$ with $y=\langle\bar r\rangle_q$, and the same bound holds with $q$ in place of $r$. The exponent is below $-1$. At $s=\tfrac12$ each $(2s-1)\zeta(2s,\alpha)$ equals $1$, so $\lim(2s-1)U(s)=\sum_{(q,r)=1}(qr)^{-3/2}=\zeta(3/2)^2/\zeta(3)$. $\square$

# 2. An exact decomposition of $G_3$ (ANS-T46d)

## 2.1 Letters and weights

Write a word of length three as $(a-1,\,M,\,N)$ and put $b=M+1$, $c=N+1$, with $a,b,c\ge2$. Then
$$E=\frac{(abc)^2}{g_1g_2},\qquad g_1=\gcd(N,b^2),\qquad g_2=\gcd\Big(\frac{MN}{g_1},\,a^2\Big).\qquad(1)$$
*Proof of (1).* The grammar gives $E_1=a^2$, $E_2=a^2b^2/h$ with $h=\gcd(M,a^2)$, and $E_3=c^2E_2/\gcd(N,E_2)$. So $E=(abc)^2/G$ with $G=h\,\gcd(N,a^2b^2/h)=\gcd(Nh,a^2b^2)$. Let $\alpha,\beta,m,n$ be the exponents of $p$ in $a^2,b^2,M,N$; since $(M,b)=1$, $\min(m,\beta)=0$. If $\beta=0$, the exponent of $G$ is $\min(n+\min(m,\alpha),\alpha)=\min(m+n,\alpha)$, that of $g_2$, and $g_1$ has exponent $0$. If $m=0$, it is $\min(n,\alpha+\beta)=\min(n,\beta)+\min\big(n-\min(n,\beta),\alpha\big)$. $\square$

Let $z=p^{-s}$. Define $\Phi(K)=\sum_{d\mid K}J_s(d)\,\rho(d)^{-2s}$, a multiplicative function with
$$\Phi(p^v)=1+(1-z)\Big(\Big\lfloor\frac v2\Big\rfloor+\Big\lceil\frac v2\Big\rceil z\Big).$$
Define $w_1,w_2$ multiplicative, with $w_i(1)=1$ and for exponents $\ge1$
$$w_1(p^\mu)=\frac{\Phi(p^\mu)+c_\mu}{L_0},\qquad w_2(p^\beta)=\frac{1+z-z^{2\beta+1}/(1+z^2)}{L_0},\qquad L_0=\frac{1+z^2+z^3}{1+z^2},\qquad(2)$$
where $c_\mu=z^3/(1+z^2)$ for even $\mu$ and $c_\mu=z^2(1-z+z^2)/(1+z^2)$ for odd $\mu$. On primes the two weights agree:
$$w_1(p)=w_2(p)=\frac{1+z+z^2}{1+z^2+z^3}.$$
Put
$$V(s)=\sum_{M\ge1}(M+1)^{-2s}\,w_1(M)\,w_2(M+1).$$

## 2.2 The theorem

For fixed $M$ let $f(N)=g_1^{\,s}\,\Phi(MN/g_1)$, let $\Lambda_M=\mu_{\rm M}*f$ be its Möbius transform, and let
$$R(s)=\sum_{M\ge1}(M+1)^{-2s}\sum_{k\ge1}\Lambda_M(k)\,k^{-2s}\,\Delta(s,k),\qquad\Delta(s,k)=\zeta\big(2s,1+\tfrac1k\big)-\zeta(2s).$$

**Theorem.** For $\operatorname{Re}s>1/2$,
$$\boxed{\,G_3(s)=\zeta(2s)^2\,\zeta(3s)\,H(s)\,V(s)+\zeta(2s)\,R(s)-G_2(s)\,}$$
where $\zeta(3s)H(s)=\prod_pL_0$ is the Euler product of depth two.

*Proof.* All series below converge absolutely for $\operatorname{Re}s>1/2$.

*First letter.* Since $\gcd(K,a^2)^s=\sum_{d\mid K,\;d\mid a^2}J_s(d)$ and $d\mid a^2$ means $\rho(d)\mid a$,
$$\sum_{a\ge2}a^{-2s}\gcd(K,a^2)^s=\zeta(2s)\,\Phi(K)-1.$$
With (1) and $G_2(s)=\sum_{b,c\ge2}(bc)^{-2s}g_1^{\,s}$ this gives
$$G_3(s)=\zeta(2s)\sum_{M,N\ge1}\big((M+1)(N+1)\big)^{-2s}f(N)-G_2(s).$$

*Last letter.* Writing $f(N)=\sum_{k\mid N}\Lambda_M(k)$,
$$\sum_{N\ge1}(N+1)^{-2s}f(N)=\sum_k\Lambda_M(k)\,k^{-2s}\,\zeta\big(2s,1+\tfrac1k\big)=\zeta(2s)\sum_k\frac{\Lambda_M(k)}{k^{2s}}+\sum_k\frac{\Lambda_M(k)\,\Delta(s,k)}{k^{2s}}.$$
Here $\Delta=O(1/k)$ and $|\Lambda_M(k)|\ll(Mk)^{\varepsilon}\gcd(k,b^2)^{\sigma}$, which justifies the convergence.

*The Euler product.* Because $(M,b)=1$, $f(N)=\prod_pf_p(v_p(N))$ with
$$f_p(j)=p^{s\min(j,2\beta)}\,\Phi\big(p^{\mu+j-\min(j,2\beta)}\big),\qquad\mu=v_p(M),\ \beta=v_p(b),$$
at most one of $\mu,\beta$ being non-zero. Hence $\Lambda_M$ factorises over primes and $\sum_k\Lambda_M(k)k^{-2s}=\prod_p\sum_j\big(f_p(j)-f_p(j-1)\big)z^{2j}$, with $f_p(-1)=0$.

- If $\beta\ge1$: the terms $1\le j\le2\beta$ add to $\sum(1-z)z^j=z-z^{2\beta+1}$. For $j=2\beta+i$ the difference is $z^{-2\beta}\big(\Phi(p^i)-\Phi(p^{i-1})\big)$, where $\Phi(p^i)-\Phi(p^{i-1})$ is $(1-z)z$ for odd $i$ and $1-z$ for even $i$; these add to $z^{2\beta}\cdot z^3/(1+z^2)$. The total is $1+z-z^{2\beta+1}/(1+z^2)$.
- If $\beta=0$: the factor is $\Phi(p^\mu)+\sum_{j\ge1}\big(\Phi(p^{\mu+j})-\Phi(p^{\mu+j-1})\big)z^{2j}=\Phi(p^\mu)+c_\mu$, by summing the two parities. For $\mu=0$ this is $1+z^3/(1+z^2)=L_0$.

So the product equals $\prod_pL_0\cdot w_1(M)\,w_2(b)$. Finally $L_0=(1-z^3)^{-1}\big(1-(z^5+z^6)/(1+z^2)\big)$, so $\prod_pL_0=\zeta(3s)H(s)$. $\square$

## 2.3 What the decomposition shows

- At primes dividing neither $M$ nor $b$ only the link between the first and last letters acts. Its Euler product factors out exactly: it is the depth-two factor $\zeta(3s)H(s)$, with its zeta quotients and zeros. The effect of that link at the other primes is absorbed into $w_1,w_2$.
- The two links through the middle letter remain coupled in $V$, a shifted series of the form studied in T46c. To first order $w_i(p)=1+z+O(z^3)$, the weights of $U$.
- The gcd corrections are the exact factors (2) and the term $R$.
- On the first side the weight does not return to that of $U$ on prime powers: $w_1(p^2)\to2$ as $p\to\infty$. On the second side $w_2(p^\beta)\to1$.

# 3. The pole at $1/3$ (ANS-T46e, T46b)

## 3.1 The conjectured residue

Take $s=\tfrac13$, write $\kappa_i=\mu_{\rm M}*w_i$, and define for each prime, with $x=p^{-2/3}$ and $y=p^{-1}$,
$$W_i(t)=\sum_{j\ge0}w_i(p^j)\,t^j,\qquad E_{1,p}=(1-y)(1-x)W_1(x)+(1-z^2)\big((1-y)W_2(y)-1\big),$$
$E_{2,p}$ with the indices exchanged, and $E_i=\prod_pE_{i,p}$.

**Positivity (proved).** $E_1,E_2$ converge to positive numbers. From (2), $w_1(p^\mu)\ge1$, since $\Phi(p^\mu)\ge1$ and $c_\mu-(L_0-1)$ is $0$ or $z^2(1-z)^2/(1+z^2)$; and $w_2(p^\beta)\ge1$, since the numerator minus $L_0$ is $(z-z^{2\beta+1})/(1+z^2)$. So $(1-y)W_i(y)\ge1$ and each $E_{i,p}>0$. Expanding the closed forms in $z=p^{-1/3}$ gives $E_{i,p}=1+O(z^4)$.

**Conjecture (ANS-T46e).** $V$ and $R$ continue meromorphically to a neighbourhood of $s=\tfrac13$; $R$ has at most a simple pole there, and $V$ has a simple pole with residue
$$r_V=\frac{\zeta(2/3)\,(E_1+E_2)}3<0.$$

The formula comes from carrying the main terms of T46c over to general weights: a large divisor on one side is averaged over residue classes, which gives $E_1$ and $E_2$. For the weights of $U$ the same recipe gives $E_{i,p}=(1-p^{-2})/(1-p^{-4/3})$ and reproduces T46c exactly. For $w_1,w_2$ it is not proved.

## 3.2 What would follow

**Proposition (proved implication).** If ANS-T46e holds, $G_3$ has a pole of order exactly two at $1/3$ and
$$\lim_{s\to1/3}\big(s-\tfrac13\big)^2G_3(s)=\frac{\zeta(2/3)^2\,H(1/3)\,r_V}3\ne0.$$
So T46b holds for $k=3$.

*Proof.* In T46d, $\zeta(3s)$ has residue $\tfrac13$, $H(1/3)>0$ and $\zeta(2/3)\ne0$. The other two terms have at most simple poles. $\square$

The corresponding term of $A_3(X)$ would be $X^{1/3}(a\log X+b)$ with $a=\zeta(2/3)^2H(1/3)\,r_V\approx-2.277$.

## 3.3 The missing step

T46c uses weights whose divisor sums are $\sum_{q\mid M}q^{-s}$, so that one variable runs smoothly through residue classes. For $w_1,w_2$ one must in addition control conditions such as $d^2\mid M$ with a coefficient that does not decay, uniformly in $d$. Applying the Kloosterman estimate separately for each $d$ loses a power of $d$ larger than the available decay, and I have not obtained the required uniformity. Because the non-decaying coefficient occurs on one side only, the problem resembles correlations of squarefree-type conditions with divisor sums; that it can be solved this way is an expectation, not a result.

# 4. Computations

Finite and floating-point checks only. Parameters and outputs are in `results/`.

- Exponents: exact integers to $n=3000$. The shares with $|e_n|>R^n/n$ are $0.690$, $0.664$, $0.665$ at $N=300,1000,3000$ (limit $2/3$). The values quoted in the review for $n=24,\dots,80$ agree.
- Formula (1): exact integer agreement with the grammar for all $216\,000$ words with letters $\le60$. $G_3(2)$ summed over words with letters $\le T$ differs from the first form in the proof, $\zeta(2s)\sum f-G_2$ (truncated alike), by $-1.3\cdot10^{-7}$, $-1.7\cdot10^{-8}$, $-2.2\cdot10^{-9}$ at $T=40,80,160$.
- For the weights of $U$ the formula for $E_{i,p}$ gives the factor stated in §3.1 (four primes, floating point).
- The closed forms of $\Phi(p^v)$ and of both local factors agree with truncated series to $10^{-15}$ at four test points.
- T46d at $s=1.5$: the first-letter identity holds within its tail bound for seven values of $K$; the last-letter identity holds to within $1.2\cdot10^{-7}$ (truncation) for eleven values of $M\le48$.
- Test of T46e through the sum $S(X)=\sum_{M\le X}w_1(M)\,w_2(M+1)$ at $s=\tfrac13$. The same recipe predicts $S(X)\approx DX+\tfrac32\zeta(2/3)(E_1+E_2)X^{2/3}$, where $D=\prod_p\big((1-y)(W_1(y)+W_2(y))-1\big)\approx2.969257$. Predicted coefficient of $X^{2/3}$: $-4.0697$.

| $X$ | $10^4$ | $10^5$ | $10^6$ | $10^7$ | $2\cdot10^7$ |
|--|--|--|--|--|--|
| $(S-DX)/X^{2/3}$ | $-3.9228$ | $-3.9863$ | $-4.0185$ | $-4.0395$ | $-4.0436$ |

- Depth-three counts of v008 (to $X=10^{12}$): fixing $a=-2.277$ or fitting it freely gives nearly equal residuals on two of three ranges, and the fitted value moves between $-2.3$ and $-5.4$. **The counts do not test the prediction.**

# 5. Open

- ANS-T46e: continuation of $V$ and $R$ past $1/3$ and the residue. This now carries T46b at $k=3$.
- ANS-T46, T46a: depth four and higher.
- Zeros of $G_2$; the sharp second term of $A_2(X)$.
- ANS-T33, T39; ANS-T38 for the complete functions. Not addressed.
