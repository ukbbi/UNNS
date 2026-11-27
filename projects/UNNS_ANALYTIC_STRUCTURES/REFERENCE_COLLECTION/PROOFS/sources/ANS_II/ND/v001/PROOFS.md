# ANS-II-ND v001 — Entropy, resource neutrality and counting under negative drift: proofs

Research notes. Uses ANS-I v003 Lemma 2, ANS-II v001 Lemma 1 and ANS-II v002.

## 0. Setting
As in ANS-II v002: letters $\ell$ are the nesting labels $N\ge1$ and a finite list $A$ of torsion multipliers; $\mu(\ell)$ is the multiplier and $X_p(\ell)$ the exponent at $p$; $P_0$ is the set of primes of $A$; $a>1$, $B=B_A(a)$,
$$\Phi(\theta)=\Phi_A(a,\theta)=\sum_\ell\mu(\ell)^{-a}\prod_pp^{a\theta_pX_p(\ell)},\qquad\rho=\rho_A(a)=\min_{[0,1]^{\mathbb P}}\Phi,$$
$\mathbb P$ the set of primes. For a probability $\pi$ on letters with $\mathbb E_\pi|\log\mu|<\infty$ let $H(\pi)$ be its entropy, $m_p(\pi)=\mathbb E_\pi X_p$, and
$$\Lambda(\pi)=\mathbb E_\pi\log\mu+\sum_p[-m_p(\pi)]_+\log p .$$
Call $\pi$ **resource-neutral** if $m_p(\pi)\ge0$ for every $p$; then $\Lambda(\pi)=\mathbb E_\pi\log\mu$. Gibbs' inequality, for any $\theta\in[0,1]^{\mathbb P}$:
$$\log\Phi(\theta)\ge H(\pi)-a\,\mathbb E_\pi\log\mu+a\sum_p\theta_pm_p(\pi)\log p,\qquad(G)$$
with equality exactly when $\pi(\ell)$ is proportional to the term of $\ell$. The exchange of sums is legitimate since $\sum_p|X_p(N)|\log p\le\log N+2\log(N+1)$.

## 1. The optimum over all non-negative weights (ND-T02)
Take $M\ge\max P_0$ (any $M$ if $A$ is empty). Let $\Phi_M$ be the sum over $N\le M$ and $A$; its primes are those $\le M+1$.

**Lemma 1.** If $\theta\ge0$ and $\Phi_M(\theta)\le B$, then $\theta_q\le R=2c$ for all primes $q\le M+1$, where $c=1+\max(0,\log B)/(2a\log2)$.

*Proof.* The letter $q-1$ has $X_q=2$ and $X_p=-v_p(q-1)$ at the other primes, all smaller than $q$. Its term is at most $B$:
$$2a\theta_q\log q\le\log B+2a\log q-a\log(q-1)+a\sum_{p<q}\theta_pv_p(q-1)\log p .$$
With $T=\max_{p<q}\theta_p$ the last sum is at most $T\log q$, so $\theta_q\le c+T/2$. Induction on $q$ gives $\theta_q\le2c$. $\square$

So $\Phi_M$ attains its minimum $L_M$ over the whole orthant $[0,\infty)^{\{p\le M+1\}}$ at some $\theta^M\in[0,R]$.

**Theorem 1.** (i) $\Phi(\theta)\ge\rho$ for every $\theta\in[0,\infty)^{\mathbb P}$: the upper restriction $\theta_p\le1$ is never active. (ii) The minimiser $\theta^\ast$ of $\Phi$ on the cube is unique, and $\theta^\ast_p<1$ for every $p$. (iii) $L_M\uparrow\rho$ and $\theta^M\to\theta^\ast$ coordinatewise.

