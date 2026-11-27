---
title: "ANS-I v012 --- Continuation of the depth-three function past $1/3$"
author: "UNNS Research Collective"
date: "27 November 2026"
---

Research notes. They continue ANS-I v011; notation is as there. All results concern the nesting grammar. New proofs are pending review; no claim of priority is made, and no comprehensive literature review has been done. Throughout, $\sigma=\operatorname{Re}s$.

# 0. Review of v011 and summary

The owner's review found T45f, T38e, T46f, T46d and T46e-i valid. Two points are adopted: the bound $\sum_k\gcd(k,b^2)^\sigma k^{-2\sigma}\le\zeta(2\sigma)\sum_{d\mid b^2}d^{-\sigma}\ll b^\varepsilon$ ($\sigma>\frac12$) completes the convergence argument of T46d; and the term $X^{1/3}\log X$ of $A_3(X)$ is a formal residue contribution until error estimates are supplied. §5 gives it in smoothed form only.

New here: the remainder $R$ continues to $\sigma>\frac27$ (§3); the shifted series $V$ continues past $1/3$ (§4); hence the conjecture T46e holds, and $G_3$ has a pole of order exactly two at $1/3$ (§5). v011 §3.3 reported that the square divisors of the middle letter could not be controlled. That described the method then used, which estimated each square divisor separately.

# 1. Square-divisor extraction (ANS-T46g)

Let $z=p^{-s}$, $P(z)=1+z^2+z^3$, $A=z(1-z^2)/P$, $B=(1-z)(1+z^3)/P$. The owner's identities
$$w_1(p^{2j+1})-w_1(p^{2j})=A,\quad w_1(p^{2j+2})-w_1(p^{2j+1})=B,\quad w_2(p^j)-w_2(p^{j-1})=Az^{2j-2}$$
$(j\ge0$, resp. $j\ge1)$ are **valid**: they follow from (2) of v011, and were checked symbolically. Hence $w_1=\sigma_{-s}*I_\square*r_{1}$ and $w_2=\sigma_{-s}*r_2$ with the stated local factors. Put $q_1=I_\square*r_1$, so that $w_1=\sigma_{-s}*q_1$, with local series
$$Q(t)=\frac{(1-zt)\big(1+At+(B-1)t^2\big)}{1-t^2},\qquad R_2(t)=(1-zt)\Big(1+\frac{At}{1-z^2t}\Big).\qquad(1)$$
For $j\ge1$ the coefficients are: $q_1(p)=A-z$; $q_1(p^j)=B-zA$ for even $j$ and $A-zB$ for odd $j\ge3$; $r_2(p)=A-z$; $r_2(p^j)=-A(1-z)z^{2j-3}$ for $j\ge2$. Consequently, uniformly in $\operatorname{Im}s$ for $\sigma$ in compact subsets of $(0.3,\infty)$ (where $P$ is bounded away from $0$),
$$|q_1(p)|,|r_2(p)|\le Cp^{-3\sigma},\qquad|q_1(p^j)|\le C,\qquad|r_2(p^j)|\le Cp^{-(2j-2)\sigma}\quad(j\ge2).\qquad(\mathrm H)$$

One qualification: the extra decay of the corrections is at primes. $q_1(p^2)\to1$, and $r_2(p^2)$ is only $O(p^{-2\sigma})$.

# 2. The first component of the remainder (ANS-T46h)

The owner's factorisation $\sum\Phi(M)M^{-2s}=\zeta(2s)\zeta(3s)\zeta(4s)B_\Phi(s)$, the continuation of $R_1$ to $\sigma>\frac14$ and the residue at $1/3$ are **valid**.

**Strengthening (ANS-T46h-i).** $R_1$ is meromorphic on $\sigma>0$, and the line $\sigma=0$ is a natural boundary.

