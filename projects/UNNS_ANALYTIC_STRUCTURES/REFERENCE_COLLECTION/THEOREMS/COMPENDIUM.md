---
title: "ASUNNS Theorem Compendium, v003"
author: "UNNS Research Collective"
date: "27 November 2026"
---

Results of Analytic Structures of the UNNS Substrate through ANS-I v015, ANS-II v002 and ANS-II-ND v003. Statements are copied by program from the proof files; the proofs stay in those files. In this edition, review attribution inside quoted statements reads UNNS Research Collective. A statement may refer to a numbered display or section of its source. Three statuses are kept apart: proof status (PROVED means that a written argument exists in the releases), mathematical review, and release or computational acceptance. No literature novelty review of these results has been completed. Entries with status CONJECTURE are not theorems.

# Standing definitions

These definitions apply to regions A to I. They are given for orientation; where a statement needs more, the entry quotes it, and the setting of each release is in the proof sources.

**Nesting grammar.** Letters are integers $N\ge1$. The step $x\mapsto r_Nx$ with $r_N=(N+1)^2/N$ is admissible at a positive integer $x$ exactly when $N\mid x$. A word $w=(N_1,\dots,N_k)$ has multiplier $Q(w)=\prod r_{N_i}$, minimal source $K(w)$ (the least integer from which $w$ is admissible) and least endpoint $E(w)=K(w)Q(w)$. Put $\mathcal W(n)=\{w:E(w)\mid n\}$.

**Series.** $G_k(s)=\sum_{|w|=k}E(w)^{-s}$ and $\mathcal G(s,t)=\sum_kt^kG_k(s)$; $\mathcal Z_H(s,t)$ is the history Dirichlet series; $B(\sigma)=\sum_Nr_N^{-\sigma}$, and $\sigma_c=1.5463810\ldots$ is the root of $B=1$. For $a>1$, $\nu_a(N)=r_N^{-a}/B(a)$.

**Counting.** $N_x(X)$ counts the histories from $x$ with endpoint at most $X$; $A(X)=\#\{w:E(w)\le X\}$; $A_k(X)$ is its depth-$k$ part; $C(X)$ counts from all sources.

**Prime coordinates.** $X_p(N)=2v_p(N+1)-v_p(N)$ and $S_p(j)=\sum_{i\le j}X_p(N_i)$.

Regions J and K use the extended grammar: finitely many further multipliers with a rational power, states in finitely many torsion classes, and admissibility meaning that integrality is preserved. Its setting is quoted at the head of those regions.


# A. Generation: recurrences, composition and factorization

## AS-001: Immediate predecessor series

**Proof status:** PROVED. **Review:** Baseline note, not separately reviewed.

**Review record:** None. **Release and computation:** Baseline note.

**Source:** Initial analytic baseline, lines 7-12. **Scope:** Selected nesting grammar. **Literature priority:** Classical content.

**Statement as recorded:**

For the selected integer nesting grammar, T_N(Nk)=k(N+1)^2 for N,k >= 1. The labelled in-degree D(y) counts m >= 2 with m^2 dividing y.

$$\sum_{y\ge1}D(y)y^{-s}=\zeta(s)(\zeta(2s)-1),\qquad \Re s>1.$$

Proof: sum over y=km^2 and use absolute convergence in the stated half-plane.

**Depends on:** no earlier result cited. **Classical inputs:** divisor sums.

Elementary baseline deduction; classical in content.

## AS-002: Root series

**Proof status:** PROVED. **Review:** Baseline note, not separately reviewed.

**Review record:** None. **Release and computation:** Baseline note.

**Source:** Initial analytic baseline, lines 14-17. **Scope:** Selected nesting grammar. **Literature priority:** Classical content.

**Statement as recorded:**

A(y)=1 if D(y)=0 and 0 otherwise. These are exactly the squarefree integers, including 1, hence A(y)=mu(y)^2.

$$\sum_{y\ge1}A(y)y^{-s}=\frac{\zeta(s)}{\zeta(2s)},\qquad \Re s>1.$$

**Depends on:** no earlier result cited. **Classical inputs:** squarefree Euler product.

Elementary baseline deduction; classical in content.

## ANS-T03: Source and endpoint recurrences

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Release not frozen: Windows acceptance pending.

**Source:** ANS-I v001, lines 13-15, 21-23. **Scope:** Integral-image grammars (see statement). **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v001): Recurrences for E(wb), K(wb); predecessor recursion

**Statement as recorded:**

**Theorem.** For every word $w$ there are integers $K(w),E(w)=K(w)Q(w)$ such that $w$ is admissible exactly from the sources $K(w)\mathbb Z_{>0}$, with endpoints exactly $E(w)\mathbb Z_{>0}$. Starting from $K=E=1$ for the empty word,
$$E(wb)=\frac{p_b\,E(w)}{\gcd(E(w),q_b)},\qquad K(wb)=\frac{q_b\,K(w)}{\gcd(E(w),q_b)} .$$
For nesting, $E(wN)=(N+1)^2E(w)/\gcd(E(w),N)$ and $K(wN)=N\,K(w)/\gcd(E(w),N)$.

**Corollary (histories ending at $n$).** Let $\mathcal W(n)=\{w:E(w)\mid n\}$. Then $\mathcal W(n)$ is the set of words of histories ending at $n$,
$$\mathcal W(n)=\{\varepsilon\}\ \sqcup\bigsqcup_{b:\;p_b\mid n}\mathcal W\!\left(\tfrac{nq_b}{p_b}\right)b,$$
and under (F) it is finite.

**Depends on:** no earlier result cited. **Used by:** ANS-T04, ANS-T05, ANS-T11, ANS-T12, ANS-T13, ANS-T14, ANS-T46m, ANS-T47.

## ANS-T04: Prime-coordinate evolution

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid. Prime-coordinate recurrence and maximum formula.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Release not frozen: Windows acceptance pending.

**Source:** ANS-I v001, lines 29-33. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v001): Prime-coordinate law, closed (maximum) form

**Statement as recorded:**

**Theorem.** A nesting transition acts by $v_p(T_N(x))=v_p(x)+2v_p(N+1)-v_p(N)$. For minimal endpoints, $e_p(w)=v_p(E(w))$ satisfies
$$e_p(wN)=2v_p(N+1)+\max\{e_p(w)-v_p(N),\,0\},$$
and, with $u_i=2v_p(N_i+1)$ and $d_i=v_p(N_i)$, for $k\ge1$
$$e_p(N_1\cdots N_k)=\max_{1\le j\le k}\Big(\sum_{i=j}^{k}u_i-\sum_{i=j+1}^{k}d_i\Big).$$
For each $p$ at most one of $v_p(N)$, $v_p(N+1)$ is non-zero.

**Depends on:** ANS-T03.

## ANS-T47: Composition of words, block factorization, supermultiplicativity

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v014, lines 23-24, 32-33, 37-41. **Scope:** Selected nesting grammar. **Literature priority:** Underlying structure classical; otherwise unreviewed.

**Release table summary** (ANS-I/v014): Composition law (bicyclic per prime), gcd identity, block factorization, supermultiplicativity

**Statement as recorded:**

**Theorem.** For words $u,v$ let $d=\gcd(E(u),K(v))$. Then
$$K(uv)=\frac{K(u)K(v)}d,\qquad E(uv)=\frac{E(u)E(v)}d .$$

**Corollary 1.** $\gcd(K(uv),E(uv))=\gcd\big(K(u)K(v),E(u)E(v)\big)/d$. If moreover $\gcd(K(u),E(u))=\gcd(K(v),E(v))=1$, then
$$\gcd(K(uv),E(uv))=\gcd(K(u),E(v)).$$

**Corollary 2 (block factorization).** Let $J_s=\mu*{\rm id}^s$ and, for $\sigma>\frac12$,
$$A_m(e;s)=\sum_{|u|=m,\;e\mid E(u)}E(u)^{-s},\qquad B_n(e;s)=\sum_{|v|=n,\;e\mid K(v)}E(v)^{-s}.$$
Then
$$G_{m+n}(s)=\sum_{e\ge1}J_s(e)\,A_m(e;s)\,B_n(e;s),$$
and consequently $G_{m+n}(\sigma)\ge G_m(\sigma)\,G_n(\sigma)$ for real $\sigma$.

**Depends on:** ANS-T03, ANS-T12. **Used by:** ANS-T46r, ANS-T46s. **Classical inputs:** bicyclic monoid (named only).

## ANS-T01: History Dirichlet factorization

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid. Absolute-convergence region as stated.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Release not frozen: Windows acceptance pending.

**Source:** ANS-I v001, lines 39-40, 44-46. **Scope:** Integral-image grammars (see statement). **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v001): History Dirichlet factorization Z_H = zeta G, with exact region

**Statement as recorded:**

Let $H_k(n)=\#\{w\in\mathcal W(n):|w|=k\}$ and $a_k(n)=\#\{w:|w|=k,\ E(w)=n\}$, and put
$$\mathcal G(s,t)=\sum_w\frac{t^{|w|}}{E(w)^s},\qquad \mathcal Z_H(s,t)=\sum_{n,k}\frac{H_k(n)t^k}{n^s}.$$

**Theorem.** For every integral-image grammar with (F),
$$H_k(n)=\sum_{d\mid n}a_k(d),\qquad a_k(n)=\sum_{d\mid n}\mu(d)H_k(n/d),$$
and, for $t\ne0$, $\mathcal Z_H(s,t)$ converges absolutely iff $\operatorname{Re}s>1$ and $\mathcal G(\operatorname{Re}s,|t|)<\infty$; there $\mathcal Z_H(s,t)=\zeta(s)\,\mathcal G(s,t)$.

**Depends on:** no earlier result cited. **Used by:** ANS-T14.

## ANS-T02: Depth-resolved Moebius inversion

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid. Exact depth-resolved Moebius inversion.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Release not frozen: Windows acceptance pending.

**Source:** ANS-I v001, lines 44-46. **Scope:** Integral-image grammars (see statement). **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v001): Depth-resolved Moebius inversion

**Statement as recorded:**

**Theorem.** For every integral-image grammar with (F),
$$H_k(n)=\sum_{d\mid n}a_k(d),\qquad a_k(n)=\sum_{d\mid n}\mu(d)H_k(n/d),$$
and, for $t\ne0$, $\mathcal Z_H(s,t)$ converges absolutely iff $\operatorname{Re}s>1$ and $\mathcal G(\operatorname{Re}s,|t|)<\infty$; there $\mathcal Z_H(s,t)=\zeta(s)\,\mathcal G(s,t)$.

**Depends on:** no earlier result cited.

## ANS-T14: Source-weighted history series and its region

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. The stated convergence regions; not a complete classification for negative source weights.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Release not frozen: Windows acceptance pending.

**Source:** ANS-I v001, lines 56-61, 101-105. **Scope:** Integral-image grammars (see statement). **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v001): Source-weighted series F(s,u,t): all-history factorization, anti-diagonal closed form, convergence region

**Statement as recorded:**

Let $\mathcal F(s,u,t)=\sum_w t^{|w|}E(w)^{-s}K(w)^{-u}=\sum_wt^{|w|}Q(w)^{-s}K(w)^{-(s+u)}$.

**Theorem.** Summing over all actual histories, given by a source $x$ and an admissible word $w$ with endpoint $y=Q(w)x$,
$$\sum_{(x,w)}\frac{t^{|w|}}{x^{u}\,y^{s}}=\zeta(s+u)\,\mathcal F(s,u,t)$$
wherever the left side converges absolutely, which for $t\ne0$ means $\operatorname{Re}(s+u)>1$ and absolute convergence of $\mathcal F$. On the anti-diagonal, for $\operatorname{Re}s>1$ and $|t|B(\operatorname{Re}s)<1$,
$$\mathcal F(s,-s,t)=\frac1{1-t\sum_b r_b^{-s}},\qquad B(\sigma)=\sum_br_b^{-\sigma}.$$

**Theorem.** Let $t\ne0$, $a=\operatorname{Re}s$ and $b=\operatorname{Re}(s+u)$.

1. If $a\le1$, or if $a>1$ and $|t|B(a)>1$, then $\mathcal F(s,u,t)$ does not converge absolutely, for any real $b$.
2. If $b\ge0$, $a>1$ and $|t|B(a)<1$, it converges absolutely.
3. The series over all actual histories in T14a converges absolutely if $b>1$, $a>1$, $|t|B(a)<1$; it does not if $b\le1$, or $a\le1$, or $a>1$ and $|t|B(a)>1$.

**Depends on:** ANS-T03, ANS-T01, ANS-T07, ANS-T09.

## ANS-T06: No ordinary Euler product

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid. Ordinary Euler-product obstruction.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Release not frozen: Windows acceptance pending.

**Source:** ANS-I v001, lines 161-161. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v001): No ordinary Euler product for Z_H or G at t = 1

**Statement as recorded:**

**Theorem.** Neither $H(n)=\#\mathcal W(n)$ nor $a(n)=\sum_ka_k(n)$ is multiplicative; hence neither $\mathcal Z_H(s,1)$ nor $\mathcal G(s,1)$ is a product over primes of series in $p^{-s}$.

**Depends on:** no earlier result cited.

## ANS-T08: Closed form for unit denominators

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid. Unit-denominator grammar.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Release not frozen: Windows acceptance pending.

**Source:** ANS-I v001, lines 169-169. **Scope:** Integral-image grammars (see statement). **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v001): Closed form when all denominators are 1

**Statement as recorded:**

**Theorem.** If every $q_b=1$ then $E(w)=Q(w)$ and $\mathcal G(s,t)=1/(1-t\sum_bp_b^{-s})$ wherever $|t|\sum_bp_b^{-\operatorname{Re}s}<1$. For the labels $\{2,3\}$, $\mathcal G(s,t)=1/(1-t(2^{-s}+3^{-s}))$, absolutely convergent iff $|t|(2^{-\sigma}+3^{-\sigma})<1$, with meromorphic continuation to the whole plane.

**Depends on:** no earlier result cited.

# B. Convergence and growth in depth

## ANS-T07: Sufficient convergence criterion

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid. A sufficient convergence criterion.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Release not frozen: Windows acceptance pending.

**Source:** ANS-I v001, lines 73-73. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v001): Sufficient convergence criterion, B(2) < 1

**Statement as recorded:**

**Theorem.** If $\operatorname{Re}s=a>1$, $\operatorname{Re}(s+u)=b\ge0$ and $|t|B(a)<1$, then $\mathcal F(s,u,t)$ converges absolutely. Also $B(2)=\zeta(2)-2\zeta(3)+\zeta(4)<1$.

**Depends on:** no earlier result cited. **Used by:** ANS-T14.

**Relations:** ANS-T09 extends ANS-T07.

## ANS-T15: Source-one generation: every prime reached; saturation

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Release not frozen: Windows acceptance pending.

**Source:** ANS-I v001, lines 79-79, 83-83. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v001): Every source's history count grows as X^(sigma_c + o(1)); all primes reachable from 1

**Statement as recorded:**

**Lemma (every prime is reached from source 1).** For each prime $p$ there is a word $w_p$ admissible from $1$ with $p\mid Q(w_p)$.

**Lemma (saturation).** Fix $\sigma\ge0$ and $M$, and let the letters of $v=(v_1,v_2,\dots)$ be independent with law $\nu(N)=r_N^{-\sigma}/B_M(\sigma)$, $N\le M$. There is a word $w_0$, admissible from $1$, such that with probability at least $1/2$ the whole infinite word $w_0v$ is admissible from $1$.

**Depends on:** no earlier result cited. **Used by:** ANS-T09, ANS-T10, ANS-T11, ANS-T23, ANS-T31.

## ANS-T09: Growth in depth and the sharp boundary sigma_c

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Release not frozen: Windows acceptance pending.

**Source:** ANS-I v001, lines 93-93, 111-113. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v001): G_k^(1/k) -> B(sigma); sharp abscissa sigma_c with B(sigma_c) = 1

**Statement as recorded:**

**Theorem.** Let $G_k(\sigma)=\sum_{|w|=k}E(w)^{-\sigma}$. Then $\lim_{k\to\infty}G_k(\sigma)^{1/k}=B(\sigma)$ for $\sigma>1$, and the limit is $+\infty$ for $0\le\sigma\le1$.

**Corollary (abscissa).** $\mathcal G(s,1)$ and $\mathcal Z_H(s,1)$ have abscissa of absolute convergence $\sigma_c$, the unique root of
$$\sum_{N\ge1}\Big(\frac{N}{(N+1)^2}\Big)^{\sigma_c}=1,\qquad\sigma_c=1.5463810\ldots$$
Because the coefficients are non-negative, $s=\sigma_c$ is a singular point of both series (Landau).

**Depends on:** ANS-T15. **Used by:** ANS-T11, ANS-T14, ANS-T19. **Classical inputs:** Landau.

**Relations:** ANS-T09 extends ANS-T07.

## ANS-T10: Growth exponent of every counting function

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Release not frozen: Windows acceptance pending.

**Source:** ANS-I v001, lines 119-122. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v001): log A(X)/log X, log C(X)/log X -> sigma_c

**Statement as recorded:**

For a source $x$ let $N_x(X)$ be the number of histories from $x$ with endpoint at most $X$. Let $A(X)=\#\{w:E(w)\le X\}$ and $C(X)=\sum_{n\le X}\#\mathcal W(n)$.

**Theorem.** For every source $x\ge1$,
$$\lim_{X\to\infty}\frac{\log N_x(X)}{\log X}=\lim\frac{\log A(X)}{\log X}=\lim\frac{\log C(X)}{\log X}=\sigma_c .$$

**Depends on:** ANS-T15. **Used by:** ANS-T37, ANS-T40.

## ANS-T12: Convergence region at fixed depth

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Release not frozen: Windows acceptance pending.

**Source:** ANS-I v001, lines 134-134. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v001): Fixed-depth region a + b > 1; abscissa of G_k is 1/2

**Statement as recorded:**

**Theorem.** Let $k\ge1$, $a>0$, $b\ge0$ and $F_k(a,b)=\sum_{|w|=k}Q(w)^{-a}K(w)^{-b}$. Then $F_k(a,b)<\infty$ iff $a+b>1$ when $b>0$, and iff $a>1$ when $b=0$. In particular $G_k(\sigma)=F_k(\sigma,\sigma)$ has abscissa exactly $1/2$ for every $k\ge1$.

**Depends on:** ANS-T03. **Used by:** ANS-T34, ANS-T35, ANS-T46m, ANS-T47.

## ANS-T11: Saturation criterion for general grammars (classification open)

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. The saturation criterion only; the general classification remains open.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Release not frozen: Windows acceptance pending.

