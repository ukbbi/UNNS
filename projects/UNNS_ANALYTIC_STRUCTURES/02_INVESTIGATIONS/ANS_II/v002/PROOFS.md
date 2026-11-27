# ANS-II v002 — Divisibility-resolved transfer operators and the convergence boundary: proofs

Research notes. Uses ANS-I v001–v003 and ANS-II v001.

## 0. Setting
As in ANS-II v001: a finite list $A$ of multipliers $\alpha_j>1$ with a rational power; letters $\ell$ are the nesting labels $N\ge1$ and the $\alpha_j$, with multiplier $\mu(\ell)$ and exponent $X_p(\ell)$ at $p$; $P_0$ is the finite set of primes of the $\alpha_j$; states are $a_\psi n$ with $\psi$ in the finite class group $\Phi_A$. $B_A(a)=\sum_\ell\mu(\ell)^{-a}$ for $a>1$, $\sigma_A$ is its root of $B_A=1$, $\nu_a(\ell)=\mu(\ell)^{-a}/B_A(a)$, and $\mu_p(a)=\mathbb E_{\nu_a}X_p$ is the drift at $p$. Fix the initial class $\varphi$. For a word $w$ from $\varphi$ let $\psi(w)$ be its terminal class and $n(w)$ the integer part of its minimal endpoint, $E_\varphi(w)=a_{\psi(w)}n(w)$. Put $\mathcal G_{\varphi,k}(s)=\sum_{|w|=k}E_\varphi(w)^{-s}$.

## 1. One letter (ANS2-T10, T14)
A letter $\ell$ takes class $\psi$ to a class $\psi'$ with $\mu(\ell)a_\psi=a_{\psi'}\,u/v$, where $u/v$ is reduced. Here $u,v$ depend on $(\psi,\ell)$. For a nesting letter $\psi'=\psi$, $u=(N+1)^2$, $v=N$. For fixed $\ell$ the map $\psi\mapsto\psi'$ is a bijection of $\Phi_A$. No sign condition on the exponents is used.

**Lemma 1.** $\displaystyle n(w\ell)=\frac{u\,n(w)}{\gcd(n(w),v)}$ and $E_\varphi(w\ell)=E_\varphi(w)\,\mu(\ell)\,\dfrac{v}{\gcd(n(w),v)}$.

*Proof.* The histories of $w$ from $\varphi$ end at the states $a_\psi n(w)m$, $m\ge1$. The letter $\ell$ is admissible there exactly when $v\mid n(w)m$, and the new integer part is $u\,n(w)m/v$. The least such $m$ is $v/\gcd(n(w),v)$. $\square$

**Lemma 2 (divisibility pullback).** For $d\ge1$ put
$$D(d)=\prod_{p:\,v_p(d)>v_p(u)}p^{\,v_p(v)+v_p(d)-v_p(u)}.$$
Then $d\mid n(w\ell)$ if and only if $D(d)\mid n(w)$. For a nesting letter this is $D_N(d)=\prod_{v_p d>2v_p(N+1)}p^{\,v_pN+v_pd-2v_p(N+1)}$.

*Proof.* Since $\gcd(u,v)=1$, $v_p(n(w\ell))=v_p(u)+\max\big(v_p(n(w))-v_p(v),0\big)$. This is at least $v_p(d)$ automatically if $v_p(d)\le v_p(u)$, and otherwise exactly when $v_p(n(w))\ge v_p(v)+v_p(d)-v_p(u)$. $\square$

## 2. The operator system (ANS2-T11, T12, T13)
Define, for $\psi\in\Phi_A$, $d\ge1$,
$$F^{(k)}_{\psi,d}(s)=\sum_{|w|=k,\ \psi(w)=\psi,\ d\mid n(w)}E_\varphi(w)^{-s},$$
and let $J_s(h)=\sum_{e\mid h}\mu_{\rm M}(e)(h/e)^s$ ($\mu_{\rm M}$ the Möbius function).

