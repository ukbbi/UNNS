---
title: "ANS-I v014 --- Composition, the local mechanism at one third, and growth at $s=1$"
author: "UNNS Research Collective"
date: "27 November 2026"
---

Research notes. They continue ANS-I v013; notation is as there. All results concern the nesting grammar. New proofs are pending review; no claim of priority is made, and no comprehensive literature review has been done.

# 0. Summary

| ID | Statement in brief | Status |
|:-----|:---------------------------------------------|:-----------|
| T47 | words compose by a bicyclic law; blocks factor through one overlap divisor | PROVED |
| T46r | middle-word overlap decomposition (proposed in the v013 review) | PROVED |
| T46s | one local expectation for every role pattern; it gives the proved leading terms | PROVED |
| T46t | leading coefficient of $G_k$ at $\frac13$ for every $k$ | CONJECTURE |
| T48 | $G_k(1)^{1/k}$ has exact order $\log k$ | PROVED |

**Not obtained.** The continuation of $G_4$ past $\frac13$ is not proved and no viable route to it has been established (§4). The question T33 about $\sigma_c$ remains open.

# 1. Composition of words (ANS-T47)

**Theorem.** For words $u,v$ let $d=\gcd(E(u),K(v))$. Then
$$K(uv)=\frac{K(u)K(v)}d,\qquad E(uv)=\frac{E(u)E(v)}d .$$

*Proof.* By T03 the histories of $u$ start at $mK(u)$ and end at $mE(u)$, $m\ge1$. Such a history continues by $v$ if and only if $K(v)\mid mE(u)$, that is $K(v)/d\mid m$. The least $m$ is $K(v)/d$, which gives $K(uv)$. The endpoint is then $mE(u)Q(v)$ with $Q(v)=E(v)/K(v)$, which gives $E(uv)$. $\square$

This is the law proposed in the v013 review. Writing $(\kappa,\varepsilon)=(v_pK,v_pE)$, it reads
$$(\kappa_1,\varepsilon_1)\circ(\kappa_2,\varepsilon_2)=(\kappa_1+\kappa_2-m,\ \varepsilon_1+\varepsilon_2-m),\qquad m=\min(\varepsilon_1,\kappa_2),$$
which is the multiplication of the **bicyclic monoid**, a classical object of semigroup theory. So $w\mapsto(K(w),E(w))$ is a homomorphism from the free monoid of words to a direct sum of bicyclic monoids, one for each prime. We did not find this law stated in the earlier ASUNNS notes, the algebraic and topological extension papers, or by a text search of the monograph; it is an immediate consequence of the minimal source and endpoint criterion used in all of them. The recurrence T03 is the case in which $v$ is a single letter.

**Corollary 1.** $\gcd(K(uv),E(uv))=\gcd\big(K(u)K(v),E(u)E(v)\big)/d$. If moreover $\gcd(K(u),E(u))=\gcd(K(v),E(v))=1$, then
$$\gcd(K(uv),E(uv))=\gcd(K(u),E(v)).$$

*Proof.* The first identity is clear. For the second take one prime. At most one of $\kappa_i,\varepsilon_i$ is non-zero for each $i$; in each of the possible cases $\min(\kappa_1+\kappa_2,\varepsilon_1+\varepsilon_2)-\min(\varepsilon_1,\kappa_2)=\min(\kappa_1,\varepsilon_2)$. $\square$

**Corollary 2 (block factorization).** Let $J_s=\mu*{\rm id}^s$ and, for $\sigma>\frac12$,
$$A_m(e;s)=\sum_{|u|=m,\;e\mid E(u)}E(u)^{-s},\qquad B_n(e;s)=\sum_{|v|=n,\;e\mid K(v)}E(v)^{-s}.$$
Then
$$G_{m+n}(s)=\sum_{e\ge1}J_s(e)\,A_m(e;s)\,B_n(e;s),$$
and consequently $G_{m+n}(\sigma)\ge G_m(\sigma)\,G_n(\sigma)$ for real $\sigma$.

