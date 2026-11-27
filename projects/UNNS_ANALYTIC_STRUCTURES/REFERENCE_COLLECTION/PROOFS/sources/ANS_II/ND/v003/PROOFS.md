# ANS-II-ND v003 — The half-weight threshold: proofs

Research notes. Uses ANS-II-ND v001 (Theorems 1, 3, 5) and v002 (Theorems 8–11).

## 0. Setting
As in ANS-II-ND v002. $\theta^\ast$ is the minimiser, $\rho=\Phi(\theta^\ast)$, $\nu^\ast$ the candidate law, $m_p$ its drifts, $E=\mathbb E_{\nu^\ast}\log\mu$, $\Gamma=\sum_p\theta^\ast_pm_p\log p$ and $D=\sum_pm_p^-\log p$. For the finite alphabet $N\le M$ (with the torsion letters) $\theta^M$, $L_M$, $\pi_M$ are the minimiser, minimum and optimal law, and $E_M=\mathbb E_{\pi_M}\log\mu$. The **feasible weightings** are the $w\ge0$ with $\Phi(w)<\infty$; $\theta^\ast$ is one of them.

**Clarification to v002 Theorem 9 (owner's review).** Monotone convergence is applied to the non-negative functions $f_1-f_s$, where $f_s=t(e^{sh}-1)/s$; they increase as $s\downarrow0$ and $f_1$ is summable.

## 1. The tail-weight constraint (ND-T12, owner's proposal)
**Lemma.** Let $w$ be feasible, $p$ a prime, $C\ge1$ an integer and $N_V=Cp^V-1$. Then
$$\sum_{q\mid N_V}w_q\,v_q(N_V)\log q\;-\;(2w_p-1)\,V\log p\;\longrightarrow\;+\infty\qquad(V\to\infty).$$

*Proof.* The terms of the distinct letters $N_V$ tend to $0$. Their logarithm is $a\log N_V-2a\log(N_V+1)+2a\sum_qw_qv_q(N_V+1)\log q-a\sum_qw_qv_q(N_V)\log q$. Here $N_V+1=Cp^V$, so the first three parts are at least $-aV\log p+2aw_pV\log p-O_C(1)$. $\square$

So a weight above $\frac12$ at $p$ forces the prime divisors of $Cp^V-1$ to carry weight, for every $C$ and every large $V$.

**Theorem 12.** For feasible $w$, with $T=\sup_pw_p$ and $T_\infty=\limsup_pw_p$: $T_\infty\ge2T-1$.

*Check of the owner's proof.* Fix $p$ and $\epsilon>0$, a finite set $S\ni p$ containing all primes with $w_q>T_\infty+\epsilon$, and $C=\prod_{S\setminus\{p\}}q$. No prime of $S$ divides $N_V$, so the sum in the lemma is at most $(T_\infty+\epsilon)\log N_V\le(T_\infty+\epsilon)(V\log p+\log C)$. The lemma gives $2w_p-1\le T_\infty+\epsilon$. The statement is **valid**. $\square$

**Corollary (owner's reduction, valid).** If some drift is negative and $\theta^\ast_p\to0$, then $\max_p\theta^\ast_p=\frac12$ exactly: $T_\infty=0$ gives $T\le\frac12$, and v002 Theorem 11 excludes $\theta^\ast_p<\frac12$ for all $p$. In addition, the set $F=\{p:\theta^\ast_p=\frac12\}$ is finite and non-empty, depletion can occur only on $F$ (v002 Theorem 10, corollary 4), and $\Phi(\theta^\ast+\epsilon e_s)=\infty$ for every $s\in F$, $\epsilon>0$ (Theorem 12): these primes lie on the boundary of the domain of $\Phi$.

## 2. The moment defect (ND-T13, owner's proposal)
**Theorem 13.** If $E_{M_j}-E\to\delta$, then $-\Gamma\le\delta\le-\dfrac{a}{a-1}\Gamma$.

*Check of the proof.* $H(\pi_M)=\log L_M+aE_M$ and $H(\nu^\ast)=\log\rho+aE-a\Gamma$. Lower semicontinuity of entropy gives $a(\delta+\Gamma)\ge0$. In the decomposition of v002 Theorem 8 with $1<a'<a$, the relative entropy to $\nu_{a'}$ changes in the limit by $-(a-a')\delta-a\Gamma\ge0$; let $a'\downarrow1$. The statement is **valid**, as is $\liminf(E_M-E)\ge D/2$. $\square$

## 3. Where the defect sits (ND-T14)
Pass to a subsequence on which $E_{M_j}-E\to\delta$ and, for every $p$,
$$\mathbb E_{\pi_{M_j}}v_p(N+1)-\mathbb E_{\nu^\ast}v_p(N+1)\to\kappa_p .$$
(Torsion letters count as $v_p(N+1)=0$. Boundedness of $E_M$ gives such a subsequence.) By Fatou's lemma $\kappa_p\ge0$. Put $\omega=\sum_p\kappa_p\log p$; it is the part of $\delta$ carried by divisibility of $N+1$ at fixed primes.

**Theorem 14.**
$$\frac D2\ \le\ \omega\ \le\ -\Gamma\ \le\ \delta\ \le\ \frac{-a\Gamma-\omega}{a-1}.$$

*Proof.* Let $S$ be a finite set of primes and $t<1<s$. Put $f(N)=s\log(N+1)-t\sum_{p\in S}v_p(N+1)\log p\ge0$ on nesting letters and $f=0$ on torsion letters. Then $\sum e^{-f}=Z<\infty$ (over $n=N+1$ it is bounded by an Euler product with factors $(1-p^{-(s-t)})^{-1}$ on $S$ and $(1-p^{-s})^{-1}$ elsewhere), and for every law with finite $\mathbb E\log\mu$,
$$H(\pi)=\mathbb E_\pi f+\log Z-D_{\rm KL}(\pi\Vert e^{-f}/Z).$$
Along the subsequence, $H(\pi_{M_j})-H(\nu^\ast)\to a(\delta+\Gamma)$. Since $\log\mu(N)-\log(N+1)\to0$ and $\pi_M\to\nu^\ast$ in total variation, the excess of $\mathbb E\log(N+1)$ over nesting letters tends to $\delta$; so $\mathbb E f$ changes by $s\delta-t\,\omega_S$ with $\omega_S=\sum_S\kappa_p\log p$. Lower semicontinuity of relative entropy gives $s\delta-t\,\omega_S-a(\delta+\Gamma)\ge0$. Let $s\downarrow1$, $t\uparrow1$, then enlarge $S$:
$$(a-1)\,\delta\ \le\ -a\Gamma-\omega .$$
With $\delta\ge-\Gamma$ (Theorem 13) this gives $\omega\le-\Gamma$. Finally $m_p(\pi)=2\mathbb E_\pi v_p(N+1)-\mathbb E_\pi v_p(N)+(\text{torsion})$. The torsion part converges, the excess of $\mathbb E v_p(N)$ has non-negative limit points (Fatou), and $m_p(\pi_M)\ge0$. So $-m_p\le\lim\big(m_p(\pi_{M_j})-m_p\big)\le2\kappa_p$, that is $\kappa_p\ge m_p^-/2$, and $\omega\ge D/2$. $\square$

**Corollaries.**

1. *Prime-by-prime criterion.* $\nu^\ast$ attains **if and only if** $\mathbb E_{\pi_M}v_p(N+1)\to\mathbb E_{\nu^\ast}v_p(N+1)$ for every prime $p$. (If it attains, $\delta=0$ by v002 Theorem 8, so $\omega=0$. If all $\kappa_p=0$ then $D=0$.) Failure of attainment is therefore visible at single fixed primes: at every depleted prime.
2. $D/2\le\omega\le-\Gamma$ contains v002 Theorem 10, by a second argument.
3. $\sum_{p\ \text{not depleted}}\kappa_p\log p\le\sum_{p\ \text{depleted}}(\theta^\ast_p-\tfrac12)\,m_p^-\log p$.
4. *Exact defect at the threshold.* If $\theta^\ast_p=\frac12$ at every depleted prime, then $-\Gamma\le D/2$, so $\omega=-\Gamma=D/2$ and $\delta=D/2$ for every limit point: $E_M\to E+D/2$. This applies to the exceptional decay case of section 1.

## 4. An average bound for the weights (ND-T15)
**Theorem 15.** (i) For $1<a'<a$, $s=1-a'/a$, with $B,E_{a'},\mu_p(a')$ the characteristic sum, mean logarithm and drifts of the unweighted law at $a'$, and any feasible $w$:
$$\sum_pw_p\,\mu_p(a')\log p\ \le\ s\,E_{a'}-\frac1a+\frac{\Phi(w)}{a\,B(a')}.$$
(ii) Consequently
$$\limsup_{\epsilon\downarrow0}\ \epsilon\sum_pw_p\,\frac{\log p}{p^{1+\epsilon}}\ \le\ 1-\frac1a .$$
In particular this holds for $w=\theta^\ast$.

*Proof.* (i) $\Phi(s\mathbf 1)=B(a')$, because $\sum_pX_p(\ell)\log p=\log\mu(\ell)$ for every letter. Apply $e^x\ge e^y(1+x-y)$ term by term, with $x,y$ the exponents at $w$ and at $s\mathbf1$, and sum; the sum converges absolutely since $w$ is bounded and $a'>1$:
$$\Phi(w)\ge B(a')+a\,B(a')\Big[\sum_pw_p\mu_p(a')\log p-s\,E_{a'}\Big].$$
(ii) Put $a'=1+\epsilon$. The nesting part of $B$ differs from $\zeta(a')$ by a function analytic near $a'=1$, so $B=\epsilon^{-1}+O(1)$ and $E_{a'}=\epsilon^{-1}+O(1)$. For $p$ outside the torsion primes, using $(N/(N+1)^2)^{a'}=n^{-a'}(1+O(1/n))$ with $n=N+1$, and $N^{-a'}(1+O(1/N))$ in the second sum,
$$B\,\mu_p(a')=\frac{2\zeta(a')}{p^{a'}-1}-\frac{\zeta(a')}{p^{a'}-1}+O\big(p^{-a'-1}\big),$$
uniformly for small $\epsilon$. Hence $\mu_p(a')=(1+O(\epsilon))/(p^{a'}-1)+O(\epsilon\,p^{-a'-1})$. The finitely many torsion primes contribute $O(1)$. Multiply (i) by $\epsilon$: the left side is $\epsilon\sum_pw_p\log p\,p^{-1-\epsilon}+O(\epsilon)$ and the right side tends to $1-1/a$. $\square$

**Remarks.** (1) The set $\{p:\theta^\ast_p\ge\tau\}$ has upper logarithmic Dirichlet density at most $(1-1/a)/\tau$. (2) For the feasible set the constant cannot be improved: every constant weighting $w\equiv s<1-1/a$ is feasible. For the optimum $\theta^\ast$ the true average may be smaller; whether it is $0$ is open.

## 5. Computed observations (floating point; finite alphabets; not proofs)
Torsion lists $(2m+1)/(2m)$, $m\le K$. Weight at $p=2$ of the truncated optimum, $a=2$:

| $K$ | $M=10^3$ | $10^4$ | $10^5$ | $6\cdot10^5$ | $1.5\cdot10^6$ |
|---|---|---|---|---|---|
| 50 | 0.4495 | 0.4312 | 0.4293 | | |
| 800 | 0.6047 | 0.5597 | 0.5403 | 0.5345 | 0.5305 |
| 3200 | 0.6653 | 0.6070 | 0.5816 | | |

The same pattern occurs at $a=1.2$ and $a=3$. For $K=800$ and $3200$ the weight is still above $\frac12$ and still decreasing. The data do not determine the limit.

**A heuristic, not a result.** If the divisors of most $2^V-1$ carried negligible weight, the supply of coordinate $2$ would grow without bound as $\theta_2\uparrow\frac12$, and any finite demand would be met below $\frac12$. In a truncation only $V\le\log_2M$ is available, which would push the finite optimum above $\frac12$ and make it decrease slowly with $M$. By the lemma of section 1, the opposite outcome $\theta^\ast_2>\frac12$ requires weight on the divisors of $C2^V-1$ for every $C$ and all large $V$. Neither alternative is proved.
