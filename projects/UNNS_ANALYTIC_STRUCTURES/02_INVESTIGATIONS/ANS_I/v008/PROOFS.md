---
title: "ANS-I v008 --- Continuation of the depth-k functions"
author: "UNNS Research Collective"
date: "27 November 2026"
---

Research notes. They continue ANS-I v007; notation is as in v005--v007. All results concern the nesting grammar. New proofs are pending review; no claim of priority is made, and no literature review has been done.

# 0. Review of v007

The owner's review found T37, T37b, T40, T41 and T42 valid, and T24a valid on renewed review. Two clarifications have been made in the v007 proofs. In §4, regular variation excludes a persistent non-constant modulation of fixed period in $\log X$, but allows slower oscillation inside the slowly varying factor. In §7, T42 concerns empirical letter and block frequencies, not independence at prescribed positions (a non-empty history from source $1$ must begin with the letter $1$).

# 1. Continuation of $G_k$ (ANS-T34)

For $D\ge1$ let
$$G_k(s;D)=\sum_{|w|=k,\ D\mid K(w)}E(w)^{-s},$$
so that $G_k(s;1)=G_k(s)$ and $G_0(s;D)=[D=1]$. The sum converges absolutely for $\operatorname{Re}s>1/2$ (T12). Put $\sigma=\operatorname{Re}s$, $\mu=\min(2\sigma,1)$, $H_k(s;D)=(2s-1)^kG_k(s;D)$, $J_s(d)=\sum_{e\mid d}\mu_{\rm M}(e)(d/e)^s$ (here $\mu_{\rm M}$ is the Möbius function) and $\rho(d)=\prod_pp^{\lceil v_p(d)/2\rceil}$, so that $d\mid a^2$ exactly when $\rho(d)\mid a$.

**Theorem.** For every $k\ge0$ and $D\ge1$, $H_k(\cdot\,;D)$ is holomorphic on $1/3<\sigma<3/4$. On every closed substrip $\frac13+\delta\le\sigma\le\frac34-\delta$ and for every $\varepsilon>0$,
$$|H_k(s;D)|\le M\,(1+|\operatorname{Im}s|)^{2k}\,D^{-\mu+\varepsilon},$$
with $M=M(k,\delta,\varepsilon)$.

## 1.1 The first-letter identity