**Source:** ANS-I v001, lines 175-177. **Scope:** Integral-image grammars (see statement). **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v001): Analytic classification across grammars

**Statement as recorded:**

**Theorem.** Let $G$ be an integral-image grammar with (F), $S$ a finite set of labels, $\sigma\ge0$ and $B_S(\sigma)=\sum_{b\in S}r_b^{-\sigma}$. Suppose that for every prime $p$ dividing some $q_b$, $b\in S$,
$$\sum_{b\in S}r_b^{-\sigma}\big(v_p(p_b)-v_p(q_b)\big)>0 .$$
Then $\liminf_kG_k(\sigma)^{1/k}\ge B_S(\sigma)$. If such sets exist with $B_S(\sigma)$ arbitrarily close to $B(\sigma)$ (or arbitrarily large when $B(\sigma)=\infty$), then $\lim G_k(\sigma)^{1/k}=B(\sigma)$.

**Depends on:** ANS-T03, ANS-T09, ANS-T15.

## ANS-T26: Finite-alphabet contrast

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v002, lines 101-101. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v002): Finite alphabets: G_k -> c_M > 0, blow-up c_M/(mu_M delta), c_M -> 0

**Statement as recorded:**

**Theorem.** Let $M\ge2$, $\sigma_M$ the root of $B_M=1$, letters $N\le M$ with law $r_N^{-\sigma_M}$. Then $K_k$ stabilizes almost surely at a finite $K_\infty$; $G^{(M)}_k(\sigma_M)\downarrow c_M=\mathbb EK_\infty^{-\sigma_M}>0$; $\delta\,\mathcal G^{(M)}(\sigma_M+\delta,1)\to c_M/\mu_M>0$ as $\delta\downarrow0$; and $c_M\to0$ as $M\to\infty$.

**Depends on:** ANS-T23.

# C. The critical exponent

## ANS-T16: Critical probability representation

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-I v002, lines 11-12. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v002): G_k(a)/B(a)^k = E[K_k^-a]

**Statement as recorded:**

Since $\Pr(N_1\cdots N_k=w)=Q(w)^{-a}/B(a)^k$ and $E=KQ$,
$$\frac{G_k(a)}{B(a)^k}=\mathbb E\,K_k^{-a};\qquad G_k(\sigma)=\mathbb E_{\nu_c}K_k^{-\sigma}.$$

**Depends on:** no earlier result cited. **Used by:** ANS-T19.

## ANS-T17: Infinite-alphabet admissibility obstruction

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-I v002, lines 19-19. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v002): Critical random words are a.s. inadmissible from any integer

**Statement as recorded:**

**Theorem (T17).** An infinite $\nu_a$-random word is almost surely not admissible from any given integer $x$.

**Depends on:** no earlier result cited. **Used by:** ANS-T18, ANS-T23.

## ANS-T18: Divergence of minimal sources

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-I v002, lines 23-23. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v002): K_k -> infinity a.s.

**Statement as recorded:**

**Theorem (T18).** $K_k\to\infty$ almost surely.

**Depends on:** ANS-T17. **Used by:** ANS-T19, ANS-T21.

## ANS-T19: Decay of the critical depth terms

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-I v002, lines 28-28. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v002): G_k(sigma_c) -> 0 with G_k^(1/k) -> 1

**Statement as recorded:**

**T19.** $G_k(\sigma)\to0$ by T18, T16 and bounded convergence, while $G_k(\sigma)^{1/k}\to B(\sigma)=1$ (v001, Theorem 4.4).

**Depends on:** ANS-T18, ANS-T16, ANS-T09. **Used by:** ANS-T20.

**Relations:** ANS-T23 quantifies ANS-T19.

## ANS-T20: No meromorphic continuation through sigma_c

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-I v002, lines 30-30. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v002): No meromorphic continuation through sigma_c

**Statement as recorded:**

**T20.** By (0), $E(wN)\ge r_NE(w)\ge4E(w)$, so $G_k(\sigma+\delta)\le4^{-k\delta}G_k(\sigma)$. Hence $\delta\,\mathcal G(\sigma+\delta,1)\le\delta\sum_k4^{-k\delta}G_k(\sigma)\to0$ since $G_k(\sigma)\to0$. A pole of order $m\ge1$ would make $\delta\,\mathcal G$ tend to a non-zero limit or to infinity; a removable point is excluded by Landau's theorem. So $\mathcal G(s,1)$ has no meromorphic continuation to a neighbourhood of $\sigma$. Theorem T22 below strengthens this.

**Depends on:** ANS-T19. **Used by:** ANS-T31, ANS-T36. **Classical inputs:** Landau.

**Relations:** ANS-T22 strengthens ANS-T20.

## ANS-T21: Strict growth suppression

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-I v002, lines 32-34. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v002): N_x, A, C are o(X^sigma_c)

**Statement as recorded:**

**T21.** Every $w$ with $E(w)\le X$ gives
$$\frac{A(X)}{X^{\sigma}}=\mathbb E_{\nu_c}\sum_{k\ge0}K_k^{-\sigma}\Big(\frac{E_k}{X}\Big)^{\sigma}\mathbf 1_{E_k\le X}.\qquad(1)$$
Since $E_{k+1}\ge4E_k$, the sum is at most $C_4=(1-4^{-\sigma})^{-1}$. Fix a word with $K_k\to\infty$. Terms with $k<k_0$ tend to $0$ as $X\to\infty$, and the others sum to at most $C_4K_{k_0}^{-\sigma}$. Dominated convergence gives $A(X)=o(X^{\sigma})$. A history from $x$ with endpoint $\le X$ has $E(w)\le X$, so $N_x(X)\le A(X)$; and $C(X)=\sum_{m\le X}A(X/m)=o(X^\sigma)$ because $\sigma>1$. $\square$

**Depends on:** ANS-T18. **Used by:** ANS-T24.

**Relations:** ANS-T24 quantifies ANS-T21.

## ANS-T22: Convergence on the critical surface; smooth singularity

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v002, lines 54-54, 58-58. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v002): On |t|B(a) = 1, a > 1: F converges absolutely iff Re(s+u) > 0; G(sigma_c,1) finite; G and Z_H are C-infinity up to Re s = sigma_c

**Statement as recorded:**

**Corollary (T22, the whole critical surface).** Let $a=\operatorname{Re}s>1$, $b=\operatorname{Re}(s+u)$ and $|t|B(a)=1$. Then $\mathcal F(s,u,t)$ converges absolutely iff $b>0$. In particular $\mathcal G(s,t)$ converges absolutely on the surface; $\mathcal G(\sigma,1)<\infty$.

**Corollary (smooth singularity).** All derivatives of $\mathcal G(s,1)$ and of $\mathcal Z_H(s,1)$ converge absolutely and uniformly on the closed half-plane $\operatorname{Re}s\ge\sigma$. Thus both functions extend to $C^\infty$ functions there, although $s=\sigma$ is a singular point. No pole, and no algebraic or logarithmic branch point that would make some derivative unbounded, can occur at $\sigma$.

**Depends on:** ANS-T23. **Used by:** ANS-T37a. **Classical inputs:** Landau.

**Relations:** ANS-T22 strengthens ANS-T20.

## ANS-T23: Rate of critical decay up to logarithms

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v002, lines 37-37, 81-83. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v002): -log(G_k(a)/B(a)^k) = k^(1/a + o(1))

**Statement as recorded:**

**Theorem.** For every $a>1$ and $b>0$ and all $k\ge2$, $\mathbb E\,K_k^{-b}\le C_b\exp(-c_b\,k^{1/a}/\log k)$.

**Theorem (T23).** For every $a>1$ and large $k$,
$$\frac{c\,k^{1/a}}{\log k}\ \le\ -\log\frac{G_k(a)}{B(a)^k}\ \le\ C\,k^{1/a}\log^2k .$$
Hence $-\log\big(G_k(a)/B(a)^k\big)=k^{1/a+o(1)}$, and $G_k(\sigma_c)=\exp(-k^{1/\sigma_c+o(1)})$.

**Depends on:** ANS-T17, ANS-T15. **Used by:** ANS-T22, ANS-T23a, ANS-T24, ANS-T26, ANS-T28a, ANS-T48, ANS2-T02, ANS2-T09a. **Classical inputs:** Ville, Chebyshev.

**Relations:** ANS-T23a sharpens ANS-T23; ANS-T23 quantifies ANS-T19.

## ANS-T23a: Strengthened critical depth bounds

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-I v003, lines 18-20. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v003): -log E[K_k^-b] <= C k^beta (with v002: >= c k^beta / log k)

**Statement as recorded:**

**Theorem.** For $a>1$, $b>0$ and large $k$,
$$\frac{c\,k^{\beta}}{\log k}\le-\log\mathbb E K_k^{-b}\le C\,k^{\beta}.$$
In particular $e^{-Ck^{\beta_c}}\le G_k(\sigma_c)\le e^{-ck^{\beta_c}/\log k}$.

**Depends on:** ANS-T23. **Used by:** ANS-T24a, ANS-T28a, ANS-T37b, ANS-T48. **Classical inputs:** Jensen.

**Relations:** ANS-T23a sharpens ANS-T23.

## ANS-T24: Growth suppression law up to logarithms

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v002, lines 90-92. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v002): N_x, A, C = X^sigma_c exp(-(log X)^(1/sigma_c + o(1)))

**Statement as recorded:**

**Theorem.** With $\sigma=\sigma_c$, for each fixed source $x$ and $Z(X)$ any of $N_x(X)$, $A(X)$, $C(X)$, for large $X$,
$$\frac{c\,(\log X)^{1/\sigma}}{\log\log X}\ \le\ -\log\frac{Z(X)}{X^{\sigma}}\ \le\ C\,(\log X)^{1/\sigma}(\log\log X)^2 .$$
($C$ may depend on $x$.) Hence $Z(X)=X^{\sigma}\exp\big(-(\log X)^{1/\sigma+o(1)}\big)$.

**Depends on:** ANS-T21, ANS-T23. **Used by:** ANS-T24a. **Classical inputs:** Chebyshev.

**Relations:** ANS-T24a sharpens ANS-T24; ANS-T24 quantifies ANS-T21.

## ANS-T27: Critical derivative growth; infimal Gevrey order sigma_c

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. Valid for the infimal Gevrey order; membership at exactly that order is open.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v003, lines 42-44. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v003): c^j j^(sigma j) <= D_j <= (C j log j)^(sigma j); infimal Gevrey order sigma_c

**Statement as recorded:**

Let $D_j=(-1)^j\mathcal G^{(j)}(\sigma,1)=\sum_w(\log E(w))^jE(w)^{-\sigma}$.

**Theorem.** There are $c,C>0$ with $c^j j^{\sigma j}\le D_j\le(Cj\log j)^{\sigma j}$ for large $j$. Hence $\log D_j=\sigma j\log j+O(j\log\log j)$, $D_j=(j!)^{\sigma+o(1)}$, the Taylor series of $\mathcal G(\cdot,1)$ at $\sigma$ has radius $0$, and $\sigma_c$ is the exact infimal Gevrey order of $\mathcal G(\cdot,1)$ on $\operatorname{Re}s\ge\sigma$ (since $|\mathcal G^{(j)}(s,1)|\le D_j$ there).

**Depends on:** ANS-T24a. **Used by:** ANS-T37a, ANS2-T04.

## ANS-T28a: Exact order of the first-introduction event

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid. Preventing harmful first introductions does not prevent depletion of primes met earlier, so this does not settle T28.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-I v003, lines 53-56. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v003): Probability that every new prime arrives through N+1 is exp(-order k^beta / log k)

**Statement as recorded:**

A prime *occurs* in $N$ if it divides $N(N+1)$. Let $S_i$ be the set of primes not occurring in $N_1,\dots,N_{i-1}$, and let $\mathcal I_k$ be the event that no $N_i$ ($i\le k$) is divisible by a prime of $S_i$: every prime met in the first $k$ letters is introduced through $N+1$ only.

**Theorem.** For $a>1$,
$$e^{-Ck^{\beta}/\log k}\le\Pr(\mathcal I_k)\le e^{-ck^{\beta}/\log k}.$$

**Depends on:** ANS-T23, ANS-T23a. **Used by:** ANS2-T07.

## ANS-T31: Holomorphic continuation across the critical line away from sigma_c

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v005, lines 21-27. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v005): G(s,1) and Z_H(s,1) continue holomorphically to {sigma > sigma_c - a min(tau^2, \|tau\|^-A), tau != 0}; sigma_c is the only singular point on the critical line (resolves the line part of ANS-T29)

**Statement as recorded:**

**Theorem.** There are constants $a>0$, $A>0$ such that $\sum_kG_k(s)$ converges locally uniformly in
$$\Omega^*=\{\sigma+i\tau:\ \tau\ne0,\ \sigma>\sigma_c-a\min(\tau^2,|\tau|^{-A})\}$$
(for $\sigma>\sigma_c$ this is the known absolute convergence, which holds for every $\tau$). Consequently $\mathcal G(s,1)$ has a holomorphic continuation to $\{\operatorname{Re}s>\sigma_c\}\cup\Omega^*$, and so has $\mathcal Z_H(s,1)=\zeta(s)\,\mathcal G(s,1)$. On $\Omega^*$ near the line, $|\mathcal G(s,1)|\le C\max(\tau^{-2},|\tau|^{A})$.

In particular **every point $\sigma_c+i\tau$ with $\tau\ne0$ is a regular point**. The line $\operatorname{Re}s=\sigma_c$ is not a natural boundary, and the real point $\sigma_c$, which is singular (Landau; ANS-T20), is its only singular point.

The word series itself does not converge absolutely for $\operatorname{Re}s<\sigma_c$. The continuation comes from cancellation inside each $G_k$.

**Depends on:** ANS-T15, ANS-T20. **Used by:** ANS-T35, ANS-T36, ANS-T37. **Classical inputs:** Landau.

## ANS-T35: Twisted continuation for unitary characters

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v006, lines 34-35, 43-43. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v006): For unitary chi not equal to q^(i tau), G_chi continues across sigma_c + i tau; finite order: uniform region over the whole line

**Statement as recorded:**

A *unitary character* is a homomorphism $\chi:\mathbb Q_{>0}\to S^1$; it is determined by arbitrary values on the primes. Put
$$G_{\chi,k}(s)=\sum_{|w|=k}\frac{\chi(Q(w))}{E(w)^s},\qquad\mathcal G_\chi(s,t)=\sum_kt^kG_{\chi,k}(s).$$

**Theorem.** Let $\chi$ be a unitary character and $\tau\in\mathbb R$. If $\chi$ is not the character $q\mapsto q^{i\tau}$, then $\mathcal G_\chi(s,t)$ continues holomorphically to a neighbourhood of $(\sigma_c+i\tau,t_0)$ for every $|t_0|=1$.

**Depends on:** ANS-T31, ANS-T12. **Used by:** ANS-T36, ANS-T37, ANS-T37b.

## ANS-T36: Finite-quotient sector functions share the singular part

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v006, lines 72-72, 76-76. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v006): For every finite quotient, sector function = G/\|Gamma\| + function holomorphic across the line

**Statement as recorded:**

Let $\varphi:\mathbb Q_{>0}\to\Gamma$ be a surjective homomorphism onto a finite abelian group, and $\mathcal G^{[\gamma]}(s)=\sum_{\varphi(Q(w))=\gamma}E(w)^{-s}$.

**Theorem.** $\mathcal G^{[\gamma]}(s)=|\Gamma|^{-1}\,\mathcal G(s,1)+R_\gamma(s)$, where $R_\gamma$ is holomorphic on a region $\{\sigma>\sigma_c-a(1+|\tau|)^{-A}\}$. Consequently each $\mathcal G^{[\gamma]}$ is singular at $\sigma_c$ and regular at every other point of the critical line.

**Depends on:** ANS-T35, ANS-T20, ANS-T31. **Used by:** ANS-T37a.

## ANS-T28: Exact order of the critical decay

**Proof status:** CONJECTURE. **Review:** Not a proved result.

**Review record:** None. **Release and computation:** Archived release.

**Source:** ANS-I v003, lines 71-73. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v003): Exact order: -log E[K_k^-b] comparable to k^beta / log k

**Statement as recorded:**

**Conjecture.** $-\log\mathbb E K_k^{-b}\asymp k^{\beta}/\log k$.

Proved: it lies between $ck^{\beta}/\log k$ and $Ck^{\beta}$. What is missing is control of repeated demands: under a law that keeps $K_k$ small, one needs the exponent of each small prime in the state to stay supplied. Under $\mathsf Q$ the introductions are handled by §5, but the drift of the individual prime coordinates under $\mathsf Q$ is not controlled.

**Depends on:** no earlier result cited.

# D. Counting, equidistribution and typical histories

## ANS-T24a: Growth suppression without logarithms in the lower estimate

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v003, lines 32-33. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v003): -log(Z(X)/X^sigma_c) <= C (log X)^beta_c, Z = N_x, A, C

**Statement as recorded:**

**Theorem.** With $\sigma=\sigma_c$, $\beta=\beta_c$, any fixed source $x$ and $Z(X)$ any of $N_x(X)$, $A(X)$, $C(X)$:
$$\frac{c(\log X)^{\beta}}{\log\log X}\le-\log\frac{Z(X)}{X^{\sigma}}\le C(\log X)^{\beta}.$$

**Depends on:** ANS-T24, ANS-T23a. **Used by:** ANS-T24b, ANS-T27, ANS-T42a, ANS2-T03, ANS2N-T04b.

**Relations:** ANS-T24a sharpens ANS-T24; ANS-T24b gives a second proof of one inequality of ANS-T24a.

## ANS-T24b: First-passage proof of the counting estimate

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Release has no archive of its own.

**Source:** ANS-I v004, lines 5-5. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v004): First-passage proof of the right inequality of T24a, without the central-limit window

**Statement as recorded:**

**Statement** (right inequality of ANS-T24a). For any fixed source $x$ and $Z(X)$ any of $N_x(X)$, $A(X)$, $C(X)$: $-\log\big(Z(X)/X^\sigma\big)\le C(\log X)^\beta$.

**Depends on:** ANS-T24a.

**Relations:** ANS-T24b gives a second proof of one inequality of ANS-T24a.

## ANS-T37a: Equidistribution of critical log-moments

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v006, lines 84-89. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v006): Critical log-moments equidistribute; liminf A_gamma/A <= 1/\|Gamma\| <= limsup (uses T27)

**Statement as recorded:**

Let $D_j=\sum_w(\log E)^jE^{-\sigma_c}$ and let $D_j^\gamma$ be the part with $\varphi(Q(w))=\gamma$.

