# Generation

The generating operation is the nesting $M\perp N=M(N+1)^2/N$. A transition $T_N(x)=r_Nx$, $r_N=(N+1)^2/N$, is admissible at an integer $x\ge1$ exactly when $N\mid x$. A *history* is an admissible sequence $x_0\xrightarrow{N_1}x_1\to\cdots\xrightarrow{N_k}x_k$; its ordered label word is $w=(N_1,\dots,N_k)$.

Several statements hold for every *integral-image grammar*: labels $b$ with multipliers $r_b=p_b/q_b>1$, $\gcd(p_b,q_b)=1$, the step $x\mapsto r_bx$ being admissible iff $q_b\mid x$. For the nesting grammar $p_N=(N+1)^2$ and $q_N=N$. We assume the finiteness condition

**(F)** every integer is divisible by $p_b$ for only finitely many labels $b$.

The nesting grammar satisfies (F). Write $Q(w)=\prod_i r_{N_i}$ for the multiplier of a word.

## T03 · Source and endpoint evolution

**Theorem.** For every word $w$ there are integers $K(w),E(w)=K(w)Q(w)$ such that $w$ is admissible exactly from the sources $K(w)\mathbb Z_{>0}$, with endpoints exactly $E(w)\mathbb Z_{>0}$. Starting from $K=E=1$ for the empty word,
$$E(wb)=\frac{p_b\,E(w)}{\gcd(E(w),q_b)},\qquad K(wb)=\frac{q_b\,K(w)}{\gcd(E(w),q_b)} .$$
For nesting, $E(wN)=(N+1)^2E(w)/\gcd(E(w),N)$ and $K(wN)=N\,K(w)/\gcd(E(w),N)$.

*Proof.* Induction on the length. A source admits $wb$ iff it admits $w$ and the endpoint $y\in E(w)\mathbb Z_{>0}$ is divisible by $q_b$, that is $y\in L\,\mathbb Z_{>0}$ with $L=\operatorname{lcm}(E(w),q_b)$. The new endpoints are $r_by\in (p_bL/q_b)\mathbb Z_{>0}$ and $p_bL/q_b=p_bE(w)/\gcd(E(w),q_b)$. The sources are $y/Q(w)\in(L/Q(w))\mathbb Z_{>0}$, and $L/Q(w)=K(w)L/E(w)=K(w)q_b/\gcd(E(w),q_b)$. $\square$

The existence of the least source and least endpoint is monograph Lemma 4.2 for the nesting grammar; the recurrences give them letter by letter.

**Corollary (histories ending at $n$).** Let $\mathcal W(n)=\{w:E(w)\mid n\}$. Then $\mathcal W(n)$ is the set of words of histories ending at $n$,
$$\mathcal W(n)=\{\varepsilon\}\ \sqcup\bigsqcup_{b:\;p_b\mid n}\mathcal W\!\left(\tfrac{nq_b}{p_b}\right)b,$$
and under (F) it is finite.

*Proof.* The first statement is the theorem. A history ends at $n$ with last letter $b$ iff $n=r_bx$ with $q_b\mid x$, which holds for an integer $x$ iff $p_b\mid n$, and then $x=nq_b/p_b<n$. Finiteness follows by strong induction on $n$. $\square$

## T04 · Prime-coordinate evolution

**Theorem.** A nesting transition acts by $v_p(T_N(x))=v_p(x)+2v_p(N+1)-v_p(N)$. For minimal endpoints, $e_p(w)=v_p(E(w))$ satisfies
$$e_p(wN)=2v_p(N+1)+\max\{e_p(w)-v_p(N),\,0\},$$
and, with $u_i=2v_p(N_i+1)$ and $d_i=v_p(N_i)$, for $k\ge1$
$$e_p(N_1\cdots N_k)=\max_{1\le j\le k}\Big(\sum_{i=j}^{k}u_i-\sum_{i=j+1}^{k}d_i\Big).$$
For each $p$ at most one of $v_p(N)$, $v_p(N+1)$ is non-zero.

*Proof.* The first two identities are the $p$-adic valuations of $T_N(x)$ and of the recurrence of T03. For the closed form, $e_k=\max\{u_k,\;u_k-d_k+e_{k-1}\}$ with $e_1=u_1$; substituting the formula for $e_{k-1}$ gives the maximum over $j\le k-1$, and the term $u_k$ is the case $j=k$. The last statement is $\gcd(N,N+1)=1$. $\square$