*Proof.* $E(uv)^{-s}=E(u)^{-s}E(v)^{-s}d^s$ and $d^s=\sum_{e\mid d}J_s(e)$. For absolute convergence, $\sum_{e\mid d}|J_s(e)|\le\tau(d)d^{\sigma}$, so the double series is dominated by $\sum E(uv)^{-\sigma}\tau(d)$, and $\tau(d)\ll_\eta E(u)^{\eta}\le E(uv)^{\eta}$ because $E$ does not decrease when letters are appended. Fixed-depth series converge for $\sigma>\frac12$ (T12). For real $\sigma>0$ all $J_\sigma(e)$ are non-negative and the term $e=1$ is $G_m G_n$; for $\sigma\le\frac12$ both sides are infinite. $\square$

# 2. The middle-word overlap (ANS-T46r)

**Theorem.** For a middle word $xy$ with $g=\gcd(y,(x+1)^2)$, $K=xy/g$ and $E=(x+1)^2(y+1)^2/g$:

(i) $\gcd(K,E)=\gcd\big(x,(y+1)^2\big)$.

(ii) With $L_0=L(0,0)=1+c_0$, for all $u,v\ge0$,
$$\frac{L(u,v)}{L_0}=\frac{L(u,0)}{L_0}\,\frac{L(0,v)}{L_0}+\frac{(1-z^v)(1+z)\,\big[\Phi(p^u)c_0-c_u\big]}{L_0^2}.$$

*Proof.* (i) is Corollary 1 for two single letters, since $\gcd(x,(x+1)^2)=1$. (ii) Here $L(u,0)=\Phi(p^u)+c_u$ and $L(0,v)=1+z-z^{v+1}+z^vc_0$. Expanding $L_0L(u,v)-L(u,0)L(0,v)$, the terms $\Phi(p^u)(1+z-z^{v+1})$ and $z^vc_0c_u$ cancel and what remains is $(\Phi(p^u)c_0-c_u)(1+z-z^{v+1}-z^v)$. $\square$

The correction vanishes if $u=0$ or $v=0$. Hence in $\Omega(K,E)$ it can occur only at primes dividing $\gcd(x,(y+1)^2)$: the weight splits into a factor depending on $K$, a factor depending on $E$, and a correction carried by the single backward overlap of the two middle letters. The correction need not be small prime by prime: for $u$ odd and $v\ge1$ its leading term contains $-z^2$.

# 3. The local mechanism at one third (ANS-T46s, T46t)

## 3.1 Role measures

Fix a prime $p$, put $x=p^{-2/3}$, $y=1/p$, $z=p^{-1/3}$. A letter $N$ has the two coprime coordinates $a=N+1$ and $N$. A **role pattern** $R\in\{{\sf S},{\sf R}\}^k$ gives each letter a dominant coordinate: $a$ for a supplying letter ${\sf S}$, $N$ for a receiving letter ${\sf R}$. Under the measure $\mathbb P_R$ the letters are independent, and for each letter

- the dominant coordinate has $p$-valuation $j\ge1$ with probability $(1-x)x^j$;
- the other coordinate has valuation $j\ge1$ with probability $(1-x)y^j$;
- otherwise both valuations are $0$.

(The three cases have total probability $1$ for every $p$.) Let $T$ be the $p$-valuation of the total gcd $G$ of the word and put
$$\mathcal E_R(p)=\mathbb E_R\big[p^{T/3}\big],\qquad L(R)=\#\{i<j:R_i={\sf S},\,R_j={\sf R}\}.$$

## 3.2 The local theorem

**Theorem (T46s-i).** $\mathcal E_R(p)=1+L(R)/p+O_k(p^{-4/3})$. Consequently
$$C_R=\prod_p\Big(1-\frac1p\Big)^{L(R)}\mathcal E_R(p)$$
converges absolutely and $C_R>0$.