**Theorem.** (1) $D_j^\gamma/D_j\to1/|\Gamma|$; the error is at most $C^j j!/D_j$. (2) With $A_\gamma(X)=\#\{w:E(w)\le X,\ \varphi(Q(w))=\gamma\}$ and $A=\sum_\gamma A_\gamma$,
$$\liminf_{X\to\infty}\frac{A_\gamma(X)}{A(X)}\le\frac1{|\Gamma|}\le\limsup_{X\to\infty}\frac{A_\gamma(X)}{A(X)} .$$

In particular, if a sector proportion has a limit, the limit is $1/|\Gamma|$.

**Depends on:** ANS-T36, ANS-T22, ANS-T27.

**Relations:** ANS-T37 strengthens ANS-T37a.

## ANS-T37: Counting equidistribution over finite quotients

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v007, lines 17-22, 58-59. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v007): A_gamma(X) ~ A(X)/\|Gamma\|, and the same for each fixed source, for every finite quotient

**Statement as recorded:**

Letters $N\ge1$, $r_N=(N+1)^2/N$, $\sigma=\sigma_c$, $\nu(N)=r_N^{-\sigma}$ (a probability law, since $B(\sigma_c)=1$). A word $w$ has source $K(w)$, multiplier $Q(w)$ and least endpoint $E=KQ$. Fix a homomorphism $\varphi$ of $\mathbb Q_{>0}$ onto a finite abelian group $\Gamma$, written additively; the *sector* of $w$ is $\varphi(Q(w))$. Two counting problems are treated:

- $H=A$: the words with $E(w)\le X$;
- $H=N_x$, for a fixed source $x$: the words with $K(w)\mid x$ and $xQ(w)\le X$.

$H_\gamma(X)$ counts those in sector $\gamma$. By ANS-T10 (v001), $H(X)=X^{\sigma+o(1)}$.

**Theorem.** For every finite quotient $\Gamma$ and every $\gamma\in\Gamma$,
$$A_\gamma(X)\sim\frac{A(X)}{|\Gamma|},\qquad N_{x,\gamma}(X)\sim\frac{N_x(X)}{|\Gamma|}\quad(x\text{ fixed}).$$

**Depends on:** ANS-T35, ANS-T31, ANS-T10. **Used by:** ANS-T40, ANS-T41, ANS-T42, ANS-T44.

**Relations:** ANS-T37 strengthens ANS-T37a.

## ANS-T40: Regular variation with index sigma_c

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v007, lines 69-71. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v007): A(lambda X)/A(X) -> lambda^sigma_c, same for N_x: A = X^sigma_c times a slowly varying factor

**Statement as recorded:**

**Theorem.** For every $\lambda>0$,
$$\frac{A(\lambda X)}{A(X)}\to\lambda^{\sigma_c},\qquad\frac{N_x(\lambda X)}{N_x(X)}\to\lambda^{\sigma_c}.$$
Thus $A(X)=X^{\sigma_c}L(X)$ with $L$ slowly varying, and likewise $N_x$.

**Depends on:** ANS-T37, ANS-T10. **Used by:** ANS-T41, ANS-T43, ANS-T44.

## ANS-T41: Asymptotic arithmetic replication

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v007, lines 83-83. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v007): C(X) ~ zeta(sigma_c) A(X), with equal sector shares

**Statement as recorded:**

**Theorem.** $C(X)\sim\zeta(\sigma_c)\,A(X)$, and $C_\gamma(X)\sim\zeta(\sigma_c)\,A(X)/|\Gamma|$.

**Depends on:** ANS-T40, ANS-T37. **Used by:** ANS-T43, ANS-T44.

## ANS-T37b: Fixed-depth sector equidistribution at sigma_c

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v007, lines 91-92. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v007): G_k sector ratio at sigma_c = 1/\|Gamma\| + O(e^(-c'k))

**Statement as recorded:**

**Theorem.** There is $c'>0$ with
$$\frac{G^{[\gamma]}_k(\sigma_c)}{G_k(\sigma_c)}=\frac1{|\Gamma|}+O(e^{-c'k}).$$

**Depends on:** ANS-T35, ANS-T23a.

## ANS-T42: Typical-history laws

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v007, lines 100-100, 104-109. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v007): Typical histories: log Q ~ log X, log K = o(log X), depth ~ log X / lambda_c, block frequencies -> product of r_N^(-sigma_c)

**Statement as recorded:**

**Theorem.** Let $\mathcal E$ be a set of words whose part of depth $k$ has $\nu$-probability at most $Ce^{-bk}$. Then the number of words of $\mathcal E$ counted by $H(X)$ is $O(X^{\sigma-\varepsilon})=o(H(X))$.

**Corollary.** Choose $w$ uniformly among the words counted by $A(X)$ (or by $N_x(X)$) and put $\lambda_c=\sum_Nr_N^{-\sigma}\log r_N=-B'(\sigma_c)=2.96846\ldots$. Then, in probability as $X\to\infty$:

1. $\log Q(w)/\log X\to1$ and $\log E(w)/\log X\to1$;
2. $\log K(w)/\log X\to0$;
3. $|w|/\log X\to1/\lambda_c=0.33687\ldots$;
4. the frequency of every finite block $v=(v_1,\dots,v_\ell)$ in $w$ tends to $\prod_ir_{v_i}^{-\sigma_c}$; in particular the letter $N$ has asymptotic share $r_N^{-\sigma_c}$.

**Depends on:** ANS-T37.

## ANS-T43: Limit law of normalized endpoints

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v008, lines 110-110. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v008): Endpoint / X tends to the Beta(sigma_c, 1) law in the populations A, N_x, C

**Statement as recorded:**

**Theorem.** Choose a history uniformly in the population counted by $A(X)$, $N_x(X)$ or $C(X)$, and let $y$ be its endpoint ($E(w)$, $xQ(w)$, or $n$). Then $y/X$ converges in distribution to the law with density $\sigma_cu^{\sigma_c-1}$ on $(0,1)$. Equivalently $\log(X/y)$ tends to an exponential variable of rate $\sigma_c$.

**Depends on:** ANS-T40, ANS-T41.

## ANS-T44: Joint limit law of sector, replication factor and endpoint

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v008, lines 116-117. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v008): Sector, replication factor and endpoint become independent: uniform, zeta, beta

**Statement as recorded:**

**Theorem.** For a finite quotient $\Gamma$ and the sector $\varphi(Q(w))$: in the populations $A$ and $N_x$ the pair (sector, $y/X$) tends to independent variables, uniform on $\Gamma$ and of density $\sigma_cu^{\sigma_c-1}$. In the population $C$, writing the history uniquely as $(m,w)$ with source $mK(w)$ and endpoint $mE(w)$,
$$\Pr\Big(m=j,\ \varphi(Q)=\gamma,\ \frac yX\le u\Big)\to\frac{j^{-\sigma_c}}{\zeta(\sigma_c)}\cdot\frac1{|\Gamma|}\cdot u^{\sigma_c}.$$

**Depends on:** ANS-T37, ANS-T40, ANS-T41.

## ANS-T42a: Concentration bounds for typical histories

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v008, lines 125-127. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v008): Concentration of multiplier deficit, depth and block frequencies, exceptional proportion exp(-c (log X)^(1/sigma_c))

**Statement as recorded:**

**Theorem.** Let $H=A$ or $N_x$, $L=\log X$, $\beta=1/\sigma_c$. For every finite block $v$ there are $D,c>0$ such that, outside a proportion $e^{-cL^\beta}$ of the counted words,
$$L-\log Q(w)\le DL^\beta,\qquad\Big|\,|w|-\frac L{\lambda_c}\Big|\le DL^{(1+\beta)/2},\qquad|f_v(w)-\nu_c(v)|\le DL^{-(1-\beta)/2}.$$
Consequently $\log K(w)\le DL^\beta$ outside the same proportion for $H=A$.

**Depends on:** ANS-T24a. **Classical inputs:** Bernstein.

# E. Fixed depth: continuation and counting

## ANS-T32: Fixed-depth counting asymptotic and the constants kappa_k

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. Valid after a correction to the limiting step, which has been applied.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v005, lines 90-94. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v005): A_k(X) ~ kappa_k sqrt(X) log^(k-1) X / (2^(k-1) (k-1)!), kappa_k finite with Euler product

**Statement as recorded:**

Let $A_k(X)=\#\{w:|w|=k,\ E(w)\le X\}$. Let $N_1,\dots,N_k$ be independent and Haar-uniform in $\hat{\mathbb Z}$; define $e_{p,0}=0$, $e_{p,i}=2v_p(N_i+1)+\max\{e_{p,i-1}-v_p(N_i),0\}$, and $g_i=\prod_pp^{\min(e_{p,i-1},\,v_p(N_i))}$. Put
$$\kappa_k=\mathbb E\,\sqrt{g_2g_3\cdots g_k}=\prod_pc_p(k),\qquad c_p(k)=\mathbb E\,p^{\frac12\sum_{i\le k}\min(e_{p,i-1},\,v_p(N_i))}.$$

**Theorem.** For every $k\ge1$, $\kappa_k$ is finite and
$$A_k(X)\sim\frac{\kappa_k}{2^{k-1}(k-1)!}\,\sqrt X\,(\log X)^{k-1}.\qquad(5)$$

**Depends on:** no earlier result cited. **Used by:** ANS-C1, ANS-T32a, ANS-T34, ANS-T34a.

**Relations:** ANS-T34a refines ANS-T32.

## ANS-C1: Real limit at one half (v001 conjecture, now corollary)

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v005, lines 96-96. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v005): (2 sigma - 1)^k G_k(sigma) -> kappa_k (conjectured in v001; corollary of T32)

**Statement as recorded:**

**Corollary (ANS-C1, now proved).** $(2\sigma-1)^kG_k(\sigma)\to\kappa_k$ as $\sigma\downarrow\tfrac12$.

**Depends on:** ANS-T32.

## ANS-T32a: Local coupling asymptotic of c_p(k)

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v006, lines 15-18, 28-28. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v006): c_p(k) = 1 + C(k,2) p^-3/2 + C(k,3) p^-2 + O_k(p^-5/2)

**Statement as recorded:**

**Theorem.** For every fixed $k\ge1$, as $p\to\infty$,
$$c_p(k)=1+\binom k2p^{-3/2}+\binom k3p^{-2}+O_k(p^{-5/2}).$$

The first term and the method are those of the review note; the $p^{-2}$ term is added here.

**Corollary.** $\displaystyle\log\kappa_k=\sum_{p\le P}\log c_p(k)+\binom k2\sum_{p>P}p^{-3/2}+\binom k3\sum_{p>P}p^{-2}+O_k(P^{-3/2}).$

**Depends on:** ANS-T32.

## ANS-T34: Every G_k is meromorphic on Re s > 1/3

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v008, lines 15-21, 68-68. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v008): Every G_k (and every source-restricted G_k(s;D)) is meromorphic on Re s > 1/3; only pole at 1/2, of order k (exactness for D > 1: v009, T34b)

**Statement as recorded:**

For $D\ge1$ let
$$G_k(s;D)=\sum_{|w|=k,\ D\mid K(w)}E(w)^{-s},$$
so that $G_k(s;1)=G_k(s)$ and $G_0(s;D)=[D=1]$. The sum converges absolutely for $\operatorname{Re}s>1/2$ (T12). Put $\sigma=\operatorname{Re}s$, $\mu=\min(2\sigma,1)$, $H_k(s;D)=(2s-1)^kG_k(s;D)$, $J_s(d)=\sum_{e\mid d}\mu_{\rm M}(e)(d/e)^s$ (here $\mu_{\rm M}$ is the Möbius function) and $\rho(d)=\prod_pp^{\lceil v_p(d)/2\rceil}$, so that $d\mid a^2$ exactly when $\rho(d)\mid a$.

**Theorem.** For every $k\ge0$ and $D\ge1$, $H_k(\cdot\,;D)$ is holomorphic on $1/3<\sigma<3/4$. On every closed substrip $\frac13+\delta\le\sigma\le\frac34-\delta$ and for every $\varepsilon>0$,
$$|H_k(s;D)|\le M\,(1+|\operatorname{Im}s|)^{2k}\,D^{-\mu+\varepsilon},$$
with $M=M(k,\delta,\varepsilon)$.

**Corollary 1.** For every $k\ge1$ the function $G_k$ is meromorphic on $\operatorname{Re}s>1/3$. Its only singularity is a pole at $s=1/2$ of order exactly $k$, with $(2s-1)^kG_k(s)\to\kappa_k$. In particular every other point of the line $\operatorname{Re}s=1/2$ is regular.

**Depends on:** ANS-T12, ANS-T32. **Used by:** ANS-T34a, ANS-T34b, ANS-T45, ANS-T46k, ANS-T46m.

**Relations:** ANS-T34b completes the exactness of ANS-T34.

## ANS-T34a: Full counting polynomial with power saving

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v008, lines 74-75. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v008): A_k(X) = sqrt(X) P_{k-1}(log X) + O(X^(1/2 - 1/(6(k+2)) + eps))

**Statement as recorded:**

**Corollary 2 (ANS-T34a).** For every $k\ge1$ there is a polynomial $P_{k-1}$ of degree $k-1$, with leading coefficient $\kappa_k/(2^{k-1}(k-1)!)$, such that
$$A_k(X)=\sqrt X\,P_{k-1}(\log X)+O_{k,\varepsilon}\Big(X^{\frac12-\frac1{6(k+2)}+\varepsilon}\Big).$$

**Depends on:** ANS-T34, ANS-T32.

**Relations:** ANS-T34a refines ANS-T32.

## ANS-T34b: Exact pole order k at one half for every restriction

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v009, lines 15-15. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v009): Pole of G_k(s;D) at 1/2 has order exactly k, for every D

**Statement as recorded:**

**Theorem.** For all $k\ge1$, $D\ge1$, the pole of $G_k(s;D)$ at $1/2$ has order exactly $k$, and $\lim_{s\to1/2}(2s-1)^kG_k(s;D)\ge1/D$.

**Depends on:** ANS-T34.

**Relations:** ANS-T34b completes the exactness of ANS-T34.

# F. Depth two

## ANS-T13: Depth-two double pole and counting asymptotic

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid. Uses the classical Delange theorem.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Release not frozen: Windows acceptance pending.

**Source:** ANS-I v001, lines 144-151. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v001): Depth-two double pole, constant kappa, A_2(X) ~ (kappa/2) sqrt(X) log X

**Statement as recorded:**

**Theorem.** $G_1(s)=\zeta(2s)-1$ and
$$G_2(s)=\sum_{a,b\ge1}\left[\frac{\gcd((a+1)^2,b)}{(a+1)^2(b+1)^2}\right]^{s}.$$
With $J_s(d)=\sum_{e\mid d}\mu(e)(d/e)^s$, $c(d)=\prod_pp^{\lceil v_p(d)/2\rceil}$ and the Hurwitz zeta function $\zeta(\cdot,\cdot)$,
$$G_2(s)=\sum_{d\ge1}\frac{J_s(d)}{d^{2s}}\,\zeta\!\left(2s,1+\tfrac1d\right)\Big(\frac{\zeta(2s)}{c(d)^{2s}}-[d=1]\Big).$$
The right side continues $G_2$ meromorphically to $\operatorname{Re}s>1/3$ with a single pole, at $s=1/2$, of order two, and $G_2(s)\sim\dfrac{\kappa}{4(s-1/2)^2}$, where
$$\kappa=\prod_p\Big(1+(1-p^{-1/2})\sum_{j\ge1}p^{-j/2-\lceil j/2\rceil}\Big)\approx1.8536 .$$
Consequently the number of depth-two words with minimal endpoint at most $X$ satisfies
$$A_2(X)\sim\frac{\kappa}{2}\sqrt X\log X .$$

**Depends on:** ANS-T03. **Classical inputs:** Delange.

## ANS-T05: Depth-two representation and continuation

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Release not frozen: Windows acceptance pending.

**Source:** ANS-I v001, lines 144-151. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v001): Depth-two double sum, Hurwitz representation, continuation to Re s > 1/3

**Statement as recorded:**

**Theorem.** $G_1(s)=\zeta(2s)-1$ and
$$G_2(s)=\sum_{a,b\ge1}\left[\frac{\gcd((a+1)^2,b)}{(a+1)^2(b+1)^2}\right]^{s}.$$
With $J_s(d)=\sum_{e\mid d}\mu(e)(d/e)^s$, $c(d)=\prod_pp^{\lceil v_p(d)/2\rceil}$ and the Hurwitz zeta function $\zeta(\cdot,\cdot)$,
$$G_2(s)=\sum_{d\ge1}\frac{J_s(d)}{d^{2s}}\,\zeta\!\left(2s,1+\tfrac1d\right)\Big(\frac{\zeta(2s)}{c(d)^{2s}}-[d=1]\Big).$$
The right side continues $G_2$ meromorphically to $\operatorname{Re}s>1/3$ with a single pole, at $s=1/2$, of order two, and $G_2(s)\sim\dfrac{\kappa}{4(s-1/2)^2}$, where
$$\kappa=\prod_p\Big(1+(1-p^{-1/2})\sum_{j\ge1}p^{-j/2-\lceil j/2\rceil}\Big)\approx1.8536 .$$
Consequently the number of depth-two words with minimal endpoint at most $X$ satisfies
$$A_2(X)\sim\frac{\kappa}{2}\sqrt X\log X .$$

**Depends on:** ANS-T03. **Used by:** ANS-T45.

**Relations:** ANS-T45 continues further than ANS-T05.

## ANS-T45: Depth two to Re s > 1/5 with a simple pole at 1/3

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v008, lines 87-91. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v008): G_2 meromorphic on Re s > 1/5, poles only at 1/2 (double) and 1/3 (simple); second term in smoothed form

**Statement as recorded:**

**Theorem.** On $\sigma>0$ let
$$F_2(s)=\sum_{d\ge1}\frac{J_s(d)}{(d\,\rho(d))^{2s}}\Big(\zeta\big(2s,1+\tfrac1d\big)-\zeta(2s)\Big),\qquad H(s)=\prod_p\Big(1-\frac{p^{-5s}+p^{-6s}}{1+p^{-2s}}\Big)\quad(\sigma>\tfrac15).$$
Then
$$G_2(s)=\zeta(2s)\Big(\zeta(2s)\,\zeta(3s)\,H(s)+F_2(s)-1\Big)+1.$$
So $G_2$ is meromorphic on $\operatorname{Re}s>1/5$, with poles only at $s=1/2$ (order two) and $s=1/3$ (simple, residue $\zeta(2/3)^2H(1/3)/3\ne0$).

**Depends on:** ANS-T05, ANS-T34. **Used by:** ANS-T45a, ANS-T45b, ANS-T46b, ANS-T46k, ANS-T46s.

