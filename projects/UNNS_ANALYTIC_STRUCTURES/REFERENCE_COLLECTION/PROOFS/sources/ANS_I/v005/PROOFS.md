---
title: "ANS-I v005 --- The critical line and the depth-k functions"
author: "UNNS Research Collective"
date: "27 November 2026"
---

Research notes. They continue ANS-I v001--v004, which are unchanged. After review, the limiting step at the end of the proof of ANS-T32 was corrected. All results concern the nesting grammar. New proofs are pending review; no claim of priority is made, and no literature review has been done.

# Notation

Letters $N\ge1$, $r_N=(N+1)^2/N\ge4$. For a word $w=(N_1,\dots,N_k)$: least source $K(w)$, multiplier $Q(w)=\prod r_{N_i}$, least endpoint $E=KQ$, with $E(wN)=(N+1)^2E(w)/g$, $g=\gcd(E(w),N)$, and $K(wN)=NK(w)/g$ (v001). Write $G_k(s)=\sum_{|w|=k}E(w)^{-s}$ and $\mathcal G(s,t)=\sum_kt^kG_k(s)$. Each $G_k$ is holomorphic for $\operatorname{Re}s>1/2$ (ANS-T12). $B(\sigma)=\sum_Nr_N^{-\sigma}$, $B(\sigma_c)=1$, $\sigma_c=1.5463810\ldots$, and $\nu_\sigma(N)=r_N^{-\sigma}/B(\sigma)$. For a prime $p$,
$$d_p(N)=v_p(N),\qquad X_p(N)=2v_p(N+1)-v_p(N),\qquad S_p(j)=\sum_{i\le j}X_p(N_i).$$

## 0. A formula for the source

From the recurrence, $v_p(E_i)=v_p(K_i)+S_p(i)$ and $v_p(K_i)=v_p(K_{i-1})+\max\{d_p(N_i)-v_p(E_{i-1}),0\}$. Hence $v_p(K_i)=\max\{v_p(K_{i-1}),\,d_p(N_i)-S_p(i-1)\}$ and
$$v_p(K_k)=\max\Big\{0,\ \max_{1\le j\le k}\big(d_p(N_j)-S_p(j-1)\big)\Big\}.\qquad(0)$$

# 1. Continuation across the critical line (ANS-T31)

**Theorem.** There are constants $a>0$, $A>0$ such that $\sum_kG_k(s)$ converges locally uniformly in
$$\Omega^*=\{\sigma+i\tau:\ \tau\ne0,\ \sigma>\sigma_c-a\min(\tau^2,|\tau|^{-A})\}$$
(for $\sigma>\sigma_c$ this is the known absolute convergence, which holds for every $\tau$). Consequently $\mathcal G(s,1)$ has a holomorphic continuation to $\{\operatorname{Re}s>\sigma_c\}\cup\Omega^*$, and so has $\mathcal Z_H(s,1)=\zeta(s)\,\mathcal G(s,1)$. On $\Omega^*$ near the line, $|\mathcal G(s,1)|\le C\max(\tau^{-2},|\tau|^{A})$.

In particular **every point $\sigma_c+i\tau$ with $\tau\ne0$ is a regular point**. The line $\operatorname{Re}s=\sigma_c$ is not a natural boundary, and the real point $\sigma_c$, which is singular (Landau; ANS-T20), is its only singular point.

The word series itself does not converge absolutely for $\operatorname{Re}s<\sigma_c$. The continuation comes from cancellation inside each $G_k$.

## 1.1 The letters that can be exchanged

Let $R=\{1,2,3\}$, with $r_1=4$, $r_2=9/2$, $r_3=16/3$. The numbers $N(N+1)$, $N\in R$, are $2,6,12$. So for $p\ge5$ and $N\in R$, $d_p(N)=X_p(N)=0$. For $p\in\{2,3\}$,

| $N$ | $d_2$ | $X_2$ | $d_3$ | $X_3$ |
|--:|--:|--:|--:|--:|
| 1 | 0 | 2 | 0 | 0 |
| 2 | 1 | $-1$ | 0 | 2 |
| 3 | 0 | 4 | 1 | $-1$ |