# Factorization

Let $H_k(n)=\#\{w\in\mathcal W(n):|w|=k\}$ and $a_k(n)=\#\{w:|w|=k,\ E(w)=n\}$, and put
$$\mathcal G(s,t)=\sum_w\frac{t^{|w|}}{E(w)^s},\qquad \mathcal Z_H(s,t)=\sum_{n,k}\frac{H_k(n)t^k}{n^s}.$$

## T01 and T02 · History factorization and depth-resolved inversion

**Theorem.** For every integral-image grammar with (F),
$$H_k(n)=\sum_{d\mid n}a_k(d),\qquad a_k(n)=\sum_{d\mid n}\mu(d)H_k(n/d),$$
and, for $t\ne0$, $\mathcal Z_H(s,t)$ converges absolutely iff $\operatorname{Re}s>1$ and $\mathcal G(\operatorname{Re}s,|t|)<\infty$; there $\mathcal Z_H(s,t)=\zeta(s)\,\mathcal G(s,t)$.

*Proof.* Group the words of $\mathcal W(n)$ by their minimal endpoint $d\mid n$ and invert. For the series, with non-negative terms and $\sigma=\operatorname{Re}s$,
$$\sum_{n,k}\frac{H_k(n)|t|^k}{n^{\sigma}}=\sum_w|t|^{|w|}\sum_{m\ge1}\frac1{(mE(w))^{\sigma}}=\zeta(\sigma)\,\mathcal G(\sigma,|t|),$$
and the same rearrangement with complex terms gives the identity. $\square$

At $t=1$ and at the level of coefficients this is the endpoint decomposition of the monograph (Theorem 19.2); the depth grading and the analytic statement are added here.

## T14a · Factorization of all actual histories

Let $\mathcal F(s,u,t)=\sum_w t^{|w|}E(w)^{-s}K(w)^{-u}=\sum_wt^{|w|}Q(w)^{-s}K(w)^{-(s+u)}$.

**Theorem.** Summing over all actual histories, given by a source $x$ and an admissible word $w$ with endpoint $y=Q(w)x$,
$$\sum_{(x,w)}\frac{t^{|w|}}{x^{u}\,y^{s}}=\zeta(s+u)\,\mathcal F(s,u,t)$$
wherever the left side converges absolutely, which for $t\ne0$ means $\operatorname{Re}(s+u)>1$ and absolute convergence of $\mathcal F$. On the anti-diagonal, for $\operatorname{Re}s>1$ and $|t|B(\operatorname{Re}s)<1$,
$$\mathcal F(s,-s,t)=\frac1{1-t\sum_b r_b^{-s}},\qquad B(\sigma)=\sum_br_b^{-\sigma}.$$

*Proof.* By T03 the histories with word $w$ are $x=mK(w)$, $y=mE(w)$, $m\ge1$; sum over $m$ first. At $u=-s$ the weight $E^{-s}K^{s}=Q^{-s}$ is multiplicative over letters. $\square$

$\mathcal G(s,t)=\mathcal F(s,0,t)$. The factorization $\mathcal Z_H=\zeta\,\mathcal G$ is the case $u=0$. Each of these functions aggregates the records $\mathcal R(w)=(w,K(w),Q(w),E(w))$: the distinct words $(1,3)$ and $(3,1)$ both have depth $2$, $K=3$ and $E=64$, so $\mathcal F$ does not separate them although their state sequences $3\to12\to64$ and $3\to16\to64$ differ.

# Convergence of the nesting grammar

From here the grammar is the nesting grammar, $B(\sigma)=\sum_{N\ge1}\big(N/(N+1)^2\big)^{\sigma}$ (finite iff $\sigma>1$), and $B_M$ is the partial sum over $N\le M$.

## T07 · Sufficient criterion

**Theorem.** If $\operatorname{Re}s=a>1$, $\operatorname{Re}(s+u)=b\ge0$ and $|t|B(a)<1$, then $\mathcal F(s,u,t)$ converges absolutely. Also $B(2)=\zeta(2)-2\zeta(3)+\zeta(4)<1$.