*Proof.* Let $\alpha$ be the sum of the positive valuations of the coordinates $a$ over all letters and $\beta$ that of the coordinates $N$. Since $G$ divides both $\prod a^2$ and $\prod N$, $T\le\min(2\alpha,\beta)$, and $T=0$ unless $p\mid a_i$ and $p\mid N_j$ for some $i<j$. A configuration of exact valuations, of total non-dominant valuation $h$, has probability times $p^{T/3}$ at most $p^{-F}$, where
$$F=\tfrac23(\alpha+\beta)+\tfrac13h-\tfrac13\min(2\alpha,\beta).$$
Take $\alpha,\beta\ge1$. If $\beta\le2\alpha$ then $F\ge(2\alpha+\beta)/3\ge\frac43$ unless $\alpha=\beta=1$. If $\beta>2\alpha$ then $F\ge\frac23\beta\ge2$. Also $F\ge(\alpha+\beta)/3$, and the number of configurations with given $\alpha,\beta$ is polynomial in $\alpha+\beta$. So all configurations with $(\alpha,\beta)\ne(1,1)$ contribute $O_k(p^{-4/3})$ to $\mathbb E_R[p^{T/3}-1]$. If $\alpha=\beta=1$ and $h\ge1$ then again $F\ge\frac43$. There remain one letter with $v_p(a)=1$ and a different letter with $v_p(N)=1$, both dominant, all other valuations $0$. Then $T=1$ exactly when the first precedes the second, which happens for $L(R)$ pairs. Each such pair contributes
$$(p^{1/3}-1)\,(1-x)^2x^2\,\big(1+O_k(p^{-2/3})\big)=p^{-1}+O_k(p^{-4/3}).$$
This proves the expansion. Then $(1-1/p)^{L(R)}\mathcal E_R=1+O_k(p^{-4/3})$, and every factor is positive. $\square$

So the pole order at one third has a local origin: each admissible link of the pattern contributes $1/p$, and everything else at that prime is smaller.

## 3.3 The end letters give $L(u,v)$

**Lemma.** Let $R$ begin with ${\sf S}$ and end with ${\sf R}$, and let $(u,v)=(v_pK,v_pE)$ for the middle word. The expectation over the first and last letters of $p$ raised to one third of the two gcd exponents that involve them equals $L(u,v)$.

*Proof.* Only $\alpha=v_p(a_1)$ and $\beta=v_p(N_k)$ enter, each equal to $j$ with probability $(1-x)x^j$. By T47 the exponents are $m=\min(2\alpha,u)$ and $\min(w,\beta)$ with $w=v+2\alpha-m$. Summation over $\beta$ gives $1+z-z^{w+1}$. Next, $\mathbb E\,z^{-m}=\Phi(p^u)$. Hence the result is
$$(1+z)\,\Phi(p^u)-z^{v+1}B_u,\qquad B_u=(1-z^2)\sum_{\alpha\ge0}z^{4\alpha-2\min(2\alpha,u)}.$$
Summing the two ranges $2\alpha\le u$ and $2\alpha>u$ gives, for $u=2n$, $B_u=(n+1)(1-z^2)+z^4/(1+z^2)$ and, for $u=2n+1$, $B_u=(n+1)(1-z^2)+z^2/(1+z^2)$. In both cases $B_u=\Phi(p^u)-c_u/z$. $\square$

This gives the function $L$ of v013 a direct meaning.

## 3.4 Agreement with every proved leading coefficient

**Theorem (T46s-ii).** For $k=2,3$, with $\ell_k=\lfloor k^2/4\rfloor$,
$$\lim_{s\to1/3}\big(s-\tfrac13\big)^{\ell_k}G_k(s)=\zeta(\tfrac23)^k\,3^{-\ell_k}\sum_{L(R)=\ell_k}C_R.\qquad(\ast)$$

*Proof.* $k=2$: $\mathcal E_{\sf SR}=L_0$ and $(1-1/p)L_0=1-(z^5+z^6)/(1+z^2)$, the factor of $H(\frac13)$. So $(\ast)$ reads $\zeta(\frac23)^2H(\frac13)/3$, which is T45.

