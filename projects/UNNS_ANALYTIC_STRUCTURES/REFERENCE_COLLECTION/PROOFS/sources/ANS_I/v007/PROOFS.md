---
title: "ANS-I v007 --- Generative scaling and equidistribution"
author: "UNNS Research Collective"
date: "27 November 2026"
---

Research notes. They continue ANS-I v006; notation is as in v005 and v006. All results concern the nesting grammar. New proofs are pending review; no claim of priority is made, and no literature review has been done.

# 0. Review of v006

The owner's review found T32a, T35, T36 and both parts of T37a valid, and T27 valid with $\sigma_c$ understood as the exact **infimal** Gevrey order. Two wording corrections have been applied: "exact infimal Gevrey order" in the v003 proofs and register, and "nonprime labels such as $1$" in place of "composite labels" in v006 (the label $1$ is not composite).

The review proposed proofs of T37 and of regular variation (T40). Both are correct. They are written out below with the details supplied in checking, together with their consequences.

# 1. Setting

Letters $N\ge1$, $r_N=(N+1)^2/N$, $\sigma=\sigma_c$, $\nu(N)=r_N^{-\sigma}$ (a probability law, since $B(\sigma_c)=1$). A word $w$ has source $K(w)$, multiplier $Q(w)$ and least endpoint $E=KQ$. Fix a homomorphism $\varphi$ of $\mathbb Q_{>0}$ onto a finite abelian group $\Gamma$, written additively; the *sector* of $w$ is $\varphi(Q(w))$. Two counting problems are treated:

- $H=A$: the words with $E(w)\le X$;
- $H=N_x$, for a fixed source $x$: the words with $K(w)\mid x$ and $xQ(w)\le X$.

$H_\gamma(X)$ counts those in sector $\gamma$. By ANS-T10 (v001), $H(X)=X^{\sigma+o(1)}$.

# 2. The exchange comparison

**Lemma 1.** Let $R$ be a finite set of letters containing $1,2,3$, and $\Delta\in\mathbb Z^R$ with $\sum\Delta_N=0$. Put $d=\sum\Delta_N\log r_N$ and $g=\sum\Delta_N\varphi(r_N)$. Then, as $X\to\infty$,
$$H_{\gamma+g}(e^dX)\ge e^{\sigma d}H_\gamma(X)-o(H(X)).$$

*Proof.* **Marking.** For a word of depth $k$ and $m=\lfloor k/2\rfloor$, mark each position $i>m$ with $w_i\in R$, independently, with probability $\eta$. Let $J$ be the set of marked positions and $c=(k,J,\text{unmarked letters})$ the *configuration*. As in v005 §1.2 and v006 §2.1, with the finite set $P_R$ of primes dividing some $N(N+1)$, $N\in R$, there is a good event depending only on $c$ on which $K(w)$ is the same for all assignments of letters of $R$ to $J$. The probability of a given $J$ for a given word is $\eta^{|J|}(1-\eta)^{u}$, where $u$ is the number of unmarked late positions carrying a letter of $R$. It depends only on $c$; call it $\pi(c)$.

**Typical assignments.** Let $\pi_N=r_N^{-\sigma}/\sum_Rr_M^{-\sigma}$, $\lambda=\eta\,\nu(R)$, $M=|J|$ and $n_N$ the number of marked positions carrying $N$. Fix small constants $c_0,\delta>0$ and let $\Omega$ consist of the pairs $(w,J)$ with: $k\ge c_0\log X$, the good event, $M\ge\lambda(k-m)/2$, and $|n_N/M-\pi_N|\le\delta$ for all $N\in R$.

**The injection.** For a configuration $c$ and counts $n=(n_N)$ let $T(c,n)$ be the set of words obtained by assigning to $J$ letters with these counts. All of them have the same $K$, $Q$ and sector. Replacing $n$ by $n+\Delta$ (possible for large $M$ when $\delta<\min\pi_N$) keeps $c$ and $K$, multiplies $Q$ and $E$ by $e^d$, and adds $g$ to the sector. For $N_x$ the condition $K\mid x$ is preserved. So if $T(c,n)$ is counted in $H_\gamma(X)$, then $T(c,n+\Delta)$ is counted in $H_{\gamma+g}(e^dX)$, and different $(c,n)$ have different images.

**The class sizes.** On $\Omega$,
$$\frac{|T(c,n+\Delta)|}{|T(c,n)|}=\prod_{N\in R}\frac{n_N!}{(n_N+\Delta_N)!}=(1+o(1))\prod_N\Big(\frac{n_N}M\Big)^{-\Delta_N}\ge(1-\omega(\delta))\prod_N\pi_N^{-\Delta_N},$$
with $\omega(\delta)\to0$; the powers of $M$ cancel because $\sum\Delta_N=0$, which also gives $\prod\pi_N^{-\Delta_N}=\prod r_N^{\sigma\Delta_N}=e^{\sigma d}$. The new counts need not satisfy the typicality condition.