**Relations:** ANS-T45 continues further than ANS-T05; ANS-T45a extends ANS-T45.

## ANS-T45a: Depth two: meromorphic on Re s > 0 with natural boundary

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v009, lines 23-26. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v009): G_2 meromorphic on Re s > 0 with natural boundary Re s = 0 (uses Estermann)

**Statement as recorded:**

Put $\mathcal P(s)=\prod_p(1+p^{-2s}+p^{-3s})$. Since $1+p^{-3s}/(1+p^{-2s})=(1+p^{-2s}+p^{-3s})/(1+p^{-2s})$ and $\prod_p(1+p^{-2s})=\zeta(2s)/\zeta(4s)$, T45 can be written
$$G_2(s)=\zeta(2s)\,\zeta(4s)\,\mathcal P(s)+\zeta(2s)\big(F_2(s)-1\big)+1.\qquad(1)$$

**Theorem.** $G_2$ is meromorphic on $\operatorname{Re}s>0$, and the line $\operatorname{Re}s=0$ is its natural boundary: it has no meromorphic continuation through any point of that line.

**Depends on:** ANS-T45. **Used by:** ANS-T46h-i. **Classical inputs:** Estermann.

**Relations:** ANS-T45a extends ANS-T45.

## ANS-T45b: Depth two: zeta factorisation and real poles to 1/12

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v009, lines 58-62, 67-67. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v009): Zeta factorisation of H up to Re s > 1/12; real poles of G_2 there at 1/2, 1/3, 1/7, 1/8

**Statement as recorded:**

With $z=p^{-s}$ the local factor of $H$ is $1-(z^5+z^6)/(1+z^2)$, and as power series
$$1-\frac{z^5+z^6}{1+z^2}=(1-z^5)(1-z^6)(1-z^7)^{-1}(1-z^8)^{-1}(1-z^9)(1-z^{10})\,\big(1+O(z^{12})\big).$$
(Coefficients computed exactly.) Hence, with $H_{12}$ the Euler product of the last factor, absolutely convergent and holomorphic on $\operatorname{Re}s>1/12$,
$$H(s)=\frac{\zeta(7s)\,\zeta(8s)}{\zeta(5s)\,\zeta(6s)\,\zeta(9s)\,\zeta(10s)}\,H_{12}(s),$$
$$G_2(s)=\zeta(2s)^2\zeta(3s)\,H(s)+\zeta(2s)\big(F_2(s)-1\big)+1.\qquad(3)$$

**Theorem.** On the real segment $s>1/12$ the poles of $G_2$ are at $1/2$ (double) and at $1/3$, $1/7$, $1/8$ (simple).

**Depends on:** ANS-T45. **Used by:** ANS-T38a, ANS-T45d.

## ANS-T45d: Depth two: exact pole divisor on Re s > 0

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v010, lines 27-33, 35-38, 52-52. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v010): Exact pole divisor of G_2 on Re s > 0; all real poles; all non-real poles under RH

**Statement as recorded:**

Let $h(z)=1-(z^5+z^6)/(1+z^2)=(1-z^3)(1+z^2+z^3)/(1+z^2)$ be the local factor of $H$, and define integers $c_n$ by
$$h(z)=\prod_{n\ge1}(1-z^n)^{-c_n}.\qquad(1)$$
Put $e_2=c_2+2$, $e_3=c_3+1$ and $e_n=c_n$ otherwise. Since $c_1=\dots=c_4=0$ we have $e_1=e_4=0$, $e_2=2$, $e_3=1$. For $M\ge4$ let $H_{M+1}=H\prod_{n\le M}\zeta(ns)^{-c_n}$. Its local factor $h(z)\prod_{n\le M}(1-z^n)^{c_n}$ is analytic in $|z|<1$ and equals $1+O(z^{M+1})$, so the product converges absolutely and locally uniformly on $\operatorname{Re}s>1/(M+1)$. There, by v009 (3),
$$G_2(s)=\mathcal M(s)+\mathcal A(s),\qquad\mathcal M=\prod_{2\le n\le M}\zeta(ns)^{e_n}\,H_{M+1},\qquad\mathcal A=\zeta(2s)(F_2-1)+1,\qquad(2)$$
and $\mathcal A$ is holomorphic on $\operatorname{Re}s>0$ apart from a simple pole at $1/2$.

For a complex number $w$ let $\mu(w)$ be the multiplicity of $w$ as a zero of $\zeta$ ($0$ if $\zeta(w)\ne0$). For $s_0$ with $\operatorname{Re}s_0>0$ let $\delta(s_0)=1$ if $1+p^{-2s_0}+p^{-3s_0}=0$ for some prime $p$, and $0$ otherwise.

**Theorem.** (i) The poles of $G_2$ on the half-line $s>0$ are exactly the points $1/n$ with $e_n>0$, and the order at $1/n$ is $e_n$.

(ii) For non-real $s_0$ with $\sigma_0=\operatorname{Re}s_0>0$, the order of the pole of $G_2$ at $s_0$ is $\max(0,-\nu(s_0))$, where
$$\nu(s_0)=\sum_{2\le n<1/\sigma_0}e_n\,\mu(ns_0)+\delta(s_0).$$

**Corollary 2.** Assume the Riemann hypothesis. The non-real poles of $G_2$ in $\operatorname{Re}s>0$ are exactly the points $\rho/n$, with $\rho$ a non-trivial zero and $e_n<0$, and the order is $|e_n|\mu(\rho)$.

**Depends on:** ANS-T45b. **Used by:** ANS-T38d, ANS-T38e, ANS-T45c. **Classical inputs:** Riemann hypothesis only where stated.

Corollary 2 (the non-real poles) assumes the Riemann hypothesis; the theorem itself does not.

## ANS-T45c: Depth two: pole of order two at 1/12

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v010, lines 44-50. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v010): G_2 has a pole of order two at 1/12

**Statement as recorded:**

**Corollary 1 (ANS-T45c, UNNS Research Collective review).** $G_2$ has a pole of order exactly two at $1/12$: $c_{12}=2$.

The first real poles and their orders are:

| $n$ | 2 | 3 | 7 | 8 | 12 | 13 | 17 | 18 | 21 | 22 | 23 | 26 | 27 | 28 |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| order at $1/n$ | 2 | 1 | 1 | 1 | 2 | 1 | 3 | 2 | 1 | 6 | 2 | 4 | 13 | 3 |

**Depends on:** ANS-T45d.

## ANS-T45e: Depth two: asymptotics and sign densities of the Euler exponents

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v010, lines 70-76. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v010): Asymptotic formula for the exponents c_n; each sign has density 1/2; unbounded pole orders

**Statement as recorded:**

Let $\alpha$ be a non-real root of $x^3+x+1$, put $R=|\alpha|=\beta^{1/2}=1.2106\ldots$ and $\theta=\arg\alpha$, and let $p_N$ be the sum of the $N$-th powers of the three roots.

**Theorem.** (i) $n\,c_n=\sum_{d\mid n}\mu_{\rm M}(n/d)\,A_d$, where $\mu_{\rm M}$ is the Möbius function and
$$A_N=-p_N-3\,[3\mid N]+2(-1)^{N/2}[2\mid N].$$
(ii) $n\,c_n=-2R^n\cos n\theta+O(\tau(n)R^{n/2})$.

(iii) The sets $\{n:e_n<0\}$ and $\{n:e_n>0\}$ both have natural density $\tfrac12$.

**Depends on:** no earlier result cited. **Used by:** ANS-T45f.

## ANS-T45f: Depth two: arcsine law of the normalised exponents

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v011, lines 17-19. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v011): Arcsine limit law of the normalised Euler exponents

**Statement as recorded:**

**Theorem.** Put $Y_n=ne_n/(2R^n)$. For $-1\le a<b\le1$,
$$\lim_{N\to\infty}\frac1N\#\{n\le N:\ a\le Y_n\le b\}=\frac{\arcsin b-\arcsin a}\pi.$$
In particular the set where $|e_n|>R^n/n$ has density $\tfrac23$, split equally between the two signs.

**Depends on:** ANS-T45e. **Classical inputs:** Weyl equidistribution.

## ANS-T38d: Depth two: vertical pole family for every negative exponent

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v010, lines 58-58. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v010): Vertical pole family at rho/n for every n with e_n < 0

**Statement as recorded:**

**Theorem.** Let $n\ge2$ with $e_n<0$. For all but $O_n(U)$ zeros $\rho=\tfrac12+i\gamma$, $0<\gamma\le U$, the point $\rho/n$ is a pole of $G_2$ of order exactly $|e_n|\,\mu(\rho)$.

**Depends on:** ANS-T45d. **Used by:** ANS-T38b, ANS-T38c, ANS-T38e. **Classical inputs:** Bohr-Landau.

**Relations:** ANS-T38d generalizes ANS-T38a; ANS-T38d generalizes ANS-T38b.

## ANS-T38a: Depth two: poles at one fifth of zeta zeros

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v009, lines 73-73. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v009): G_2 has poles at rho/5 for zeta zeros rho on the critical line outside a set of smaller order; >> T log T poles on Re s = 1/10 (uses Selberg, Bohr-Landau)

**Statement as recorded:**

**Theorem.** Let $\rho=\tfrac12+i\gamma$ be a zero of $\zeta$ of multiplicity $m$ with $\zeta(n\rho/5)\ne0$ for $n=2,3,6,7,8,9$. Then $G_2$ has a pole of order exactly $m$ at $\rho/5$. Consequently the number of distinct poles of $G_2$ on $\operatorname{Re}s=1/10$ with $|\operatorname{Im}s|\le T$ is $\gg T\log T$.

**Depends on:** ANS-T45b. **Classical inputs:** Selberg, Bohr-Landau.

**Relations:** ANS-T38d generalizes ANS-T38a.

## ANS-T38b: Depth two: poles at one sixth of zeta zeros

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v010, lines 62-62. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v010): Poles at rho/6 for all but O(T) critical-line zeros

**Statement as recorded:**

The cases $n=5$ (T38a) and $n=6$ (T38b, UNNS Research Collective review) have $e_n=-1$.

**Depends on:** ANS-T38d.

**Relations:** ANS-T38d generalizes ANS-T38b.

## ANS-T38c: Depth two: lower bounds for the number of poles

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v010, lines 64-64. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v010): At least (n/(5 pi)) T log T poles of order exactly abs(e_n) on Re s = 1/(2n) when e_n < 0 (uses Conrey)

**Statement as recorded:**

**Corollary (ANS-T38c; the method is the UNNS Research Collective's).** The number of poles of $G_2$ of order exactly $|e_n|$ on $\operatorname{Re}s=1/(2n)$ with $0<\operatorname{Im}s\le T$ is at least $\big(\tfrac{n}{5\pi}+o(1)\big)T\log T$. In particular $\rho/5$ and $\rho/6$ give at least $(1/\pi+o(1))T\log T$ and $(6/(5\pi)+o(1))T\log T$ **simple** poles.

**Depends on:** ANS-T38d. **Classical inputs:** Conrey.

## ANS-T38e: Depth two: pole populations on the lines Re s = 1/(2n)

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v011, lines 25-29. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v011): Number of distinct poles of G_2 on Re s = 1/(2n), for fixed n

**Statement as recorded:**

Let $N_0^*(T)$ count the distinct zeros $\tfrac12+i\gamma$ of $\zeta$ with $0<\gamma\le T$, and $P_n(T)$ the distinct poles of $G_2$ on $\operatorname{Re}s=1/(2n)$ with $0<\operatorname{Im}s\le T$.

**Theorem.** For each fixed $n\ge1$,
$$P_n(T)=\begin{cases}N_0^*(nT)+O_n(T),&e_n<0,\\O_n(T),&e_n\ge0.\end{cases}$$
Hence $P_n(T)\asymp_nT\log T$ when $e_n<0$.

**Depends on:** ANS-T45d, ANS-T38d. **Classical inputs:** Selberg, Bohr-Landau.

# G. Depth three

## ANS-T46c: Linked-letter model: only a simple pole at 1/3

**Proof status:** PROVED (model). **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v010, lines 90-95. **Scope:** Selected nesting grammar. **Literature priority:** Classical shifted divisor sum; no novelty claimed.

**Release table summary** (ANS-I/v010): Model series with a letter linked on both sides: only a simple pole at 1/3 (classical shifted divisor sum)

**Statement as recorded:**

In the mechanism of v009 §3, a middle letter $M$ may receive a prime $q$ from the first letter ($q\mid M$) and send a prime $r$ to the last ($r\mid M+1$). The weights are about $q^{-s}$ and $r^{-s}$. This leads to the series
$$U(s)=\sum_{M\ge1}M^{-2s}\sigma_{-s}(M)\,\sigma_{-s}(M+1),\qquad\sigma_{-s}(M)=\sum_{d\mid M}d^{-s},$$
absolutely convergent for $\operatorname{Re}s>1/2$. It is a **model**: $G_3$ also contains Möbius corrections, the link from the first letter to the last, and the interaction of the three gcds. Counting each link separately suggests two factors $\zeta(3s)$.

**Theorem.** $U$ is meromorphic on $\operatorname{Re}s>3/10$. Its poles there are simple poles at $1/2$ and $1/3$, and
$$\operatorname{Res}_{s=1/3}U=\frac{2\,\zeta(2/3)\,\zeta(4/3)}{3\,\zeta(2)}\ne0.$$

**Depends on:** no earlier result cited. **Used by:** ANS-T46f, ANS-T46j. **Classical inputs:** Ingham-Estermann, Weil bound, Shparlinski.

A model series, not the depth-three function.

## ANS-T46f: Linked-letter model: residue at one half

**Proof status:** PROVED (model). **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v011, lines 37-37. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v011): Residue of the linked-letter model at 1/2

**Statement as recorded:**

**Theorem.** $\operatorname{Res}_{s=1/2}U=\zeta(3/2)^2/(2\zeta(3))$.

**Depends on:** ANS-T46c.

A model series, not the depth-three function.

## ANS-T46d: Depth three: exact decomposition for Re s > 1/2

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v011, lines 45-46, 49-56, 60-65. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v011): Exact decomposition of G_3: depth-two factor, a shifted series V, a remainder R, minus G_2 (Re s > 1/2)

**Statement as recorded:**

Write a word of length three as $(a-1,\,M,\,N)$ and put $b=M+1$, $c=N+1$, with $a,b,c\ge2$. Then
$$E=\frac{(abc)^2}{g_1g_2},\qquad g_1=\gcd(N,b^2),\qquad g_2=\gcd\Big(\frac{MN}{g_1},\,a^2\Big).\qquad(1)$$

Let $z=p^{-s}$. Define $\Phi(K)=\sum_{d\mid K}J_s(d)\,\rho(d)^{-2s}$, a multiplicative function with
$$\Phi(p^v)=1+(1-z)\Big(\Big\lfloor\frac v2\Big\rfloor+\Big\lceil\frac v2\Big\rceil z\Big).$$
Define $w_1,w_2$ multiplicative, with $w_i(1)=1$ and for exponents $\ge1$
$$w_1(p^\mu)=\frac{\Phi(p^\mu)+c_\mu}{L_0},\qquad w_2(p^\beta)=\frac{1+z-z^{2\beta+1}/(1+z^2)}{L_0},\qquad L_0=\frac{1+z^2+z^3}{1+z^2},\qquad(2)$$
where $c_\mu=z^3/(1+z^2)$ for even $\mu$ and $c_\mu=z^2(1-z+z^2)/(1+z^2)$ for odd $\mu$. On primes the two weights agree:
$$w_1(p)=w_2(p)=\frac{1+z+z^2}{1+z^2+z^3}.$$
Put
$$V(s)=\sum_{M\ge1}(M+1)^{-2s}\,w_1(M)\,w_2(M+1).$$

For fixed $M$ let $f(N)=g_1^{\,s}\,\Phi(MN/g_1)$, let $\Lambda_M=\mu_{\rm M}*f$ be its Möbius transform, and let
$$R(s)=\sum_{M\ge1}(M+1)^{-2s}\sum_{k\ge1}\Lambda_M(k)\,k^{-2s}\,\Delta(s,k),\qquad\Delta(s,k)=\zeta\big(2s,1+\tfrac1k\big)-\zeta(2s).$$

**Theorem.** For $\operatorname{Re}s>1/2$,
$$\boxed{\,G_3(s)=\zeta(2s)^2\,\zeta(3s)\,H(s)\,V(s)+\zeta(2s)\,R(s)-G_2(s)\,}$$
where $\zeta(3s)H(s)=\prod_pL_0$ is the Euler product of depth two.

**Depends on:** no earlier result cited. **Used by:** ANS-T46e, ANS-T46e-i, ANS-T46g, ANS-T46k.

## ANS-T46e-i: Depth three: positivity of E1, E2 and the implication for the pole

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v011, lines 98-103, 111-113. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v011): E1 and E2 are positive; T46e implies a pole of order exactly two of G_3 at 1/3

**Statement as recorded:**

Take $s=\tfrac13$, write $\kappa_i=\mu_{\rm M}*w_i$, and define for each prime, with $x=p^{-2/3}$ and $y=p^{-1}$,
$$W_i(t)=\sum_{j\ge0}w_i(p^j)\,t^j,\qquad E_{1,p}=(1-y)(1-x)W_1(x)+(1-z^2)\big((1-y)W_2(y)-1\big),$$
$E_{2,p}$ with the indices exchanged, and $E_i=\prod_pE_{i,p}$.

**Positivity (proved).** $E_1,E_2$ converge to positive numbers. From (2), $w_1(p^\mu)\ge1$, since $\Phi(p^\mu)\ge1$ and $c_\mu-(L_0-1)$ is $0$ or $z^2(1-z)^2/(1+z^2)$; and $w_2(p^\beta)\ge1$, since the numerator minus $L_0$ is $(z-z^{2\beta+1})/(1+z^2)$. So $(1-y)W_i(y)\ge1$ and each $E_{i,p}>0$. Expanding the closed forms in $z=p^{-1/3}$ gives $E_{i,p}=1+O(z^4)$.

**Proposition (proved implication).** If ANS-T46e holds, $G_3$ has a pole of order exactly two at $1/3$ and
$$\lim_{s\to1/3}\big(s-\tfrac13\big)^2G_3(s)=\frac{\zeta(2/3)^2\,H(1/3)\,r_V}3\ne0.$$
So T46b holds for $k=3$.

**Depends on:** ANS-T46d. **Used by:** ANS-T46e.

**Relations:** ANS-T46e discharges the hypothesis of ANS-T46e-i.

## ANS-T46g: Depth three: square-divisor convolution identities

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v012, lines 17-24. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v012): Exact convolution identities for w1, w2 (square-divisor extraction)