Put $m_p=\min_RX_p=-1$ and $\delta_p=\max_Rd_p=1$.

## 1.2 Representation, marking and the good event

Fix an interval $I=[\sigma_c-\delta_0,\sigma_c+\delta_0]$ with $\sigma_c-\delta_0>1$, take $s=\sigma+i\tau$ with $\sigma\in I$, and let the letters be independent with law $\nu=\nu_\sigma$. Since $E^{-s}=K^{-s}Q^{-s}$,
$$G_k(s)=B(\sigma)^k\,\mathbb E\big[K_k^{-s}\,Q_k^{-i\tau}\big],\qquad|K_k^{-s}|\le1.\qquad(1)$$
Put $m=\lfloor k/2\rfloor$. Each position $i>m$ with $N_i\in R$ is *marked*, independently, with probability $\eta\in(0,1)$. Let $J$ be the set of marked positions and $\mathcal H$ the information consisting of $J$ and of all unmarked letters. Conditionally on $\mathcal H$ the marked letters are independent with law $\nu(\cdot\mid R)$, and $|J|$ is binomial with parameters $k-m$ and $\lambda=\eta\,\nu(R)$.

For $p\in\{2,3\}$ let $\hat X_p(i)=m_p$ and $\hat d_p(i)=\delta_p$ if $i\in J$, and $\hat X_p(i)=X_p(N_i)$, $\hat d_p(i)=d_p(N_i)$ otherwise. Let $L_p(j)=\sum_{i\le j}\hat X_p(i)$. The *good event*
$$\mathsf A=\{\hat d_p(j)-L_p(j-1)\le0\ \text{ for } p\in\{2,3\}\text{ and } m<j\le k\}$$
depends only on $\mathcal H$.

**Lemma 1.** On $\mathsf A$ the source $K_k$ is determined by $\mathcal H$: it does not change when the marked letters are replaced by any other letters of $R$.

*Proof.* Use (0). For $p\ge5$ a marked position has $d_p=X_p=0$ whichever letter of $R$ it carries, so no term of (0) depends on that choice. For $p\in\{2,3\}$ and $j>m$ we have $d_p(N_j)\le\hat d_p(j)$ and $S_p(j-1)\ge L_p(j-1)$, so on $\mathsf A$ the term $d_p(N_j)-S_p(j-1)$ is not positive. Hence $v_p(K_k)$ is the maximum over $j\le m$ and $0$, and those positions are unmarked. $\square$

## 1.3 Cancellation

Let
$$c(s)=\mathbb E\big[r_N^{-i\tau}\mid N\in R\big]=\frac{\sum_{N\in R}r_N^{-s}}{\sum_{N\in R}r_N^{-\sigma}} .$$
By Lemma 1, on $\mathsf A$ the only factors in (1) that depend on the marked letters are the phases $r_{N_i}^{-i\tau}$, $i\in J$. Conditioning on $\mathcal H$ gives $\big|\mathbb E[K_k^{-s}Q_k^{-i\tau}\mathbf 1_{\mathsf A}\mid\mathcal H]\big|\le|c(s)|^{|J|}$. Therefore
$$\frac{|G_k(s)|}{B(\sigma)^k}\le\mathbb E\,|c|^{|J|}+\Pr(\mathsf A^c)=\rho^{\,k-m}+\Pr(\mathsf A^c),\qquad\rho=1-\lambda(1-|c(s)|).\qquad(2)$$

## 1.4 The good event fails with exponentially small probability