$k=3$: for ${\sf SRR}$ the middle letter has state $(j,0)$ with probability $(1-x)x^j$ and $(0,2j)$ with probability $(1-x)y^j$, $j\ge1$, and no gcd of its own. With $W_1(t)=\sum_jt^jL(j,0)/L_0$ and $W_2(t)=\sum_jt^jL(0,2j)/L_0$ one finds
$$(1-y)\,\mathcal E_{\sf SRR}=L_0\,(1-x)\big[(1-y)W_1(x)+(1-y)W_2(y)-1\big]=L_0\,E_{1,p},$$
with $E_{1,p}$ as in v012. For ${\sf SSR}$ the states are $(0,2j)$ with weight $x^j$ and $(j,0)$ with weight $y^j$, which gives $L_0E_{2,p}$. Hence $C_{\sf SRR}+C_{\sf SSR}=H(\frac13)(E_1+E_2)$. The limit proved in v012 is $\zeta(\frac23)^3H(\frac13)(E_1+E_2)/9$. $\square$

**Theorem (T46s-iii).** In the model $F_{r,t}$ of T46o, let the letters be independent with only their dominant coordinate, of law $(1-x)x^j$, and let $T=\min\big(2\sum\alpha_i,\sum\beta_j\big)$. Then
$$\lim_{s\to1/3}\big(s-\tfrac13\big)^{rt}F_{r,t}(s)=\zeta(\tfrac23)^{r+t}\,3^{-rt}\prod_p\Big(1-\frac1p\Big)^{rt}\mathbb E\big[p^{T/3}\big].$$

*Proof.* By T46o the limit is $\zeta(\frac23)^{r+t}3^{-rt}Q_0(\frac13)$, where $Q_0(\frac13)=\prod_p(1-1/p)^{rt}E_p(0)$ and
$$E_p(0)=\sum_{v\ge0}J_s(p^v)\,z^{2\lceil v/2\rceil}g_r(p^{\lceil v/2\rceil})\cdot z^{2v}g_t(p^v),\qquad s=\tfrac13.$$
Here $z^{2h}g_r(p^h)=\Pr(\sum\alpha_i\ge h)$ and $z^{2v}g_t(p^v)=\Pr(\sum\beta_j\ge v)$, because a sum of $r$ geometric variables has the negative binomial law. So $E_p(0)=\sum_vJ_s(p^v)\Pr(v\le T)=\mathbb E\big[p^{sT}\big]$. $\square$

## 3.5 The general coefficient

**Conjecture (T46t).** Formula $(\ast)$ holds for every $k\ge2$: the maximal patterns are ${\sf S}^{k/2}{\sf R}^{k/2}$ for even $k$, and the two patterns with block lengths $\frac{k\pm1}2$ for odd $k$.

Because $C_R>0$, the conjecture includes the conjectured exact order $\ell_k$ (T46q, T46b) and predicts the sign $(-1)^k$. At depth four it predicts a single pattern ${\sf SSRR}$ and
$$\lim_{s\to1/3}\big(s-\tfrac13\big)^4G_4(s)\approx0.014596 .$$
This number is a numerical evaluation of a conjectured formula, not a computed property of $G_4$.

**What supports it, and what does not.** It is proved for $k=2,3$, and its analogue is proved for every pole order $rt$ in the model. But the model omits exactly the interactions that make $k\ge4$ hard, and at $k\ge4$ nothing independent of the formula has been checked.

| quantity | formula, Euler product (numerical) | independent value |
|:--------------------|---------------------:|----------------------:|
| $k=2$ | $0.839436$ | proved identity |
| $k=3$ | $-0.759179$ | $-0.759164$ (v012) |
| $F_{2,2}$ | $0.0068451$ | $0.0068448$ (v013) |
| $k=4$ | $0.014596$ | none |

The differences are of the size of the truncation error of the numerical products.

# 4. Depth four: where the attempted routes stop

This section records an assessment. It is not a theorem, and it does not show that no route exists.