**Statement as recorded:**

Let $z=p^{-s}$, $P(z)=1+z^2+z^3$, $A=z(1-z^2)/P$, $B=(1-z)(1+z^3)/P$. The UNNS Research Collective's identities
$$w_1(p^{2j+1})-w_1(p^{2j})=A,\quad w_1(p^{2j+2})-w_1(p^{2j+1})=B,\quad w_2(p^j)-w_2(p^{j-1})=Az^{2j-2}$$
$(j\ge0$, resp. $j\ge1)$ are **valid**: they follow from (2) of v011, and were checked symbolically. Hence $w_1=\sigma_{-s}*I_\square*r_{1}$ and $w_2=\sigma_{-s}*r_2$ with the stated local factors. Put $q_1=I_\square*r_1$, so that $w_1=\sigma_{-s}*q_1$, with local series
$$Q(t)=\frac{(1-zt)\big(1+At+(B-1)t^2\big)}{1-t^2},\qquad R_2(t)=(1-zt)\Big(1+\frac{At}{1-z^2t}\Big).\qquad(1)$$
For $j\ge1$ the coefficients are: $q_1(p)=A-z$; $q_1(p^j)=B-zA$ for even $j$ and $A-zB$ for odd $j\ge3$; $r_2(p)=A-z$; $r_2(p^j)=-A(1-z)z^{2j-3}$ for $j\ge2$. Consequently, uniformly in $\operatorname{Im}s$ for $\sigma$ in compact subsets of $(0.3,\infty)$ (where $P$ is bounded away from $0$),
$$|q_1(p)|,|r_2(p)|\le Cp^{-3\sigma},\qquad|q_1(p^j)|\le C,\qquad|r_2(p^j)|\le Cp^{-(2j-2)\sigma}\quad(j\ge2).\qquad(\mathrm H)$$

One qualification: the extra decay of the corrections is at primes. $q_1(p^2)\to1$, and $r_2(p^2)$ is only $O(p^{-2\sigma})$.

**Depends on:** ANS-T46d. **Used by:** ANS-T46e, ANS-T46h, ANS-T46i.

## ANS-T46h: Depth three: first remainder component continues past 1/3

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v012, lines 28-28. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v012): R_1 continues to Re s > 1/4; poles and residue at 1/3

**Statement as recorded:**

The UNNS Research Collective's factorisation $\sum\Phi(M)M^{-2s}=\zeta(2s)\zeta(3s)\zeta(4s)B_\Phi(s)$, the continuation of $R_1$ to $\sigma>\frac14$ and the residue at $1/3$ are **valid**.

**Depends on:** ANS-T46g. **Used by:** ANS-T46i.

Consolidation note: the releases record the factorisation behind this result as the UNNS Research Collective's and declare it valid without writing out a derivation. A derivation is in `PROVENANCE/AUDIT_v001.md`, section 5; the foundational audit of 27 November 2026 accepted it.

## ANS-T46h-i: Depth three: R_1 has a natural boundary

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. A normal-convergence clarification was requested and added in ANS-I v013.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v012, lines 30-30. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v012): R_1 meromorphic on Re s > 0 with natural boundary Re s = 0

**Statement as recorded:**

**Strengthening (ANS-T46h-i).** $R_1$ is meromorphic on $\sigma>0$, and the line $\sigma=0$ is a natural boundary.

**Depends on:** ANS-T45a. **Classical inputs:** Estermann.

## ANS-T46i: Depth three: remainder meromorphic on Re s > 2/7

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v012, lines 36-36. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v012): R meromorphic on Re s > 2/7; at most simple poles at 1/2, 1/3

**Statement as recorded:**

**Theorem.** $R$ is meromorphic on $\sigma>\frac27$. Its only possible singularities there are simple poles at $\frac12$ and $\frac13$.

**Depends on:** ANS-T46h, ANS-T46g. **Used by:** ANS-T46e. **Classical inputs:** convexity bounds for L-functions.

## ANS-T46j: Shifted series with square-supported weights

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. Two scope clarifications were requested and made in ANS-I v013.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v012, lines 65-72. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v012): Shifted series with weights satisfying (H): continuation to Re s > 1/3 - 1/1500 and residue at 1/3

**Statement as recorded:**

Let $q,r$ be multiplicative, with values holomorphic in $s$, satisfying (H) with $q_1,r_2$ replaced by $q,r$ for $\sigma>\frac13-\delta_0$, where $\delta_0=1/1500$; constants are uniform in $\operatorname{Im}s$ up to a power of $|s|$. Put $w_q=\sigma_{-s}*q$ and
$$V(s)=\sum_{M\ge1}(M+1)^{-2s}\,w_q(M)\,w_r(M+1).$$

**Theorem.** $V$ is meromorphic on $\sigma>\frac13-\delta_0$. Its only possible singularities there are simple poles at $\frac12$ and $\frac13$. With $\kappa_q=\mu_{\rm M}*w_q$ (so $\kappa_q(d)=\sum_{am=d}q(a)m^{-s}$), all quantities taken at $s=\frac13$,
$$\operatorname{Res}_{1/3}V=\frac{\zeta(2/3)}3\,(E_1+E_2),\qquad E_1=\sum_{(e,a)=1}\frac{\kappa_r(e)}{e}\prod_{p\mid e}(1-p^{-2/3})\cdot\frac{q(a)}{a^{2/3}},$$
and $E_2$ is the same with $q$ and $r$ exchanged.

The hypotheses hold for $q=q_1$, $r=r_2$ (the series of T46d), for $q=I_\square$, $r=\delta_1$ (the UNNS Research Collective's model $U_\square$), and for $q=r=\delta_1$ (the model of T46c).

**Depends on:** ANS-T46c. **Used by:** ANS-T46e, ANS-T46k-i. **Classical inputs:** Weil-Estermann.

## ANS-T46e: Depth three: continuation of V and R and the residue of V

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v012, lines 160-162. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v012): V and R continue past 1/3; residue of V is zeta(2/3)(E1+E2)/3 < 0

**Statement as recorded:**

**Theorem (ANS-T46e).** $V$ and $R$ of T46d continue meromorphically past $\frac13$, and
$$\operatorname{Res}_{1/3}V=r_V=\frac{\zeta(2/3)(E_1+E_2)}3<0,$$
with $E_1,E_2$ the Euler products of v011 §3.1. This is the residue conjectured there.

**Depends on:** ANS-T46d, ANS-T46g, ANS-T46i, ANS-T46j, ANS-T46e-i. **Used by:** ANS-T46k.

**Relations:** ANS-T46e discharges the hypothesis of ANS-T46e-i.

## ANS-T46k: Depth three: pole of order exactly two at 1/3

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v012, lines 168-170. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v012): G_3 meromorphic on Re s > 1/3 - 1/1500; pole of order exactly two at 1/3

**Statement as recorded:**

**Corollary (ANS-T46k).** $G_3$ is meromorphic on $\sigma>\frac13-\frac1{1500}$. Its only singularities there are the pole of order three at $\frac12$ and a pole of order **exactly two** at $\frac13$, with
$$\lim_{s\to1/3}\big(s-\tfrac13\big)^2G_3(s)=\frac{\zeta(2/3)^2\,H(1/3)\,r_V}3\approx-0.75916.$$
In particular ANS-T46b holds for $k=3$.

**Depends on:** ANS-T46d, ANS-T46e, ANS-T45, ANS-T34. **Used by:** ANS-T46b, ANS-T46l, ANS-T46s.

**Relations:** ANS-T46k-i widens the margin of ANS-T46k.

## ANS-T46l: Depth three: second term for smoothed counts

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v012, lines 174-176. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v012): Depth three: second term X^(1/3)(a log X + b) for smoothed counts

**Statement as recorded:**

**Corollary (smoothed second term).** For all large $m$ there are constants $b_m$ and $\eta>0$ with
$$\sum_{E\le X}\Big(1-\frac EX\Big)^m=\mathrm{Res}_{1/2}+X^{1/3}\big(a_m\log X+b_m\big)+O\big(X^{1/3-\eta}\big),$$
where the sum is over words of length three, $\mathrm{Res}_{1/2}$ is the residue of $G_3(s)X^s\,m!/(s(s+1)\cdots(s+m))$ at $\frac12$, and $a_m=\dfrac{\zeta(2/3)^2H(1/3)r_V}3\cdot\dfrac{m!}{\prod_{j=0}^m(\frac13+j)}\ne0$.

**Depends on:** ANS-T46k. **Classical inputs:** Perron-type smoothing.

## ANS-T46k-i: Depth three: continuation margin 1/200

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v013, lines 24-24. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v013): Continuation margin of G_3: Re s > 1/3 - 1/200

**Statement as recorded:**

**Proposition.** T46j, and therefore T46k and T46l, hold with $\delta_0=1/200$. So $G_3$ is meromorphic on $\sigma>\frac13-\frac1{200}$.

**Depends on:** ANS-T46j.

**Relations:** ANS-T46k-i widens the margin of ANS-T46k.

# H. Arbitrary depth at one third

## ANS-T46m: Every depth: decomposition by end letters

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v013, lines 42-57. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v013): Decomposition of every G_k (k >= 2, Re s > 1/2) by its end letters; weight depends on source and endpoint of the middle word

**Statement as recorded:**

For a word $\mu$ let $E(\mu)$ be its endpoint and $K(\mu)$ its minimal source; $E=K=1$ for the empty word. By T03 and the first-letter identity of v008,
$$E(x\,w)=\frac{(x+1)^2E(w)}{\gcd(K(w),(x+1)^2)},$$
and, with $g=\gcd(P,E(\mu))$,
$$E(\mu P)=\frac{(P+1)^2E(\mu)}g,\qquad K(\mu P)=\frac{PK(\mu)}g.$$
Here $E=\prod(x+1)^2/G$ and $K=\prod x/G$ with the same total gcd $G$, which gives the formula for $K(\mu P)$. Hence a word with first letter $a-1$, middle word $\mu$ and last letter $P$ has
$$E=\frac{a^2(P+1)^2E(\mu)}{g\,h},\qquad h=\gcd\Big(\frac{PK(\mu)}g,\;a^2\Big).\qquad(1)$$

Let $\Phi$, $L_0=(1+z^2+z^3)/(1+z^2)$ and $c_u=\sum_{i\ge1}\big(\Phi(p^{u+i})-\Phi(p^{u+i-1})\big)z^{2i}$ be as in v011, so that $c_u=z^3/(1+z^2)$ for even $u$ and $z^2(1-z+z^2)/(1+z^2)$ for odd $u$. For $u,v\ge0$ put
$$L(u,v)=\Phi(p^u)\,\big(1+z-z^{v+1}\big)+z^v\,c_u,\qquad\Omega(K,E)=\prod_p\frac{L(v_pK,\,v_pE)}{L_0}.\qquad(2)$$
Note $L(0,0)=L_0$. For $k\ge2$ define
$$M_k(s)=\sum_{|\mu|=k-2}E(\mu)^{-s}\,\Omega\big(K(\mu),E(\mu)\big),$$
and, with $f_\mu(P)=\gcd(P,E(\mu))^s\,\Phi\big(PK(\mu)/\gcd(P,E(\mu))\big)$ and $\Lambda_\mu=\mu_{\rm M}*f_\mu$,
$$R_k(s)=\sum_{|\mu|=k-2}E(\mu)^{-s}\sum_{q\ge1}\Lambda_\mu(q)\,q^{-2s}\,\Delta(s,q),\qquad\Delta(s,q)=\zeta\big(2s,1+\tfrac1q\big)-\zeta(2s).$$

**Theorem.** For every $k\ge2$ and $\sigma>\frac12$, with all series absolutely convergent,
$$\boxed{\,G_k(s)=\zeta(2s)^2\,\zeta(3s)\,H(s)\,M_k(s)\;+\;\zeta(2s)\,R_k(s)\;-\;G_{k-1}(s).\,}$$

**Depends on:** ANS-T03, ANS-T34, ANS-T12. **Used by:** ANS-T46n, ANS-T46p, ANS-T46q.

## ANS-T46n: Links active at one prime: maximum floor(k^2/4)

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v013, lines 75-77. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v013): Links active at one prime: at most floor(k^2/4); maximal role assignments

**Statement as recorded:**

Write a word as $x_1\cdots x_k$ and $a_i=x_i+1$. A prime $p$ activates the link $(i,j)$, $i<j$, when $p\mid a_i$ and $p\mid x_j$. Since $\gcd(x_i,a_i)=1$, at one prime a letter can supply ($p\mid a_i$, role S) or receive ($p\mid x_i$, role R), not both. So the sets of links active at one prime are contained in the sets $\{(i,j):i\in S,\ j\in R,\ i<j\}$ for assignments of roles.

**Proposition.** The largest such set has $\lfloor k^2/4\rfloor$ links. It requires all S letters to precede all R letters, with $\lfloor k/2\rfloor$ or $\lceil k/2\rceil$ letters of role S: one assignment for even $k$, two for odd $k\ge3$ (the first letter taken as S and the last as R).

**Depends on:** ANS-T46m.

## ANS-T46o: Model F_{r,t}: pole of order exactly rt at 1/3

**Proof status:** PROVED (model). **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v013, lines 103-108. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v013): Model F_{r,t}: meromorphic on Re s > 1/4, pole of order exactly rt at 1/3

**Statement as recorded:**

Keep only the links from $r$ supplying letters to $t$ later receiving letters:
$$F_{r,t}(s)=\sum_{a\in\mathbb N^r}\ \sum_{x\in\mathbb N^t}\ \prod_ia_i^{-2s}\prod_j(x_j+1)^{-2s}\,\gcd\Big(\prod_jx_j,\;\big(\prod_ia_i\big)^2\Big)^s.$$

**Theorem.** For $\sigma>\frac12$,
$$F_{r,t}(s)=\sum_{i=0}^t\zeta(2s)^{r+t-i}\,\zeta(3s)^{r(t-i)}\,Q_i(s),$$
with every $Q_i$ holomorphic on $\sigma>\frac14$. Hence $F_{r,t}$ is meromorphic there, with poles only at $\frac12$, of order exactly $r+t$, and at $\frac13$, of order **exactly $rt$**. Moreover $Q_0(\frac13)>0$, and $\lim_{s\to1/3}(s-\frac13)^{rt}F_{r,t}=\zeta(\frac23)^{r+t}\,Q_0(\frac13)\,3^{-rt}$.

**Depends on:** no earlier result cited. **Used by:** ANS-T46s.

A model series, not G_k.

## ANS-T46p: Conditions implying pole order floor(k^2/4)

**Proof status:** PROVED (implication). **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v013, lines 131-131. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v013): Conditions on M_k, R_k, G_{k-1} that imply T46b at depth k

**Statement as recorded:**

**Proposition (ANS-T46p, proved implication).** Let $k\ge3$. Suppose $M_k$ and $R_k$ continue meromorphically to a neighbourhood of $\frac13$, that $M_k$ has there a pole of order exactly $\lfloor k^2/4\rfloor-1$, and that the pole order of $R_k$ is less than $\lfloor k^2/4\rfloor$. Suppose also that $G_{k-1}$ continues there with pole order less than $\lfloor k^2/4\rfloor$. Then $G_k$ has a pole of order exactly $\lfloor k^2/4\rfloor$ at $\frac13$.

**Depends on:** ANS-T46m.

An implication; its hypotheses are not established for any k >= 4.

## ANS-T46r: Middle-word gcd identity and overlap decomposition

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v014, lines 47-52. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v014): Middle-word gcd identity and overlap decomposition of L(u,v)/L0

**Statement as recorded:**

**Theorem.** For a middle word $xy$ with $g=\gcd(y,(x+1)^2)$, $K=xy/g$ and $E=(x+1)^2(y+1)^2/g$:

(i) $\gcd(K,E)=\gcd\big(x,(y+1)^2\big)$.

(ii) With $L_0=L(0,0)=1+c_0$, for all $u,v\ge0$,
$$\frac{L(u,v)}{L_0}=\frac{L(u,0)}{L_0}\,\frac{L(0,v)}{L_0}+\frac{(1-z^v)(1+z)\,\big[\Phi(p^u)c_0-c_u\big]}{L_0^2}.$$

**Depends on:** ANS-T47.

## ANS-T46s: Role patterns: local expectation and agreement with proved coefficients

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v014, lines 62-69, 73-75, 87-87, 97-98, 106-107. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v014): (i) E_R(p)=1+L(R)/p+O(p^-4/3); (ii) formula equals proved coefficients k=2,3; (iii) and the model F_{r,t}

**Statement as recorded:**

Fix a prime $p$, put $x=p^{-2/3}$, $y=1/p$, $z=p^{-1/3}$. A letter $N$ has the two coprime coordinates $a=N+1$ and $N$. A **role pattern** $R\in\{{\sf S},{\sf R}\}^k$ gives each letter a dominant coordinate: $a$ for a supplying letter ${\sf S}$, $N$ for a receiving letter ${\sf R}$. Under the measure $\mathbb P_R$ the letters are independent, and for each letter

- the dominant coordinate has $p$-valuation $j\ge1$ with probability $(1-x)x^j$;
- the other coordinate has valuation $j\ge1$ with probability $(1-x)y^j$;
- otherwise both valuations are $0$.

(The three cases have total probability $1$ for every $p$.) Let $T$ be the $p$-valuation of the total gcd $G$ of the word and put
$$\mathcal E_R(p)=\mathbb E_R\big[p^{T/3}\big],\qquad L(R)=\#\{i<j:R_i={\sf S},\,R_j={\sf R}\}.$$

**Theorem (T46s-i).** $\mathcal E_R(p)=1+L(R)/p+O_k(p^{-4/3})$. Consequently
$$C_R=\prod_p\Big(1-\frac1p\Big)^{L(R)}\mathcal E_R(p)$$
converges absolutely and $C_R>0$.

**Lemma.** Let $R$ begin with ${\sf S}$ and end with ${\sf R}$, and let $(u,v)=(v_pK,v_pE)$ for the middle word. The expectation over the first and last letters of $p$ raised to one third of the two gcd exponents that involve them equals $L(u,v)$.

**Theorem (T46s-ii).** For $k=2,3$, with $\ell_k=\lfloor k^2/4\rfloor$,
$$\lim_{s\to1/3}\big(s-\tfrac13\big)^{\ell_k}G_k(s)=\zeta(\tfrac23)^k\,3^{-\ell_k}\sum_{L(R)=\ell_k}C_R.\qquad(\ast)$$

