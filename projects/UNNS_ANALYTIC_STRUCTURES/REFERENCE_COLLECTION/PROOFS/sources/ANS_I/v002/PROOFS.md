# ANS-I v002 — Critical admissibility: proofs

Research notes. Builds on ANS-I v001 (`../v001/PROOFS.md`), which is unchanged.

## Notation
Nesting grammar $T_N(x)=x(N+1)^2/N$, $N\mid x$; $r_N=(N+1)^2/N\ge4$; for a word $w$: least source $K(w)$, multiplier $Q(w)$, least endpoint $E=KQ$, with
$$E(wN)=\frac{(N+1)^2E(w)}{\gcd(E(w),N)},\qquad K(wN)=\frac{N\,K(w)}{\gcd(E(w),N)}.\qquad(0)$$
For $a>1$ let $B(a)=\sum_N r_N^{-a}$ and let $\nu_a(N)=r_N^{-a}/B(a)$. Letters $N_1,N_2,\dots$ are independent with law $\nu_a$; $E_k,K_k,Q_k$ refer to the first $k$ of them. $\sigma=\sigma_c$ is the root of $B=1$, and $\nu_c=\nu_\sigma$. Constants $c,C$ are positive and depend only on $a$.

## 1. Critical representation (T16)
Since $\Pr(N_1\cdots N_k=w)=Q(w)^{-a}/B(a)^k$ and $E=KQ$,
$$\frac{G_k(a)}{B(a)^k}=\mathbb E\,K_k^{-a};\qquad G_k(\sigma)=\mathbb E_{\nu_c}K_k^{-\sigma}.$$

## 2. Obstruction and divergence of sources (T17, T18)
**Lemma A.** For a set $S$ of primes put $D(S)=\{N:\exists p\in S,\ p\mid N\}$ and $U(S)=\{N:\exists p\in S,\ p\mid N+1\}$. Then $\nu_a(U(S))\le2^a\nu_a(D(S))$.

*Proof.* $N\mapsto N+1$ maps $U(S)$ injectively into $D(S)$, and $\nu_a(N)/\nu_a(N+1)=(r_{N+1}/r_N)^a\le2^a$, because $r_{N+1}/r_N=N(N+2)^2/(N+1)^3\le2$. $\square$

**Theorem (T17).** An infinite $\nu_a$-random word is almost surely not admissible from any given integer $x$.

*Proof.* Choose a prime $p$ not dividing the current state and wait for the first letter with $p\mid N(N+1)$; it comes almost surely. Until then $v_p$ of the state stays $0$. If that letter has $p\mid N$ it is inadmissible, and by Lemma A (with $S=\{p\}$) this has conditional probability at least $c_0=1/(1+2^a)$. Otherwise choose a new prime not dividing the state reached, and repeat. By the strong Markov property the probability of passing $j$ stages is at most $(1-c_0)^j$. $\square$

**Theorem (T18).** $K_k\to\infty$ almost surely.

*Proof.* By (0), $K_k\mid K_{k+1}$. A bounded sequence of this kind stabilizes at an integer admitting the whole infinite word. Apply T17 to each of the countably many integers. $\square$

## 3. Decay, singularity, suppression (T19–T21)
**T19.** $G_k(\sigma)\to0$ by T18, T16 and bounded convergence, while $G_k(\sigma)^{1/k}\to B(\sigma)=1$ (v001, Theorem 4.4).

**T20.** By (0), $E(wN)\ge r_NE(w)\ge4E(w)$, so $G_k(\sigma+\delta)\le4^{-k\delta}G_k(\sigma)$. Hence $\delta\,\mathcal G(\sigma+\delta,1)\le\delta\sum_k4^{-k\delta}G_k(\sigma)\to0$ since $G_k(\sigma)\to0$. A pole of order $m\ge1$ would make $\delta\,\mathcal G$ tend to a non-zero limit or to infinity; a removable point is excluded by Landau's theorem. So $\mathcal G(s,1)$ has no meromorphic continuation to a neighbourhood of $\sigma$. Theorem T22 below strengthens this.