*Proof.* $K(w)\ge1$, so $\sum_w|t|^{|w|}Q^{-a}K^{-b}\le\sum_k(|t|B(a))^k$. With $m=N+1$, $(m-1)^2/m^4=m^{-2}-2m^{-3}+m^{-4}$; also $B(2)<\sum_{m\ge3}m^{-2}<1$ because $r_N>N+2$. $\square$

## T15 · Source-one generation

**Lemma (every prime is reached from source 1).** For each prime $p$ there is a word $w_p$ admissible from $1$ with $p\mid Q(w_p)$.

*Proof.* Take $w_2=(1)$. For $p>2$ write $p-1=\prod q^{f_q}$ with $q<p$, and concatenate $f_q$ copies of each $w_q$. A word admissible from $1$ is admissible from every integer, so concatenations of such words are admissible from $1$ and their multipliers, which are integers, multiply. The state reached is divisible by $p-1$; applying the letter $p-1$ gives a state divisible by $p^2$. $\square$

**Lemma (saturation).** Fix $\sigma\ge0$ and $M$, and let the letters of $v=(v_1,v_2,\dots)$ be independent with law $\nu(N)=r_N^{-\sigma}/B_M(\sigma)$, $N\le M$. There is a word $w_0$, admissible from $1$, such that with probability at least $1/2$ the whole infinite word $w_0v$ is admissible from $1$.