**Theorem (T46s-iii).** In the model $F_{r,t}$ of T46o, let the letters be independent with only their dominant coordinate, of law $(1-x)x^j$, and let $T=\min\big(2\sum\alpha_i,\sum\beta_j\big)$. Then
$$\lim_{s\to1/3}\big(s-\tfrac13\big)^{rt}F_{r,t}(s)=\zeta(\tfrac23)^{r+t}\,3^{-rt}\prod_p\Big(1-\frac1p\Big)^{rt}\mathbb E\big[p^{T/3}\big].$$

**Depends on:** ANS-T47, ANS-T45, ANS-T46k, ANS-T46o. **Used by:** ANS-T46t.

## ANS-T46b: Pole of order floor(k^2/4) at 1/3

**Proof status:** PROVED for k <= 3; CONJECTURE for k >= 4. **Review:** UNNS Research Collective review: valid. k = 2, 3 proved and reviewed (T45, T46k); k >= 4 conjecture.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v009, lines 87-89. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v014): Pole order floor(k^2/4)

**Statement as recorded:**

**Conjecture (ANS-T46b).** For $k\ge2$, $G_k$ has a pole at $s=1/3$ of order $\lfloor k^2/4\rfloor$.

This gives order $1$ at $k=2$ (proved, T45), order $2$ at $k=3$ and order $4$ at $k=4$. A proof needs (i) continuation past $1/3$, (ii) equidistribution, with a power saving, of the least elements above, which involves inverses modulo $P_{\rm out}$ and so estimates of Kloosterman type, and (iii) a non-vanishing check on the leading coefficient. The depth-three counts of v008 are compatible with order $2$ but do not test it.

**Depends on:** ANS-T45, ANS-T46k.

## ANS-T46q: Weighted middle-word sum: pole order floor(k^2/4)-1

**Proof status:** CONJECTURE (k = 2, 3 proved). **Review:** Not a proved result.

**Review record:** None. **Release and computation:** Archived release.

**Source:** ANS-I v013, lines 135-137. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v014): M_k has order floor(k^2/4)-1

**Statement as recorded:**

**Conjecture (ANS-T46q).** $M_k$ has a pole of order exactly $\lfloor k^2/4\rfloor-1$ at $\frac13$.

Since $\lfloor k^2/4\rfloor-1=\lfloor(k-2)^2/4\rfloor+(k-2)$, this says that the weight $\Omega$ raises the order of $G_{k-2}$ by one for each middle letter. It holds for $k=2$ ($M_2=1$) and $k=3$ (v012). This is the form in which depth four can now be tested, and it is a candidate for an induction on depth; no induction step is proved.

**Depends on:** ANS-T46m.

## ANS-T46t: General continuation, pole order floor(k^2/4) and leading coefficient at 1/3

**Proof status:** CONJECTURE (k = 2, 3 proved). **Review:** Not a proved result.

**Review record:** None. **Release and computation:** Archived release.

**Source:** ANS-I v015, lines 149-151. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v015): G_k: continuation near 1/3, order floor(k^2/4), leading coefficient

**Statement as recorded:**

Following the review: **for every $k\ge2$, $G_k$ continues meromorphically to a neighbourhood of $\frac13$, has there a pole of order exactly $\ell_k=\lfloor k^2/4\rfloor$, and its leading Laurent coefficient is**
$$\zeta(\tfrac23)^k\,3^{-\ell_k}\sum_{L(R)=\ell_k}C_R .$$
Status: CONJECTURE for $k\ge4$; proved for $k=2,3$ (T45, T46k, T46s-ii).

**Depends on:** ANS-T46s.

# I. Collective growth at and below s = 1

## ANS-T48: Growth of G_k at s = 1 of exact order log k

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-I v014, lines 147-149. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v014): G_k(1)^(1/k) of exact order log k; lower bound k^(1-s) for 1/2<s<1

**Statement as recorded:**

**Theorem.** (i) As $k\to\infty$,
$$\log k-\log\log k+O(1)\ \le\ G_k(1)^{1/k}\ \le\ \big(e^{\gamma}\zeta(2)+o(1)\big)\log k .$$
(ii) For $\frac12<s<1$ and large $k$, $G_k(s)^{1/k}\ge c_s\,k^{1-s}$.

**Depends on:** ANS-T23, ANS-T23a. **Used by:** ANS-T48a, ANS-T48b, ANS-T49, ANS-T50. **Classical inputs:** Ville, Mertens, Chebyshev.

**Relations:** ANS-T48a sharpens the upper constant of ANS-T48; ANS-T49 raises the lower constant of ANS-T48; ANS-T50 extends to a window the setting of ANS-T48.

## ANS-T48a: Upper constant e^gamma

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** UNNS Research Collective review, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-I v015, lines 28-31. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v015): limsup G_k(1)^(1/k)/log k <= e^gamma

**Statement as recorded:**

For $a,b>0$ put $D_{a,b}(E)=\sum_{d\mid E}d^{-a}\prod_{p\mid d}(1-p^{-b})$. The step estimate of v014 §5.2 holds in the sharper form
$$\sum_Nr_N^{-a}\Big(\frac{\gcd(E,N)}N\Big)^b\le\zeta(a+b)\,D_{a,b}(E),$$
because $J_b(d)=d^b\prod_{p\mid d}(1-p^{-b})$ was previously bounded by $d^b$. The function $D_{a,b}$ is multiplicative and
$$D_{a,b}(p^{\ell})=1+(1-p^{-b})\sum_{j=1}^{\ell}p^{-aj}\le F_p=\frac{1-p^{-a-b}}{1-p^{-a}} .$$

**Depends on:** ANS-T48. **Used by:** ANS-T50. **Classical inputs:** Mertens.

**Relations:** ANS-T48a sharpens the upper constant of ANS-T48.

## ANS-T48b: Exponential history function: order one, infinite type

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. The bounding constants satisfy 0 < c_- <= c_+ < infinity.

**Review record:** UNNS Research Collective review, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-I v015, lines 36-39. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v015): Exponential history function: order 1, infinite type, maximum-modulus bounds

**Statement as recorded:**

Let $\mathcal B_1(t)=\sum_kG_k(1)t^k/k!$. Suppose
$$c_-\le\liminf\frac{G_k(1)^{1/k}}{\log k},\qquad\limsup\frac{G_k(1)^{1/k}}{\log k}\le c_+ .$$
Then $\mathcal B_1$ is entire of order $1$ and infinite type, and
$$c_-\le\liminf_{r\to\infty}\frac{\log\mathcal B_1(r)}{r\log r}\le\limsup_{r\to\infty}\frac{\log\mathcal B_1(r)}{r\log r}\le c_+ .$$

**Depends on:** ANS-T48. **Classical inputs:** Stirling.

## ANS-T49: Lower constant 1.1079

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** UNNS Research Collective review, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-I v015, lines 47-52, 56-59. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v015): liminf G_k(1)^(1/k)/log k >= 1 + beta* I(1/beta*) = 1.1079...

**Statement as recorded:**

Let $\rho$ be the Dickman function and $I(v)=\int_v^{\infty}\rho(u)\,du$. We use two classical facts: $\int_0^{\infty}\rho=e^{\gamma}$, and for fixed $u\ge0$ the sum of $1/m$ over $z$-smooth $m\le z^u$ is $\big(\int_0^u\rho+o(1)\big)\log z$. With Mertens' theorem this gives, uniformly for $t=z^v$ with $v$ in a bounded range,
$$T_z(t):=\sum_{m>t,\;P^+(m)\le z}\frac1m=\big(I(v)+o(1)\big)\log z.\qquad(1)$$

**Theorem.** Put $\beta_*=2/(2+e^{\gamma})=0.52895\ldots$ Then
$$\liminf_{k\to\infty}\frac{G_k(1)^{1/k}}{\log k}\ \ge\ 1+\beta_*\,I(1/\beta_*)=1.1079\ldots,$$
where, since $1<1/\beta_*<2$, $I(v)=e^{\gamma}+1-v(2-\log v)$ at $v=1/\beta_*$.

Fix $\beta<\beta_*$ and put $Y=\lfloor k/\log k\rfloor$, $z=Y^{\beta}$. Let
$$\mathcal A=\{N\le Y\}\ \cup\ \{N>Y:\ P^+(N)\le z\},\qquad\mu(N)=r_N^{-1}=\frac N{(N+1)^2}.$$
Call the two parts *base* and *extra*. Only primes $p\le Y$ divide letters of $\mathcal A$. The extra letters are unbounded. By (1) with $v=1/\beta$,
$$B_{\mathcal A}=\sum_{N\in\mathcal A}\mu(N)=\big(1+\beta I(1/\beta)+o(1)\big)\log Y.$$

**Depends on:** ANS-T48. **Classical inputs:** Dickman function, Mertens.

**Relations:** ANS-T49 raises the lower constant of ANS-T48.

## ANS-T50: Growth bounds in the window around s = 1

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. Fixed real tau as k tends to infinity; no uniform statement for tau = tau(k).

**Review record:** UNNS Research Collective review, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-I v015, lines 94-99. **Scope:** Selected nesting grammar. **Literature priority:** Unreviewed.

**Release table summary** (ANS-I/v015): Growth bounds in the window s = 1 + tau/log k

**Statement as recorded:**

Let $\mathrm{Ein}(\tau)=\int_0^1(1-e^{-\tau u})\,du/u$.

**Theorem.** For every real $\tau$, with $s_k=1+\tau/\log k$,
$$\int_0^1e^{-\tau u}du\ \le\ \liminf_k\frac{G_k(s_k)^{1/k}}{\log k}\ \le\ \limsup_k\frac{G_k(s_k)^{1/k}}{\log k}\ \le\ e^{\gamma-\mathrm{Ein}(\tau)} .$$

At $\tau=0$ these are $1$ and $e^{\gamma}$. As $\tau\to+\infty$ the left side is $(1-e^{-\tau})/\tau$ and the right side is $e^{-E_1(\tau)}/\tau$, with $E_1$ the exponential integral. Both approach $1/\tau$.

**Depends on:** ANS-T48, ANS-T48a. **Classical inputs:** Mertens.

**Relations:** ANS-T50 extends to a window the setting of ANS-T48.

# J. Extended generation: torsion multipliers

**Setting (ANS-II v001).**

**Extension.** $A=(\alpha_1,\dots,\alpha_m)$ is a finite list of multipliers $\alpha_j>1$ with a rational power, $\alpha_j=\prod_pp^{w_{jp}}$, $w_{jp}\in\mathbb Q$. Letters are the nesting labels $N\ge1$ (multiplier $r_N$) and the symbols $\alpha_j$. Write $\mu(\ell)$ for the multiplier of a letter and $X_p(\ell)$ for its exponent at $p$: $X_p(N)=2v_p(N+1)-v_p(N)$, $X_p(\alpha_j)=w_{jp}$. Let $P_0$ be the finite set of primes with some $w_{jp}\ne0$, and $R=\prod_{p\in P_0}p$.

**States and admissibility [TC].** States are $x=a_\varphi n$, $n\in\mathbb N$, where $a_\varphi=\prod p^{\varphi_p}$, $0\le\varphi_p<1$, and $\varphi$ runs over the finite group $\Phi$ generated by the vectors $w_j$ modulo $\mathbb Z$. A letter is admissible at $x$ when $\mu(\ell)x$ again has all prime exponents non-negative (integrality preservation). For a nesting letter this is $N\mid n$.

**Histories.** For a word $w$ and a class $\varphi$, $K_\varphi(w)$ is the least $n$ such that $w$ is admissible from $a_\varphi n$; $Q(w)=\prod\mu$; $E_\varphi(w)=a_\varphi K_\varphi(w)Q(w)$. Put $\mathcal G_\varphi(s,t)=\sum_wt^{|w|}E_\varphi(w)^{-s}$, $A_\varphi(X)=\#\{w:E_\varphi(w)\le X\}$, and let $\mathcal Z_\varphi(s,t)$ be the sum of $t^{|w|}(\text{endpoint})^{-s}$ over all pairs (source $a_\varphi n$, admissible $w$).

**Characteristic function.** For $a>1$, $B_A(a)=\sum_N r_N^{-a}+\sum_j\alpha_j^{-a}$. It decreases from $\infty$ to $0$; $\sigma_A$ is the root of $B_A=1$. The letter law is $\nu_a(\ell)=\mu(\ell)^{-a}/B_A(a)$ and $\mu_p(a)=\mathbb E_{\nu_a}X_p$ is the **drift** at $p$.

**Hypothesis (D).** $\mu_p(\sigma_A)>0$ for every $p\in P_0$.

## ANS2-T00: Classwise invariance on valuation-type classes

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v001, lines 17-17. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v001): Z_C = alpha_C^-s Z_H on a valuation-type class

**Statement as recorded:**

**Theorem.** Take $A$ empty and any base point $\alpha_C>0$, with admissibility $N\mid n$ on $\alpha_Cn$ ([AT], classwise decomposition). Then $\mathcal Z_C(s,t)=\alpha_C^{-s}\mathcal Z_H(s,t)$ and $N_{\alpha_Cx}(\alpha_CX)=N_x(X)$.

**Depends on:** no earlier result cited. **Used by:** ANS2-T05.

## ANS2-L1: Source formula in extended grammars

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v001, lines 24-24. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v001): v_p(K) = max_j -floor(phi_p + S_p(j))

**Statement as recorded:**

**Lemma 1 (ANS2-L1).** With $S_p(j)$ the sum of $X_p$ over the first $j$ letters, $v_p(K_\varphi(w))=\max_{0\le j\le|w|}\big(-\lfloor\varphi_p+S_p(j)\rfloor\big)$, and $w$ is admissible from $a_\varphi n$ exactly when $K_\varphi(w)\mid n$.

**Depends on:** no earlier result cited. **Used by:** ANS2-L2, ANS2-T02, ANS2-T05, ANS2-T16, ANS2N-T04b.

## ANS2-L2: Comparison of torsion classes

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v001, lines 28-30. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v001): All torsion classes are comparable, K_phi / K_0 / R K_phi

**Statement as recorded:**

**Lemma 2 (ANS2-L2).** $K_\varphi(w)\mid K_0(w)\mid R\,K_\varphi(w)$. Hence for real $a>0$ and each depth $k$,
$$a_\varphi^{-a}\,\mathcal G_{0,k}(a)\le\mathcal G_{\varphi,k}(a)\le(R/a_\varphi)^{a}\,\mathcal G_{0,k}(a).$$

**Depends on:** ANS2-L1. **Used by:** ANS2-T16.

## ANS2-T01: Factorization in torsion classes

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v001, lines 35-35. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v001): Z_phi = zeta G_phi

**Statement as recorded:**

**Factorization (ANS2-T01).** $\mathcal Z_\varphi(s,t)=\zeta(s)\,\mathcal G_\varphi(s,t)$ where convergent: the admissible sources are $n=K_\varphi(w)m$, with endpoint $E_\varphi(w)m$.

**Depends on:** no earlier result cited.

## ANS2-T02: Positive drift: depth bounds and abscissa

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v001, lines 43-43, 50-51, 57-57. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v001): Depth bounds k^beta/log k to k^beta; abscissa sigma_A; critical convergence

**Statement as recorded:**

**Lemma 3.** Under (D) there are a neighbourhood $I$ of $\sigma_A$, $\eta>0$ and $M_0$ such that $\mathbb E\,e^{-\eta X_p}\le1$ for all primes $p$, all $a\in I$, and letters restricted to $N\le M$ (all $\alpha_j$ kept), $M_0\le M\le\infty$. If all $w_{jp}\ge0$, then (D) holds and every compact interval $I\subset(1,\infty)$ may be used.

**Theorem.** Under (D), for $a\in I$, $\beta=1/a$, $b>0$ and large $k$,
$$\frac{c\,k^{\beta}}{\log k}\le-\log\mathbb E\,K_{\varphi,k}^{-b}\le C\,k^{\beta}.$$

**Corollaries** (under (D)). (i) $\mathcal G_{\varphi,k}(a)^{1/k}\to B_A(a)$, and the abscissa of $\mathcal G_\varphi(\cdot,1)$ is exactly $\sigma_A$; for divergence below $\sigma_A$ use $a\in I$ and monotonicity ($E_\varphi\ge1$). The counting statement $A_\varphi(X)=X^{\sigma_A+o(1)}$ does not follow from the abscissa alone; it is a consequence of the counting theorem of §5 (whose proof uses only §§2–4). (ii) $K_{\varphi,k}\to\infty$ almost surely at $a\in I$. (iii) On $|t|B_A(a)=1$, $a=\operatorname{Re}s\in I$, the series $\sum_wt^{|w|}E_\varphi^{-s}K_\varphi^{-u}$ converges absolutely iff $\operatorname{Re}(s+u)>0$. (iv) $\mathcal G_\varphi(\sigma_A,1)<\infty$.

**Depends on:** ANS2-L1, ANS-T23. **Used by:** ANS2-T03, ANS2-T08, ANS2-T09a, ANS2-T16. **Classical inputs:** Jensen, Ville.

**Relations:** ANS2-T16 treats the abscissa for any drift signs, beyond ANS2-T02.

## ANS2-T03: Positive drift: counting functions

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v001, lines 60-61. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v001): X^sigma_A exp(-(log X)^beta) up to log log, all counting functions

**Statement as recorded:**

**Theorem.** Under (D), with $\sigma=\sigma_A$, $\beta=1/\sigma$, and $Z(X)$ equal to $A_\varphi(X)$, to the number $N_x(X)$ of histories from a fixed state $x=a_\varphi n$ with endpoint at most $X$, or to the number $C_\varphi(X)=\sum_{m\le X}A_\varphi(X/m)$ from all sources,
$$\frac{c(\log X)^{\beta}}{\log\log X}\le-\log\frac{Z(X)}{X^{\sigma}}\le C(\log X)^{\beta}.$$

**Depends on:** ANS2-T02, ANS-T24a. **Used by:** ANS2-T04.

## ANS2-T04: Positive drift: derivatives and infimal Gevrey order

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. Valid for the infimal Gevrey order.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v001, lines 80-80. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v001): Derivative bounds; smooth singular point; infimal Gevrey order sigma_A (membership at order sigma_A open)

**Statement as recorded:**

**Theorem.** Under (D), $D_j=\sum_w(\log E_\varphi)^jE_\varphi^{-\sigma_A}$ satisfies $c^jj^{\sigma_Aj}\le D_j\le(Cj\log j)^{\sigma_Aj}$. Consequently $\mathcal G_\varphi(\cdot,1)$ and $\mathcal Z_\varphi(\cdot,1)$ extend infinitely differentiably to $\operatorname{Re}s\ge\sigma_A$; $\sigma_A$ is a singular point at which neither has a meromorphic continuation; and the infimal Gevrey order of $\mathcal G_\varphi(\cdot,1)$ on the closed half-plane is $\sigma_A$.