For $N\sim\nu_\sigma$ the drift $\mu_p=\mathbb E X_p$ is positive: $\mathbb EX_p\ge\nu_\sigma(p-1)$ (the injection argument of v001, which applies to the whole alphabet because $r_N$ increases). It is therefore bounded below on $I$. Since $|X_p(N)|\le3\log_p(N+1)$, the moments $\mathbb E[X_p^2e^{\theta|X_p|}]$ are bounded on $I$ for small $\theta>0$. Choose $\eta$ so small that $\lambda\,\mathbb E[X_p-m_p\mid R]\le\mu_p/2$ on $I$. A position $i\le m$ has $\mathbb Ee^{-\theta\hat X_p(i)}=\varphi_0(\theta)=\mathbb Ee^{-\theta X_p}$, and a position $i>m$ has
$$\varphi_1(\theta)=\varphi_0(\theta)+\eta\,\nu(R)\,\mathbb E\big[e^{-\theta m_p}-e^{-\theta X_p}\mid R\big].$$
Here $\varphi_0(\theta)=1-\theta\mu_p+O(\theta^2)$ and $\varphi_1(\theta)=1-\theta\big(\mu_p-\lambda\,\mathbb E[X_p-m_p\mid R]\big)+O(\theta^2)$, uniformly on $I$. So there are $\theta>0$ and $f<1$, independent of $\sigma\in I$ and of $\tau$, with $\varphi_0,\varphi_1\le f$. The positions are independent, and $\mathbb Ee^{\theta\hat d_p(j)}$ is bounded. Hence
$$\Pr(\mathsf A^c)\le\sum_{p=2,3}\sum_{j>m}\mathbb E\,e^{\theta(\hat d_p(j)-L_p(j-1))}\le C\sum_{j>m}f^{\,j-1}\le C'f^{\,k/2}.\qquad(3)$$

## 1.5 The phases do not align

$|c(s)|=1$ would require $r_1^{-i\tau}=r_2^{-i\tau}=r_3^{-i\tau}$, that is $\tau\alpha,\tau\beta\in2\pi\mathbb Z$ with $\alpha=\log(9/8)$ and $\beta=\log(4/3)$. The numbers $9/8=2^{-3}3^2$ and $4/3=2^23^{-1}$ generate the same multiplicative group as $2$ and $3$ (the exponent matrix has determinant $-1$). So $\tau\log2,\tau\log3\in2\pi\mathbb Z$, and $\tau=0$ since $\log3/\log2$ is irrational.

Quantitatively, with weights $\omega_N=\nu(N\mid R)\ge\omega_0>0$ on $I$,
$$|c|^2=1-2\sum_{a<b}\omega_a\omega_b\Big(1-\cos\big(\tau\log\tfrac{r_b}{r_a}\big)\Big),$$
so $1-|c|\ge\tfrac12(1-|c|^2)\ge8\omega_0^2\big(\|\tau\alpha/2\pi\|^2+\|\tau\beta/2\pi\|^2\big)$, where $\|x\|$ is the distance to the nearest integer. For $|\tau|\le1$ this is at least a constant times $\tau^2$. For large $|\tau|$ let $\tau\alpha/2\pi=n_1+e_1$ and $\tau\beta/2\pi=n_2+e_2$ with nearest integers $n_1,n_2$, not both zero, and $\epsilon=\max|e_i|$. Then $n_2\alpha-n_1\beta=2\pi(n_2e_1-n_1e_2)/\tau$ is $O(\epsilon)$. It equals $(2n_2+n_1)\log3-(3n_2+2n_1)\log2$, a non-zero integer combination with coefficients $O(|\tau|)$. By Baker's theorem on linear forms in logarithms (Mathematika 13, 1966) it is at least $c\,|\tau|^{-\kappa_0}$ for some constant $\kappa_0$. Hence $\epsilon\ge c'|\tau|^{-\kappa_0}$. On the remaining compact range $1-|c|$ has a positive minimum. Consequently, with $A=2\kappa_0$,
$$1-|c(\sigma+i\tau)|\ge b\,\min(\tau^2,|\tau|^{-A})\qquad(\sigma\in I,\ \tau\ne0).\qquad(4)$$

## 1.6 Conclusion

By (2) and (3), $|G_k(s)|\le(B(\sigma)\rho^{1/2})^k+C'(B(\sigma)f^{1/2})^k$. Near $\sigma_c$, $\log B(\sigma)\le C_1\max(\sigma_c-\sigma,0)$. After shrinking $\delta_0$ the second ratio is bounded by a constant below $1$. The first is at most $\exp(-\lambda(1-|c|)/4)$ if $\sigma_c-\sigma\le\lambda(1-|c|)/(4C_1)$, which by (4) holds in $\Omega^*$ for suitable $a$. So $\sum_kG_k(s)$ converges locally uniformly there, its sum is bounded by $C/(1-|c(s)|)$, and it agrees with $\mathcal G(s,1)$ for $\sigma>\sigma_c$. $\square$

