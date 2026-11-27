---
title: "ANS-I v015 --- Collective analytic growth near $s=1$"
author: "UNNS Research Collective"
date: "27 November 2026"
---

Research notes. They continue ANS-I v014; notation is as there. All results concern the nesting grammar. New proofs are pending review; no claim of priority is made, and no comprehensive literature review has been done.

# 0. Summary

| ID | Statement in brief | Status |
|:-----|:---------------------------------------------|:-----------|
| T48a | $\limsup G_k(1)^{1/k}/\log k\le e^{\gamma}$ (v014 review) | PROVED |
| T48b | the exponential history function has order $1$, infinite type (v014 review) | PROVED |
| T49 | $\liminf G_k(1)^{1/k}/\log k\ge1.1079$ | PROVED |
| T50 | growth in the window $s=1+\tau/\log k$ | PROVED |
| T46t | restated as the review recommends | CONJECTURE |

Combining T48a and T49,
$$1.1079\ldots\le\liminf_{k}\frac{G_k(1)^{1/k}}{\log k}\le\limsup_{k}\frac{G_k(1)^{1/k}}{\log k}\le e^{\gamma}=1.7810\ldots$$

**Not obtained.** Whether the limit exists, and its value, are open; §5 gives a heuristic reason to doubt that it is $e^{\gamma}$. T33 (the singularity at $\sigma_c$) was not advanced in this version. Depth four is unchanged.

# 1. The two deductions of the v014 review

## 1.1 Sharper upper constant (ANS-T48a)

For $a,b>0$ put $D_{a,b}(E)=\sum_{d\mid E}d^{-a}\prod_{p\mid d}(1-p^{-b})$. The step estimate of v014 §5.2 holds in the sharper form
$$\sum_Nr_N^{-a}\Big(\frac{\gcd(E,N)}N\Big)^b\le\zeta(a+b)\,D_{a,b}(E),$$
because $J_b(d)=d^b\prod_{p\mid d}(1-p^{-b})$ was previously bounded by $d^b$. The function $D_{a,b}$ is multiplicative and
$$D_{a,b}(p^{\ell})=1+(1-p^{-b})\sum_{j=1}^{\ell}p^{-aj}\le F_p=\frac{1-p^{-a-b}}{1-p^{-a}} .$$
**Checked: the deduction is correct.** It is the case $\tau=0$ of the upper bound in §3, where the remaining details are written out.

## 1.2 The exponential history function (ANS-T48b)

Let $\mathcal B_1(t)=\sum_kG_k(1)t^k/k!$. Suppose
$$c_-\le\liminf\frac{G_k(1)^{1/k}}{\log k},\qquad\limsup\frac{G_k(1)^{1/k}}{\log k}\le c_+ .$$
Then $\mathcal B_1$ is entire of order $1$ and infinite type, and
$$c_-\le\liminf_{r\to\infty}\frac{\log\mathcal B_1(r)}{r\log r}\le\limsup_{r\to\infty}\frac{\log\mathcal B_1(r)}{r\log r}\le c_+ .$$