*Proof.* $L_M$ increases with $M$, and $L_M\le\Phi_M(\theta)\le\rho$ at a cube minimiser $\theta$. Let $\theta^\infty$ be an accumulation point of $\theta^M$ in $[0,R]^{\mathbb P}$. For fixed $M'$, $\Phi_{M'}(\theta^\infty)=\lim\Phi_{M'}(\theta^M)\le\liminf L_M$ along the subsequence, so $\Phi(\theta^\infty)\le L=\lim L_M\le\rho$.

Let $T=\sup_p\theta^\infty_p$. For a prime $p$ and $v\ge1$ the letter $N=p^v-1$ has $X_p=2v$, and its other exponents are $-v_q(N)$; hence its term is at least
$$N^{a}p^{-2av}\,p^{2a\theta^\infty_pv}\,N^{-aT}\ \ge\ 2^{-a}\,p^{av(2\theta^\infty_p-1-T)}$$
(for $T>1$ use $N<p^v$ and drop $2^{-a}$). These are distinct letters and $\Phi(\theta^\infty)<\infty$, so $\theta^\infty_p<(1+T)/2$ for every $p$. Taking the supremum, $T\le(1+T)/2$, that is $T\le1$. So $\theta^\infty$ lies in the cube, $\Phi(\theta^\infty)\ge\rho$, and $L=\rho=\Phi(\theta^\infty)$. Also $\theta^\infty_p<(1+T)/2\le1$.

*Uniqueness.* For two cube minimisers, Cauchy–Schwarz termwise gives $\Phi(\text{midpoint})\le\sqrt{\Phi\,\Phi}=\rho$, with equality only if the terms are proportional, hence equal. So $\sum_p\Delta_pX_p(\ell)\log p=0$ for their difference $\Delta$. The letters $N=q-1$, in increasing order of the prime $q$, give $\Delta_q=0$. Therefore every accumulation point equals $\theta^\ast$, which proves (iii). Finally (i): for $\theta\ge0$, $\Phi(\theta)\ge\Phi_M(\theta)\ge L_M\to\rho$. $\square$

## 2. Variational principles (ND-T01, ND-T02)
**Theorem 2.**
$$\log\rho=\sup_{\pi}\big[H(\pi)-a\Lambda(\pi)\big]=\sup_{\pi\ \text{resource-neutral}}\big[H(\pi)-a\,\mathbb E_\pi\log\mu\big],$$
both over finitely supported $\pi$. For multipliers $>1$, the abscissa $\sigma^\ast$ satisfies
$$\sigma^\ast=\sup_\pi\frac{H(\pi)}{\Lambda(\pi)}=\sup_{\pi\ \text{resource-neutral}}\frac{H(\pi)}{\mathbb E_\pi\log\mu}.$$
The first formula in each line is the owner's proposal.

*Proof.* In $(G)$ at $\theta^\ast$, $\theta^\ast_pm_p\ge-[-m_p]_+$; so $\log\rho\ge H-a\Lambda$ for every $\pi$. Let $\pi_M(\ell)$ be the term of $\ell$ at $\theta^M$ divided by $L_M$. The minimum over the orthant gives $a\log p\,L_M\,m_p(\pi_M)=\partial_p\Phi_M\ge0$, with equality if $\theta^M_p>0$. So $\pi_M$ is resource-neutral and, by equality in $(G)$, $H(\pi_M)-a\,\mathbb E\log\mu=\log L_M\to\log\rho$. For $\sigma^\ast$: $\rho_A(\sigma^\ast)=1$ gives $H\le\sigma^\ast\Lambda$ always, and neutral $\pi_M$ at $a=\sigma^\ast$ have $H-\sigma^\ast\mathbb E\log\mu\to0$ with $\mathbb E\log\mu$ bounded below by a positive constant. $\square$

**Corollary 1 (depletion is never optimal).** For every $\pi$,
$$\log\rho-\big[H(\pi)-a\Lambda(\pi)\big]\ \ge\ a\sum_{p:\,m_p<0}(1-\theta^\ast_p)\,|m_p(\pi)|\log p,$$
which is positive as soon as some drift is negative. *Proof:* $(G)$ at $\theta^\ast$ and $\theta^\ast_p<1$. $\square$

## 3. The optimal law (ND-T03)
**Theorem 3.** Let $\nu^\ast(\ell)=\mu(\ell)^{-a}\prod p^{a\theta^\ast_pX_p(\ell)}/\rho$. Then $\nu^\ast$ is a probability, $\pi_M\to\nu^\ast$ in total variation, and $\mathbb E_{\nu^\ast}\log\mu<\infty$. There is a probability $\pi$ on the full alphabet, with $\mathbb E_\pi\log\mu<\infty$, that is resource-neutral and attains $H(\pi)-a\,\mathbb E_\pi\log\mu=\log\rho$ if and only if
$$m_p(\nu^\ast)\ge0\ \text{ and }\ \theta^\ast_p\,m_p(\nu^\ast)=0\quad\text{for all }p;\qquad(\mathrm N)$$
in that case $\pi=\nu^\ast$. Condition (N) holds if $\sup_p\theta^\ast_p<(a-1)/(2a)$.

*Proof.* $\sum_\ell\nu^\ast=\Phi(\theta^\ast)/\rho=1$, and $\pi_M\to\nu^\ast$ pointwise by Theorem 1; Scheffé's lemma gives total variation. For $1<a'<a$, Gibbs gives $H(\pi_M)\le a'\mathbb E_{\pi_M}\log\mu+\log B_A(a')$; with $H(\pi_M)=a\,\mathbb E_{\pi_M}\log\mu+\log L_M$ this bounds $\mathbb E_{\pi_M}\log\mu$, and Fatou's lemma applies. If $\pi$ attains, then in $\log\rho\ge H-a\,\mathbb E\log\mu+a\sum\theta^\ast_pm_p\log p\ge\log\rho$ both inequalities are equalities: $\pi=\nu^\ast$ and $\theta^\ast_pm_p=0$. Conversely (N) and equality in $(G)$ give attainment. If $\sup\theta^\ast_p\le t<(a-1)/(2a)$, every $\theta$ with $\sup\theta_p\le t'$, $t<t'<(a-1)/(2a)$, has finite $\Phi$ (the nesting term of $N$ is at most $N^{-a(1-2t')}$). So $\Phi$ can be differentiated in each coordinate at $\theta^\ast$, and Theorem 1(i) gives (N). $\square$

