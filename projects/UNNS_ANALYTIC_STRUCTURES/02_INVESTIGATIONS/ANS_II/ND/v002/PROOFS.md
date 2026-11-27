# ANS-II-ND v002 — Attainment and infinite prime-coordinate dynamics: proofs

Research notes. Uses ANS-II-ND v001 (Lemma 1, Theorems 1 and 3), ANS-II v002 and Linnik's theorem.

## 0. Setting
As in ANS-II-ND v001. Letters $\ell$ are the nesting labels $N\ge1$ and a finite list $A$ of torsion multipliers, with multiplier $\mu(\ell)$ and exponents $X_p(\ell)$; $P_0$ is the set of primes of $A$; $a>1$; $\Phi(\theta)=\sum_\ell\mathrm{term}_\theta(\ell)$ with $\mathrm{term}_\theta(\ell)=\mu(\ell)^{-a}\prod_pp^{a\theta_pX_p(\ell)}$. By Theorem 1 of v001, $\rho=\min\Phi$ over $\theta\in[0,\infty)^{\mathbb P}$, the minimiser $\theta^\ast$ is unique and $\theta^\ast_p<1$. Put $\nu^\ast=\mathrm{term}_{\theta^\ast}/\rho$, $m_p=\mathbb E_{\nu^\ast}X_p$, $E=\mathbb E_{\nu^\ast}\log\mu<\infty$, $m_p^+=\max(m_p,0)$, $m_p^-=\max(-m_p,0)$. Since $\sum_p|X_p(N)|\log p\le\log N+2\log(N+1)$ and $\log(N+1)<\log\mu(N)$, the series $\sum_p|m_p|\log p$ converges. Write
$$\Gamma=\sum_p\theta^\ast_p\,m_p\log p .$$
$\theta^M$, $L_M$, $\pi_M$ are the minimiser, minimum and optimal law for the alphabet $N\le M$ together with $A$; $\pi_M$ is resource-neutral and $\theta^M_pm_p(\pi_M)=0$.

Attainment means that some law on the full alphabet, with finite $\mathbb E\log\mu$, is resource-neutral and attains $H(\pi)-a\,\mathbb E_\pi\log\mu=\log\rho$. By v001 Theorem 3 the only candidate is $\nu^\ast$, and attainment is equivalent to condition (N): $m_p\ge0$ and $\theta^\ast_pm_p=0$ for all $p$.

## 1. The Euler-summability criterion (ND-T07, owner's proposal)
**Theorem 7.** If $\theta^\ast_p<\tfrac12$ for all $p$ and $\sum_pp^{-c_p}<\infty$, where $c_p=a(1-2\theta^\ast_p)$, then $\nu^\ast$ attains.

*Check of the proof.* The nesting term of $N$ is at most $(N+1)^{-a}\prod_pp^{2a\theta^\ast_pv_p(N+1)}=\prod_pp^{-c_pv_p(N+1)}$, so the sum over $N$ is at most $\prod_p(1-p^{-c_p})^{-1}<\infty$. Changing one $\theta_q$ by a small amount changes one Euler factor and keeps it finite (only increases are needed where $\theta^\ast_q=0$). Hence $\Phi$ is differentiable in each coordinate from the admissible sides at its minimum, which gives (N). The statement is **valid**. Its corollary ($\theta^\ast_p<\frac12$ for all $p$ and $\limsup\theta^\ast_p<(a-1)/(2a)$) is **valid**, because then $c_p\ge1+\delta$ for all large $p$. Theorem 10 below shows that the summability hypothesis can be removed.

## 2. The moment criterion (ND-T08, owner's proposal)
**Theorem 8.** $\nu^\ast$ attains if and only if $\log\mu$ is uniformly integrable under the family $(\pi_M)$; equivalently, if and only if $\mathbb E_{\pi_M}\log\mu\to E$.