*Proof.* $-R_1(s)=D(s,s)+\sum_M\big[(M+1)^{-2s}-M^{-2s}\big]\Phi(M;s)$, where $D(s,w)=\sum_M\Phi(M;s)M^{-2w}$. The local numerator of $D(s,s)$ is $1+z^3-z^4-z^5=(1-z)(1+z)(1+z^2+z^3)$, not a product of cyclotomic polynomials; by Estermann's theorem, as in T45a, $D(s,s)$ is meromorphic on $\sigma>0$ with natural boundary $\sigma=0$. Expand $(M+1)^{-2s}$ binomially for $M\ge2$; the $n$-th term involves $D(s,s+n/2)$ (without $M=1$). For $n\ge1$ one has $D(s,s+n/2)=\zeta(2s+n)\,\zeta(4s+2n)\prod_p(1+p^{-3s-n}-p^{-4s-n}-p^{-5s-2n})$, and the product is $\zeta(3s+n)/\zeta(4s+n)$ times one converging absolutely for $\sigma>-1/10$. So the whole difference is meromorphic across $\sigma=0$ and cannot remove the boundary. $\square$

# 3. The remainder (ANS-T46i)

**Theorem.** $R$ is meromorphic on $\sigma>\frac27$. Its only possible singularities there are simple poles at $\frac12$ and $\frac13$.

## 3.1 A second form

Put $\delta_s(N)=(N+1)^{-2s}-N^{-2s}$ and $g=\gcd(N,(M+1)^2)$. Then, for $\sigma>\frac12$,
$$R(s)=\sum_{N\ge1}\delta_s(N)\,F_N(s),\qquad F_N(s)=\sum_{M\ge1}(M+1)^{-2s}\,g^{\,s}\,\Phi(MN/g).\qquad(2)$$
Indeed $k^{-2s}\Delta(s,k)=\sum_{n\ge1}\delta_s(nk)$ and $\sum_{k\mid N}\Lambda_M(k)=f_M(N)=g^s\Phi(MN/g)$; the series converge absolutely. The point is that $|\delta_s(N)|\le|2s|N^{-2\sigma-1}$: it suffices to continue each $F_N$ with growth below $N^{2\sigma}$.

## 3.2 One value of $N$