Whether (N) always holds is open.

## 4. Counting functions (ND-T04)
**Theorem 4.** Let all torsion multipliers exceed $1$. For every state $x=a_\varphi n$, with $N_x$ the number of histories from $x$, $A_\varphi$ the number of minimal histories and $C_\varphi$ the all-source count, each with endpoint at most $X$,
$$\lim_{X\to\infty}\frac{\log N_x(X)}{\log X}=\lim\frac{\log A_\varphi(X)}{\log X}=\lim\frac{\log C_\varphi(X)}{\log X}=\sigma^\ast,$$
for any signs of the drifts.

*Proof.* A history from $x$ with endpoint at most $X$ has $E_\varphi(w)\le X$, so $N_x\le A_\varphi\le C_\varphi$. By ANS-II v002 Corollary 2, $A_\varphi(Y)\le C_\epsilon Y^{\sigma^\ast+\epsilon}$; summing over $A_\varphi(X/m)$, with $\sigma^\ast>1$, gives $C_\varphi(X)=O(X^{\sigma^\ast+\epsilon})$. It remains to bound $N_x$ from below.

Let $\pi$ be finitely supported and resource-neutral, with support in the letters $N\le M$ and $A$, and let $v$ consist of $k$ independent letters of law $\pi$. For $p\le M+1$ write $S_p(j)=m_pj+M_p(j)$ with $m_p\ge0$. By ANS-II v001 Lemma 1, $v_p(K_\varphi(v))\le1+\max_{j\le k}|M_p(j)|$, and $v_p=0$ for larger $p$. By Doob's inequality there is $C$ such that with probability at least $3/4$ every $v_p(K_\varphi(v))\le t_k=\lceil C\sqrt k\rceil$. By the law of large numbers, with probability tending to $1$, $\Pr(v)\le e^{-k(H-\epsilon)}$ and $\log Q(v)\le k(\mathbb E\log\mu+\epsilon)$. So for large $k$ at least $\tfrac12e^{k(H-\epsilon)}$ words have all three properties.

Let $T=\prod_{p\le M+1}p^{t_k}$ and let $w^\ast$ be the nesting word of ANS-I v003 Lemma 2: it is admissible from $1$, $T\mid Q(w^\ast)$ and $\log Q(w^\ast)\le2\log T+2\theta(M+1)=O(\sqrt k)$. Being a nesting word admissible from $1$, it is admissible from $a_\varphi n$ and ends at $a_\varphi nQ(w^\ast)$, whose integer part is divisible by every such $K_\varphi(v)$. So every $w^\ast v$ is a history from $x$, with endpoint $x\,Q(w^\ast)Q(v)$. Choosing $k=\lfloor\log X/(\mathbb E\log\mu+2\epsilon)\rfloor$,
$$\liminf\frac{\log N_x(X)}{\log X}\ge\frac{H-\epsilon}{\mathbb E\log\mu+2\epsilon}.$$
Let $\epsilon\to0$ and take the supremum with Theorem 2. $\square$