*Check of the proof.* Sufficiency: $|X_p(N)|\log p\le2\log\mu(N)$, and the finitely many torsion letters are bounded. Uniform integrability and $\pi_M\to\nu^\ast$ in total variation give $m_p(\pi_M)\to m_p$, hence $m_p\ge0$; if $\theta^\ast_p>0$ then $\theta^M_p>0$ eventually, so $m_p(\pi_M)=0$ and $m_p=0$. Necessity: for $1<a'<a$,
$$H(\pi)-a\,\mathbb E_\pi\log\mu=\log B_A(a')-D_{\rm KL}(\pi\Vert\nu_{a'})-(a-a')\,\mathbb E_\pi\log\mu .$$
Both subtracted functionals are lower semicontinuous ($\log\mu$ is bounded below, which covers torsion multipliers below $1$). The left side at $\pi_M$ equals $\log L_M\to\log\rho$, its value at an attaining $\nu^\ast$; so each of the two converges, and $\mathbb E_{\pi_M}\log\mu\to E$. For non-negative variables (after adding a constant) convergence of means together with pointwise convergence of the laws gives uniform integrability. The statement is **valid**. $\square$

## 3. A variational inequality at the candidate (ND-T09)
**Theorem 9.** For every $w\in[0,\infty)^{\mathbb P}$ with $\Phi(w)<\infty$,
$$\sum_p(w_p-\theta^\ast_p)\,m_p\log p\ \ge\ 0 .$$

*Proof.* $w$ is bounded by v001 Lemma 1, applied to every finite alphabet with the bound $\max(\Phi(w),B_A(a))$. For $s\in(0,1]$ let $g(s)=\Phi(\theta^\ast+s(w-\theta^\ast))$. By convexity $g$ is finite, and $g(s)\ge g(0)=\rho$ by v001 Theorem 1(i). Each term has the form $t\,e^{sh(\ell)}$ with $h(\ell)=a\sum_p(w_p-\theta^\ast_p)X_p(\ell)\log p$. The quotients $t(e^{sh}-1)/s$ decrease as $s\downarrow0$ and are summable at $s=1$. By monotone convergence $0\le g'(0^+)=\sum_\ell t(\ell)h(\ell)$. The sum converges absolutely because $w-\theta^\ast$ is bounded, so the order of summation may be exchanged. $\square$

## 4. Depletion and surplus (ND-T10)
**Theorem 10.**
$$\sum_p\Big(\tfrac12-\theta^\ast_p\Big)m_p^-\log p\ +\ \sum_p\theta^\ast_p\,m_p^+\log p\ \le\ 0 .\qquad(\mathrm D)$$

*Proof.* Let $S$ be a finite set of primes with $m_p<0$ and $0<u<\frac12$; put $w_p=u$ on $S$ and $w_p=0$ elsewhere. Then $\Phi(w)<\infty$: the nesting sum is at most $\prod_{p\in S}(1-p^{-a(1-2u)})^{-1}\prod_{p\notin S}(1-p^{-a})^{-1}$. Theorem 9 reads $-u\sum_Sm_p^-\log p-\Gamma\ge0$. Let $S$ increase to all depleting primes and $u\uparrow\frac12$: $-\Gamma\ge\frac12\sum_pm_p^-\log p$. Now $-\Gamma=\sum\theta^\ast_pm_p^-\log p-\sum\theta^\ast_pm_p^+\log p$. $\square$

**Corollaries.**

1. *Neutrality is enough.* $\nu^\ast$ attains if and only if $m_p\ge0$ for all $p$. (If every $m_p^-=0$, (D) forces $\theta^\ast_pm_p^+=0$.)
2. *Attainment criterion.* $\nu^\ast$ attains if $\theta^\ast_p<\frac12$ at every prime with $m_p<0$. In particular **it attains if $\theta^\ast_p<\frac12$ for all $p$**. No summability, decay or uniform margin is needed; Theorem 7 and the criterion of v001 Theorem 3 are special cases.
3. *What failure would require.* If $\nu^\ast$ does not attain, there is a prime $s$ with $m_s<0$ and $\theta^\ast_s\ge\frac12$, and $\Phi(\theta^\ast+\epsilon e_s)=\infty$ for every $\epsilon>0$. (The last assertion: if it were finite, Theorem 9 would give $\epsilon\,m_s\ge0$.) Moreover $H(\nu^\ast)-aE=\log\rho-a\Gamma$ and
$$\tfrac12\sum_pm_p^-\log p\ \le\ -\Gamma\ \le\ \sum_p\theta^\ast_pm_p^-\log p .$$
4. If $\theta^\ast_p\le\frac12$ for all $p$, depletion can occur only at primes with $\theta^\ast_p=\frac12$, and $m_p=0$ at every prime with $0<\theta^\ast_p<\frac12$.

## 5. The weights cannot both stay below 1/2 and tend to zero (ND-T11)
Let $L$ be an admissible Linnik exponent: the least prime $q\equiv b\pmod d$, $(b,d)=1$, is at most $C_Ld^L$. Xylouris (Acta Arith. 150 (2011)) gives $L=5.18$.

**Theorem 11.** Suppose that some unweighted drift $\mu_p(a)$ is negative, that $\theta^\ast_p<\frac12$ for all $p$, and that $\sum_pp^{-c_p}<\infty$. Then
$$\limsup_{q\to\infty}\theta^\ast_q\ \ge\ \frac{2}{3L}\,\sup_p\theta^\ast_p\ >0 .$$
Consequently, when some drift is negative, **the two statements "$\theta^\ast_p<\frac12$ for all $p$" and "$\theta^\ast_p\to0$" cannot both hold.**

*Proof.* $\theta^\ast\ne0$ (v001 Theorem 5). Fix $p_0$ with $\theta_0=\theta^\ast_{p_0}>0$. For large $n$ let $q$ be the least prime with $q\equiv-1\pmod{p_0^{\,n}}$. Then $q\ge p_0^{\,n}-1\to\infty$, $q\notin P_0$, and $p_0^{\,n}\ge(q/C_L)^{1/L}$. By Theorem 10, $m_q\ge0$.

*Supply.* Positive exponents of $q$ come only from $N=jq-1$, with $X_q=2(1+v_q(j))$. Put $F(j)=\prod_pp^{2a\theta^\ast_pv_p(j)}$. Dropping the denominator factors, $\mathrm{term}(jq-1)\le(jq)^{-a}F(jq)=q^{-a(1-2\theta^\ast_q)}\,j^{-a}F(j)$. Hence the positive part of $\rho\,m_q$ is at most $q^{-a(1-2\theta^\ast_q)}C_q$ with $C_q=\sum_j2(1+v_q(j))j^{-a}F(j)$. The sum $\sum_jj^{-a}F(j)$ is the convergent Euler product $\prod_p(1-p^{-c_p})^{-1}$, and the factor $1+v_q(j)$ multiplies its $q$-th factor by at most a constant, because $q^{-c_q}\to0$. So $C_q\le C$ independently of $q$.

*Demand.* The letter $N=q$ has $X_q=-1$, and since $(q+1)^2\le4q^2$,
$$\mathrm{term}(q)\ge2^{-2a}q^{-a}q^{-a\theta^\ast_q}p_0^{\,2a\theta_0n}\ge c\,q^{-a-a\theta^\ast_q+2a\theta_0/L}.$$

Since $m_q\ge0$, supply is at least demand: $C\,q^{-a+2a\theta^\ast_q}\ge c\,q^{-a-a\theta^\ast_q+2a\theta_0/L}$, so
$$\theta^\ast_q\ge\frac{2\theta_0}{3L}-O\Big(\frac1{\log q}\Big).$$
For the last statement: if $\theta^\ast_p<\frac12$ and $\theta^\ast_p\to0$, then $c_p\to a>1$ and all $c_p>0$, so the sum converges, and the inequality contradicts the decay. $\square$

## 6. Where attainment stands
- Proved: attainment follows from $\theta^\ast_p<\frac12$ (all $p$, or only the depleting ones).
- Not proved: that this bound holds. v001 gives only $\theta^\ast_p<1$.
- Theorem 11 shows that, under that bound, finitely many large weights are not the whole picture: primes $q$ for which $q+1$ has a large power of a weighted prime keep weights bounded away from zero. This answers the decay question negatively in that regime. Without the bound it remains open.
- The computations below show truncated weights above $\frac12$ for one large torsion list. This does not decide the limit.

## 7. Computed observations (floating point; not proofs)
`nd2_checks.py`, results in `results/nd2_checks.json`.

- $2/\sqrt3$ at $a=2.06064$: largest weight about $0.093$ (at $p=3$) up to $M=2\cdot10^5$; most primes have weight $0$. Weights at primes $q=k\cdot3^n-1$ grow with $n$ (about $0.009$ at $53$, $0.040$ at $13121$).
- $3^{12}/2^{19}$ at $a=2$: at the Mersenne prime $131071=2^{17}-1$ the weight is about $0.068$, against $0.113$ at $p=2$.
- $200$ letters $(2m+1)/(2m)$ at $a=2$: the weight at $p=2$ is about $0.525$ for $M=10^3$ and $0.492$ for $M=2\cdot10^5$.
- Certificate of ND-T06 rerun with explicit validity checks on the trial weights; the same margins are obtained.

**Literature.** T. Xylouris, *On the least prime in an arithmetic progression and estimates for the zeros of Dirichlet L-functions*, Acta Arith. 150 (2011), 65–91, doi:10.4064/aa150-1-4. Only the existence of some finite $L$ (Linnik, 1944) is needed for positivity of the limit superior.