**T21.** Every $w$ with $E(w)\le X$ gives
$$\frac{A(X)}{X^{\sigma}}=\mathbb E_{\nu_c}\sum_{k\ge0}K_k^{-\sigma}\Big(\frac{E_k}{X}\Big)^{\sigma}\mathbf 1_{E_k\le X}.\qquad(1)$$
Since $E_{k+1}\ge4E_k$, the sum is at most $C_4=(1-4^{-\sigma})^{-1}$. Fix a word with $K_k\to\infty$. Terms with $k<k_0$ tend to $0$ as $X\to\infty$, and the others sum to at most $C_4K_{k_0}^{-\sigma}$. Dominated convergence gives $A(X)=o(X^{\sigma})$. A history from $x$ with endpoint $\le X$ has $E(w)\le X$, so $N_x(X)\le A(X)$; and $C(X)=\sum_{m\le X}A(X/m)=o(X^\sigma)$ because $\sigma>1$. $\square$

## 4. Rate of decay: upper bound (T22, T23)
**Theorem.** For every $a>1$ and $b>0$ and all $k\ge2$, $\mathbb E\,K_k^{-b}\le C_b\exp(-c_b\,k^{1/a}/\log k)$.

*Proof.* **Fresh letters.** A prime *occurs* in $N$ if it divides $N(N+1)$. Call letter $i$ *fresh* if some prime occurs in it for the first time, and *successful* if such a new prime divides $N_i$. With $S_i$ the set of primes not occurring before $i$ (determined by the past), fresh means $N_i\in D(S_i)\cup U(S_i)$ and successful means $N_i\in D(S_i)$. By Lemma A, given the past and freshness, success has probability at least $c_0$.

**Success enlarges the source.** If $p\in S_i$ divides $N_i$, no earlier letter involves $p$, so by (0) $p\nmid E_{i-1}$ and $v_p(K_i)\ge v_p(N_i)\ge1$. Different successful letters supply different primes and $K_i\mid K_k$. Thus $K_k\ge2^{Z_k}$, where $Z_k$ counts successes among the first $k$ letters.

**Supermartingale.** Let $F_k$ count fresh letters and $\theta=1-c_0(1-2^{-b})<1$. Then $M_k=2^{-bZ_k}\theta^{-F_k}$ is a supermartingale with $M_0=1$: a letter that is not fresh leaves it unchanged, and for a fresh one with success probability $q\ge c_0$ the expected factor is $(1-q(1-2^{-b}))/\theta\le1$. Hence for every $J$
$$\mathbb E\,K_k^{-b}\le\mathbb E\,2^{-bZ_k}\le\Pr(F_k<J)+\theta^J\,\mathbb E\big[M_k\big]\le\Pr(F_k<J)+\theta^J .\qquad(2)$$

**Many primes appear.** Put $P=(k/\Lambda)^{1/a}$ with $\Lambda=2\cdot8^aB(a)$, let $W$ be the set of primes in $(P,2P]$ and $m=|W|\ge P/(2\log P)$ for large $k$. Each $p\in W$ has $\nu_a(p)\ge(8P)^{-a}/B(a)$, so $k\,\nu_a(p)\ge2$. The probability that no primes of a given set $T\subseteq W$ ever occur *as a letter* is $(1-\sum_{p\in T}\nu_a(p))^k\le e^{-2|T|}$. A union bound over $|T|=\lceil m/2\rceil$ shows: outside an event of probability at most $2^me^{-m}$, at least $m/2$ primes of $W$ are among the letters.