- **Reduction that works formally.** Expanding the links $13,14,23,24$ of the pattern ${\sf SSRR}$, and the internal links $12,34$, into divisor variables makes the sums over letters independent progression sums once the divisors are fixed; the link $14$ involves only the end letters.
- **First obstruction.** When the divisor attached to the link $23$ between the two middle letters is large compared with the others, one needs the joint distribution of two modular inverses weighted by a product of two singular weights. Applying the one-variable counting estimate of v011 to each separately and combining the bounds gives a convergent estimate only for $2\sigma<\frac12$, which excludes $\sigma=\frac13$.
- **Second obstruction.** The irregular term in which a letter equals the divisor is not negligible (it has size $d^{-2/3}$), so the divisor must also be averaged.
- **A smaller problem.** Dropping the link $34$ leaves two receivers and only one letter in a mixed position; the order should still be four. Even this needs an equidistribution estimate for modular inverses weighted by a divisor function, a weighted form of T46j. With a sharp cut-off the error terms we obtain are too large at $\sigma=\frac13$.

A reasonable next target is that weighted estimate. Until it or a substitute is available we do not claim a route to $M_4$ and $R_4$.

# 5. The unrestricted history function: growth at $s=1$ (ANS-T48)

The unrestricted function is $\sum_kG_k(s)t^k$. For $s>1$ one has $G_k(s)^{1/k}\to B(s)$ (v001, Theorem 4.4). For $\frac12<s\le1$ it was shown that the radius of convergence in $t$ is zero (v001). The following gives the rate.

**Theorem.** (i) As $k\to\infty$,
$$\log k-\log\log k+O(1)\ \le\ G_k(1)^{1/k}\ \le\ \big(e^{\gamma}\zeta(2)+o(1)\big)\log k .$$
(ii) For $\frac12<s<1$ and large $k$, $G_k(s)^{1/k}\ge c_s\,k^{1-s}$.

## 5.1 Lower bounds

**Lemma 1.** For letters $N\le M$ with law proportional to $r_N^{-a}$, $\frac12\le a\le1$, there is an absolute $\eta>0$ with $\mathbb E_Me^{-\eta X_p}\le1$ for every prime $p$, where $X_p=2v_p(N+1)-v_p(N)$.

*Proof.* If $p>M+1$ then $X_p=0$; if $p=M+1$ then $X_p\ge0$. Let $p\le M$ and follow v002, Lemma B, with $\pi_j=\Pr(v_p(N+1)\ge j)$. Step (i) there uses only that the weight decreases. In step (ii) the ratio of the weights of $p^jm-1$ and $pm-1$ is at most $(2p^{1-j})^a$, which for $\frac12\le a\le1$ is at most $2\cdot2^{-(j-1)/2}$. Hence $\pi_j\le2\cdot2^{-(j-1)/2}\pi_1$. The same Taylor inequality gives
$$\mathbb E_Me^{-\eta X_p}-1\le\pi_1\big(-\eta+C\eta^2\big),\qquad C=\sum_{j\ge1}j^2\Big(\tfrac12e^{j/10}+2\Big)2^{1-(j-1)/2},$$
for $\eta\le\frac1{10}$; the series converges since $e^{1/10}<\sqrt2$. Take $\eta=\min(\frac1{10},1/C)$. $\square$

*Proof of the lower bounds.* Restrict to letters $N\le M$ and let $B_M(s)=\sum_{N\le M}r_N^{-s}$. By Jensen,
$$G_k(s)\ge B_M(s)^k\,\mathbb E_M K_k^{-s}\ge B_M(s)^k\exp\big(-s\,\mathbb E_M\log K_k\big).$$
Only primes $p\le M$ divide $K_k$. By v003, Lemma 1, $v_p(K_k)=\max_{j\le k}(-S_p(j))$; Lemma 1 and Ville's inequality give $\Pr(v_p(K_k)\ge r)\le e^{-\eta r}$. So $\mathbb E\,v_p(K_k)\le1/(e^{\eta}-1)$ and $\mathbb E\log K_k\ll\theta(M)\ll M$, uniformly in $k$. Therefore
$$G_k(s)^{1/k}\ge B_M(s)\exp\big(-O(M/k)\big).$$
For $s=1$ take $M=\lfloor k/\log k\rfloor$: $B_M(1)=\log M+O(1)$ and the exponential is $1-O(1/\log k)$. For $s<1$ take $M=k$: $B_k(s)\gg_s k^{1-s}$. $\square$

## 5.2 Upper bound