Write $w=Nw'$ and $a=N+1$, and let $K',E'$ belong to $w'$. From the definition of the source,
$$K(w)=N\,\frac{K'}{g},\qquad E(w)=\frac{a^2E'}{g},\qquad g=\gcd(K',a^2).\qquad(1)$$
(A source $x$ must satisfy $N\mid x$ and $K'\mid a^2x/N$.)

Let $n=\gcd(D,N)$ and $h=D/n$. Since $\gcd(h,N/n)=1$, the condition $D\mid NK'/g$ means $h\mid K'/g$, that is, $v_p(K')\ge v_p(h)+2v_p(a)$ for every $p\mid h$. Let $t$ be the part of $a$ composed of primes of $h$. Then $g=t^2\gcd(K',(a/t)^2)$ and
$$\gcd(K',(a/t)^2)^s=\sum_{d\mid (a/t)^2,\ d\mid K'}J_s(d),\qquad(d,h)=1.$$
The two conditions on $K'$ combine to $ht^2d\mid K'$. Hence, for $\sigma>1/2$, where all rearrangements converge absolutely,
$$G_k(s;D)=\sum_{nh=D}\ \sum_{t\mid h^\infty}t^{2s}\sum_{(d,h)=1}J_s(d)\,G_{k-1}(s;ht^2d)\,Z(s),\qquad(2)$$
where
$$Z=\sum a^{-2s}\quad\text{over }a\ge2\text{ with }\rho(d)\mid a,\ \ a_h=t,\ \ \gcd(a-1,D)=n,$$
and $a_h$ is the part of $a$ composed of primes of $h$. By Möbius inversion,
$$Z=\sum_{f,e\mid{\rm rad}\,h}\mu_{\rm M}(f)\mu_{\rm M}(e)\sum_{\substack{a\ge2,\ ft\rho(d)\mid a\\ ne\mid a-1}}a^{-2s}.\qquad(3)$$

## 1.2 One progression

An inner sum in (3) is empty unless $(ft\rho(d),ne)=1$. It then runs over $a=r,r+q,r+2q,\dots$ with $q=ft\rho(d)\,ne$ and $2\le r\le q+1$. Comparing the sum with the integral,
$$\sum_{m\ge0}(r+mq)^{-2s}=\frac{r^{1-2s}}{q(2s-1)}+R_1,\qquad|R_1|\le r^{-2\sigma}\Big(1+\frac{|s|}{\sigma}\Big),$$
and $\dfrac{r^{1-2s}-1}{(2s-1)q}=-\dfrac1q\displaystyle\int_1^rx^{-2s}dx$ has modulus at most $q^{-1}r^{\max(1-2\sigma,0)}\log r$. Since $r\le 2q$, together
$$\sum_{m\ge0}(r+mq)^{-2s}=\frac1{q(2s-1)}+R,\qquad|R|\le C(1+|s|)\,r^{-\mu}\log(2r).\qquad(4)$$
The remainder $R$ is holomorphic on $\sigma>0$, through $s=1/2$: $R_1=\sum_{m\ge0}\big[(r+mq)^{-2s}-\int_m^{m+1}(r+uq)^{-2s}du\big]$ is a normally convergent series of holomorphic functions there.

Let $r_0=r_0(t,\rho)$ be the least $a\ge2$ with $t\rho\mid a$ and $n\mid a-1$. The progression in (3) is contained in this larger set, so $r\ge r_0$ **whatever $f$ and $e$ are**.

## 1.3 Induction

The case $k=0$ is trivial. Assume the theorem for $k-1$. Multiplying (2) by $(2s-1)^k$ gives
$$H_k(s;D)=\sum_{n,h,t,d}t^{2s}J_s(d)\,H_{k-1}(s;ht^2d)\,\big[(2s-1)Z\big],\qquad(5)$$
and by (4) $(2s-1)Z=\sum_{f,e}\mu_{\rm M}(f)\mu_{\rm M}(e)\,[q^{-1}+(2s-1)R]$, each term entire or holomorphic on the strip. It suffices to bound (5) by absolute values. Put $\nu=\mu-\sigma=\min(\sigma,1-\sigma)>0$. Since $|J_s(d)|\le2^{\omega(d)}d^\sigma$, the induction hypothesis gives, apart from the factor in $\operatorname{Im}s$ and arbitrarily small powers,
$$\big|t^{2s}J_s(d)H_{k-1}(s;ht^2d)\big|\ll h^{-\mu}\,t^{-2\nu}\,d^{-\nu}.$$
The pairs $f,e$ contribute at most $4^{\omega(h)}\ll h^{\varepsilon}$. For a given $\rho$ there are at most $2^{\omega(\rho)}$ integers $d$ with $\rho(d)=\rho$, all with $d\ge\rho$.

*The terms $q^{-1}$.* Here $q\ge tn\rho$, and $\sum_t t^{-2\nu-1}\sum_\rho\rho^{-\nu-1+\varepsilon}$ converges. The result is $\ll n^{-1}\le n^{-\mu}$.

*The remainders.* We need
$$T(t)=\sum_{\rho}\rho^{-\nu+\varepsilon}\,r_0(t,\rho)^{-\mu+\varepsilon}\ll n^{-\mu+C\varepsilon}\qquad(6)$$
uniformly in $t$. Group the $\rho$ by the value $a=r_0=1+nj$, $j\ge1$. Then $t\rho\mid a$. Moreover $r_0\le tn\rho+1$, so $\rho\ge j/t$. For each $a$ there are at most $\tau(a)\ll a^\varepsilon$ values of $\rho$, and $a$ occurs only if $t\mid 1+nj$, which restricts $j$ to one residue class $j_0$ modulo $t$ with $1\le j_0\le t$. Hence
$$T(t)\ll n^{-\mu+C\varepsilon}\sum_{j\equiv j_0\ (t)}j^{-\mu+C\varepsilon}\min\Big(1,\frac tj\Big)^{\nu}.$$
The term $j=j_0$ is at most $1$. The others are $j=j_0+it$ with $i\ge1$, so $j\ge it$, and their sum is at most $t^{-\mu+C\varepsilon}\sum_ii^{-\mu-\nu+C\varepsilon}$. This converges because $\mu+\nu>1$ on the substrip: for $\sigma\le1/2$ this says $3\sigma>1$, and for $\sigma>1/2$ it says $2-\sigma>1$. This proves (6).

Finally $\sum_{t\mid h^\infty}t^{-2\nu+\varepsilon}=\prod_{p\mid h}(1-p^{-2\nu+\varepsilon})^{-1}\ll h^{\varepsilon}$. So the terms with given $n,h$ are $\ll(nh)^{-\mu+C\varepsilon}=D^{-\mu+C\varepsilon}$, and there are $\tau(D)$ choices. Each factor $(2s-1)R$ adds at most $(1+|\operatorname{Im}s|)^2$. The series (5) therefore converges locally uniformly on the whole strip and satisfies the bound. It equals $(2s-1)^kG_k(s;D)$ for $\sigma>1/2$, so it is the continuation. $\square$

## 1.4 Consequences

**Corollary 1.** For every $k\ge1$ the function $G_k$ is meromorphic on $\operatorname{Re}s>1/3$. Its only singularity is a pole at $s=1/2$ of order exactly $k$, with $(2s-1)^kG_k(s)\to\kappa_k$. In particular every other point of the line $\operatorname{Re}s=1/2$ is regular.

(The order is exact because $\kappa_k\ge1$ and the real limit is given by T32.)

At $k=1,2$ this was known (T05, v001); the identity (2) with $D=1$ and $k=2$ is the v001 formula.

**Corollary 2 (ANS-T34a).** For every $k\ge1$ there is a polynomial $P_{k-1}$ of degree $k-1$, with leading coefficient $\kappa_k/(2^{k-1}(k-1)!)$, such that
$$A_k(X)=\sqrt X\,P_{k-1}(\log X)+O_{k,\varepsilon}\Big(X^{\frac12-\frac1{6(k+2)}+\varepsilon}\Big).$$

*Proof.* Let $m=k+1$ and $\sigma_0=\frac13+\delta$. By the theorem $|G_k(s)|\ll(1+|\operatorname{Im}s|)^{k}$ on $\sigma_0\le\sigma\le 0.6$ away from $1/2$. So in
$$\sum_{E\le X}\Big(1-\frac EX\Big)^m=\frac1{2\pi i}\int_{(0.6)}G_k(s)\,X^s\,\frac{m!\,ds}{s(s+1)\cdots(s+m)}$$
the line may be moved to $\sigma_0$: the result is the residue at $1/2$ plus $O(X^{\sigma_0})$. Thus $F(X)=\sum_{E\le X}(X-E)^m/m!$ equals $X^m/m!$ times that. The $m$-th forward difference with step $h$ satisfies $h^mA_k(X)\le\Delta_h^mF(X)\le h^mA_k(X+mh)$, since it is the integral of $A_k(X+t_1+\dots+t_m)$ over $[0,h]^m$. The $m$-th derivative of the main term of $F$ is $\sqrt X\,P_{k-1}(\log X)$. Therefore
$$A_k(X)=\sqrt X\,P_{k-1}(\log X)+O\Big(hX^{-1/2}\log^{k-1}X+X^{m+\sigma_0}h^{-m}\Big),$$
using $\Delta_h^mF(X-mh)$ for the other side. Take $h=X^{1-\eta}$ with $\eta=(\frac12-\sigma_0)/(m+1)$. $\square$

This improves the leading-term asymptotic of T32 to the full polynomial with a power saving. The exponent is not optimised.

# 2. Depth two beyond $1/3$ (ANS-T45)

**Theorem.** On $\sigma>0$ let
$$F_2(s)=\sum_{d\ge1}\frac{J_s(d)}{(d\,\rho(d))^{2s}}\Big(\zeta\big(2s,1+\tfrac1d\big)-\zeta(2s)\Big),\qquad H(s)=\prod_p\Big(1-\frac{p^{-5s}+p^{-6s}}{1+p^{-2s}}\Big)\quad(\sigma>\tfrac15).$$
Then
$$G_2(s)=\zeta(2s)\Big(\zeta(2s)\,\zeta(3s)\,H(s)+F_2(s)-1\Big)+1.$$
So $G_2$ is meromorphic on $\operatorname{Re}s>1/5$, with poles only at $s=1/2$ (order two) and $s=1/3$ (simple, residue $\zeta(2/3)^2H(1/3)/3\ne0$).

*Proof.* By v001, or (2) with $D=1$, $G_2(s)=\zeta(2s)\sum_dJ_s(d)\rho(d)^{-2s}G_1(s;d)-G_1(s)$ with $G_1(s;d)=d^{-2s}\zeta(2s,1+1/d)$. Add and subtract $\zeta(2s)$. With $x=p^{-s}$ the Euler factor of $\sum_dJ_s(d)(d\rho(d))^{-2s}$ is
$$1+(1-x)\,\frac{x^3+x^4}{1-x^4}=1+\frac{x^3}{1+x^2},\qquad(1-x^3)\Big(1+\frac{x^3}{1+x^2}\Big)=1-\frac{x^5+x^6}{1+x^2},$$
so the sum is $\zeta(3s)H(s)$. The difference of zeta functions equals $\sum_{m\ge1}[(m+1/d)^{-2s}-m^{-2s}]$, of modulus at most $|2s|\,\zeta(1+2\sigma)/d$. The terms of $F_2$ are therefore $O(2^{\omega(d)}d^{-1-\sigma}\rho(d)^{-2\sigma})$ times $|2s|$, so $F_2$ is holomorphic for $\sigma>0$ and of at most linear growth on closed strips. At $s=1/3$ every factor of $H$ is positive and the product converges absolutely. $\square$

**Corollaries.**

- $\kappa_2=\zeta(3/2)H(1/2)=\prod_p\big(1+p^{-3/2}/(1+p^{-1})\big)$.
- In Corollary 2 at $k=2$ one has $P_1(L)=c_1L+c_0$ with $c_1=\kappa_2/2$ and $c_0=\tfrac12\Phi'(\tfrac12)+(2\gamma-1)\kappa_2+F_2(\tfrac12)-1$, where $\Phi(s)=\zeta(3s)H(s)$ and $\gamma$ is Euler's constant.
- A second term holds for smoothed counts: for $m$ large, the Riesz mean $\sum_{E\le X}(1-E/X)^m$ equals its residue term at $1/2$, plus $\dfrac{\zeta(2/3)^2H(1/3)}3\cdot\dfrac{m!}{\prod_{j=0}^m(1/3+j)}\,X^{1/3}$, plus $O(X^{1/5+\varepsilon})$.
- For the sharp count the corresponding second term would be $\zeta(2/3)^2H(1/3)X^{1/3}$. **It is not proved**: the available growth bounds lose more than this in removing the smoothing.

So the estimate in §1 cannot be extended as a holomorphy statement past $1/3$ at depth two. The nature of $G_k$ at $1/3$ for $k\ge3$ is open.

# 3. Limit laws

## 3.1 Endpoints (ANS-T43)

**Theorem.** Choose a history uniformly in the population counted by $A(X)$, $N_x(X)$ or $C(X)$, and let $y$ be its endpoint ($E(w)$, $xQ(w)$, or $n$). Then $y/X$ converges in distribution to the law with density $\sigma_cu^{\sigma_c-1}$ on $(0,1)$. Equivalently $\log(X/y)$ tends to an exponential variable of rate $\sigma_c$.

*Proof.* $\Pr(y\le uX)=H(uX)/H(X)\to u^{\sigma_c}$ by T40, and by T40 with T41 for $C$. $\square$

## 3.2 Joint law (ANS-T44)

**Theorem.** For a finite quotient $\Gamma$ and the sector $\varphi(Q(w))$: in the populations $A$ and $N_x$ the pair (sector, $y/X$) tends to independent variables, uniform on $\Gamma$ and of density $\sigma_cu^{\sigma_c-1}$. In the population $C$, writing the history uniquely as $(m,w)$ with source $mK(w)$ and endpoint $mE(w)$,
$$\Pr\Big(m=j,\ \varphi(Q)=\gamma,\ \frac yX\le u\Big)\to\frac{j^{-\sigma_c}}{\zeta(\sigma_c)}\cdot\frac1{|\Gamma|}\cdot u^{\sigma_c}.$$

*Proof.* The probability is $A_\gamma(uX/j)/C(X)$ for $u\le1$. Use T37, T40 and T41. The limits over $j$ and $\gamma$ add to $u^{\sigma_c}$, so no mass escapes. $\square$

The limit of $m$ has the zeta distribution of parameter $\sigma_c$, whose mean is infinite.

## 3.3 Concentration (ANS-T42a)

**Theorem.** Let $H=A$ or $N_x$, $L=\log X$, $\beta=1/\sigma_c$. For every finite block $v$ there are $D,c>0$ such that, outside a proportion $e^{-cL^\beta}$ of the counted words,
$$L-\log Q(w)\le DL^\beta,\qquad\Big|\,|w|-\frac L{\lambda_c}\Big|\le DL^{(1+\beta)/2},\qquad|f_v(w)-\nu_c(v)|\le DL^{-(1-\beta)/2}.$$
Consequently $\log K(w)\le DL^\beta$ outside the same proportion for $H=A$.

*Proof.* By T24a, $H(X)\ge X^{\sigma_c}e^{-C_0L^\beta}$. Counted words have depth at most $L/\log4$, and the number with $Q\le Xe^{-u}$ is at most $\sum_{k\le L/\log4}\sum_{|w|=k}(Xe^{-u}/Q)^{\sigma_c}\le(1+L/\log4)X^{\sigma_c}e^{-\sigma_cu}$. Take $u=DL^\beta$. For the depth, the number of counted words with $|\log Q-\lambda_c|w||>a$ is at most $X^{\sigma_c}\sum_{k\le L/\log4}\Pr_\nu(|S_k-\lambda_ck|>a)$, where $S_k=\sum\log r_{N_i}$. Bernstein's inequality gives $2\exp(-c_1\min(a^2/k,a))$; take $a=D_1L^{(1+\beta)/2}$ and combine with the first bound. For blocks use Hoeffding's inequality on $|v|$ interleaved families, with deviation $D_2L^{(1+\beta)/2}$ in the number of occurrences. On the event already established for the depth, $|w|$ is comparable to $L$; dividing by the number of positions gives the bound for $f_v$, and the end effects of a block of fixed length are $O(1/L)$. $\square$

Here $(1-\beta)/2=0.17666\ldots$. These are upper bounds, not a fluctuation law. By T43, $L-\log Q=\log K+O_{\sf P}(1)$ in the population $A$, so the size of the multiplier deficit is the size of the source; a matching lower bound is open (with T28).

# 4. Computations

Finite and floating-point checks only; none is a proof. Parameters and outputs are in `results/`.

- Identity (2)--(3), evaluated on finite sets of letters at $s=0.9+0.4i$ for depths $2,3,4$ and ten values of $D$: largest relative error $1.4\cdot10^{-14}$.
- Depth counts by an exact program, agreeing with an independent enumeration at five small cases.
- Depth two: $\kappa_2=1.8536462$, $c_1=0.9268231$, $c_0=-4.545106$, predicted coefficient of $X^{1/3}$: $2.51830$.

| $X$ | $A_2(X)$ | $(A_2-\text{main})/X^{1/3}$ | remainder after second term, $/X^{1/4}$ |
|--|--:|--:|--:|
| $10^6$ | 8529 | 2.696 | 0.561 |
| $10^8$ | 126468 | 2.568 | 0.230 |
| $10^{10}$ | 1685029 | 2.530 | 0.079 |
| $10^{12}$ | 21089365 | 2.540 | 0.219 |
| $10^{14}$ | 253438509 | 2.523 | 0.066 |

- Depth three, up to $X=10^{12}$: with the leading coefficient fixed and two lower coefficients fitted, the residual divided by $X^{1/3}$ stays below $25$ in size and changes sign. A four-parameter fit adding $X^{1/3}(a\log X+b)$ leaves a residual below $2.2\,X^{1/4}$. These are fits; the lower coefficients were not computed from theory, so this tests little beyond consistency.
- Limit laws against the v007 census at $X=2\cdot10^8$: $\Pr(E\le X/2)=0.407$ (limit $0.342$); in $C$, $\Pr(m=1)=0.214$ (limit $0.409$) and $\Pr(m=2)=0.087$ (limit $0.140$). Convergence is slow, as for the underlying ratios.

# 5. Open

- ANS-T33: the singularity at $\sigma_c$. Not addressed.
- Continuation of $G_k$, $k\ge3$, to and past $1/3$; the expected pole there and its order (ANS-T46).
- The error exponent in T34a, and the sharp second term at depth two.
- ANS-T38, T39: not addressed.
- Uniformity in $k$: the constants of §1 grow with $k$ and are not tracked, so nothing here concerns $\sum_kG_k$.