**Few of them are spoiled by large letters.** Let $Y_i$ be the number of primes of $W$ occurring in $N_i$ if $N_i>P^2$, and $Y_i=0$ otherwise. Then $e^{Y_i}\le(N_i(N_i+1))^{1/\log P}$ on $\{N_i>P^2\}$, and for large $P$
$$\mathbb E\,e^{Y_i}\le1+C\sum_{N>P^2}N^{-a+2/\log P}\le1+C'P^{2(1-a)} .$$
By independence and Markov's inequality, $\Pr(\sum_{i\le k}Y_i\ge m/4)\le\exp(C'kP^{2-2a}-m/4)=\exp(C'\Lambda P^{2-a}-m/4)\le e^{-m/8}$ for large $P$, since $2-a<1$.

**Conclusion.** Outside both events at least $m/4$ primes of $W$ occur among the first $k$ letters and only in letters $N\le P^2$. The first occurrence of such a prime is a fresh letter, and one letter $N\le P^2$ contains at most $\log(N(N+1))/\log P\le5$ primes of $W$. So $F_k\ge m/20$. Take $J=\lceil m/20\rceil$ in (2). $\square$

**Corollary (T22, the whole critical surface).** Let $a=\operatorname{Re}s>1$, $b=\operatorname{Re}(s+u)$ and $|t|B(a)=1$. Then $\mathcal F(s,u,t)$ converges absolutely iff $b>0$. In particular $\mathcal G(s,t)$ converges absolutely on the surface; $\mathcal G(\sigma,1)<\infty$.

*Proof.* The series of absolute values is $\sum_k\mathbb E\,K_k^{-b}$. It is summable for $b>0$ by the theorem, and for $b\le0$ each term is at least $1$. $\square$

**Corollary (smooth singularity).** All derivatives of $\mathcal G(s,1)$ and of $\mathcal Z_H(s,1)$ converge absolutely and uniformly on the closed half-plane $\operatorname{Re}s\ge\sigma$. Thus both functions extend to $C^\infty$ functions there, although $s=\sigma$ is a singular point. No pole, and no algebraic or logarithmic branch point that would make some derivative unbounded, can occur at $\sigma$.

*Proof.* $K\le\prod N_i\le Q$, so $\log E\le2\log Q$. By Cauchy–Schwarz and $K^{-2\sigma}\le K^{-\sigma}$,
$$\sum_{|w|=k}\frac{(\log E)^j}{E^{\sigma}}\le2^j\big(\mathbb E(\log Q_k)^{2j}\big)^{1/2}G_k(\sigma)^{1/2}\le C_jk^jG_k(\sigma)^{1/2},$$
because $\log r_N$ has all moments under $\nu_c$. The right side is summable. $\zeta$ is analytic and non-zero at $\sigma>1$. Singularity is Landau's theorem. $\square$

## 5. Rate of decay: lower bound (T23)
Fix $a>1$, $M\ge2$, and let $\nu_M$ be $\nu_a$ conditioned on $N\le M$. For a prime $p\le M$ put $V=v_p(N+1)$, $W=v_p(N)$, $X_p=2V-W$.

**Lemma B.** There is $\eta>0$, depending only on $a$, with $\mathbb E_M e^{-\eta X_p}\le1$ for all primes $p\le M$.

*Proof.* Let $\pi_j=\nu_M(V\ge j)$. (i) $N=mq\mapsto mq-1$ ($q=p^j$) increases weight, so $\nu_M(W\ge j)\le\pi_j$. (ii) $p^jm-1\mapsto pm-1$ is injective into $[1,M]$ and
$$\frac{\nu_a(p^jm-1)}{\nu_a(pm-1)}=\Big(\frac{p^jm-1}{pm-1}\,p^{2-2j}\Big)^a\le(2p^{1-j})^a\le2^a2^{1-j},$$
so $\pi_j\le2^a2^{1-j}\pi_1$. At most one of $V,W$ is non-zero, hence
$$\mathbb E e^{-\eta X_p}-1=\mathbb E(e^{\eta W}-1)+\mathbb E(e^{-2\eta V}-1)\le\mathbb E\big(e^{\eta V}+e^{-2\eta V}-2\big),$$
using (i). For $x\ge0$, $e^{x}+e^{-2x}-2\le-x+x^2(e^{x}/2+2)$. With $x=\eta V$, $\mathbb EV\ge\pi_1$, and (ii), the right side is at most $\pi_1(-\eta+C_a\eta^2)$, where $C_a=2^a\sum_jj^2(e^{j/10}/2+2)2^{1-j}$ and $\eta\le1/10$. Take $\eta=\min(1/10,1/C_a)$. Here $\pi_1>0$ because $p-1\le M$. $\square$

**Lemma C.** There is a word $w_M$, admissible from $1$, with $\log Q(w_M)\le C M\log^2M$, such that an infinite $\nu_M$-random word $v$ has $w_Mv$ admissible from $1$ with probability at least $1/2$.

*Proof.* The words $w_p$ of v001 Lemma 4.2 satisfy $L(p)=\log Q(w_p)\le3\log^2p$: check $p=2,3$; for $p\ge5$ every prime $q\mid p-1$ is at most $(p-1)/2$, and with $p-1=\prod q^{f_q}$,
$$L(p)=\sum f_qL(q)+\log\tfrac{p^2}{p-1}\le3(\log p-\log2)\log p+2\log p\le3\log^2p .$$
By Lemma B, $e^{-\eta S_p(k)}$ is a supermartingale, $S_p(k)=\sum_{i\le k}X_p(v_i)$, so by Ville's inequality $\Pr(\exists k:S_p(k)\le-r)\le e^{-\eta r}$. With $r=\lceil\log(2M)/\eta\rceil$, with probability at least $1/2$ no $p\le M$ ever has $S_p\le-r$. Let $R=r+\lceil\log_2M\rceil$ and let $w_M$ concatenate $R$ copies of $w_p$ for all $p\le M$. Then $v_p(Q(w_M))\ge R$, and on the good event the state before letter $v_i$ has $v_p\ge R+S_p(i-1)\ge\log_2M\ge v_p(v_i)$. Finally $\log Q(w_M)\le R\sum_{p\le M}3\log^2p=O(M\log^2M)$ by Chebyshev's bound for $\pi(M)$. $\square$

**Theorem (T23).** For every $a>1$ and large $k$,
$$\frac{c\,k^{1/a}}{\log k}\ \le\ -\log\frac{G_k(a)}{B(a)^k}\ \le\ C\,k^{1/a}\log^2k .$$
Hence $-\log\big(G_k(a)/B(a)^k\big)=k^{1/a+o(1)}$, and $G_k(\sigma_c)=\exp(-k^{1/\sigma_c+o(1)})$.

*Proof.* The left inequality is §4 with $b=a$. For the right one take $M=\lceil n^{1/a}\rceil$, $w_M$ from Lemma C, and $k=n-|w_M|\ge n/2$ (possible since $|w_M|\le\log Q(w_M)/\log4=o(n)$). Good continuations have $E(w_Mv)=Q(w_Mv)$, so $G_n(a)\ge\tfrac12Q(w_M)^{-a}B_M(a)^k$, and therefore
$$\frac{G_n(a)}{B(a)^n}\ge\tfrac12Q(w_M)^{-a}B(a)^{-|w_M|}\Big(\frac{B_M(a)}{B(a)}\Big)^k .$$
The first two factors are $\exp(-O(M\log^2M))$ and, as $B-B_M=O(M^{1-a})$, the last is $\exp(-O(kM^{1-a}))=\exp(-O(n^{1/a}))$. $\square$

## 6. Quantitative growth suppression (T24)
**Theorem.** With $\sigma=\sigma_c$, for each fixed source $x$ and $Z(X)$ any of $N_x(X)$, $A(X)$, $C(X)$, for large $X$,
$$\frac{c\,(\log X)^{1/\sigma}}{\log\log X}\ \le\ -\log\frac{Z(X)}{X^{\sigma}}\ \le\ C\,(\log X)^{1/\sigma}(\log\log X)^2 .$$
($C$ may depend on $x$.) Hence $Z(X)=X^{\sigma}\exp\big(-(\log X)^{1/\sigma+o(1)}\big)$.

*Proof of the upper estimate for $Z$.* Split (1) at $k_0$. The terms $k\ge k_0$ contribute at most $C_4\,\mathbb EK_{k_0}^{-\sigma}=C_4G_{k_0}(\sigma)$. For $k<k_0$ choose $a=(1+\sigma)/2$; the number of words of length $k$ with $E\le X$ is at most $\sum_{|w|=k}(X/Q)^a=X^aB(a)^k$. With $k_0=\lfloor(\sigma-a)\log X/(2\log B(a))\rfloor$ these contribute at most $k_0X^{-(\sigma-a)/2}$ to $A(X)/X^\sigma$. Apply §4 to $G_{k_0}$. This bounds $A$, hence $N_x\le A$. For $C(X)=\sum_{m\le X}A(X/m)$, use the bound for $A(X/m)$ when $m\le\sqrt X$, and $A(Y)\le CY^\sigma$ for the rest, whose total is $O(X^{\sigma-(\sigma-1)/2})$.

*Proof of the lower estimate for $Z$.* It suffices to treat $N_1$, since $N_x(X)\ge N_1(X/x)$ and $N_1\le A\le C$. Let $M=\lceil(\log X)^{1/\sigma}\rceil$, take $w_M$ from Lemma C at $a=\sigma$, and put $Y=\log X-\log Q(w_M)=\log X-o(\log X)$. Under $\nu_M$ let $\mu_M$ be the mean of $\log r_N$; its variance is bounded by some $\tau^2$ uniformly, and $\mu_M\to\mu>0$. With $h=2\tau\sqrt{2/\mu}$ and $k=\lfloor(Y-h\sqrt Y)/\mu_M\rfloor$, Chebyshev gives, with probability at least $3/4$, $Y-2h\sqrt Y-\mu_M\le\log Q(v)\le Y$. So with probability at least $1/4$ the word $v$ of length $k$ is also good. Each such $v$ has probability $Q(v)^{-\sigma}/B_M(\sigma)^k$, whence
$$N_1(X)\ge\tfrac14\,e^{\sigma(Y-2h\sqrt Y-\mu_M)}\,B_M(\sigma)^k .$$
Here $e^{\sigma Y}=X^\sigma\exp(-O((\log X)^{1/\sigma}(\log\log X)^2))$, $\sqrt Y=o((\log X)^{1/\sigma})$ because $\sigma<2$, and $B_M(\sigma)^k=\exp(-O(kM^{1-\sigma}))=\exp(-O((\log X)^{1/\sigma}))$. $\square$

## 7. Contrast with finite alphabets (T26)
**Theorem.** Let $M\ge2$, $\sigma_M$ the root of $B_M=1$, letters $N\le M$ with law $r_N^{-\sigma_M}$. Then $K_k$ stabilizes almost surely at a finite $K_\infty$; $G^{(M)}_k(\sigma_M)\downarrow c_M=\mathbb EK_\infty^{-\sigma_M}>0$; $\delta\,\mathcal G^{(M)}(\sigma_M+\delta,1)\to c_M/\mu_M>0$ as $\delta\downarrow0$; and $c_M\to0$ as $M\to\infty$.

*Proof.* For $p\le M$, (i) in Lemma B (valid for any $a\ge0$) gives $\mathbb EX_p\ge\mathbb EV>0$, so $S_p(k)\to\infty$ and $v_p(K_k)=\max\{0,\max_{i\le k}(v_p(N_i)-S_p(i-1))\}$ stabilizes. Bounded convergence gives $c_M$. Next, $\mathcal G^{(M)}(\sigma_M+\delta,1)=\sum_k\mathbb E[K_k^{-\sigma_M}E_k^{-\delta}]$, and $k^{-1}\log E_k\to\mu_M$ almost surely, so $\delta\sum_kK_k^{-\sigma_M}E_k^{-\delta}\to K_\infty^{-\sigma_M}/\mu_M$, dominated by $\delta\sum_k4^{-k\delta}$. Finally fix $a_0\in(1,\sigma_c)$. Since $\sigma_M\uparrow\sigma_c$, eventually $\sigma_M\ge a_0$, and $\sum_{|w|=k}E(w)^{-a_0}=G_k(a_0)\le B(a_0)^k<\infty$ dominates the terms of $G^{(M)}_k(\sigma_M)$. Hence for fixed $k$, $c_M\le G^{(M)}_k(\sigma_M)\to G_k(\sigma_c)$ as $M\to\infty$; and $G_k(\sigma_c)\to0$. $\square$

The $1/\delta$ statement concerns the approach along the real axis; no meromorphic continuation of the finite-alphabet function is claimed. Every finite truncation therefore blows up like $1/\delta$ at its boundary, while the complete grammar stays bounded, with all derivatives, at $\sigma_c$.