Let $F_n(a,b)=\sum_{|w|=n}Q(w)^{-a}K(w)^{-b}$, so $G_k(1)=F_k(1,1)$.

**Lemma 2.** Let $\epsilon=1/(k\log^2k)$ and $1-k\epsilon\le a\le1$. Then for all $n\ge1$, uniformly as $k\to\infty$,
$$\sum_{d\mid n}d^{-a}\le C\,n^{\epsilon},\qquad C=(e^{\gamma}+o(1))\log k .$$

*Proof.* The left side is at most $\prod_{p\mid n}(1-p^{-a})^{-1}$ and $n\ge\prod_{p\mid n}p$, so one may take $\log C=\sum_p\max\big(0,\,-\log(1-p^{-a})-\epsilon\log p\big)$. Put $P=1/\epsilon$. For $p>P$ we have $p^{-a}\le P^{-a}=\epsilon\,(1+o(1))$ and $\epsilon\log p\ge\epsilon\log P$, so these terms vanish for large $k$. For $p\le P$, $(1-a)\log P\to0$, whence
$$\sum_{p\le P}-\log(1-p^{-a})=\sum_{p\le P}-\log\Big(1-\frac1p\Big)+O\Big((1-a)\sum_{p\le P}\frac{\log p}p\Big)=\sum_{p\le P}-\log\Big(1-\frac1p\Big)+o(1).$$
Mertens' theorem and $\log P=(1+o(1))\log k$ finish the proof. $\square$

*Proof of the upper bound.* Appending $N$ multiplies $Q$ by $r_N$ and $K$ by $N/g$, $g=\gcd(E(w),N)$. Since $r_N^{-a}\le N^{-a}$, for $a+b>1$,
$$\sum_Nr_N^{-a}\Big(\frac gN\Big)^b\le\sum_{d\mid E(w)}J_b(d)\sum_{d\mid N}N^{-a-b}\le\zeta(a+b)\sum_{d\mid E(w)}d^{-a}.$$
With $E=QK$ and Lemma 2 this gives
$$F_{n+1}(a,b)\le\zeta(a+b)\,C\,F_n(a-\epsilon,b-\epsilon).$$
Apply it $k$ times starting from $a=b=1$. All exponents stay at least $1-k\epsilon=1-1/\log^2k$, so each $\zeta(a+b)=\zeta(2)+o(1)$, and $F_0=1$. $\square$

## 5.3 What this says, and what it does not

At $s=1$ the population of depth $k$ grows like $(c\log k)^k$ with $c$ between $1+o(1)$ and $e^{\gamma}\zeta(2)+o(1)$. In particular $\sum_kG_k(1)t^k/k!$ is entire. The letters that produce the lower bound are of size about $k/\log k$: at depth $k$ the dominant restriction on letters grows with the depth. The theorem concerns real $s\le1$. It says nothing new about T33, the nature of the singularity at $\sigma_c\approx1.5464$ and the behaviour just to its left. The constant in (i) is not determined.

# 6. Computations

All in `v014_checks.py`; results in `results/`.

- `composition`: T47 and Corollary 1 on $100{,}000$ random word pairs, with $K(uv)$ also computed by the independent first-letter recursion; T46r(i) for $x,y\le400$; the bicyclic form for all valuations at most $8$. No failures.
- `overlap`: T46r(ii) symbolically for $u,v\le6$.
- `roles`: the two identities of T46s-ii at six primes (error below $2\cdot10^{-15}$); the end-letter form against enumeration of all letters for $p=11,101$; the remainder $(\mathcal E_R-1-L/p)p^{4/3}$ for all patterns up to $k=5$.
- `coefficient`, `model`: the Euler products in §3.5, with a fitted tail. Floating point, not certified.
- `drift`: $\mathbb E\,(21/20)^{-X_p}\le1$ for $49$ primes, three exponents and all $4\le M\le200{,}000$ (illustrates Lemma 1; the proof does not depend on it).
- `growth`: $G_2\ge G_1^2$ on truncated alphabets and the size of the constant in Lemma 2. The asymptotics in T48 are not verified numerically.