**Remarks.** The counting limits for $A_\varphi$ and $C_\varphi$ follow also from the owner's argument with depleting laws. For a fixed source a depleting law cannot be used, because its sources grow exponentially with depth; Theorem 2 shows that none is needed. Hence a fixed state has the same exponent as the complete family of minimal histories. Lower-order factors are not determined.

## 5. The optimal weights have infinite support (ND-T05)
**Theorem 5.** Let $a>1$. If all drifts $\mu_p(a)$ under the unweighted law $\nu_a$ are non-negative, then $\theta^\ast=0$. If one is negative, then $\theta^\ast_p>0$ for infinitely many primes $p$.

*Proof.* In the first case $e^x\ge1+x$ gives $\Phi(\theta)\ge B$ for $\theta\ge0$ (ANS-II v002 Corollary 3). In the second, $\Phi(\epsilon e_p)<B$ for small $\epsilon$, so $\theta^\ast\ne0$. Suppose its support $S$ is finite and pick $p_0\in S$.

(a) *Every $\theta^\ast_s<1/2$.* Fix $s\in S$ and let $n_0$ be the product of the other primes of $S$. The letters $N=s^vn_0-1$, $v\ge1$, are prime to all of $S$, so their terms are at least $N^a(N+1)^{-2a}s^{2a\theta^\ast_sv}\ge c\,s^{-av(1-2\theta^\ast_s)}$. Finiteness of $\Phi(\theta^\ast)$ forces $\theta^\ast_s<1/2$.

(b) *Perturbation.* For finitely supported $\theta$ with all $\theta_s<1/2$, the nesting term of $N$ is at most $(N+1)^{-a}\prod_Ss^{2a\theta_sv_s(N+1)}$, and the sum over $n=N+1$ factors into convergent Euler factors. So for a prime $q\notin S\cup P_0$ the function $\epsilon\mapsto\Phi(\theta^\ast+\epsilon e_q)$ is finite near $0$, and minimality gives $\sum_\ell\mathrm{term}(\ell)X_q(\ell)\ge0$.

(c) *Supply of $q$ is bounded.* The positive exponents of $q$ come from $N=jq-1$, with $X_q=2(1+v_q(j))$. Such a term is at most $(jq)^{-a}\prod_Ss^{2a\theta^\ast_sv_s(j)}$. Hence the positive part is at most $Cq^{-a}$, where
$$C=\sum_{j\ge1}2(1+\log_2j)\,j^{-a}\prod_{s\in S}s^{2a\theta^\ast_sv_s(j)}<\infty$$
does not depend on $q$.

(d) *Demand of one letter is larger.* The negative part includes the letter $N=q$, with $X_q=-1$ and term $q^a(q+1)^{-2a}\prod_Ss^{2a\theta^\ast_sv_s(q+1)}\ge2^{-2a}q^{-a}\,p_0^{2a\theta^\ast_{p_0}v_{p_0}(q+1)}$. By Dirichlet's theorem there are primes $q\equiv-1\pmod{p_0^{\,n}}$ for every $n$. For $n$ large the demand exceeds $Cq^{-a}$, so the sum in (b) is negative: a contradiction. $\square$

Thus a finite torsion list with one negative drift changes the optimal weights at infinitely many primes.

## 6. A certified interval for $2/\sqrt3$ (ND-T06)
$$2.06055\le\sigma^\ast\le2.06072 .$$
*Method.* The inequalities of ANS-II v002 §7 are valid for any weights. The weights are found in floating point; the two certificates are then evaluated with MPFR arithmetic at 80 bits, every operation rounded in the safe direction (`certify.py`), at $a=2.06055+2^{-40}$ (lower certificate $\ge1$, margin $5.8\cdot10^{-6}$) and $a=2.06072-2^{-40}$ (upper certificate $<1$, margin $1.3\cdot10^{-6}$). The statement relies on the correct rounding of MPFR and on the program.