Replacing $(M+1)^{-2s}$ by $M^{-2s}$ changes $F_N$ by a function holomorphic on $\sigma>0$ and $O_s(N^{\sigma+\varepsilon})$. In the new sum write $M=mM'$, where $m$ is composed of primes of $N$ and $(M',N)=1$. Since $(g,M)=1$, the summand is $m^{-2s}M'^{-2s}\Phi(M')\,g^s\Phi(mN/g)$. The last factor is a product over $p^v\,\|\,N$ of
$$H_p(i)=p^{s\min(v,2i)}\,\Phi\big(p^{\mu+v-\min(v,2i)}\big),\qquad\mu=v_p(m),\ i=\min\big(v_p(mM'+1),\lceil v/2\rceil\big),$$
with $i=0$ if $\mu\ge1$. Writing $H_p(i)=\sum_{j\le i}\kappa_p(j)$ gives $g^s\Phi(mN/g)=\sum_e\kappa_m(e)\,[\,e\mid mM'+1\,]$, where $e$ runs over divisors of $\rho(N)$ prime to $m$ and $\kappa_m=\prod_p\kappa_p$. The condition is $M'\equiv-\bar m\pmod e$. Expanding it in characters modulo $e$,
$$\sum_{m}m^{-2s}\sum_e\frac{\kappa_m(e)}{\varphi(e)}\sum_{\chi\bmod e}\bar\chi(-\bar m)\,D_{\chi,N}(s),\qquad D_{\chi,N}(s)=\sum_{(M',N)=1}\chi(M')\,\Phi(M')\,M'^{-2s}.$$
As in §2, $D_{\chi,N}(s)=L_N(2s,\chi)\,L_N(3s,\chi)\,L_N(4s,\chi^2)\,B_{\chi,N}(s)$, where the subscript $N$ removes the Euler factors at $p\mid N$, and $B_{\chi,N}$ has local factors $1-\chi z^4-\chi^2z^5-\chi^2z^6+\chi^2z^7+\chi^3z^8$ (here $\chi=\chi(p)$). So $B_{\chi,N}$ is uniformly bounded for $\sigma\ge\frac14+\eta$.

Only principal characters give poles, at $\frac12$ and $\frac13$. The convexity bound $L(u,\chi^*)\ll(f(1+|\operatorname{Im}u|))^{(1-\operatorname{Re}u)/2+\varepsilon}$ for primitive $\chi^*$ of conductor $f$, $0\le\operatorname{Re}u\le1$, and the bound $N^\varepsilon$ for the removed Euler factors, give on compact subsets of $\sigma>\frac27$
$$\big|(2s-1)(3s-1)D_{\chi,N}(s)\big|\ll_s N^\varepsilon e^{\theta},\qquad\theta=\tfrac12\big(\max(0,1-2\sigma)+\max(0,1-3\sigma)\big).$$
Now $|\kappa_m(e)|\ll N^{\sigma+\varepsilon}m^\varepsilon$ summed over the $O(N^\varepsilon)$ values of $e\le N$, and $\sum_mm^{-2\sigma+\varepsilon}\ll N^\varepsilon$. Hence $(2s-1)(3s-1)F_N(s)$ is holomorphic and $O_s(N^{\sigma+\theta+\varepsilon})$.

## 3.3 Conclusion

The terms of $(2s-1)(3s-1)R$ in (2) are $O_s(N^{-\sigma-1+\theta+\varepsilon})$. We need $\theta<\sigma$: for $\sigma\ge\frac13$ this is $\sigma>\frac14$; for $\sigma<\frac13$ it reads $1-\tfrac52\sigma<\sigma$, that is $\sigma>\frac27$. The bounds grow polynomially in $\operatorname{Im}s$. $\square$

**Residue.** $\operatorname{Res}_{1/3}R=C_\Phi\sum_N\delta_{1/3}(N)\,\lambda(N)$, where $C_\Phi=\zeta(\frac23)\zeta(\frac43)B_\Phi(\frac13)/3$ and $\lambda$ is multiplicative: with $W_\Phi(t)=\sum_j\Phi(p^j)t^j$, $t=p^{-2/3}$,
$$\lambda(p^v)=\frac{H_p(0)+\sum_{j=1}^{\lceil v/2\rceil}\dfrac{\kappa_p(j)}{\varphi(p^j)}+\sum_{\mu\ge1}\Phi(p^{\mu+v})\,t^\mu}{W_\Phi(t)}\qquad(H_p,\kappa_p\text{ at }\mu=0).$$

# 4. The shifted series (ANS-T46j)

Let $q,r$ be multiplicative, with values holomorphic in $s$, satisfying (H) with $q_1,r_2$ replaced by $q,r$ for $\sigma>\frac13-\delta_0$, where $\delta_0=1/1500$; constants are uniform in $\operatorname{Im}s$ up to a power of $|s|$. Put $w_q=\sigma_{-s}*q$ and
$$V(s)=\sum_{M\ge1}(M+1)^{-2s}\,w_q(M)\,w_r(M+1).$$

**Theorem.** $V$ is meromorphic on $\sigma>\frac13-\delta_0$. Its only possible singularities there are simple poles at $\frac12$ and $\frac13$. With $\kappa_q=\mu_{\rm M}*w_q$ (so $\kappa_q(d)=\sum_{am=d}q(a)m^{-s}$), all quantities taken at $s=\frac13$,
$$\operatorname{Res}_{1/3}V=\frac{\zeta(2/3)}3\,(E_1+E_2),\qquad E_1=\sum_{(e,a)=1}\frac{\kappa_r(e)}{e}\prod_{p\mid e}(1-p^{-2/3})\cdot\frac{q(a)}{a^{2/3}},$$
and $E_2$ is the same with $q$ and $r$ exchanged.

The hypotheses hold for $q=q_1$, $r=r_2$ (the series of T46d), for $q=I_\square$, $r=\delta_1$ (the owner's model $U_\square$), and for $q=r=\delta_1$ (the model of T46c).

## 4.1 Expansion

Writing $d=am$, $e=bn$ in $w_q(M)=\sum_{d\mid M}\kappa_q(d)$ gives, for $\sigma>\frac12$,
$$V=\sum_{(am,\,bn)=1}T,\qquad T=q(a)\,r(b)\,(ab)^{-2s}(mn)^{-3s}\,\zeta(2s,\alpha),\qquad\alpha=\frac{M_0+1}{abmn},\qquad(3)$$
where $M_0$ is the least positive $M$ with $am\mid M$, $bn\mid M+1$; here $M_0\le abmn$. Since $\zeta(2s,\alpha)=\alpha^{-2s}+\zeta(2s,1+\alpha)$ and $(abmn)^{-2s}\alpha^{-2s}=(M_0+1)^{-2s}$, away from $s=\frac12$
$$|T|\ll_s|q(a)r(b)|\Big[(mn)^{-\sigma}(M_0+1)^{-2\sigma}+(ab)^{-2\sigma}(mn)^{-3\sigma}\Big].\qquad(4)$$

## 4.2 Two facts on the weights

(F1) $\sum|q(a)|a^{-\beta}$ and $\sum|r(b)|b^{-\beta}$ converge for $\beta>\frac12$. (Euler products; the only terms of $q$ without extra decay sit on squares and higher powers.)

(F2) Let $\sigma_0$ be within $\delta_0$ of $\frac13$, let $q,r$ be taken at an $s$ with $\sigma=\sigma_0$, or with $\sigma\ge\sigma_0=\frac13$, and let $0\le\tau\le\frac1{48}$, $F(n)=\sum_{a\mid n}|q(a)|a^{\sigma_0+\tau}$, $G(n)=\sum_{b\mid n}|r(b)|b^{\sigma_0+\tau}$. Then
$$\sum_{M\le Y}F(M)\,G(M+1)\ll Y^{1+\varepsilon}.\qquad(5)$$
*Proof.* By Hölder it suffices that $\sum_{n\le2Y}F^{4/3}$ and $\sum_{n\le2Y}G^4$ are $O(Y^{1+\varepsilon})$. Since $F(n)^k\le\tau(n)^{k-1}\sum_{a\mid n}(|q(a)|a^{\sigma_0+\tau})^k$, we need $\sum_a(|q(a)|a^{\sigma_0+\tau})^ka^{-1}$ to converge up to $a^\varepsilon$. For $k=\frac43$ the exponent of $p$ is $(-2\sigma_0+\tau)k-1<-1$ at primes and at most $j\big((\sigma_0+\tau)k-1\big)$ at $p^j$, $j\ge2$, where $(\sigma_0+\tau)k<\frac12$. For $G$ and $k=4$ it is $(-2\sigma_0+\tau)4-1$ at primes, and at $p^j$ at most $(2-j)\sigma_0 k+j\tau k-j$, below $-1$. $\square$

## 4.3 The half-plane $\sigma>\frac13$

Here $(2s-1)\sum T$ converges normally. The second part of (4) is clear from (F1). In the first, $mn\ge M_0/(ab)$, so $(mn)^{-\sigma}\le(ab/M_0)^{1/3}$; group by $M=M_0$ and note that $a\mid M$, $b\mid M+1$, while $m,n$ number at most $M^\varepsilon$. The bound is $\sum_MM^{-2\sigma-1/3+\varepsilon}F(M)G(M+1)$ with $\sigma_0=\frac13$, $\tau=0$ (the bounds (H) only improve for $\sigma>\frac13$), which converges by (5). So (3) continues $V$ to $\sigma>\frac13$.

## 4.4 Splitting near $1/3$

Let $|\sigma-\frac13|<\delta_0$. Divide the quadruples into
$$\mathcal S:\ \max(m,n)\le(ab)^4;\qquad\mathcal A:\ n\ge m,\ n>(ab)^4;\qquad\mathcal B:\ m>n,\ m>(ab)^4.$$

## 4.5 The set $\mathcal S$: absolute convergence

*Second part of (4).* $\sum_{m\le(ab)^4}m^{-3\sigma}\ll(ab)^{12\delta_0+\varepsilon}$, so the terms with given $a,b$ total $O\big(|qr|\,(ab)^{-2\sigma+24\delta_0+\varepsilon}\big)$; use (F1).

*First part.* Now $(mn)^{-\sigma}\le(ab/M_0)^\sigma$, and $M_0\le abmn\le(ab)^9$. For $M_0=M\in[Y,2Y]$ we therefore have $ab\ge Y^{1/9}$, whence $1\le(ab)^\tau Y^{-\tau/9}$. With $\tau=\frac1{48}$, (5) bounds the block by
$$Y^{-3\sigma-\tau/9+\varepsilon}\sum_{M\le2Y}F(M)G(M+1)\ll Y^{\,1-3\sigma-1/432+\varepsilon}.$$
Since $1-3\sigma<3\delta_0=1/500<1/432$, the dyadic blocks are summable. $\square$

## 4.6 A counting lemma

Let $(u,b)=1$, and for $(n,u)=1$ let $j(n)\in[1,u]$ be the inverse of $\pm bn$ modulo $u$ (a fixed sign). Put $\bar Z_u=\varphi(u)^{-1}\sum_{(j,u)=1,\,j\le u}\zeta(2s,j/u)$ and $\Delta(I)=\sum_{n\in I,(n,u)=1}\big[\zeta(2s,j(n)/u)-\bar Z_u\big]$.

**Lemma.** Let $\frac14<\sigma<\frac12$. For $I\subset(N,2N]$, $N\ge\max(1,\sqrt u/2)$,
$$|\Delta(I)|\ll_s(buN)^\varepsilon\big(u^{1/2-\sigma}N^{2\sigma}+(bN)^{2\sigma}\big).$$

*Proof.* Let $C(y)$ count the $n\in I$ with $j(n)\le y$, and $E(y)=C(y)-\dfrac{|I^*|}{\varphi(u)}U(y)$, where $|I^*|$ counts the $n\in I$ prime to $u$ and $U(y)$ the units $\le y$. Then $\Delta=\int\zeta(2s,y/u)\,dE(y)$.

(a) $E(y)\ll u^{1/2+\varepsilon}$. $E$ is additive in $I$ and vanishes on a complete period, so let $|I|<u$. This is then the equidistribution of modular inverses: detect $j(n)\le y$ by additive characters and use the Weil--Estermann bound for incomplete Kloosterman sums (the estimate used in T46c).

(b) $C(y)\ll(buN)^\varepsilon(Ny/u+1)$, and $C(y)=0$ if $y<u/(3bN)$. Take the sign $+$: $bnj=1+tu$ with $t\ge1$ (as $n\ge2$), $t\le2bNy/u$, and $b\mid1+tu$ fixes $t$ modulo $b$. So there are $O(Ny/u+1)$ values of $t$, none if $2bNy<u$, and each has $O((buN)^\varepsilon)$ pairs $(n,j)$. For the sign $-$: $bnj=tu-1$ and the same argument applies (for $u=1$ the bound is trivial).

(c) Split $\zeta(2s,x)=x^{-2s}+\zeta(2s,1+x)$. The second function has bounded derivative on $[0,1]$, so its integral against $dE$ is $\ll_su^{1/2+\varepsilon}$, which is admissible. For the first, if $N>u^{3/2}$ integrate by parts over $[1,u]$: the result is $\ll_su^{1/2+2\sigma+\varepsilon}\le u^{1/2-\sigma+\varepsilon}N^{2\sigma}$. Otherwise let $Y_0=\min(u,u^{3/2}/N)$. For $j>Y_0$, integration by parts and (a) give $(u/Y_0)^{2\sigma}u^{1/2+\varepsilon}$. For $j\le Y_0$ bound the two parts of $dE$ separately: by (b) and partial summation,
$$\int_1^{Y_0}\Big(\frac uy\Big)^{2\sigma}dC\ll(buN)^\varepsilon\big(Nu^{2\sigma-1}Y_0^{1-2\sigma}+(bN)^{2\sigma}\big),$$
and the mean term is $\ll Nu^{2\sigma-1+\varepsilon}Y_0^{1-2\sigma}$. The choice of $Y_0$ gives the lemma. $\square$

## 4.7 The set $\mathcal A$

Fix $a,b,m$ and let $u=am$. In $\mathcal A$ the variable $n$ runs over $n\ge n_0=\max(m,(ab)^4+1)$, $(n,u)=1$. Here $bn\ge2$ and $\alpha=j/u$ exactly, with $j\equiv(bn)^{-1}\pmod u$. So $\sum_nn^{-3s}\zeta(2s,\alpha)=\mathrm P+\mathrm E$ with
$$\mathrm P=\bar Z_u\sum_{n\ge n_0,(n,u)=1}n^{-3s},\qquad\mathrm E=\sum_{n\ge n_0,(n,u)=1}n^{-3s}\big[\zeta(2s,j/u)-\bar Z_u\big].$$
Cut into blocks $(N,2N]$ with $N=2^i(n_0-1)$; then $N\ge\sqrt u/2$. Partial summation and the lemma give
$$|\mathrm E|\ll_s(abm)^\varepsilon\big((am)^{1/2-\sigma}+b^{2\sigma}\big)N_0^{-\sigma+\varepsilon},\qquad N_0=n_0-1\ge\tfrac12\max\big(m,(ab)^4\big),$$
where for $m=1$ the lower bound is $N_0\ge(ab)^4$. Multiply by $|q(a)r(b)|(ab)^{-2\sigma}m^{-3\sigma}$ and use $N_0^{-\sigma}\ll m^{-\sigma\theta}(ab)^{-4\sigma(1-\theta)}$, with $\theta=\frac34$ for the first term and $\theta=\frac12$ for the second. The powers of $a$, $b$, $m$ become

| term | $a$ | $b$ | $m$ |
|--|--|--|--|
| first | $\frac12-4\sigma$ | $-3\sigma$ | $\frac12-\frac{19}4\sigma$ |
| second | $-4\sigma$ | $-2\sigma$ | $-\frac72\sigma$ |

Near $\frac13$ the exponents of $a,b$ are below $-\frac12$ and that of $m$ below $-1$. By (F1), $\sum_{a,b,m}|\ldots\mathrm E|$ converges.

## 4.8 The set $\mathcal B$

Fix $a,b,n$ and let $v=bn$; now $m\ge m_0=\max(n+1,(ab)^4+1)$, $(m,v)=1$. One has $\alpha=j/v+1/(abmn)$, with $j\in[1,v]$, $j\equiv-(am)^{-1}\pmod v$. Write $\zeta(2s,\alpha)=\bar Z_v+[\zeta(2s,j/v)-\bar Z_v]+D(m)$. The middle term is treated by the lemma with $(u,b)$ replaced by $(v,a)$; here $m\ge n$ and $m>b^4$ give $m\ge\sqrt v/2$. The table of §4.7 holds with $a,b$ exchanged and $n$ in place of $m$.

*The shift.* With $h=1/(abmn)$ and $x=j/v$, $|D(m)|\ll_sh\,(x^{-2\sigma-1}+1)$. By part (b) of the lemma,
$$\sum_{M<m\le2M}(v/j(m))^{2\sigma+1}\ll(abnM)^\varepsilon\big(Mv^{2\sigma}+(aM)^{2\sigma+1}\big),$$
so the block of $\sum_mm^{-3\sigma}|D(m)|$ is $\ll M^{-3\sigma+\varepsilon}v^{2\sigma-1}a^{-1}+M^{-\sigma+\varepsilon}a^{2\sigma}v^{-1}+M^{-3\sigma+\varepsilon}(av)^{-1}$. Sum over $M=2^i(m_0-1)$ and multiply by $|q(a)r(b)|(ab)^{-2\sigma}n^{-3\sigma}$. The powers of $a,b,n$ are all below $-\frac12,-\frac12,-1$ (for the second term use $M_0^{-\sigma}\le n^{-\sigma/2}(ab)^{-2\sigma}$, giving $a^{-2\sigma}b^{-4\sigma-1}n^{-7\sigma/2-1}$). So the shift sum converges absolutely.

## 4.9 The principal parts

$\bar Z_u=\varphi(u)^{-1}u^{2s}\zeta(2s)\prod_{p\mid u}(1-p^{-2s})$, so $|\bar Z_u|\ll_su^{2\sigma-1+\varepsilon}$. The sum $\sum_{n\ge n_0,(n,u)=1}n^{-3s}$ is $\zeta(3s)\prod_{p\mid u}(1-p^{-3s})$ minus a finite sum; after multiplication by $3s-1$ it is entire and $\ll_su^\varepsilon n_0^{3\delta_0+\varepsilon}$, with $n_0\le3m(ab)^4$. Hence the terms of $(3s-1)\sum\mathrm P$ over $\mathcal A$ are bounded by
$$|q(a)r(b)|\,a^{-1+12\delta_0+\varepsilon}\,b^{-2\sigma+12\delta_0+\varepsilon}\,m^{-\sigma-1+3\delta_0+\varepsilon},$$
which is summable. For $\mathcal B$ exchange $a$ and $b$.

## 4.10 Conclusion

For $\frac13<\sigma<\frac13+\delta_0$ the series (3) converges absolutely (§4.3), so it may be regrouped as $\mathcal S+\sum_{\mathcal A}(\mathrm P+\mathrm E)+\sum_{\mathcal B}(\mathrm P+\mathrm E+D)$, each sum converging absolutely. By §§4.5--4.9 the right side, multiplied by $3s-1$, converges normally on the whole strip. This continues $V$ with at most a simple pole at $\frac13$. All bounds are polynomial in $\operatorname{Im}s$.

*Residue.* Only the principal parts contribute. As $s\to\frac13$, $(s-\frac13)\sum_{n\ge n_0}n^{-3s}\to\varphi(u)/(3u)$, and $\bar Z_u\varphi(u)/u=\zeta(\frac23)u^{-1/3}\prod_{p\mid u}(1-p^{-2/3})$. The coprimality conditions on $\mathcal A$ amount to $(am,b)=1$. Summing first over $d=am$, with $\sum_{am=d}q(a)a^{-2/3}m^{-1}(am)^{-1/3}=\kappa_q(d)/d$, shows that $\mathcal A$ gives $\zeta(\frac23)E_2/3$; $\mathcal B$ gives $\zeta(\frac23)E_1/3$. $\square$

# 5. Consequences for depth three

**Theorem (ANS-T46e).** $V$ and $R$ of T46d continue meromorphically past $\frac13$, and
$$\operatorname{Res}_{1/3}V=r_V=\frac{\zeta(2/3)(E_1+E_2)}3<0,$$
with $E_1,E_2$ the Euler products of v011 §3.1. This is the residue conjectured there.

*Proof.* (H) holds by §1; apply §§3 and 4. For these weights the Euler factor of the sum $E_1$ in §4 is
$$1+(1-p^{-2/3})\big[(1-p^{-1})W_2(p^{-1})-1\big]+\big[Q(p^{-2/3})-1\big]=E_{1,p},$$
because $Q(t)=(1-zt)(1-t)W_1(t)$ and $zt=p^{-1}$ at $t=p^{-2/3}$; similarly for $E_2$. Positivity is T46e-i. $\square$

**Corollary (ANS-T46k).** $G_3$ is meromorphic on $\sigma>\frac13-\frac1{1500}$. Its only singularities there are the pole of order three at $\frac12$ and a pole of order **exactly two** at $\frac13$, with
$$\lim_{s\to1/3}\big(s-\tfrac13\big)^2G_3(s)=\frac{\zeta(2/3)^2\,H(1/3)\,r_V}3\approx-0.75916.$$
In particular ANS-T46b holds for $k=3$.

*Proof.* T46d and the above; $H$ is holomorphic on $\sigma>\frac15$, $G_2$ has at most a simple pole at $\frac13$ (T45) and so has $\zeta(2s)R$. The pole at $\frac12$ is that of T34. $\square$

**Corollary (smoothed second term).** For all large $m$ there are constants $b_m$ and $\eta>0$ with
$$\sum_{E\le X}\Big(1-\frac EX\Big)^m=\mathrm{Res}_{1/2}+X^{1/3}\big(a_m\log X+b_m\big)+O\big(X^{1/3-\eta}\big),$$
where the sum is over words of length three, $\mathrm{Res}_{1/2}$ is the residue of $G_3(s)X^s\,m!/(s(s+1)\cdots(s+m))$ at $\frac12$, and $a_m=\dfrac{\zeta(2/3)^2H(1/3)r_V}3\cdot\dfrac{m!}{\prod_{j=0}^m(\frac13+j)}\ne0$.

*Proof.* Perron's formula and a shift of the contour; $G_3$ grows polynomially on vertical strips away from its poles. $\square$

No such statement is made for the unsmoothed count $A_3(X)$.

# 6. Limits, and what to check

- $\delta_0=1/1500$ is not optimised; it is set by the Hölder step of §4.5. How far $G_3$ continues is open.
- The proof of §4 is new and deserves independent examination, in this order: the counting lemma (b), where the divisor bound replaces short-range cancellation; the choice of the sets in §4.4 against the bound $M_0\le(ab)^9$; the moment estimate (5).
- Classical inputs: Weil--Estermann bounds, convexity bounds for Dirichlet $L$-functions, Estermann's theorem on Euler products.

# 7. Computations

Finite and floating-point checks only. Parameters and outputs are in `results/`.

- Algebra (symbolic): T46g for $j\le8$; the two residue identities of §5, exactly; $E_{1,p}=1+2z^4-3z^5+O(z^6)$ and $E_{2,p}=1+z^4-2z^5+O(z^6)$, as in the review; for $q=r=\delta_1$ the factor of T46c.
- The two formulas for $\alpha$: exact, all coprime pairs $u,v\le120$.
- The exponent inequalities of §§3--4, in exact fractions at $\sigma=\frac13,\frac13\pm\delta_0$ ($\varepsilon$ powers omitted).
- Lemma, sanity only: at $s=\frac13$, sampled $u\le5000$, the ratio of $\sup|\Delta|$ to the bound without $\varepsilon$ factor stays below $0.83$.
- $\kappa_3$: $D(\frac12)\,\zeta(\frac32)\,H(\frac12)=5.1053517$, with $D$ the mean-value product of v011; the value recorded in v006 is $5.105352$. This tests T46d against an independent computation.
- Fixed $N$ (§3): the sums $\sum_{M\le X}g^s\,\Phi(MN/g)$ at $s=\frac13$, mean term removed, against the residue formula. Coefficient of $X^{2/3}$ at $X=10^7$ and its predicted value:

| $N$ | 1 | 4 | 12 | 36 |
|--|--|--|--|--|
| observed | $-1.524$ | $-2.050$ | $-2.559$ | $-3.168$ |
| predicted | $-1.543$ | $-2.075$ | $-2.588$ | $-3.202$ |

- $\operatorname{Res}_{1/3}R\approx0.433$ (partial sums to $10^6$).
- General residue formula on a second weight pair, $U_\square$ (frozen at $s=\frac13$): predicted coefficient $-36.18$; computed $-33.13,\,-34.39,\,-35.00,\,-35.47,\,-35.55$ at $X=10^4,10^5,10^6,10^7,2\cdot10^7$. For $w_1,w_2$ see v011 ($-4.0436$ against $-4.0697$).

The frozen-weight sums do not test the continuation itself; they test the residue formulas.

# 8. Open

- The largest half-plane for $G_3$; its singularities beyond $\frac13$; zeros.
- A sharp form of the second term of $A_3(X)$ and of $A_2(X)$.
- Depth four and higher (T46, T46a), including T46b for $k\ge4$.
- ANS-T33, T39; ANS-T38 for the complete functions. Not addressed.