*Proof.* For a prime $p\le M$ let $X_p(N)=2v_p(N+1)-v_p(N)$. For each power $q=p^j$, the map $N=mq\mapsto mq-1$ sends multiples of $q$ in $[1,M]$ injectively to integers $N'\in[1,M]$ with $q\mid N'+1$, and $\nu(N')\ge\nu(N)$ because $r_N$ increases. Summing over $j$ gives $\mathbb E\,v_p(N+1)\ge\mathbb E\,v_p(N)$, hence
$$\mathbb E\,X_p\ge\mathbb E\,v_p(N+1)\ge\nu(p-1)>0 .$$
The partial sums $S_p(k)=\sum_{i\le k}X_p(v_i)$ therefore tend to $+\infty$ almost surely, so there is $C$ with $\Pr\{\min_{k\ge0}S_p(k)\ge-C\ \text{for all }p\le M\}\ge1/2$. Let $D_p=\max_{N\le M}v_p(N)$ and let $w_0$ concatenate $C+D_p$ copies of $w_p$ for every $p\le M$; then $v_p(Q(w_0))\ge C+D_p$. On the event above, if the first $i-1$ letters of $v$ have been applied, the state $x$ has $v_p(x)=v_p(Q(w_0))+S_p(i-1)\ge D_p$ for every $p\le M$, so $v_i\mid x$. $\square$

The drift $\mathbb E[2v_p(N+1)-v_p(N)]>0$ is the arithmetic content: nesting by $N$ returns the square of $N+1$ for one factor of $N$, and long histories accumulate enough divisibility to admit every later letter.

## T09 · Exponential growth in depth and the sharp boundary

**Theorem.** Let $G_k(\sigma)=\sum_{|w|=k}E(w)^{-\sigma}$. Then $\lim_{k\to\infty}G_k(\sigma)^{1/k}=B(\sigma)$ for $\sigma>1$, and the limit is $+\infty$ for $0\le\sigma\le1$.

*Proof.* $E\ge Q$ gives $G_k\le B^k$. Call $v\in\{1..M\}^k$ *good* if $w_0v$ is admissible from $1$. Then $K(w_0v)=1$, so $E(w_0v)=Q(w_0v)$, and
$$G_{|w_0|+k}(\sigma)\ge Q(w_0)^{-\sigma}\sum_{v\ \mathrm{good}}Q(v)^{-\sigma}=Q(w_0)^{-\sigma}B_M(\sigma)^k\,\nu(\mathrm{good})\ge\tfrac12Q(w_0)^{-\sigma}B_M(\sigma)^k .$$
Hence $\liminf G_k^{1/k}\ge B_M(\sigma)$ for every $M$. $\square$

## T14b · The region of absolute convergence

**Theorem.** Let $t\ne0$, $a=\operatorname{Re}s$ and $b=\operatorname{Re}(s+u)$.

1. If $a\le1$, or if $a>1$ and $|t|B(a)>1$, then $\mathcal F(s,u,t)$ does not converge absolutely, for any real $b$.
2. If $b\ge0$, $a>1$ and $|t|B(a)<1$, it converges absolutely.
3. The series over all actual histories in T14a converges absolutely if $b>1$, $a>1$, $|t|B(a)<1$; it does not if $b\le1$, or $a\le1$, or $a>1$ and $|t|B(a)>1$.

*Proof.* (1) For $a\ge0$ choose $M$ with $|t|B_M(a)>1$; this is possible in both cases since $B_M(a)\to\infty$ for $a\le1$. The words with $K=1$ carry no factor of $b$, and the estimate of T09 shows that their contribution already diverges. For $a<0$ each term is at least the corresponding term at $a=0$. (2) is T07. (3) combines (1), (2) and the factor $\zeta(b)$. $\square$

The source weight $K^{-b}$, $b\ge0$, therefore does not move the exponential boundary. The surface $|t|B(a)=1$ itself is not decided here.

**Corollary (abscissa).** $\mathcal G(s,1)$ and $\mathcal Z_H(s,1)$ have abscissa of absolute convergence $\sigma_c$, the unique root of
$$\sum_{N\ge1}\Big(\frac{N}{(N+1)^2}\Big)^{\sigma_c}=1,\qquad\sigma_c=1.5463810\ldots$$
Because the coefficients are non-negative, $s=\sigma_c$ is a singular point of both series (Landau).

*Proof.* $B$ decreases continuously from $+\infty$ (as $\sigma\to1^+$) to $B(2)<1$. Apply T14b with $u=0$, and T01. Since $\sigma_c>1$, the factor $\zeta(s)$ does not change the abscissa. The decimal value is a floating-point evaluation with an explicit two-sided tail bound. $\square$

## T10 and T15 · Growth of generative histories

For a source $x$ let $N_x(X)$ be the number of histories from $x$ with endpoint at most $X$. Let $A(X)=\#\{w:E(w)\le X\}$ and $C(X)=\sum_{n\le X}\#\mathcal W(n)$.

**Theorem.** For every source $x\ge1$,
$$\lim_{X\to\infty}\frac{\log N_x(X)}{\log X}=\lim\frac{\log A(X)}{\log X}=\lim\frac{\log C(X)}{\log X}=\sigma_c .$$

*Proof.* Upper bounds: for $\sigma>\sigma_c$, $N_x(X)$ and $A(X)$ are at most $\#\{w:Q(w)\le X\}\le\sum_w(X/Q(w))^{\sigma}=X^{\sigma}/(1-B(\sigma))$, and $C(X)=\sum_{E(w)\le X}\lfloor X/E(w)\rfloor\le X^{\sigma}\mathcal G(\sigma,1)$.

Lower bounds: words admissible from $1$ are admissible from $x$ and have $E=Q$, so $N_x(X)\ge N_1(X/x)$ and $N_1(X)\le A(X)\le C(X)$. Fix $\alpha<\sigma_c$, choose $M$ with $B_M(\alpha)>1$, and let $\alpha_M\in(\alpha,\sigma_c)$ solve $B_M(\alpha_M)=1$. Take $\nu$ at $\sigma=\alpha_M$, let $\lambda=\sum_{N\le M}\nu(N)\log r_N>0$, fix $\varepsilon\in(0,1/2)$ and put $k=\lfloor(1-\varepsilon)\log X/\lambda\rfloor$. By the law of large numbers, with probability tending to $1$ a word $v$ of length $k$ satisfies $(1-2\varepsilon)\log X\le\log Q(v)\le(1-\varepsilon/2)\log X$. By saturation, for large $X$ the words that are also good have probability at least $1/3$. Each such $v$ has $\nu(v)=Q(v)^{-\alpha_M}\le X^{-(1-2\varepsilon)\alpha_M}$, so there are at least $X^{(1-2\varepsilon)\alpha_M}/3$ of them, and $Q(w_0v)\le X$ for large $X$. Let $\varepsilon\to0$ and $\alpha\to\sigma_c$. $\square$

In words: the forward history tree of any single integer, already that of $1$, grows with the same exponent as the whole architecture, and that exponent is fixed by the nesting multipliers.

# Fixed depth

## T12 · Convergence at fixed depth

**Theorem.** Let $k\ge1$, $a>0$, $b\ge0$ and $F_k(a,b)=\sum_{|w|=k}Q(w)^{-a}K(w)^{-b}$. Then $F_k(a,b)<\infty$ iff $a+b>1$ when $b>0$, and iff $a>1$ when $b=0$. In particular $G_k(\sigma)=F_k(\sigma,\sigma)$ has abscissa exactly $1/2$ for every $k\ge1$.

*Proof.* For $b=0$, $F_k=B(a)^k$. Let $b>0$. Divergence for $a+b\le1$: the words $(N,1,\dots,1)$ have $K=N$ and $Q=r_N4^{k-1}$, so their terms are of order $N^{-a-b}$. Convergence: by T03, $K(wN)=K(w)N/g$ with $g=\gcd(E(w),N)$, and $r_N\ge N$, so
$$\sum_Nr_N^{-a}\Big(\frac gN\Big)^{b}\le\sum_N\frac{g^{b}}{N^{a+b}}\le\sum_{d\mid E(w)}d^{b}\sum_{d\mid N}N^{-a-b}=\zeta(a+b)\sum_{d\mid E(w)}d^{-a}\le\zeta(a+b)\,\tau(E(w)).$$
Since $\tau(E)\le C_\eta E^{\eta}=C_\eta Q^{\eta}K^{\eta}$, we get $F_{k+1}(a,b)\le C_\eta\,\zeta(a+b)\,F_k(a-\eta,b-\eta)$. Choose $\eta$ small compared with $a/k$, $b/k$ and $(a+b-1)/(2k)$ and induct from $F_0=1$. $\square$

Every single depth converges down to $1/2$, while the sum over depths stops at $\sigma_c>3/2$: the boundary is produced by the accumulation of depth. In the interval $1/2<\sigma\le1$ all coefficients of $\mathcal G(\sigma,t)$ are finite and its radius of convergence in $t$ is zero.

## T05 and T13 · Depth two

**Theorem.** $G_1(s)=\zeta(2s)-1$ and
$$G_2(s)=\sum_{a,b\ge1}\left[\frac{\gcd((a+1)^2,b)}{(a+1)^2(b+1)^2}\right]^{s}.$$
With $J_s(d)=\sum_{e\mid d}\mu(e)(d/e)^s$, $c(d)=\prod_pp^{\lceil v_p(d)/2\rceil}$ and the Hurwitz zeta function $\zeta(\cdot,\cdot)$,
$$G_2(s)=\sum_{d\ge1}\frac{J_s(d)}{d^{2s}}\,\zeta\!\left(2s,1+\tfrac1d\right)\Big(\frac{\zeta(2s)}{c(d)^{2s}}-[d=1]\Big).$$
The right side continues $G_2$ meromorphically to $\operatorname{Re}s>1/3$ with a single pole, at $s=1/2$, of order two, and $G_2(s)\sim\dfrac{\kappa}{4(s-1/2)^2}$, where
$$\kappa=\prod_p\Big(1+(1-p^{-1/2})\sum_{j\ge1}p^{-j/2-\lceil j/2\rceil}\Big)\approx1.8536 .$$
Consequently the number of depth-two words with minimal endpoint at most $X$ satisfies
$$A_2(X)\sim\frac{\kappa}{2}\sqrt X\log X .$$

*Proof.* The double sum is T03. Expand $\gcd(\cdot,\cdot)^s=\sum_{d\mid\gcd}J_s(d)$. Here $d\mid m^2$ iff $c(d)\mid m$, so $\sum_{m\ge2,\,d\mid m^2}m^{-2s}=c(d)^{-2s}\zeta(2s)-[d=1]$, and $\sum_{d\mid b}(b+1)^{-2s}=d^{-2s}\zeta(2s,1+1/d)$. Since $|J_s(d)|\le d^{\sigma}2^{\omega(d)}$, the rearrangement is dominated by a constant times $\sum_d2^{\omega(d)}d^{-\sigma}c(d)^{-2\sigma}$, whose Euler factor is $1+2\sum_{j\ge1}p^{-\sigma(j+2\lceil j/2\rceil)}$. The leading exponent is $3\sigma$, so this converges for $\sigma>1/3$. The functions $\zeta(2s,1+1/d)$ are uniformly bounded on compact sets avoiding $s=1/2$, which gives the continuation; multiplying by $(s-1/2)^2$ gives locally uniform convergence at $s=1/2$. There $(s-\tfrac12)\zeta(2s,\alpha)\to\tfrac12$, hence $(s-\tfrac12)^2G_2(s)\to\tfrac14\sum_dJ_{1/2}(d)/(d\,c(d))=\kappa/4$, and the sum factorizes over primes. The coefficients of $G_2$ are non-negative and $G_2$ has no other singularity on $\operatorname{Re}s=1/2$, so Delange's Tauberian theorem gives the asymptotic. $\square$

The constant $\kappa$ is the mean value of $\sqrt{\gcd((a+1)^2,b)}$ over independent profinitely uniform labels $a,b$: it measures the arithmetic coupling of two successive nestings.

# Factorization obstructions and other grammars

## T06 · No ordinary Euler product

**Theorem.** Neither $H(n)=\#\mathcal W(n)$ nor $a(n)=\sum_ka_k(n)$ is multiplicative; hence neither $\mathcal Z_H(s,1)$ nor $\mathcal G(s,1)$ is a product over primes of series in $p^{-s}$.

*Proof.* $\mathcal W(4)=\{\varepsilon,(1)\}$, $\mathcal W(9)=\{\varepsilon,(2)\}$ and $\mathcal W(36)$ has six elements, so $H(36)=6\ne H(4)H(9)$. If $a$ were multiplicative, so would be $H=1*a$. $\square$

For $k\ge1$, $H_k(1)=0$, so no $H_k$ is multiplicative; explicit coprime witnesses are listed with the computations.

## T08 · Grammars with unit denominators

**Theorem.** If every $q_b=1$ then $E(w)=Q(w)$ and $\mathcal G(s,t)=1/(1-t\sum_bp_b^{-s})$ wherever $|t|\sum_bp_b^{-\operatorname{Re}s}<1$. For the labels $\{2,3\}$, $\mathcal G(s,t)=1/(1-t(2^{-s}+3^{-s}))$, absolutely convergent iff $|t|(2^{-\sigma}+3^{-\sigma})<1$, with meromorphic continuation to the whole plane.

*Proof.* Every word is admissible from $1$; expand the geometric series. $\square$

## T11 (partial) · A saturation criterion for general grammars

**Theorem.** Let $G$ be an integral-image grammar with (F), $S$ a finite set of labels, $\sigma\ge0$ and $B_S(\sigma)=\sum_{b\in S}r_b^{-\sigma}$. Suppose that for every prime $p$ dividing some $q_b$, $b\in S$,
$$\sum_{b\in S}r_b^{-\sigma}\big(v_p(p_b)-v_p(q_b)\big)>0 .$$
Then $\liminf_kG_k(\sigma)^{1/k}\ge B_S(\sigma)$. If such sets exist with $B_S(\sigma)$ arbitrarily close to $B(\sigma)$ (or arbitrarily large when $B(\sigma)=\infty$), then $\lim G_k(\sigma)^{1/k}=B(\sigma)$.

*Proof.* Let letters be independent with law $r_b^{-\sigma}/B_S$. By T03, $v_p(E(wb))\ge v_p(E(w))+v_p(p_b)-v_p(q_b)$, and the increments have positive mean. As in the saturation lemma there is $C$ such that all relevant partial sums stay above $-C$ with probability at least $1/2$. By the law of large numbers some word $w_0$ over $S$ has $v_p(E(w_0))\ge C+\max_{b\in S}v_p(q_b)$ for all these $p$. For a good continuation $v$ every gcd in T03 is the full denominator, so $E(w_0v)=E(w_0)Q(v)$, and the estimate of T09 applies. The upper bound is $E\ge Q$. $\square$

The condition holds for nesting with $S=\{1..M\}$, for $x\mapsto x(N+1)^3/N$ by the same injection, and vacuously when every $q_b=1$. It cannot be dropped: for the two multipliers $3/2$ and $9/4$ each numerator is odd, so $E(wb)=p_bE(w)$ and $\mathcal G=1/(1-t(3^{-s}+9^{-s}))$. Its boundary at $t=1$ is $\sigma\approx0.4380$, far below the root $\sigma\approx1.1868$ of $(2/3)^{\sigma}+(4/9)^{\sigma}=1$.