The same bounds are locally uniform for $t$ near $1$, so $\mathcal G(s,t)$ is holomorphic in both variables near $(\sigma_c+i\tau,1)$ for every $\tau\ne0$.

## 1.7 What the theorem does not say

The region closes up as $\tau\to0$. The proof does not decide whether the continuations obtained above and below the real axis agree on an interval to the left of $\sigma_c$, or what kind of singularity $\sigma_c$ is beyond what is known (ANS-T20, T22, T27). It gives no continuation to a fixed half-plane. The argument uses the particular letters $1,2,3$ and positive drift at $2$ and $3$; no statement for other grammars is made here.

# 2. Counting at fixed depth (ANS-T32)

Let $A_k(X)=\#\{w:|w|=k,\ E(w)\le X\}$. Let $N_1,\dots,N_k$ be independent and Haar-uniform in $\hat{\mathbb Z}$; define $e_{p,0}=0$, $e_{p,i}=2v_p(N_i+1)+\max\{e_{p,i-1}-v_p(N_i),0\}$, and $g_i=\prod_pp^{\min(e_{p,i-1},\,v_p(N_i))}$. Put
$$\kappa_k=\mathbb E\,\sqrt{g_2g_3\cdots g_k}=\prod_pc_p(k),\qquad c_p(k)=\mathbb E\,p^{\frac12\sum_{i\le k}\min(e_{p,i-1},\,v_p(N_i))}.$$

**Theorem.** For every $k\ge1$, $\kappa_k$ is finite and
$$A_k(X)\sim\frac{\kappa_k}{2^{k-1}(k-1)!}\,\sqrt X\,(\log X)^{k-1}.\qquad(5)$$

**Corollary (ANS-C1, now proved).** $(2\sigma-1)^kG_k(\sigma)\to\kappa_k$ as $\sigma\downarrow\tfrac12$.

For $k=2$, (5) is the asymptotic $\frac\kappa2\sqrt X\log X$ of ANS-T13 with $\kappa_2=\kappa$. The arithmetic coupling between letters changes only the constant, not the power of $\log X$.

## 2.1 A moment bound

For a word, $E(w)=\prod_in_i^2/G$ with $n_i=N_i+1$ and $G=g_2\cdots g_k$, where now $g_i=\gcd(E_{i-1},N_i)$. Consider independent letters whose laws satisfy, uniformly in the law considered,
$$\Pr(d\mid N)\le C_0/d,\qquad\mathbb E\,f(N+1)^M\le C_M\quad(\text{every }M>0),\qquad f(n)=\sum_{e\mid n^2}e^{-0.4}.\qquad(\mathrm P)$$

**Lemma 2.** The following laws satisfy (P) uniformly: Haar measure; and the uniform law of $n=N+1$ on the integers of $(2^a,2^{a+1}]$, $a\ge0$.

*Proof.* For Haar measure $\Pr(d\mid N)=1/d$. For a block, the multiples of $d$ among the $2^a$ values of $N$ number zero if $d>2^{a+1}$ and at most $2^a/d+1\le3\cdot2^a/d$ otherwise. For the moments, $F=f^M$ is multiplicative with $F(p^j)$ increasing in $j$, so $F=1*h$ with $h\ge0$ multiplicative. Here $h(p)=(1+p^{-0.4}+p^{-0.8})^M-1=O_M(p^{-0.4})$, and $F(p^j)\le(1-p^{-0.4})^{-M}$ is bounded. Hence $\sum_eh(e)/e=\prod_p(1+\sum_{j\ge1}h(p^j)p^{-j})<\infty$. The mean of $F(n)$ over $n\le Y$ is at most this sum, which gives the bound for blocks and for Haar measure. $\square$