**Depends on:** ANS2-T03, ANS-T27. **Classical inputs:** Landau.

## ANS2-T05: Negative drift: abscissa below the characteristic root

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v001, lines 91-93. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v001): Abscissa strictly below the characteristic root

**Statement as recorded:**

**Theorem.** Suppose $\mu_p(\sigma_A)<0$ for some $p\in P_0$. Then the abscissa $\sigma^\ast$ of $\mathcal G_\varphi(\cdot,1)$ satisfies $\sigma_c\le\sigma^\ast<\sigma_A$, where $\sigma_c$ is the nesting exponent. Moreover $\sigma^\ast\le a$ whenever $\Phi_p(a,\theta)<1$ for some $\theta\in[0,1]$, where
$$\Phi_p(a,\theta)=\sum_\ell\mu(\ell)^{-a}p^{\theta aX_p(\ell)}.$$

**Depends on:** ANS2-L1, ANS2-T00.

**Relations:** ANS2-T16 gives the exact value bounded in ANS2-T05.

## ANS2-T06: First-letter identity between classes

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v001, lines 99-101. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v001): First-letter identity between classes

**Statement as recorded:**

**Proposition.** Let all $w_{jp}\ge0$ for $\alpha=\alpha_j$, applied in class $\varphi$, with image class $\psi$ and integer carry $c$ ($\alpha a_\varphi=a_\psi c$). Then, with $K'=K_\psi(w)$ and $g=\gcd(K',c)$,
$$K_\varphi(\alpha w)=K'/g,\qquad E_\varphi(\alpha w)=E_\psi(w)\cdot c/g .$$

**Depends on:** no earlier result cited.

## ANS2-T07: First introductions in extended grammars

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. Valid with the precise event definition, now in the text.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v001, lines 84-86. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v001): Event I_k (every prime dividing a nesting letter occurred earlier through N or N+1): probability exp(-order k^beta/log k)

**Statement as recorded:**

**First introductions (ANS2-T07).** A prime *occurs* in a nesting letter $N$ if it divides $N(N+1)$; it has been *encountered before step $i$* if it occurs in some nesting letter at a step $j<i$, whether through $N_j$ or through $N_j+1$. Adjoined letters are ignored by this observable. Let $\mathcal I_k$ be the event that, for every $i\le k$ at which the letter is a nesting letter $N_i$, every prime dividing $N_i$ has been encountered before step $i$.

**Theorem.** For every $a>1$, $\Pr(\mathcal I_k)=\exp(-\Theta(k^\beta/\log k))$.

**Depends on:** ANS-T28a.

## ANS2-T08: Dependence on the multiplier

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v001, lines 108-110. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v001): Dependence on multiplier size; 2^(1/d) asymptotic

**Statement as recorded:**

(i) Under (D), $\sigma_A$ is determined by the real values of the multipliers, and adjoining a multiplier increases the root of $B_A=1$. (ii) The torsion order does not determine it: $\sqrt2$ and $2^{3/2}$ both have order 2 and different roots. (iii) For $\alpha=2^{1/d}$,
$$\sigma_d=\log_4d-\log_4\log d+O(1),\qquad\beta_d=1/\sigma_d\to0 .$$

**Depends on:** ANS2-T02.

## ANS2-T14: One-letter formula for any signs

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v002, lines 9-11. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v002): One letter formula and operator for multipliers of any signs

**Statement as recorded:**

A letter $\ell$ takes class $\psi$ to a class $\psi'$ with $\mu(\ell)a_\psi=a_{\psi'}\,u/v$, where $u/v$ is reduced. Here $u,v$ depend on $(\psi,\ell)$. For a nesting letter $\psi'=\psi$, $u=(N+1)^2$, $v=N$. For fixed $\ell$ the map $\psi\mapsto\psi'$ is a bijection of $\Phi_A$. No sign condition on the exponents is used.

**Lemma 1.** $\displaystyle n(w\ell)=\frac{u\,n(w)}{\gcd(n(w),v)}$ and $E_\varphi(w\ell)=E_\varphi(w)\,\mu(\ell)\,\dfrac{v}{\gcd(n(w),v)}$.

**Depends on:** no earlier result cited. **Used by:** ANS2-T10, ANS2-T11, ANS2-T15.

## ANS2-T10: Divisibility pullback

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v002, lines 15-17. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v002): Divisibility pullback d divides n' iff D(d) divides n

**Statement as recorded:**

**Lemma 2 (divisibility pullback).** For $d\ge1$ put
$$D(d)=\prod_{p:\,v_p(d)>v_p(u)}p^{\,v_p(v)+v_p(d)-v_p(u)}.$$
Then $d\mid n(w\ell)$ if and only if $D(d)\mid n(w)$. For a nesting letter this is $D_N(d)=\prod_{v_p d>2v_p(N+1)}p^{\,v_pN+v_pd-2v_p(N+1)}$.

**Depends on:** ANS2-T14. **Used by:** ANS2-T11.

## ANS2-T11: Nesting transfer operator

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v002, lines 22-28. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v002): Nesting transfer operator

**Statement as recorded:**

Define, for $\psi\in\Phi_A$, $d\ge1$,
$$F^{(k)}_{\psi,d}(s)=\sum_{|w|=k,\ \psi(w)=\psi,\ d\mid n(w)}E_\varphi(w)^{-s},$$
and let $J_s(h)=\sum_{e\mid h}\mu_{\rm M}(e)(h/e)^s$ ($\mu_{\rm M}$ the Möbius function).

**Theorem.** For $\operatorname{Re}s>1$, $F^{(k+1)}=L_sF^{(k)}$ with
$$(L_sF)_{\psi',d}=\sum_{\ell}\mu(\ell)^{-s}v^{-s}\sum_{h\mid v}J_s(h)\,F_{\psi,\,\operatorname{lcm}(h,D(d))},$$
where for each $\ell$, $\psi$ is the class carried to $\psi'$ and $u,v,D$ belong to $(\psi,\ell)$. The initial vector is $F^{(0)}_{\psi,d}=a_\varphi^{-s}[\psi=\varphi][d=1]$, and $\mathcal G_{\varphi,k}=\sum_\psi F^{(k)}_{\psi,1}$.

**Depends on:** ANS2-T10, ANS2-T14. **Used by:** ANS2-T12, ANS2-T13.

## ANS2-T12: Torsion carry operator

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v002, lines 32-34. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v002): Torsion carry operator, non-negative exponents

**Statement as recorded:**

**The two kinds of letter.** Nesting letters keep the class: with $v=N$, $\mu^{-s}v^{-s}=(N+1)^{-2s}$, giving
$$(T_NF)_{\psi,d}=(N+1)^{-2s}\sum_{h\mid N}J_s(h)F_{\psi,\operatorname{lcm}(h,D_N(d))}.$$
A torsion letter with non-negative exponents has $v=1$ and integer carry $u=c$, giving the pure shift $(S_\alpha F)_{\psi',d}=\alpha^{-s}F_{\psi,\,d/\gcd(d,c)}$.

**Depends on:** ANS2-T11. **Used by:** ANS2-T13.

## ANS2-T13: Closed countable operator system

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v002, lines 22-28, 32-34. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v002): Closed countable operator system, Re s > 1

**Statement as recorded:**

Define, for $\psi\in\Phi_A$, $d\ge1$,
$$F^{(k)}_{\psi,d}(s)=\sum_{|w|=k,\ \psi(w)=\psi,\ d\mid n(w)}E_\varphi(w)^{-s},$$
and let $J_s(h)=\sum_{e\mid h}\mu_{\rm M}(e)(h/e)^s$ ($\mu_{\rm M}$ the Möbius function).

**Theorem.** For $\operatorname{Re}s>1$, $F^{(k+1)}=L_sF^{(k)}$ with
$$(L_sF)_{\psi',d}=\sum_{\ell}\mu(\ell)^{-s}v^{-s}\sum_{h\mid v}J_s(h)\,F_{\psi,\,\operatorname{lcm}(h,D(d))},$$
where for each $\ell$, $\psi$ is the class carried to $\psi'$ and $u,v,D$ belong to $(\psi,\ell)$. The initial vector is $F^{(0)}_{\psi,d}=a_\varphi^{-s}[\psi=\varphi][d=1]$, and $\mathcal G_{\varphi,k}=\sum_\psi F^{(k)}_{\psi,1}$.

**The two kinds of letter.** Nesting letters keep the class: with $v=N$, $\mu^{-s}v^{-s}=(N+1)^{-2s}$, giving
$$(T_NF)_{\psi,d}=(N+1)^{-2s}\sum_{h\mid N}J_s(h)F_{\psi,\operatorname{lcm}(h,D_N(d))}.$$
A torsion letter with non-negative exponents has $v=1$ and integer carry $u=c$, giving the pure shift $(S_\alpha F)_{\psi',d}=\alpha^{-s}F_{\psi,\,d/\gcd(d,c)}$.

**Depends on:** ANS2-T11, ANS2-T12.

## ANS2-T15: Uniform and weighted l^1 realizations

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. Bounded only when the norm is finite (in the text).

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v002, lines 39-46. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v002): Realizations: uniform norm B_A(s); norm Phi_A(s, theta) on weighted l^1

**Statement as recorded:**

Let $s>1$ be real.

**Uniform norm.** On $\ell^\infty(\Phi_A\times\mathbb N)$ the operator $L_s$ is positive and $L_s\mathbf 1=B_A(s)\mathbf 1$, because $\sum_{h\mid v}J_s(h)=v^s$. Hence $\|L_s\|=B_A(s)$ and $B_A(s)$ is its spectral radius. This norm does not see the drifts.

**Measures on states.** Put $m_k(\psi,n)=\sum_{|w|=k,\,\psi(w)=\psi,\,n(w)=n}E_\varphi(w)^{-s}$. Then $m_{k+1}=Mm_k$, where $M$ sends a unit mass at $(\psi,n)$ to the masses $\mu^{-s}(\gcd(n,v)/v)^s$ at $(\psi',un/\gcd(n,v))$, and $\mathcal G_{\varphi,k}(s)=\|m_k\|_1$. For $\theta=(\theta_q)\in[0,1]^{\text{primes}}$ let
$$V_\theta(\psi,n)=\prod_qq^{\,\theta_qs\,v_q(a_\psi n)}\ge1,\qquad\Phi_A(s,\theta)=\sum_\ell\mu(\ell)^{-s}\prod_qq^{\,\theta_qsX_q(\ell)}\in(0,\infty].$$

**Theorem.** $\|M\|_{\ell^1(V_\theta)}=\Phi_A(s,\theta)$, in the following sense: the supremum of the weighted column sums equals $\Phi_A(s,\theta)$; $M$ is a bounded operator on $\ell^1(V_\theta)$ with this norm when $\Phi_A(s,\theta)<\infty$, and is unbounded when it is infinite.

**Depends on:** ANS2-T14. **Used by:** ANS2-T16.

## ANS2-T16: Growth rate, abscissa, drift dichotomy

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v002, lines 53-59, 79-79, 83-83. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v002): lim G_k(a)^(1/k) = min over theta of Phi_A(a, theta); abscissa is the root; sharp drift dichotomy

**Statement as recorded:**

For $a>1$ let
$$\rho_A(a)=\min_{\theta\in[0,1]^{\text{primes}}}\Phi_A(a,\theta).$$
The minimum exists: the cube is compact, $\Phi_A$ is lower semicontinuous (a sum of positive continuous functions of finitely many coordinates), and $\Phi_A(a,0)=B_A(a)<\infty$. $\Phi_A(a,\cdot)$ is convex.

**Theorem.** For every finite list $A$ as in §0 (any signs of the drifts), every $a>1$ and every class $\varphi$,
$$\lim_{k\to\infty}\mathcal G_{\varphi,k}(a)^{1/k}=\rho_A(a).$$

**Corollary 2 (abscissa).** The abscissa $\sigma^\ast$ of $\mathcal G_\varphi(s,1)=\sum_k\mathcal G_{\varphi,k}(s)$ is the unique root of $\rho_A(a)=1$; it is the same in every class and lies in $[\sigma_c,\sigma_A]$. Consequently $\limsup\log A_\varphi(X)/\log X=\sigma^\ast$.

**Corollary 3 (sharp dichotomy).** $\sigma^\ast=\sigma_A$ if every drift $\mu_p(\sigma_A)$, $p\in P_0$, is $\ge0$; and $\sigma^\ast<\sigma_A$ if one of them is negative.

**Depends on:** ANS2-L1, ANS2-L2, ANS2-T15, ANS2-T02. **Used by:** ANS2-C16, ANS2-T09, ANS2-T09a, ANS2N-T01, ANS2N-T02, ANS2N-T04a, ANS2N-T04b, ANS2N-T05. **Classical inputs:** Doob.

**Relations:** ANS2-T16 gives the exact value bounded in ANS2-T05; ANS2-T16 treats the abscissa for any drift signs, beyond ANS2-T02.

## ANS2-T09: Nonnegative drift: finiteness at the abscissa

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v002, lines 92-92. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v002): Drifts >= 0 (zero allowed): G(sigma_A, 1) finite and abscissa sigma_A

**Statement as recorded:**

**Proposition (T09, the UNNS Research Collective review).** If one or more drifts vanish at $\sigma_A$ and the others are positive, then $\mathcal G_\varphi(\sigma_A,1)<\infty$ and the abscissa is $\sigma_A$.

**Depends on:** ANS2-T16.

## ANS2-T09a: Nonnegative drift: depth order

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II v002, lines 98-99. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v002): Drifts >= 0 at a > 1: -log E[K^-b] between orders k^beta / log k and k^beta (no sqrt k term)

**Statement as recorded:**

**Theorem (T09a).** Let $a>1$, $b>0$, $\beta=1/a$, and suppose $\mu_p(a)\ge0$ for all $p\in P_0$. Then for large $k$
$$\frac{c\,k^\beta}{\log k}\le-\log\mathbb E_{\nu_a}K_{\varphi,k}^{-b}\le C\,k^\beta.$$

**Depends on:** ANS2-T02, ANS2-T16, ANS-T23. **Classical inputs:** Ville.

## ANS2-C16: Interval for 2/sqrt3 (floating point; certified as ANS2N-T06)

**Proof status:** COMPUTED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release; floating-point computation.

**Source:** ANS-II v002, lines 123-129. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/v002): 2/sqrt3: 2.06055 <= abscissa <= 2.06072

**Statement as recorded:**

- *Lower side.* By convexity, for any $\theta^0$, $\min_{[0,1]}\Phi_M\ge\Phi_M(\theta^0)+\sum_q\min\big(-g_q\theta^0_q,\;g_q(1-\theta^0_q)\big)$, $g=\nabla\Phi_M(\theta^0)$. Since $\min\Phi_M\le\rho_A$, a value $\ge1$ at $a$ gives $\sigma^\ast\ge a$.
- *Upper side.* If all $\theta_q\le t<1$, the nesting term of $N$ is at most $N^{-a(1-2t)}$, so $\Phi_A(a,\theta)\le\Phi_M(a,\theta)+M^{1-c}/(c-1)$ with $c=a(1-2t)>1$. A value $<1$ gives $\sigma^\ast<a$.

With $M=2\cdot10^5$ for the lower side and $10^6$ for the upper side,
$$2.06055\le\sigma^\ast\le2.06072.$$
The computed values are $2.0605567\ldots$ and $2.0607189\ldots$, rounded outward. (A certified evaluation is in ANS-II-ND v001.)

**Depends on:** ANS2-T16. **Used by:** ANS2N-T06.

**Relations:** ANS2N-T06 certifies ANS2-C16.

Floating-point evaluation. The interval is certified by ANS2N-T06.

# K. Negative drift: entropy and attainment

**Setting (ANS-II-ND v001).**

As in ANS-II v002: letters $\ell$ are the nesting labels $N\ge1$ and a finite list $A$ of torsion multipliers; $\mu(\ell)$ is the multiplier and $X_p(\ell)$ the exponent at $p$; $P_0$ is the set of primes of $A$; $a>1$, $B=B_A(a)$,
$$\Phi(\theta)=\Phi_A(a,\theta)=\sum_\ell\mu(\ell)^{-a}\prod_pp^{a\theta_pX_p(\ell)},\qquad\rho=\rho_A(a)=\min_{[0,1]^{\mathbb P}}\Phi,$$
$\mathbb P$ the set of primes. For a probability $\pi$ on letters with $\mathbb E_\pi|\log\mu|<\infty$ let $H(\pi)$ be its entropy, $m_p(\pi)=\mathbb E_\pi X_p$, and
$$\Lambda(\pi)=\mathbb E_\pi\log\mu+\sum_p[-m_p(\pi)]_+\log p .$$
Call $\pi$ **resource-neutral** if $m_p(\pi)\ge0$ for every $p$; then $\Lambda(\pi)=\mathbb E_\pi\log\mu$. Gibbs' inequality, for any $\theta\in[0,1]^{\mathbb P}$:
$$\log\Phi(\theta)\ge H(\pi)-a\,\mathbb E_\pi\log\mu+a\sum_p\theta_pm_p(\pi)\log p,\qquad(G)$$
with equality exactly when $\pi(\ell)$ is proportional to the term of $\ell$. The exchange of sums is legitimate since $\sum_p|X_p(N)|\log p\le\log N+2\log(N+1)$.

## ANS2N-T02: Weights above one never help

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II-ND v001, lines 17-17, 23-25. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v001): Weights above 1 never help; unique minimiser below 1; supremum attained in the limit by resource-neutral laws; deficits are strictly suboptimal

**Statement as recorded:**

**Lemma 1.** If $\theta\ge0$ and $\Phi_M(\theta)\le B$, then $\theta_q\le R=2c$ for all primes $q\le M+1$, where $c=1+\max(0,\log B)/(2a\log2)$.

So $\Phi_M$ attains its minimum $L_M$ over the whole orthant $[0,\infty)^{\{p\le M+1\}}$ at some $\theta^M\in[0,R]$.

**Theorem 1.** (i) $\Phi(\theta)\ge\rho$ for every $\theta\in[0,\infty)^{\mathbb P}$: the upper restriction $\theta_p\le1$ is never active. (ii) The minimiser $\theta^\ast$ of $\Phi$ on the cube is unique, and $\theta^\ast_p<1$ for every $p$. (iii) $L_M\uparrow\rho$ and $\theta^M\to\theta^\ast$ coordinatewise.

**Depends on:** ANS2-T16. **Used by:** ANS2N-T01, ANS2N-T03, ANS2N-T05, ANS2N-T09, ANS2N-T15.