*Proof.* The coefficient $c_k=G_k(1)/k!$ satisfies $\log(1/c_k)=k\log k-k\log\log k+O(k)$, so the order $\limsup k\log k/\log(1/c_k)$ is $1$, and $k\,c_k^{1/k}\to\infty$ gives infinite type. All coefficients are positive, so the maximum modulus is $\mathcal B_1(r)$. *Lower bound:* for $c<c_-$ keep the single term $k=\lfloor cr\log r\rfloor$. By Stirling its logarithm is at least $k\log\big((c+o(1))\,er\log k/k\big)=(1+o(1))\,k$. *Upper bound:* put $K=r\log^2r$. For $k\le K$ one has $\log k\le(1+o(1))\log r$, so apart from a bounded number of initial terms the sum is at most $\exp\big((c_++o(1))\,r\log r\big)$. For $k>K$ the terms are at most $(C\,r\log k/k)^k\le(C'/\log r)^k$. $\square$

With $c_-=1$, $c_+=e^{\gamma}$ this is the statement of the review. **It is correct**, and T49 raises $c_-$ to $1.1079\ldots$

# 2. The lower constant $1$ is not sharp (ANS-T49)

Let $\rho$ be the Dickman function and $I(v)=\int_v^{\infty}\rho(u)\,du$. We use two classical facts: $\int_0^{\infty}\rho=e^{\gamma}$, and for fixed $u\ge0$ the sum of $1/m$ over $z$-smooth $m\le z^u$ is $\big(\int_0^u\rho+o(1)\big)\log z$. With Mertens' theorem this gives, uniformly for $t=z^v$ with $v$ in a bounded range,
$$T_z(t):=\sum_{m>t,\;P^+(m)\le z}\frac1m=\big(I(v)+o(1)\big)\log z.\qquad(1)$$

**Theorem.** Put $\beta_*=2/(2+e^{\gamma})=0.52895\ldots$ Then
$$\liminf_{k\to\infty}\frac{G_k(1)^{1/k}}{\log k}\ \ge\ 1+\beta_*\,I(1/\beta_*)=1.1079\ldots,$$
where, since $1<1/\beta_*<2$, $I(v)=e^{\gamma}+1-v(2-\log v)$ at $v=1/\beta_*$.

## 2.1 The alphabet

Fix $\beta<\beta_*$ and put $Y=\lfloor k/\log k\rfloor$, $z=Y^{\beta}$. Let
$$\mathcal A=\{N\le Y\}\ \cup\ \{N>Y:\ P^+(N)\le z\},\qquad\mu(N)=r_N^{-1}=\frac N{(N+1)^2}.$$
Call the two parts *base* and *extra*. Only primes $p\le Y$ divide letters of $\mathcal A$. The extra letters are unbounded. By (1) with $v=1/\beta$,
$$B_{\mathcal A}=\sum_{N\in\mathcal A}\mu(N)=\big(1+\beta I(1/\beta)+o(1)\big)\log Y.$$

## 2.2 A property of $\beta$

**Lemma 1.** For $\beta<\beta_*$ there is $\kappa>0$ with $\beta I\big(\frac{1-\theta}{\beta}\big)\le(1-\kappa)(1-\theta)$ for all $\theta\in[0,\beta]$.

*Proof.* $g(\theta)=\beta I((1-\theta)/\beta)-(1-\theta)$ has derivative $\rho+1>0$, so it is largest at $\theta=\beta$, where $g=\beta(I(v)-v)$ with $v=(1-\beta)/\beta$. Here $v>e^{\gamma}/2$. If $v<1$ then $I(v)=e^{\gamma}-v<v$. If $v\ge1$ then $I(v)\le e^{\gamma}-1<1\le v$. So $g<0$ on $[0,\beta]$. $\square$

## 2.3 The balance of every prime is preserved

**Lemma 2.** There is $\eta>0$ such that for large $k$ and every prime $p$, with $x=e^{\eta}$ and $X_p=2v_p(N+1)-v_p(N)$,
$$\sum_{N\in\mathcal A}\mu(N)\big(x^{-X_p}-1\big)\le0.$$

*Proof.* If $p>Y$ then $p$ divides no letter, so $X_p\ge0$. Let $p\le Y$. By v014, Lemma 1, the base letters contribute at most $-\pi_p(\eta-C\eta^2)$, where $\pi_p$ is the sum of $\mu(N)$ over $N\le Y$ with $p\mid N+1$. If $z<p\le Y$ then $p$ divides no extra letter, so the extra letters contribute at most $0$.

Let $p\le z$ and $\theta=\log p/\log Y\le\beta$. Summing over $N=mp-1$,
$$\pi_p=\frac{(1-\theta)\log Y+O(1)}p.\qquad(2)$$
An extra letter contributes at most $\mu(N)(x^{v_p(N)}-1)$, and $x^v-1=\sum_{j\le v}(x-1)x^{j-1}$. Writing $N=p^jm$, the extra contribution is at most
$$(x-1)\sum_{j\ge1}x^{j-1}p^{-j}\,T_z(Y/p^j).$$
Let $p_0$ be a large constant. *For $p\ge p_0$:* the term $j=1$ is $(x-1)\big(\beta I((1-\theta)/\beta)+o(1)\big)\log Y/p$ by (1); the terms $j\ge2$ are at most $(x-1)\,C'x\log Y/(p(p-x))$. By Lemma 1 the total is at most $(x-1)(1-\kappa/2)(1-\theta)\log Y/p$ if $p_0$ is large. *For $p<p_0$:* here $T_z(Y/p^j)=(I(1/\beta)+o(1))\log z$ for each fixed $j$ and is $O(\log Y)$ always, so the total is at most $(x-1)\big(\beta I(1/\beta)+o(1)\big)\log Y/(p-x)$. Since $\beta I(1/\beta)\,p/(p-x)<\frac12$ for $p\ge2$ and $x$ near $1$, the same bound holds with room to spare.

Adding (2), the whole sum is at most
$$\frac{(1-\theta)\log Y}p\Big[-\eta+C\eta^2+(e^{\eta}-1)(1-\kappa')+o(1)\Big]$$
for some $\kappa'>0$. This is negative for a small fixed $\eta$ and large $k$. $\square$

*Proof of the theorem.* With letters drawn from $\mu/B_{\mathcal A}$, Jensen gives $G_k(1)\ge B_{\mathcal A}^k\exp(-\mathbb E\log K_k)$. By Lemma 2 and Ville's inequality, $\mathbb E\,v_p(K_k)\le1/(e^{\eta}-1)$, and only $p\le Y$ occur, so $\mathbb E\log K_k=O(Y)=o(k)$. Hence $G_k(1)^{1/k}\ge(1-o(1))B_{\mathcal A}$. Let $k\to\infty$ and then $\beta\to\beta_*$. $\square$

## 2.4 Meaning

The base letters are those of v014. The extra letters are arbitrarily large but contain only primes up to about $Y^{0.529}$. The base letters supply every prime up to $Y$ more than they consume, and the margin $(1-\theta)\log Y/p$ pays for the demand of the extra letters. So the growth is **not** carried by letters of size at most $k/\log k$ alone. This corrects the reading of v014 §5.3, as the review asked: that cut-off gave a sufficient family, not a description of the typical letters.

The constant $1.1079\ldots$ is what this simplest two-layer choice gives. Mixtures of several smoothness levels should give more; we have not optimised them.

# 3. The window around $s=1$ (ANS-T50)

Let $\mathrm{Ein}(\tau)=\int_0^1(1-e^{-\tau u})\,du/u$.

**Theorem.** For every real $\tau$, with $s_k=1+\tau/\log k$,
$$\int_0^1e^{-\tau u}du\ \le\ \liminf_k\frac{G_k(s_k)^{1/k}}{\log k}\ \le\ \limsup_k\frac{G_k(s_k)^{1/k}}{\log k}\ \le\ e^{\gamma-\mathrm{Ein}(\tau)} .$$

At $\tau=0$ these are $1$ and $e^{\gamma}$. As $\tau\to+\infty$ the left side is $(1-e^{-\tau})/\tau$ and the right side is $e^{-E_1(\tau)}/\tau$, with $E_1$ the exponential integral. Both approach $1/\tau$.

## 3.1 Lower bound

v014, Lemma 1, holds uniformly for $\frac12\le a\le2$: in its proof the ratio of weights is at most $(2p^{1-j})^a\le4\cdot2^{-(j-1)/2}$, which only changes $C$. Take letters $N\le Y=\lfloor k/\log k\rfloor$. As in v014 §5.1, $G_k(s)^{1/k}\ge B_Y(s)\exp(-O(Y/k))$. Here
$$B_Y(s)=\sum_{N\le Y}N^{-s}+O(1)=\log Y\int_0^1e^{-(s-1)(\log Y)u}\,du+O(1),$$
and $(s_k-1)\log Y\to\tau$. $\square$

## 3.2 Upper bound

Take $\epsilon=1/(k\log^2k)$, $P=1/\epsilon$ and exponents $a,b\in[s_k-k\epsilon,\,s_k]$. By §1.1, $D_{a,b}(E)\le C\,E^{\epsilon}$ with
$$\log C=\sum_p\max\big(0,\ \log F_p-\epsilon\log p\big).$$
For $p>P$ we have $\log F_p\le(1+o(1))p^{-a}\le(1+o(1))P^{-a}$, and $P^{-a}=\epsilon\,e^{(1-a)\log P}=\epsilon\,(e^{-\tau}+o(1))$, which is smaller than $\epsilon\log p$. So these terms vanish. For $p\le P$,
$$\sum_{p\le P}\log F_p=-\sum_{p\le P}\log\Big(1-\frac1p\Big)+\sum_{p\le P}\frac{p^{1-a}-1}p-\log\zeta(2)+o(1).$$
Since $(1-a)\log P\to-\tau$, Mertens' theorem and partial summation give $\sum_{p\le P}(p^{1-a}-1)/p\to-\mathrm{Ein}(\tau)$. As $\log P\sim\log k$,
$$C\le\Big(\frac{e^{\gamma-\mathrm{Ein}(\tau)}}{\zeta(2)}+o(1)\Big)\log k .$$
Now $F_{n+1}(a,b)\le\zeta(a+b)\,C\,F_n(a-\epsilon,b-\epsilon)$. Apply this $k$ times from $a=b=s_k$; then $\zeta(a+b)\to\zeta(2)$ and $F_0=1$. $\square$

## 3.3 Reading

The transition at $s=1$ has width $1/\log k$. To the right, far into the window, the growth per letter approaches $\log k/\tau=1/(s-1)$, the leading size of $B(s)$ near $1$: the source restriction no longer matters at leading order. At the centre it is of order $\log k$ with an undetermined constant. To the left the two bounds separate quickly: the upper bound grows doubly exponentially in $|\tau|$ and the lower bound only like $e^{|\tau|}/|\tau|$. The theorem is for fixed $\tau$; it does not give uniformity as $|\tau|$ grows with $k$.

# 4. Two remarks on the review's other suggestions

**Superadditivity.** By T47, $\log G_k(\sigma)$ is superadditive for $\sigma>\frac12$, so $\lim\log G_k(\sigma)/k$ exists in $(-\infty,+\infty]$. This agrees with v001, Theorem 4.4, which identifies it as $\log B(\sigma)$ for $\sigma>1$ and $+\infty$ below.

**A transfer operator.** On functions of the state, $(\mathcal L_sf)(E)=\sum_N\big(\gcd(E,N)/(N+1)^2\big)^sf\big((N+1)^2E/\gcd(E,N)\big)$ keeps multiplicities and $G_k(s)=(\mathcal L_s^k1)(1)$. On bounded functions its norm is $\sup_E(\mathcal L_s1)(E)=B(s)$, finite only for $s>1$. So on that space it adds nothing to what is known. A useful version needs a space that records how much of each prime is available. We have not constructed one.

# 5. Is the upper constant attained? (open)

**A necessary condition (immediate).** Since $E(w)$ is an integer,
$$v_p(K(w))\ge\sum_iv_p(N_i)-2\sum_iv_p(N_i+1)$$
for every word and prime. So if a family of letters consumes a prime $p$ faster than it supplies it, the source pays about $p$ raised to the deficit.

**Heuristic, not a proof.** The upper bound corresponds to all letters being $Y$-smooth with $Y$ near $k$, weighted by $1/N$. That distribution has total weight about $e^{\gamma}\log Y$, and $\Pr(p\mid N)=1/p$. Take $p=Y^{\theta}$. Below $p$ the only letter with $p\mid N+1$ is $p-1$. If the numbers $N+1$ with $N$ smooth and larger than $p$ are evenly spread over the classes modulo $p$, then
$$\Pr(p\mid N+1)\approx\frac{1-\theta e^{-\gamma}}p .$$
The supply $2\Pr(p\mid N+1)$ falls below the consumption when $\theta>e^{\gamma}/2\approx0.89$. This would leave a deficit linear in $k/p$ for many primes and a cost of order $k\log k$ in $\log K_k$, far larger than any constant-factor gain. **This suggests that the limit, if it exists, is strictly below $e^{\gamma}$.** The even distribution is not proved here, and no value of the limit is proposed.

**Finite data** (`balance`: smooth $N\le2\cdot10^7$, $Y=300$, so the tail of the distribution is missing):

| range of $\theta$ | mean of $p\Pr(p\mid N+1)$ | prediction at mid-range | mean of $p\Pr(p\mid N)$ |
|:---------------|-------------:|-------------:|-------------:|
| $0.5$ to $0.7$ | $0.646$ | $0.663$ | $0.968$ |
| $0.7$ to $0.9$ | $0.540$ | $0.551$ | $0.947$ |
| $0.9$ to $1$ | $0.473$ | $0.467$ | $0.929$ |

The supply follows the prediction closely. The balance in the top range is near zero in these truncated data (slightly positive at $Y=300$, slightly negative at $Y=100$); it becomes negative only if consumption reaches its limiting value $1$.

# 6. The general coefficient conjecture, restated (ANS-T46t)

Following the review: **for every $k\ge2$, $G_k$ continues meromorphically to a neighbourhood of $\frac13$, has there a pole of order exactly $\ell_k=\lfloor k^2/4\rfloor$, and its leading Laurent coefficient is**
$$\zeta(\tfrac23)^k\,3^{-\ell_k}\sum_{L(R)=\ell_k}C_R .$$
Status: CONJECTURE for $k\ge4$; proved for $k=2,3$ (T45, T46k, T46s-ii).

# 7. Computations

All in `v015_checks.py`; results in `results/`. Floating point, nothing certified.

- `divisor`: the product form of $D_{a,b}(E)$ and the bound by $\prod F_p$, for $E\le3000$ and four exponent pairs.
- `crossover`: $\prod_{p\le X}(1-p^{-s})^{-1}/\log X$ for $X\le10^7$, approaching the upper bound of T50 slowly (the error behaves like a constant over $\log X$).
- `dickman`: $\int_0^{12}\rho$, the closed form of $I$, the constant $1.10791$, and Lemma 1 at $\beta=0.52$.
- `drift`: the sum in Lemma 2 for $Y=10^3,10^4$, $\beta=0.52$, $x=1.01$, extra letters truncated at $2\cdot10^7$; negative for every $p$. This illustrates the lemma, which concerns large $k$ and the untruncated alphabet.
- `balance`: §5.

The asymptotic statements T48a, T49 and T50 are not verified numerically.