**Lemma 3.** Put $b_k=\tfrac12+0.1\cdot2^{-(k-1)}$. Under (P), $\mathbb E\,(g_2\cdots g_k)^{b_k}\le C_k$.

*Proof.* Induction on $k$; $k=1$ is trivial. Let $b=b_k\le0.6$. Given the first $k-1$ letters,
$$\mathbb E\,\gcd(E_{k-1},N_k)^{b}\le\sum_{d\mid E_{k-1}}d^{b}\Pr(d\mid N_k)\le C_0\sum_{d\mid E_{k-1}}d^{b-1}\le C_0\sum_{d\mid E_{k-1}}d^{-0.4}\le C_0\prod_{i<k}f(n_i),$$
because $E_{k-1}$ divides $\prod_{i<k}n_i^2$ and the divisor sum is submultiplicative. Apply Hölder with $q=b_{k-1}/b_k>1$:
$$\mathbb E\Big[(g_2\cdots g_{k-1})^{b}\prod_{i<k}f(n_i)\Big]\le\Big(\mathbb E(g_2\cdots g_{k-1})^{b_{k-1}}\Big)^{1/q}\prod_{i<k}\Big(\mathbb Ef(n_i)^{q'}\Big)^{1/q'},\quad q'=\frac q{q-1}.\qquad\square$$

In particular $\kappa_k<\infty$.

## 2.2 Proof of (5)

**Truncation.** For $P,\Lambda\ge1$ let $U$ be the set of words in which no $p^{\Lambda+1}$, $p\le P$, divides any $N_i$ or $n_i$, and let $G^\flat=\prod_{p\le P}p^{v_p(G)}$. On $U$, both $G^\flat$ (a bounded quantity) and membership in $U$ depend only on the residues of the $N_i$ modulo $\mathfrak M=\prod_{p\le P}p^{\Lambda+1}$. Call a word *bad* if it is not in $U$ or if some prime $p>P$ divides some $g_i$.

**The main set.** Let $\mathcal S=\{w\in U:\ \prod n_i^2\le XG^\flat\}$. Since $G\ge G^\flat$, every $w\in\mathcal S$ has $E(w)\le X$; and a word with $E(w)\le X$ outside $\mathcal S$ is bad, because a good word has $G=G^\flat$. So
$$\#\mathcal S\le A_k(X)\le\#\mathcal S+\#\{\text{bad }w:E(w)\le X\}.$$
In each residue class modulo $\mathfrak M$, the number of $(n_1,\dots,n_k)$ with all $n_i\ge2$ and $\prod n_i\le Y$ is asymptotic to $Y(\log Y)^{k-1}/((k-1)!\,\mathfrak M^k)$. With $Y=\sqrt{XG^\flat}$, $\log Y\sim\tfrac12\log X$, summing over the classes in $U$ gives
$$\#\mathcal S\sim\frac{\mathbb E_{\rm Haar}\big[\mathbf 1_U\sqrt{G^\flat}\big]}{2^{k-1}(k-1)!}\sqrt X(\log X)^{k-1}.\qquad(6)$$

**The bad words.** Cut into blocks $n_i\in(2^{a_i},2^{a_i+1}]$ and write $|a|=\sum a_i$. A block contains $2^{|a|}$ words, and there $\prod n_i^2>4^{|a|}$, so $E(w)\le X$ forces $G>4^{|a|}/X$. Hence for every $b>0$ the number of bad words of the block with $E\le X$ is at most $2^{|a|}\,\mathbb E_a\big[\mathbf 1_{\rm bad}G^{b}\big](X4^{-|a|})^{b}$, where $\mathbb E_a$ is the average over the block. Take $b_\pm=\tfrac12\pm\delta$ with $\delta=(b_k-\tfrac12)/2$. By Hölder and Lemmas 2, 3, $\mathbb E_a[\mathbf 1_{\rm bad}G^{b_\pm}]\le C_k\,\pi^{\vartheta}$, where $\vartheta=1-b_+/b_k>0$ and $\pi$ bounds $\Pr_a(\text{bad})$. A prime $p$ divides $g_i$ only if $p\mid N_i$ and $p\mid n_j$ for some $j<i$. So by (P), and $\Pr_a(d\mid n)\le C/d$ (same counting),
$$\pi\le C_k\Big(\sum_{p}p^{-\Lambda-1}+\sum_{p>P}p^{-2}\Big),$$
uniformly in the block, and $\pi\to0$ as $P,\Lambda\to\infty$. The number of blocks with $|a|=h$ is at most $C_k(h+1)^{k-1}$. Let $H=\log_2\sqrt X$. Use $b_-$ for $h\le H$ and $b_+$ for $h>H$:
$$\sum_{h\le H}(h+1)^{k-1}X^{b_-}2^{2\delta h}+\sum_{h>H}(h+1)^{k-1}X^{b_+}2^{-2\delta h}\le C_k\sqrt X\,(\log X)^{k-1}.$$
Hence the bad words number at most $C_k\pi^{\vartheta}\sqrt X(\log X)^{k-1}$.

**Conclusion.** Let $P,\Lambda\to\infty$. Almost surely $p^2$ divides some $N_i$ or $n_i$ for only finitely many $p$, and the remaining valuations are finite; so a word lies in $U$ once $\Lambda$ is large, whatever $P$ is. Hence $\mathbf 1_U\sqrt{G^\flat}\to\sqrt G$ almost surely, with $0\le\mathbf 1_U\sqrt{G^\flat}\le\sqrt G$ and $\mathbb E\sqrt G<\infty$ (Lemma 3). By dominated convergence $\mathbb E[\mathbf 1_U\sqrt{G^\flat}]\to\kappa_k$, and $\pi\to0$. This proves (5). Independence of the $p$-adic coordinates under Haar measure, with monotone convergence in $P$ alone, gives the product over primes. $\square$

**Proof of the corollary.** We have $G_k(\sigma)=\sigma\int_1^\infty A_k(X)X^{-\sigma-1}dX$. Insert (5) and use
$$\int_1^\infty X^{-(\sigma-1/2)-1}(\log X)^{k-1}\,dX=(k-1)!\,(\sigma-\tfrac12)^{-k}.\qquad\square$$

## 2.3 What remains open at fixed depth

Formula (5) and the corollary describe the behaviour at $s=\tfrac12$ along the real axis and the counting function. They give no meromorphic continuation of $G_k$ to the left of $\operatorname{Re}s=1/2$ for $k\ge3$ (known for $k=2$ down to $1/3$), no information on other points of that line, and no lower-order terms.

# 3. Computations

All are finite or statistical checks, not proofs. Parameters and outputs are in `results/`.

- Formula (0) agreed with the recurrence on 3000 random words.
- Lemma 1 was tested by exchanging marked letters: no change of $K_k$ in any trial on the good event; changes do occur off it.
- Finite-sample values of $|\mathbb E[K_k^{-s}Q_k^{-i\tau}]|$ decay quickly with $k$ for $\tau=1,5$. The bound of the proof is far from sharp.
- At $p=2,3$, truncated floating-point values show positive drift also after thinning with $\eta=1/2$.
- $c_p(k)$ by dynamic programming agrees with the product of ANS-T13 for $k=2$ and with direct summation for $k=3$. Truncated products with a first-order tail correction give

| $k$ | 1 | 2 | 3 | 4 | 5 | 6 |
|--|--:|--:|--:|--:|--:|--:|
| $\kappa_k$ (computed) | 1 | 1.85365 | 5.1053 | 19.119 | 92.64 | 561.0 |

- Observed, not proved: $c_p(k)-1$ is close to $\binom k2p^{-3/2}$.
- Exact counts $A_k(X)$ (integer program, checked against direct enumeration for $X\le10^6$) approach (5) slowly, as expected from lower powers of $\log X$. At the largest $X$ used the ratio of the count to the leading term is $0.82$ ($k=2$, $X=10^{12}$), $0.50$ ($k=3$, $10^{10}$) and $0.21$ ($k=4$, $10^9$). With the leading coefficient fixed, the next coefficient for $k=2$ is stable near $-4.5$. For $k=3,4$ the counts do not by themselves confirm the constant.