Summing $\pi(c)|T(c,n+\Delta)|$ over the typical counted classes, and using that for each word the probabilities of all $J$ add to $1$,
$$H_{\gamma+g}(e^dX)\ge(1-\omega(\delta))\,e^{\sigma d}\sum_{w\in H_\gamma(X)}\Pr\big((w,J)\in\Omega\mid w\big).\qquad(1)$$

**The exceptional words.** It remains to show that $\sum_{w\in H(X)}\Pr(\Omega^c\mid w)=O(X^{\sigma-\varepsilon})$.

*Shallow words, $k<c_0\log X$.* A counted word has $Q(w)\le X$. For $1<a<\sigma$ the number of words of depth $k$ with $Q\le X$ is at most $X^aB(a)^k$, and $B(a)>1$. With $c_0$ so small that $a+c_0\log B(a)<\sigma$, the total over shallow depths is $O(X^{\sigma-\varepsilon})$.

*Deep words.* Since $Q(w)\le X$, we have $1\le X^\sigma Q(w)^{-\sigma}=X^\sigma\nu(w)$. Hence the sum over counted words of depth $k$ is at most $X^\sigma\Pr_\nu(\Omega^c)$, where now the letters are independent with law $\nu$. For $k\ge c_0\log X$ the three remaining conditions fail with probability at most $Ce^{-b(\delta)k}$: the good event by the estimate of v005 §1.4, extended to $P_R$ as in v006 (every prime drift is positive and $P_R$ is finite); the size of $J$ and the frequencies, which given $J$ come from independent letters of law $\pi$, by Hoeffding's inequality. Summing over $k\ge c_0\log X$ gives $O(X^{\sigma-\varepsilon})$.

Since $X^{\sigma-\varepsilon}=o(H(X))$, (1) and $H_\gamma\le H$ give $\liminf\,[H_{\gamma+g}(e^dX)-e^{\sigma d}H_\gamma(X)]/H(X)\ge-\omega(\delta)e^{\sigma d}$. Let $\delta\to0$. $\square$

## 2.1 Enough exchanges

**Lemma 2.** There is a finite $R\supseteq\{1,2,3\}$ such that for every $g\in\Gamma$ and $\varepsilon>0$ some $\Delta$ as in Lemma 1 has sector shift $g$ and $d\in(-\varepsilon,0)$.

*Proof.* The differences $\varphi(r_N)-\varphi(r_1)$, for $N\in\{2,3\}$ and $N$ prime, generate $\Gamma$: otherwise a non-trivial character of $\Gamma$, composed with $\varphi$, would be constant on $r_1,r_2,r_3$ and on every $r_p$, contradicting the separation lemma (v006, Lemma 1). As $\Gamma$ is finite, finitely many of these primes suffice; this defines $R$. So some $\Delta_g$ with zero sum has sector shift $g$. Let $e$ be the exponent of $\Gamma$. Adding $e\,(-a-b,a,b)$ on the letters $1,2,3$ keeps the shift and changes $d$ by $e\,(a\log\frac98+b\log\frac43)$. These numbers are dense in $\mathbb R$ because $\log\frac43/\log\frac98$ is irrational (v005 §1.5). $\square$

# 3. Counting equidistribution (ANS-T37)

**Theorem.** For every finite quotient $\Gamma$ and every $\gamma\in\Gamma$,
$$A_\gamma(X)\sim\frac{A(X)}{|\Gamma|},\qquad N_{x,\gamma}(X)\sim\frac{N_x(X)}{|\Gamma|}\quad(x\text{ fixed}).$$