**Theorem.** For $\operatorname{Re}s>1$, $F^{(k+1)}=L_sF^{(k)}$ with
$$(L_sF)_{\psi',d}=\sum_{\ell}\mu(\ell)^{-s}v^{-s}\sum_{h\mid v}J_s(h)\,F_{\psi,\,\operatorname{lcm}(h,D(d))},$$
where for each $\ell$, $\psi$ is the class carried to $\psi'$ and $u,v,D$ belong to $(\psi,\ell)$. The initial vector is $F^{(0)}_{\psi,d}=a_\varphi^{-s}[\psi=\varphi][d=1]$, and $\mathcal G_{\varphi,k}=\sum_\psi F^{(k)}_{\psi,1}$.

*Proof.* By Lemma 1 a word $w\ell$ has weight $E_\varphi(w)^{-s}\mu^{-s}v^{-s}\gcd(n(w),v)^s$, and by Lemma 2 it is counted in $F_{\psi',d}$ when $D(d)\mid n(w)$. Möbius inversion gives $\gcd(n,v)^s=\sum_{h\mid\gcd(n,v)}J_s(h)$. Exchange the sums; the two conditions $h\mid n(w)$ and $D(d)\mid n(w)$ are $\operatorname{lcm}(h,D(d))\mid n(w)$. For $\sigma=\operatorname{Re}s>1$ the double sum is bounded by $\sum_\ell\mu^{-\sigma}\tau(v)^2\sup|F|<\infty$ ($\tau$ the divisor function), so all rearrangements are legitimate. $\square$

**The two kinds of letter.** Nesting letters keep the class: with $v=N$, $\mu^{-s}v^{-s}=(N+1)^{-2s}$, giving
$$(T_NF)_{\psi,d}=(N+1)^{-2s}\sum_{h\mid N}J_s(h)F_{\psi,\operatorname{lcm}(h,D_N(d))}.$$
A torsion letter with non-negative exponents has $v=1$ and integer carry $u=c$, giving the pure shift $(S_\alpha F)_{\psi',d}=\alpha^{-s}F_{\psi,\,d/\gcd(d,c)}$.

**Why infinitely many coordinates.** A representation with finitely many deterministic states that reproduces every letter weight is impossible: the weights of Lemma 1 involve $\gcd(n,N)$ for all $N$, which determine $n$, and infinitely many $n$ occur. This does not exclude other kinds of finite description.

## 3. Bounded realizations (ANS2-T15)
Let $s>1$ be real.

**Uniform norm.** On $\ell^\infty(\Phi_A\times\mathbb N)$ the operator $L_s$ is positive and $L_s\mathbf 1=B_A(s)\mathbf 1$, because $\sum_{h\mid v}J_s(h)=v^s$. Hence $\|L_s\|=B_A(s)$ and $B_A(s)$ is its spectral radius. This norm does not see the drifts.

**Measures on states.** Put $m_k(\psi,n)=\sum_{|w|=k,\,\psi(w)=\psi,\,n(w)=n}E_\varphi(w)^{-s}$. Then $m_{k+1}=Mm_k$, where $M$ sends a unit mass at $(\psi,n)$ to the masses $\mu^{-s}(\gcd(n,v)/v)^s$ at $(\psi',un/\gcd(n,v))$, and $\mathcal G_{\varphi,k}(s)=\|m_k\|_1$. For $\theta=(\theta_q)\in[0,1]^{\text{primes}}$ let
$$V_\theta(\psi,n)=\prod_qq^{\,\theta_qs\,v_q(a_\psi n)}\ge1,\qquad\Phi_A(s,\theta)=\sum_\ell\mu(\ell)^{-s}\prod_qq^{\,\theta_qsX_q(\ell)}\in(0,\infty].$$

**Theorem.** $\|M\|_{\ell^1(V_\theta)}=\Phi_A(s,\theta)$, in the following sense: the supremum of the weighted column sums equals $\Phi_A(s,\theta)$; $M$ is a bounded operator on $\ell^1(V_\theta)$ with this norm when $\Phi_A(s,\theta)<\infty$, and is unbounded when it is infinite.

*Proof.* Let $\delta_q=\max(v_q(v)-v_q(n),0)$. By Lemma 1, $v_q(a_{\psi'}n')-v_q(a_\psi n)=X_q(\ell)+\delta_q$ and $(\gcd(n,v)/v)^s=\prod q^{-s\delta_q}$. So the weight of the move, times $V_\theta(\text{image})/V_\theta(\text{source})$, equals
$$\mu^{-s}\prod_qq^{\,\theta_qsX_q}\,q^{-s(1-\theta_q)\delta_q}\le\mu^{-s}\prod_qq^{\,\theta_qsX_q},$$
with equality when $v\mid n$. The norm is the supremum over $(\psi,n)$ of the sum over letters. It is at most $\Phi_A$; taking $n$ divisible by every $v$ of the letters $N\le M$ and of the $\alpha_j$, and then $M\to\infty$, shows it is at least $\Phi_A$. $\square$

## 4. The growth rate (ANS2-T16)
For $a>1$ let
$$\rho_A(a)=\min_{\theta\in[0,1]^{\text{primes}}}\Phi_A(a,\theta).$$
The minimum exists: the cube is compact, $\Phi_A$ is lower semicontinuous (a sum of positive continuous functions of finitely many coordinates), and $\Phi_A(a,0)=B_A(a)<\infty$. $\Phi_A(a,\cdot)$ is convex.

**Theorem.** For every finite list $A$ as in §0 (any signs of the drifts), every $a>1$ and every class $\varphi$,
$$\lim_{k\to\infty}\mathcal G_{\varphi,k}(a)^{1/k}=\rho_A(a).$$

*Proof of the upper bound.* $\mathcal G_{\varphi,k}=\|m_k\|_1\le\|m_k\|_{\ell^1(V_\theta)}\le\Phi_A(a,\theta)^kV_\theta(\varphi,1)a_\varphi^{-a}\le C\,\Phi_A(a,\theta)^k$ with $C$ depending only on $A$ and $a$. $\square$

*Proof of the lower bound.* Keep the $\alpha_j$ and only the nesting letters $N\le M$ ($M$ large), and write $\Phi_M$ for the corresponding sum; it depends on the coordinates $\theta_q$ for a finite set $\mathcal P_M$ of primes and is continuous. Let $\theta^\ast$ minimise it on the cube, and let $\nu^\ast(\ell)=\mu(\ell)^{-a}\prod_qq^{\theta^\ast_qaX_q(\ell)}/\Phi_M(\theta^\ast)$, a probability on the truncated alphabet. Put $m_q=\mathbb E_{\nu^\ast}X_q$. Since $\partial\Phi_M/\partial\theta_q=a\log q\,\Phi_M\,m_q$ at $\theta^\ast$, the conditions for a minimum on the cube are
$$\theta^\ast_q=0\Rightarrow m_q\ge0,\qquad0<\theta^\ast_q<1\Rightarrow m_q=0,\qquad\theta^\ast_q=1\Rightarrow m_q\le0.\qquad(\ast)$$
Writing $S_q(j)$ for the sum of $X_q$ over the first $j$ letters, and using $E_\varphi=a_\varphi K_\varphi Q$ and $Q^{-a}=\nu^\ast(w)\,\Phi_M^k\prod_i\prod_qq^{-\theta^\ast_qaX_q(\ell_i)}$,
$$\mathcal G^{(M)}_{\varphi,k}=a_\varphi^{-a}\,\Phi_M(\theta^\ast)^k\;\mathbb E_{\nu^\ast}\prod_{q\in\mathcal P_M}q^{-a\,(v_q(K_{\varphi,k})+\theta^\ast_qS_q(k))}.$$
By Jensen's inequality it suffices to show $\mathbb E_{\nu^\ast}\big(v_q(K_{\varphi,k})+\theta^\ast_qS_q(k)\big)\le C_M(1+\sqrt k)$. By ANS-II v001 Lemma 1, $v_q(K_{\varphi,k})\le1+\max_{0\le j\le k}(-S_q(j))$. Drop the index $q$, write $\theta=\theta^\ast_q$ and $S_j=mj+M_j$, where $M_j$ is a martingale with bounded independent increments. Then
$$v+\theta S_k\le1+\max_j\big[\theta(S_k-S_j)-(1-\theta)S_j\big].$$
The part of the bracket coming from the drift is $\theta m(k-j)-(1-\theta)mj$, which is $\le0$ in each of the three cases $(\ast)$. The rest is $\theta(M_k-M_j)-(1-\theta)M_j\le|M_k|+\max_j|M_j|$, whose mean is $O(\sqrt k)$ by Doob's inequality. Hence $\mathcal G^{(M)}_{\varphi,k}\ge c\,\Phi_M(\theta^\ast)^ke^{-C_M\sqrt k}$.

Since $\mathcal G_{\varphi,k}\ge\mathcal G^{(M)}_{\varphi,k}$, $\liminf\mathcal G_{\varphi,k}^{1/k}\ge\min\Phi_M$ for every $M$. It remains to see that $L=\sup_M\min\Phi_M$ is at least $\min\Phi_A$ (it is clearly at most it). The sets $\{\theta:\Phi_M(\theta)\le L\}$ are closed, non-empty and decreasing in $M$ in the compact cube, so some $\theta$ lies in all of them. Then $\Phi_A(a,\theta)=\sup_M\Phi_M(\theta)\le L$. $\square$

**Remark.** The theorem on the growth rate does not use $\alpha_j>1$; the statements on abscissae below do.

**Corollary 1 (operator form).** With $\theta$ a minimiser, $M$ is bounded on $\ell^1(V_\theta)$ with norm and spectral radius equal to $\rho_A(a)$.

*Proof.* The norm is $\Phi_A(a,\theta)=\rho_A(a)$ (§3), and $\|M^km_0\|_{\ell^1(V_\theta)}\ge\mathcal G_{\varphi,k}$ bounds the spectral radius below by $\rho_A(a)$. $\square$

## 5. The convergence boundary (ANS2-T16, continued)
**Corollary 2 (abscissa).** The abscissa $\sigma^\ast$ of $\mathcal G_\varphi(s,1)=\sum_k\mathcal G_{\varphi,k}(s)$ is the unique root of $\rho_A(a)=1$; it is the same in every class and lies in $[\sigma_c,\sigma_A]$. Consequently $\limsup\log A_\varphi(X)/\log X=\sigma^\ast$.

*Proof.* $E_\varphi(w)\ge\lambda^{|w|}$ with $\lambda=\min(4,\min\alpha_j)>1$, so $\rho_A(a+\delta)\le\lambda^{-\delta}\rho_A(a)$: $\rho_A$ is strictly decreasing. $\log\rho_A$ is a limit of the convex functions $k^{-1}\log\mathcal G_{\varphi,k}$ and is finite, hence convex and continuous. Words of nesting letters alone give $\rho_A(a)\ge\rho_{\emptyset}(a)=B_{\emptyset}(a)$ (ANS-I v001, Theorem 4.4, with ANS-II v001 Lemma 2), which exceeds $1$ for $a<\sigma_c$; and $\rho_A\le B_A<1$ for $a>\sigma_A$. The root test finishes the first statement. The second is the usual formula for the abscissa of a Dirichlet series with non-negative coefficients (here $\sigma^\ast>0$). $\square$

**Corollary 3 (sharp dichotomy).** $\sigma^\ast=\sigma_A$ if every drift $\mu_p(\sigma_A)$, $p\in P_0$, is $\ge0$; and $\sigma^\ast<\sigma_A$ if one of them is negative.

*Proof.* For $p\notin P_0$ the drift is positive (ANS-II v001 §3). Suppose all drifts are $\ge0$ at $\sigma=\sigma_A$. By $e^x\ge1+x$,
$$\Phi_A(\sigma,\theta)\ge\sum_\ell\mu^{-\sigma}\Big(1+\sigma\sum_q\theta_qX_q(\ell)\log q\Big)=1+\sigma\sum_q\theta_q\,\mu_q(\sigma)\log q\ge1,$$
the exchange of sums being justified by $\sum_q|X_q(N)|\log q\le\log N+2\log(N+1)$. So $\rho_A(\sigma_A)=1$. If $\mu_p(\sigma_A)<0$, then $\theta\mapsto\Phi_A(\sigma_A,\theta e_p)$ equals $1$ at $0$ with negative derivative, so $\rho_A(\sigma_A)<1$. $\square$

This contains the abscissa statements of v001 (T02, T05) and the zero-drift case.

## 6. Non-negative drift: depth order (ANS2-T09, T09a)
**Proposition (T09, the owner's review).** If one or more drifts vanish at $\sigma_A$ and the others are positive, then $\mathcal G_\varphi(\sigma_A,1)<\infty$ and the abscissa is $\sigma_A$.

*Proof.* The inequality $\mathbb E_{\nu_a}K_{\varphi,k}^{-b}\le\exp(-ck^{1/a}/\log k)$ of v001 §4 uses no drift hypothesis, and $\mathcal G_{\varphi,k}(\sigma_A)=a_\varphi^{-\sigma_A}\mathbb E K_{\varphi,k}^{-\sigma_A}$ is therefore summable. The abscissa follows from $\mathcal G_{\varphi,k}(\sigma_A-\delta)\ge\lambda^{k\delta}\mathcal G_{\varphi,k}(\sigma_A)$ as in Corollary 2, or from Corollary 3. $\square$

The review note also controls the depth bound with $\mathbb E v_p(K_{\varphi,k})=O(\sqrt k)$ at a zero-drift prime, which gives $-\log\mathbb E K^{-b}=O(k^\beta+\sqrt k)$. The next theorem removes the $\sqrt k$.

**Theorem (T09a).** Let $a>1$, $b>0$, $\beta=1/a$, and suppose $\mu_p(a)\ge0$ for all $p\in P_0$. Then for large $k$
$$\frac{c\,k^\beta}{\log k}\le-\log\mathbb E_{\nu_a}K_{\varphi,k}^{-b}\le C\,k^\beta.$$

*Proof.* The left inequality is v001 §4. If no drift vanishes, the right one is the argument of v001 §4. Otherwise let $Z\subseteq P_0$ be the set of zero-drift primes and $N^\ast=\prod_{p\in Z}p-1$, a letter with $X_p(N^\ast)=2$ for all $p\in Z$. Fix $\eta\in(0,\beta)$ and $\varepsilon_j=\varepsilon_0j^{-(1-\eta)/2}$, and let $\mathsf Q$ make the letters independent, the $j$-th with law $(1-\varepsilon_j)\nu_a+\varepsilon_j\delta_{N^\ast}$.

**Cost.** By the variational inequality $-\log\mathbb E_\nu e^{-b\log K}\le b\,\mathbb E_{\mathsf Q}\log K+\mathrm{KL}(\mathsf Q\,\|\,\nu_a^k)$, and
$$\mathrm{KL}\le\sum_{j\le k}\chi^2=\sum_{j\le k}\varepsilon_j^2\Big(\frac1{\nu_a(N^\ast)}-1\Big)=O(k^\eta)=O(k^\beta).$$
It remains to show $\mathbb E_{\mathsf Q}\log K_{\varphi,k}=O(k^\beta)$. Recall $v_p(K_{\varphi,k})\le1+\max_{j\le k}(-S_p(j))$.

**(i) $p\in Z$.** $S_p(j)=D_j+M_j$ with $D_j=\mathbb E_{\mathsf Q}S_p(j)=2\sum_{i\le j}\varepsilon_i\ge2\varepsilon_0j^{(1+\eta)/2}$, and $M_j$ a martingale whose independent increments have uniformly exponential tails. Hence $\Pr(\max_{j\le n}(-M_j)\ge x)\le\exp(-c\min(x^2/n,x))$. If $-S_p(j)\ge r\ge1$ for some $j\in[2^i,2^{i+1})$, then $\max_{j\le2^{i+1}}(-M_j)\ge r+D_{2^i}$. The probability is at most
$$\exp\big(-c(2^{i\eta}+r\,2^{-i(1-\eta)/2})\big)+\exp\big(-c(r+2^{i(1+\eta)/2})\big).$$
Both terms are summable over $r\ge1$ and $i\ge0$ (the first because $\sum_i2^{i(1-\eta)/2}e^{-c2^{i\eta}}<\infty$). So $\mathbb E_{\mathsf Q}v_p(K_{\varphi,k})\le C$, uniformly in $k$.

**(ii) The other primes in $P_0$, and primes dividing $N^\ast$.** These are finitely many, none in $Z$ (the primes of $N^\ast+1$ are exactly those of $Z$), and each has $\mu_p(a)>0$. So $\mathbb E_{\nu_a}e^{-\eta_pX_p}<1$ for a small $\eta_p>0$, and for $\varepsilon_0$ small the same expectation under every step law is $\le1$. Ville's inequality bounds $\mathbb E_{\mathsf Q}v_p(K_{\varphi,k})$.

**(iii) All remaining primes.** Here $X_p(N^\ast)=0$, so each step law satisfies $\mathbb E e^{-\eta X_p}\le1$ with the uniform $\eta$ of ANS-I v002 Lemma B. Let $\tau$ be the first step with a nesting letter divisible by $p$. The atom $N^\ast$ is not divisible by $p$, so $\Pr_{\mathsf Q}(\tau\le k)\le k\,\nu_a(p\mid N)\le Ckp^{-a}$, and given $p\mid N_\tau$ the letter has the conditioned $\nu_a$ law. Before $\tau$, $S_p\ge0$; after it, $-S_p(j)\le v_p(N_\tau)+\sup_h\big(S_p(\tau)-S_p(\tau+h)\big)$. Both have bounded conditional mean. So $\mathbb E_{\mathsf Q}v_p(K_{\varphi,k})\le C\min(1,kp^{-a})$, and these primes contribute $\sum_p\log p\min(1,kp^{-a})=O(k^\beta)$. $\square$

**Corollary 4.** At $a>1$: if all drifts are $\ge0$, then $-\log\mathbb E K_{\varphi,k}^{-a}$ is between orders $k^\beta/\log k$ and $k^\beta$. If one is negative, then $\rho_A(a)<B_A(a)$ and $-k^{-1}\log\mathbb E K_{\varphi,k}^{-a}\to\log\big(B_A(a)/\rho_A(a)\big)>0$.

*Proof.* T09a; and §4 with $\mathcal G_{\varphi,k}=B_A^ka_\varphi^{-a}\mathbb E K_{\varphi,k}^{-a}$, noting that a negative drift at $p$ makes $\Phi_A(a,\theta e_p)<B_A(a)$ for small $\theta$. $\square$

No extension with a drift exactly zero at $\sigma_A$ is known; T09a covers the case if it occurs, and it also applies at any other $a$ where a drift vanishes.

## 7. The extension $2/\sqrt3$ (computed)
Here $\sigma_A=2.100608$ and the drift at $3$ is negative. Floating-point evaluation, no interval arithmetic.

- *Lower side.* By convexity, for any $\theta^0$, $\min_{[0,1]}\Phi_M\ge\Phi_M(\theta^0)+\sum_q\min\big(-g_q\theta^0_q,\;g_q(1-\theta^0_q)\big)$, $g=\nabla\Phi_M(\theta^0)$. Since $\min\Phi_M\le\rho_A$, a value $\ge1$ at $a$ gives $\sigma^\ast\ge a$.
- *Upper side.* If all $\theta_q\le t<1$, the nesting term of $N$ is at most $N^{-a(1-2t)}$, so $\Phi_A(a,\theta)\le\Phi_M(a,\theta)+M^{1-c}/(c-1)$ with $c=a(1-2t)>1$. A value $<1$ gives $\sigma^\ast<a$.

With $M=2\cdot10^5$ for the lower side and $10^6$ for the upper side,
$$2.06055\le\sigma^\ast\le2.06072.$$
The computed values are $2.0605567\ldots$ and $2.0607189\ldots$, rounded outward. (A certified evaluation is in ANS-II-ND v001.)
The minimising weight is not concentrated on the prime $3$: after weighting $3$ alone, other primes ($53,107,269,431,\dots$) have negative drift under the weighted law. So the single-prime bound of v001 §7 is not sharp.