## ANS2N-T01: Entropy-admissibility variational principle

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II-ND v001, lines 36-46. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v001): log rho = sup [H - a Lambda]; abscissa = sup H / Lambda

**Statement as recorded:**

**Theorem 2.**
$$\log\rho=\sup_{\pi}\big[H(\pi)-a\Lambda(\pi)\big]=\sup_{\pi\ \text{resource-neutral}}\big[H(\pi)-a\,\mathbb E_\pi\log\mu\big],$$
both over finitely supported $\pi$. For multipliers $>1$, the abscissa $\sigma^\ast$ satisfies
$$\sigma^\ast=\sup_\pi\frac{H(\pi)}{\Lambda(\pi)}=\sup_{\pi\ \text{resource-neutral}}\frac{H(\pi)}{\mathbb E_\pi\log\mu}.$$
The first formula in each line is the UNNS Research Collective's proposal.

*Proof.* In $(G)$ at $\theta^\ast$, $\theta^\ast_pm_p\ge-[-m_p]_+$; so $\log\rho\ge H-a\Lambda$ for every $\pi$. Let $\pi_M(\ell)$ be the term of $\ell$ at $\theta^M$ divided by $L_M$. The minimum over the orthant gives $a\log p\,L_M\,m_p(\pi_M)=\partial_p\Phi_M\ge0$, with equality if $\theta^M_p>0$. So $\pi_M$ is resource-neutral and, by equality in $(G)$, $H(\pi_M)-a\,\mathbb E\log\mu=\log L_M\to\log\rho$. For $\sigma^\ast$: $\rho_A(\sigma^\ast)=1$ gives $H\le\sigma^\ast\Lambda$ always, and neutral $\pi_M$ at $a=\sigma^\ast$ have $H-\sigma^\ast\mathbb E\log\mu\to0$ with $\mathbb E\log\mu$ bounded below by a positive constant. $\square$

**Corollary 1 (depletion is never optimal).** For every $\pi$,
$$\log\rho-\big[H(\pi)-a\Lambda(\pi)\big]\ \ge\ a\sum_{p:\,m_p<0}(1-\theta^\ast_p)\,|m_p(\pi)|\log p,$$
which is positive as soon as some drift is negative. *Proof:* $(G)$ at $\theta^\ast$ and $\theta^\ast_p<1$. $\square$

**Depends on:** ANS2N-T02, ANS2-T16. **Used by:** ANS2N-T04a, ANS2N-T04b. **Classical inputs:** Gibbs inequality.

## ANS2N-T03: Optimal law and attainment criterion

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. Convergence valid; attainment is open.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II-ND v001, lines 49-51. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v001): Optimal finite laws converge to one probability; criterion and a sufficient condition for attainment

**Statement as recorded:**

**Theorem 3.** Let $\nu^\ast(\ell)=\mu(\ell)^{-a}\prod p^{a\theta^\ast_pX_p(\ell)}/\rho$. Then $\nu^\ast$ is a probability, $\pi_M\to\nu^\ast$ in total variation, and $\mathbb E_{\nu^\ast}\log\mu<\infty$. There is a probability $\pi$ on the full alphabet, with $\mathbb E_\pi\log\mu<\infty$, that is resource-neutral and attains $H(\pi)-a\,\mathbb E_\pi\log\mu=\log\rho$ if and only if
$$m_p(\nu^\ast)\ge0\ \text{ and }\ \theta^\ast_p\,m_p(\nu^\ast)=0\quad\text{for all }p;\qquad(\mathrm N)$$
in that case $\pi=\nu^\ast$. Condition (N) holds if $\sup_p\theta^\ast_p<(a-1)/(2a)$.

**Depends on:** ANS2N-T02. **Used by:** ANS2N-T07, ANS2N-T08. **Classical inputs:** Scheffe, Gibbs.

## ANS2N-T04a: Counting limits for A and C

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II-ND v001, lines 58-60. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v001): log A / log X and log C / log X tend to the abscissa

**Statement as recorded:**

**Theorem 4.** Let all torsion multipliers exceed $1$. For every state $x=a_\varphi n$, with $N_x$ the number of histories from $x$, $A_\varphi$ the number of minimal histories and $C_\varphi$ the all-source count, each with endpoint at most $X$,
$$\lim_{X\to\infty}\frac{\log N_x(X)}{\log X}=\lim\frac{\log A_\varphi(X)}{\log X}=\lim\frac{\log C_\varphi(X)}{\log X}=\sigma^\ast,$$
for any signs of the drifts.

**Depends on:** ANS2N-T01, ANS2-T16. **Classical inputs:** Doob.

## ANS2N-T04b: Fixed-source counting exponent

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II-ND v001, lines 58-60. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v001): Every fixed-source count has the same limit

**Statement as recorded:**

**Theorem 4.** Let all torsion multipliers exceed $1$. For every state $x=a_\varphi n$, with $N_x$ the number of histories from $x$, $A_\varphi$ the number of minimal histories and $C_\varphi$ the all-source count, each with endpoint at most $X$,
$$\lim_{X\to\infty}\frac{\log N_x(X)}{\log X}=\lim\frac{\log A_\varphi(X)}{\log X}=\lim\frac{\log C_\varphi(X)}{\log X}=\sigma^\ast,$$
for any signs of the drifts.

**Depends on:** ANS2N-T01, ANS2-T16, ANS2-L1, ANS-T24a. **Classical inputs:** Doob.

## ANS2N-T05: Optimal weights zero or infinitely supported

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II-ND v001, lines 73-73. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v001): Optimal weights are zero or supported on infinitely many primes

**Statement as recorded:**

**Theorem 5.** Let $a>1$. If all drifts $\mu_p(a)$ under the unweighted law $\nu_a$ are non-negative, then $\theta^\ast=0$. If one is negative, then $\theta^\ast_p>0$ for infinitely many primes $p$.

**Depends on:** ANS2N-T02, ANS2-T16. **Used by:** ANS2N-T11. **Classical inputs:** Dirichlet theorem on primes.

## ANS2N-T06: Certified interval for 2/sqrt3

**Proof status:** CERTIFIED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. Method valid and stored result reviewed; no independent rerun.

**Review record:** Release review records. **Release and computation:** Archived release; certificate not independently rerun.

**Source:** ANS-II-ND v001, lines 90-91. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v001): 2.06055 <= abscissa of 2/sqrt3 <= 2.06072

**Statement as recorded:**

$$2.06055\le\sigma^\ast\le2.06072 .$$
*Method.* The inequalities of ANS-II v002 §7 are valid for any weights. The weights are found in floating point; the two certificates are then evaluated with MPFR arithmetic at 80 bits, every operation rounded in the safe direction (`certify.py`), at $a=2.06055+2^{-40}$ (lower certificate $\ge1$, margin $5.8\cdot10^{-6}$) and $a=2.06072-2^{-40}$ (upper certificate $<1$, margin $1.3\cdot10^{-6}$). The statement relies on the correct rounding of MPFR and on the program.

**Depends on:** ANS2-C16. **Classical inputs:** MPFR directed rounding.

**Relations:** ANS2N-T06 certifies ANS2-C16.

## ANS2N-T07: Euler-summability criterion (hypothesis superseded by T10)

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. Valid; its hypothesis is superseded by ANS2N-T10.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II-ND v002, lines 13-13. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v002): Attainment if all weights are below 1/2 and sum p^(-a(1-2 theta_p)) converges (and its limsup corollary)

**Statement as recorded:**

**Theorem 7.** If $\theta^\ast_p<\tfrac12$ for all $p$ and $\sum_pp^{-c_p}<\infty$, where $c_p=a(1-2\theta^\ast_p)$, then $\nu^\ast$ attains.

**Depends on:** ANS2N-T03.

**Relations:** ANS2N-T10 supersedes the hypothesis of ANS2N-T07.

## ANS2N-T08: Attainment iff uniform integrability

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II-ND v002, lines 18-18. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v002): Attainment iff log mu is uniformly integrable under the finite optima

**Statement as recorded:**

**Theorem 8.** $\nu^\ast$ attains if and only if $\log\mu$ is uniformly integrable under the family $(\pi_M)$; equivalently, if and only if $\mathbb E_{\pi_M}\log\mu\to E$.

**Depends on:** ANS2N-T03. **Used by:** ANS2N-T13, ANS2N-T14.

## ANS2N-T09: Variational inequality at the candidate law

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. Valid; a proof clarification is recorded in ANS-II-ND v003.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II-ND v002, lines 25-26. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v002): sum (w_p - theta_p) m_p log p >= 0 for every weighting w with finite Phi(w)

**Statement as recorded:**

**Theorem 9.** For every $w\in[0,\infty)^{\mathbb P}$ with $\Phi(w)<\infty$,
$$\sum_p(w_p-\theta^\ast_p)\,m_p\log p\ \ge\ 0 .$$

**Depends on:** ANS2N-T02. **Used by:** ANS2N-T10.

## ANS2N-T10: Depletion-surplus inequality

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II-ND v002, lines 31-33, 38-42. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v002): Depletion-surplus inequality; neutrality of the candidate is equivalent to attainment; attainment if weights are below 1/2 at depleting primes

**Statement as recorded:**

**Theorem 10.**
$$\sum_p\Big(\tfrac12-\theta^\ast_p\Big)m_p^-\log p\ +\ \sum_p\theta^\ast_p\,m_p^+\log p\ \le\ 0 .\qquad(\mathrm D)$$

1. *Neutrality is enough.* $\nu^\ast$ attains if and only if $m_p\ge0$ for all $p$. (If every $m_p^-=0$, (D) forces $\theta^\ast_pm_p^+=0$.)
2. *Attainment criterion.* $\nu^\ast$ attains if $\theta^\ast_p<\frac12$ at every prime with $m_p<0$. In particular **it attains if $\theta^\ast_p<\frac12$ for all $p$**. No summability, decay or uniform margin is needed; Theorem 7 and the criterion of v001 Theorem 3 are special cases.
3. *What failure would require.* If $\nu^\ast$ does not attain, there is a prime $s$ with $m_s<0$ and $\theta^\ast_s\ge\frac12$, and $\Phi(\theta^\ast+\epsilon e_s)=\infty$ for every $\epsilon>0$. (The last assertion: if it were finite, Theorem 9 would give $\epsilon\,m_s\ge0$.) Moreover $H(\nu^\ast)-aE=\log\rho-a\Gamma$ and
$$\tfrac12\sum_pm_p^-\log p\ \le\ -\Gamma\ \le\ \sum_p\theta^\ast_pm_p^-\log p .$$
4. If $\theta^\ast_p\le\frac12$ for all $p$, depletion can occur only at primes with $\theta^\ast_p=\frac12$, and $m_p=0$ at every prime with $0<\theta^\ast_p<\frac12$.

**Depends on:** ANS2N-T09. **Used by:** ANS2N-C12, ANS2N-T11, ANS2N-T14.

**Relations:** ANS2N-T10 supersedes the hypothesis of ANS2N-T07; ANS2N-T14 contains, by a second argument, part of ANS2N-T10.

## ANS2N-T11: Weights below one half cannot tend to zero

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** Release review records. **Release and computation:** Archived release.

**Source:** ANS-II-ND v002, lines 45-49. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v002): Under negative drift, "all weights below 1/2" and "weights tend to zero" cannot both hold; limsup bound 2/(3L) times the supremum under T07's hypotheses

**Statement as recorded:**

Let $L$ be an admissible Linnik exponent: the least prime $q\equiv b\pmod d$, $(b,d)=1$, is at most $C_Ld^L$. Xylouris (Acta Arith. 150 (2011)) gives $L=5.18$.

**Theorem 11.** Suppose that some unweighted drift $\mu_p(a)$ is negative, that $\theta^\ast_p<\frac12$ for all $p$, and that $\sum_pp^{-c_p}<\infty$. Then
$$\limsup_{q\to\infty}\theta^\ast_q\ \ge\ \frac{2}{3L}\,\sup_p\theta^\ast_p\ >0 .$$
Consequently, when some drift is negative, **the two statements "$\theta^\ast_p<\frac12$ for all $p$" and "$\theta^\ast_p\to0$" cannot both hold.**

**Depends on:** ANS2N-T10, ANS2N-T05. **Used by:** ANS2N-C12. **Classical inputs:** Linnik (Xylouris exponent).

## ANS2N-T12a: Weight above one half forces weight on divisors of C p^V - 1

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** UNNS Research Collective review, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-II-ND v003, lines 11-12, 16-16. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v003): Weight above 1/2 at p forces weight on the divisors of C p^V - 1

**Statement as recorded:**

**Lemma.** Let $w$ be feasible, $p$ a prime, $C\ge1$ an integer and $N_V=Cp^V-1$. Then
$$\sum_{q\mid N_V}w_q\,v_q(N_V)\log q\;-\;(2w_p-1)\,V\log p\;\longrightarrow\;+\infty\qquad(V\to\infty).$$

So a weight above $\frac12$ at $p$ forces the prime divisors of $Cp^V-1$ to carry weight, for every $C$ and every large $V$.

**Depends on:** no earlier result cited. **Used by:** ANS2N-T12.

## ANS2N-T12: Tail-weight constraint

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** UNNS Research Collective review, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-II-ND v003, lines 18-18. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v003): Tail-weight constraint: limsup w_p >= 2 sup w_p - 1 for every feasible weighting

**Statement as recorded:**

**Theorem 12.** For feasible $w$, with $T=\sup_pw_p$ and $T_\infty=\limsup_pw_p$: $T_\infty\ge2T-1$.

**Depends on:** ANS2N-T12a. **Used by:** ANS2N-C12.

## ANS2N-C12: Decaying weights have maximum exactly one half

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. Valid under its hypotheses.

**Review record:** UNNS Research Collective review, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-II-ND v003, lines 22-22. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v003): Negative drift and decaying weights force a maximum of exactly 1/2

**Statement as recorded:**

**Corollary (UNNS Research Collective's reduction, valid).** If some drift is negative and $\theta^\ast_p\to0$, then $\max_p\theta^\ast_p=\frac12$ exactly: $T_\infty=0$ gives $T\le\frac12$, and v002 Theorem 11 excludes $\theta^\ast_p<\frac12$ for all $p$. In addition, the set $F=\{p:\theta^\ast_p=\frac12\}$ is finite and non-empty, depletion can occur only on $F$ (v002 Theorem 10, corollary 4), and $\Phi(\theta^\ast+\epsilon e_s)=\infty$ for every $s\in F$, $\epsilon>0$ (Theorem 12): these primes lie on the boundary of the domain of $\Phi$.

**Depends on:** ANS2N-T12, ANS2N-T11, ANS2N-T10.

## ANS2N-T13: Logarithmic moment defect bounds

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** UNNS Research Collective review, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-II-ND v003, lines 25-25. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v003): Moment defect: -Gamma <= delta <= -a Gamma/(a-1)

**Statement as recorded:**

**Theorem 13.** If $E_{M_j}-E\to\delta$, then $-\Gamma\le\delta\le-\dfrac{a}{a-1}\Gamma$.

**Depends on:** ANS2N-T08. **Used by:** ANS2N-T14.

## ANS2N-T14: Location of the defect

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid, with a recorded qualification. Proof-writing clarification: in the final Fatou step use a limit superior for the drift difference, or a further convergent subsequence. The theorem is unaffected; the release file is not edited.

**Review record:** UNNS Research Collective review, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-II-ND v003, lines 31-35, 45-48. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v003): D/2 <= omega <= -Gamma <= delta <= (-a Gamma - omega)/(a-1); attainment iff E v_p(N+1) converges to its candidate value for every p; defect D/2 at the threshold

**Statement as recorded:**

$$\mathbb E_{\pi_{M_j}}v_p(N+1)-\mathbb E_{\nu^\ast}v_p(N+1)\to\kappa_p .$$
(Torsion letters count as $v_p(N+1)=0$. Boundedness of $E_M$ gives such a subsequence.) By Fatou's lemma $\kappa_p\ge0$. Put $\omega=\sum_p\kappa_p\log p$; it is the part of $\delta$ carried by divisibility of $N+1$ at fixed primes.

**Theorem 14.**
$$\frac D2\ \le\ \omega\ \le\ -\Gamma\ \le\ \delta\ \le\ \frac{-a\Gamma-\omega}{a-1}.$$

1. *Prime-by-prime criterion.* $\nu^\ast$ attains **if and only if** $\mathbb E_{\pi_M}v_p(N+1)\to\mathbb E_{\nu^\ast}v_p(N+1)$ for every prime $p$. (If it attains, $\delta=0$ by v002 Theorem 8, so $\omega=0$. If all $\kappa_p=0$ then $D=0$.) Failure of attainment is therefore visible at single fixed primes: at every depleted prime.
2. $D/2\le\omega\le-\Gamma$ contains v002 Theorem 10, by a second argument.
3. $\sum_{p\ \text{not depleted}}\kappa_p\log p\le\sum_{p\ \text{depleted}}(\theta^\ast_p-\tfrac12)\,m_p^-\log p$.
4. *Exact defect at the threshold.* If $\theta^\ast_p=\frac12$ at every depleted prime, then $-\Gamma\le D/2$, so $\omega=-\Gamma=D/2$ and $\delta=D/2$ for every limit point: $E_M\to E+D/2$. This applies to the exceptional decay case of section 1.

**Depends on:** ANS2N-T13, ANS2N-T08, ANS2N-T10.

**Relations:** ANS2N-T14 contains, by a second argument, part of ANS2N-T10.

## ANS2N-T15: Average weight at most 1 - 1/a

**Proof status:** PROVED. **Review:** UNNS Research Collective review: valid.

**Review record:** UNNS Research Collective review, 27 November 2026 (PROVENANCE/REVIEWS). **Release and computation:** Archived release.

**Source:** ANS-II-ND v003, lines 51-55. **Scope:** Extended grammar with torsion multipliers. **Literature priority:** Unreviewed.

**Release table summary** (ANS-II/ND/v003): limsup eps sum w_p log p / p^(1+eps) <= 1 - 1/a for every feasible weighting

**Statement as recorded:**

**Theorem 15.** (i) For $1<a'<a$, $s=1-a'/a$, with $B,E_{a'},\mu_p(a')$ the characteristic sum, mean logarithm and drifts of the unweighted law at $a'$, and any feasible $w$:
$$\sum_pw_p\,\mu_p(a')\log p\ \le\ s\,E_{a'}-\frac1a+\frac{\Phi(w)}{a\,B(a')}.$$
(ii) Consequently
$$\limsup_{\epsilon\downarrow0}\ \epsilon\sum_pw_p\,\frac{\log p}{p^{1+\epsilon}}\ \le\ 1-\frac1a .$$
In particular this holds for $w=\theta^\ast$.

**Depends on:** ANS2N-T02.