*Proof.* Let $\gamma,\gamma'\in\Gamma$, and take $\Delta$ from Lemma 2 with $g=\gamma'-\gamma$ and $-\varepsilon<d<0$. By monotonicity and Lemma 1,
$$H_{\gamma'}(X)\ge H_{\gamma'}(e^dX)\ge e^{\sigma d}H_\gamma(X)-o(H(X))\ge e^{-\sigma\varepsilon}H_\gamma(X)-o(H(X)).$$
So $\liminf(H_{\gamma'}-H_\gamma)/H\ge e^{-\sigma\varepsilon}-1$, and $\varepsilon\to0$ gives $\liminf\ge0$. Exchanging $\gamma$ and $\gamma'$ gives $(H_{\gamma'}-H_\gamma)/H\to0$. The $|\Gamma|$ proportions add to $1$. $\square$

In particular the seven classes of the index-seven quotient each receive asymptotically one seventh of the words. No rate is obtained.

# 4. Regular variation (ANS-T40)

**Theorem.** For every $\lambda>0$,
$$\frac{A(\lambda X)}{A(X)}\to\lambda^{\sigma_c},\qquad\frac{N_x(\lambda X)}{N_x(X)}\to\lambda^{\sigma_c}.$$
Thus $A(X)=X^{\sigma_c}L(X)$ with $L$ slowly varying, and likewise $N_x$.

*Proof.* Take $\Gamma$ trivial, $R=\{1,2,3\}$. Let $h\in\mathbb R$, $\varepsilon>0$, and choose $d\in(h-\varepsilon,h)$ of the form $a\log\frac98+b\log\frac43$. Lemma 1 gives $H(e^hX)\ge H(e^dX)\ge e^{\sigma d}H(X)-o(H(X))$, so $\liminf H(e^hX)/H(X)\ge e^{\sigma h}$. The same statement for $-h$, applied at $Y=e^hX$, gives $\limsup H(e^hX)/H(X)\le e^{\sigma h}$. $\square$

**The slowly varying factor.** From v003 (T24a, review pending),
$$\frac{c\,(\log X)^{1/\sigma_c}}{\log\log X}\le-\log L(X)\le C\,(\log X)^{1/\sigma_c}.$$
The reviewed estimate T24 (v002) gives the same lower bound and the upper bound with an extra factor $(\log\log X)^2$. So $L\to0$ and is slowly varying; its precise form is not known. Regular variation excludes a persistent non-constant modulation of fixed period in $\log X$ (a factor $P(\log X)$ with $P$ periodic and non-constant times a slowly varying factor), although the letter weights $r_N$ are discrete; it allows slower oscillation inside $L$.

# 5. Arithmetic replication (ANS-T41)

$C(X)=\sum_{n\le X}\#\mathcal W(n)$ counts histories from all sources, and $C(X)=\sum_{m\ge1}A(X/m)$, with the same identity in each sector.

**Theorem.** $C(X)\sim\zeta(\sigma_c)\,A(X)$, and $C_\gamma(X)\sim\zeta(\sigma_c)\,A(X)/|\Gamma|$.

*Proof.* Fix $1<\sigma'<\sigma_c$. By T40 there is $X_0$ with $A(Y/2)\le2^{-\sigma'}A(Y)$ for $Y\ge X_0$. If $X/m\ge X_0$ and $j=\lfloor\log_2m\rfloor$, iterating and using monotonicity gives
$$A(X/m)\le A(X/2^j)\le2^{-\sigma'j}A(X)\le2^{\sigma'}m^{-\sigma'}A(X).$$
So these terms of $\sum_mA(X/m)/A(X)$ have a summable majorant and tend to $m^{-\sigma_c}$. The other non-zero terms have $m\le X$ and $A(X/m)\le A(X_0)$; their sum is at most $A(X_0)X=o(A(X))$. Dominated convergence gives the first statement. Since $A_\gamma\le A$ the same majorant serves each sector, where T37 gives the limit $m^{-\sigma_c}/|\Gamma|$. $\square$

# 6. Fixed depth (ANS-T37b)

**Theorem.** There is $c'>0$ with
$$\frac{G^{[\gamma]}_k(\sigma_c)}{G_k(\sigma_c)}=\frac1{|\Gamma|}+O(e^{-c'k}).$$

*Proof.* For $\chi\ne1$ the bound in the proof of T35, at $s=\sigma_c$, is $|G_{\chi\circ\varphi,k}(\sigma_c)|\le Ce^{-c_1k}$. By T23a (v003), $G_k(\sigma_c)\ge e^{-C_2k^{1/\sigma_c}}$, and $1/\sigma_c<1$. Orthogonality of characters finishes the proof. $\square$

The sector bias therefore decays exponentially although $G_k(\sigma_c)$ itself decays only like a stretched exponential.

# 7. Typical histories (ANS-T42)

**Theorem.** Let $\mathcal E$ be a set of words whose part of depth $k$ has $\nu$-probability at most $Ce^{-bk}$. Then the number of words of $\mathcal E$ counted by $H(X)$ is $O(X^{\sigma-\varepsilon})=o(H(X))$.

*Proof.* This is the argument for the exceptional words in Lemma 1, with $\mathcal E$ in place of $\Omega^c$. $\square$

**Corollary.** Choose $w$ uniformly among the words counted by $A(X)$ (or by $N_x(X)$) and put $\lambda_c=\sum_Nr_N^{-\sigma}\log r_N=-B'(\sigma_c)=2.96846\ldots$. Then, in probability as $X\to\infty$:

1. $\log Q(w)/\log X\to1$ and $\log E(w)/\log X\to1$;
2. $\log K(w)/\log X\to0$;
3. $|w|/\log X\to1/\lambda_c=0.33687\ldots$;
4. the frequency of every finite block $v=(v_1,\dots,v_\ell)$ in $w$ tends to $\prod_ir_{v_i}^{-\sigma_c}$; in particular the letter $N$ has asymptotic share $r_N^{-\sigma_c}$.

*Proof.* (1) Take $\sigma''>\sigma$ with $(1-\epsilon)\sigma''<\sigma$. The number of words, of all depths, with $Q\le X^{1-\epsilon}$ is at most $X^{(1-\epsilon)\sigma''}/(1-B(\sigma''))=o(H(X))$. Counted words have $Q\le X$, and $E\le X$ for $A$; for $N_x$, $Q\le E\le xQ\le X$. (2) $K=E/Q$. (3) Under $\nu$, $\log r_N$ has mean $\lambda_c$ and exponential moments, because $\sum r_N^{\theta-\sigma}<\infty$ for $\theta<\sigma-1$; so $|\log Q/k-\lambda_c|>\epsilon$ has exponentially small probability. Apply the theorem, then (1). (4) Block indicators at distance at least $\ell$ are independent, so Hoeffding's inequality on $\ell$ interleaved families gives exponential concentration. Apply the theorem; shallow words are negligible. $\square$

So a typical history with endpoint at most $X$ has the letter and block frequencies of an independent sequence of law $\nu$, and its source is only $X^{o(1)}$. This describes empirical frequencies, not independence at prescribed positions (a non-empty history from source $1$ must begin with the letter $1$). It says nothing about $L(X)$, which is governed by how rare small sources are.

# 8. Three forms of equidistribution

| Form | Statement | Weighting | Rate | ID |
|--|--|--|--|--|
| Critical moments | $D_j^\gamma/D_j\to1/\lvert\Gamma\rvert$ | $(\log E)^jE^{-\sigma_c}$ | factorial against $D_j$ | T37a |
| Fixed depth | $G_k^{[\gamma]}/G_k\to1/\lvert\Gamma\rvert$ | $E^{-\sigma_c}$, one depth | $e^{-c'k}$ | T37b |
| Counting | $A_\gamma/A\to1/\lvert\Gamma\rvert$ | all words with $E\le X$ | none | T37 |

# 9. Computations

Finite and floating-point checks only; none is a proof. Parameters and outputs are in `results/`.

- Exact census of all words with $E\le2\cdot10^8$ (about $9.3\times10^8$ words), checked against an independent enumeration at the five thresholds up to $10^5$.

| $X$ | $10^4$ | $10^6$ | $10^8$ | limit |
|--|--:|--:|--:|--:|
| $A(2X)/A(X)$ | 2.284 | 2.375 | 2.455 | $2^{\sigma_c}=2.921$ |
| $C(X)/A(X)$ | 7.97 | 6.27 | 4.82 | $\zeta(\sigma_c)=2.446$ |
| largest sector deviation from $1/7$ | .0602 | .0078 | .0013 | 0 |
| mean $\log Q/\log X$ | .738 | .804 | .844 | 1 |
| mean $\log K/\log X$ | .168 | .138 | .114 | 0 |
| mean depth$/\log X$ | .409 | .425 | .432 | .337 |
| share of letter 1 | .308 | .268 | .244 | .117 |

  Convergence is slow. **Mean depth$/\log X$ is still moving away from its limit in this range.** It is the product of mean depth$/$mean $\log Q$, which falls (.554, .529, .512) towards $.337$, and mean $\log Q/\log X$, which rises towards $1$. The table does not test the limits quantitatively.

- Exchange vectors for the index-seven quotient on letters $1,2,3$, all seven shifts, with $-\varepsilon<d<0$ for $\varepsilon=0.1,0.01,0.001$. The ratio of class sizes divided by $e^{\sigma d}$ is $0.767,\ 0.977,\ 0.998,\ 0.99998$ for $M=10^2,10^3,10^4,10^6$ and one test vector.

- Fixed-depth sectors by sampling (200000 words per depth): largest deviation from $1/7$ equal to $.493,.231,.079,.027$ at $k=1,2,4,6$. At $k=8$ and $12$ the effective sample sizes are about 365 and 85, so sampling noise dominates and these depths show nothing.

# 10. Open

- A rate in T37 and T40, and the form of $L(X)$ (with T28).
- ANS-T33: the singularity at $\sigma_c$. Regular variation of $A$ is a new input; no consequence for the continuation is claimed here.
- ANS-T34: continuation of $G_k$ for $k\ge3$.
- ANS-T38, T39: complex zeros; the twists $q^{i\tau_0}$ at $\tau_0$.
