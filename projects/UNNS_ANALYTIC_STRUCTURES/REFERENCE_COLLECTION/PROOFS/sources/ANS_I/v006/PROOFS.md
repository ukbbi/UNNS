---
title: "ANS-I v006 --- Character decomposition and local coupling"
author: "UNNS Research Collective"
date: "27 November 2026"
---

Research notes. They continue ANS-I v005; notation is as there. All results concern the nesting grammar. New proofs are pending review; no claim of priority is made, and no literature review has been done.

# 0. Review of v005

The owner's review found T31 and T32 valid and ANS-C1 settled, with one correction: in the last step of the proof of T32, $\mathbb E[\mathbf 1_U\sqrt{G^\flat}]$ need not be monotone in $(P,\Lambda)$ jointly, because increasing $P$ adds conditions to $U$. The correct argument is dominated convergence, and it has been placed in the v005 proofs. The review also recommends citing Matveev's quantitative theorem (Izv. Math. 64, 2000) beside Baker's for the large-height part of T31.

# 1. Local coupling asymptotic (ANS-T32a)

**Theorem.** For every fixed $k\ge1$, as $p\to\infty$,
$$c_p(k)=1+\binom k2p^{-3/2}+\binom k3p^{-2}+O_k(p^{-5/2}).$$

The first term and the method are those of the review note; the $p^{-2}$ term is added here.

*Proof.* For one word put $a_i=v_p(N_i+1)$, $d_i=v_p(N_i)$, $A=\sum a_i$, $D=\sum d_i$ and $C=\sum_i\min(e_{i-1},d_i)$, so that $c_p(k)-1=\mathbb E(p^{C/2}-1)$. The recurrence is $e_i=2a_i+e_{i-1}-\min(e_{i-1},d_i)$. Since $e_k\ge0$ we have $C\le2A$, and clearly $C\le D$. Hence $C\le\min(2A,D)\le\frac23L$ with $L=A+D$. For each letter at most one of $a_i,d_i$ is non-zero, and each value $m\ge1$ of either has Haar probability $p^{-m}(1-p^{-1})$. So $\Pr(L=\ell)\le C_k(\ell+1)^{k-1}p^{-\ell}$. A non-zero $C$ needs $A\ge1$ and $D\ge1$.

$L=2$. Then $A=D=1$ at two different positions, and $C=1$ exactly when the numerator position comes first. Each of the $\binom k2$ ordered patterns has probability $p^{-2}(1-p^{-1})^2(1-2p^{-1})^{k-2}$. The contribution is $\binom k2(p^{-3/2}-p^{-2})+O_k(p^{-5/2})$.

$L=3$. If $(A,D)=(2,1)$ then $C\le1$ and the contribution is $O_k(p^{-5/2})$. If $(A,D)=(1,2)$ then $C\le2$, and only $C=2$ matters at order $p^{-2}$. It occurs in two ways: one later letter with $d=2$ ($\binom k2$ patterns), or two later letters with $d=1$ ($\binom k3$ patterns). Each pattern has probability $p^{-3}(1+O_k(p^{-1}))$ and excess weight $p-1$. The contribution is $\big(\binom k2+\binom k3\big)p^{-2}+O_k(p^{-5/2})$.

$L\ge4$. For $\ell=4$ the integer $C$ is at most $2$, so the contribution is $O_k(p^{-3})$. For $\ell\ge5$ we have $\mathbb E[p^{C/2};L=\ell]\le C_k(\ell+1)^{k-1}p^{-2\ell/3}$, with total $O_k(p^{-10/3})$. Adding the three cases proves the formula. $\square$

**Corollary.** $\displaystyle\log\kappa_k=\sum_{p\le P}\log c_p(k)+\binom k2\sum_{p>P}p^{-3/2}+\binom k3\sum_{p>P}p^{-2}+O_k(P^{-3/2}).$

The constant in the error term is not made explicit, so numerical values of $\kappa_k$ remain uncertified.

# 2. Characters of the multiplier

A *unitary character* is a homomorphism $\chi:\mathbb Q_{>0}\to S^1$; it is determined by arbitrary values on the primes. Put
$$G_{\chi,k}(s)=\sum_{|w|=k}\frac{\chi(Q(w))}{E(w)^s},\qquad\mathcal G_\chi(s,t)=\sum_kt^kG_{\chi,k}(s).$$

**Lemma 1 (separation).** Suppose $\chi(r_N)=z$ for $N=1,2,3$ and for every prime label $N=p$. Then $z=1$ and $\chi$ is trivial.

*Proof.* From $r_1=4$, $r_2=9/2$, $r_3=16/3$: $\chi(2)^2=z$, $\chi(3)^2=z\,\chi(2)$ and $\chi(2)^4=z\,\chi(3)$. The first and third give $\chi(3)=\chi(2)^2$. The second then gives $\chi(2)^3=z=\chi(2)^2$, so $\chi(2)=1$, $z=1$, $\chi(3)=1$. For $p\ge5$, $\chi(p)=\chi(p+1)^2\overline{\chi(r_p)}=\chi(p+1)^2$, and the primes dividing $p+1$ are smaller than $p$. Induction gives $\chi(p)=1$. $\square$

## 2.1 Twisted continuation (ANS-T35)

**Theorem.** Let $\chi$ be a unitary character and $\tau\in\mathbb R$. If $\chi$ is not the character $q\mapsto q^{i\tau}$, then $\mathcal G_\chi(s,t)$ continues holomorphically to a neighbourhood of $(\sigma_c+i\tau,t_0)$ for every $|t_0|=1$.

*Proof.* The character $\psi(q)=\chi(q)q^{-i\tau}$ is non-trivial. By Lemma 1 there is a finite set $R$, consisting of $1,2,3$ and at most one prime label, on which $\psi(r_N)$ is not constant. Repeat v005 §1 with this $R$ and $s_0=\sigma_c+i\tau$. Let $P_R$ be the finite set of primes dividing some $N(N+1)$, $N\in R$, and for $p\in P_R$ let $m_p=\min_RX_p$, $\delta_p=\max_Rd_p$.

1. With letters of law $\nu_\sigma$, $\sigma=\operatorname{Re}s$,
$$G_{\chi,k}(s)=B(\sigma)^k\,\mathbb E\big[K_k^{-s}\,\chi(Q_k)\,Q_k^{-i\operatorname{Im}s}\big].$$
2. Mark late letters of $R$ with probability $\eta$. For $p\notin P_R$ the source valuation never depends on the marked values, and for $p\in P_R$ it does not on the good event, by formula (0) of v005.
3. Every drift $\mathbb EX_p$ is positive, and $P_R$ is finite. So $\eta,\theta$ can be chosen with $\Pr(\mathsf A^c)\le Cf^{k/2}$, $f<1$.
4. The marked letters contribute independent factors with mean
$$c_\chi(s)=\frac{\sum_{N\in R}\chi(r_N)\,r_N^{-s}}{\sum_{N\in R}r_N^{-\sigma}} .$$
At $s_0$ the phases are $\psi(r_N)$, which are not all equal, so $|c_\chi(s_0)|<1$, and by continuity $|c_\chi(s)|\le q<1$ near $s_0$.

Hence $|G_{\chi,k}(s)|\le B(\sigma)^k\big((1-\lambda(1-q))^{k/2}+C'f^{k/2}\big)$, with $\lambda=\eta\,\nu_\sigma(R)$, and $|t|^k$ times this is summable uniformly near $(s_0,t_0)$. Each $G_{\chi,k}$ is holomorphic for $\operatorname{Re}s>1/2$ because $|\chi|=1$ (ANS-T12), and for $\operatorname{Re}s>\sigma_c$ the sum is the absolutely convergent series. $\square$

**Consequences.**

- $\chi=1$ gives T31 (every $\tau\ne0$), by the same mechanism.
- If $\chi$ is non-trivial of finite order, it is never $q^{i\tau}$. So $\mathcal G_\chi(s,1)$ is **regular at every point of the critical line, including $\sigma_c$**.
- The same holds for every unitary character not of the form $q^{i\tau}$.
- The exceptional case is $\chi(q)=q^{i\tau_0}$. Then the theorem applies at all $\tau\ne\tau_0$. At $\tau=\tau_0\ne0$ it says nothing: there $\mathcal G_\chi(\sigma+i\tau_0,1)=\sum_wQ^{-\sigma}K^{-\sigma-i\tau_0}$, a function with a complex source weight (ANS-T39, open).

## 2.2 A uniform region for finite order

**Theorem.** For $\chi$ non-trivial of finite order $m$ there are $a,A,C>0$ such that $\mathcal G_\chi(s,1)$ is holomorphic on $\{\sigma>\sigma_c-a(1+|\tau|)^{-A}\}$ and bounded there, near the line, by $C(1+|\tau|)^A$.

*Proof.* Take one set $R=\{1,2,3\}$ plus, if needed, a prime label on which $\chi(r_N)$ differs from $\chi(r_1)$. For $\tau=0$ the phases $\chi(r_N)r_N^{-i\tau}$ are not all equal by the choice of $R$ and Lemma 1. For $\tau\ne0$, alignment on $\{1,2,3\}$ raised to the power $m$ would give $m\tau\log(9/8),m\tau\log(4/3)\in2\pi\mathbb Z$, impossible by v005 §1.5. So $|c_\chi(\sigma+i\tau)|<1$ for all $\tau$. For large $|\tau|$, $\|m x\|\le m\|x\|$ shows that the distance from alignment is at least $1/m$ times the quantity bounded in v005 (4), with $m\tau$ in place of $\tau$. Hence $1-|c_\chi|\ge b\,(1+|\tau|)^{-A}$ everywhere on $I$. Continue as in v005 §1.6. $\square$

# 3. Finite quotients

Let $\varphi:\mathbb Q_{>0}\to\Gamma$ be a surjective homomorphism onto a finite abelian group, and $\mathcal G^{[\gamma]}(s)=\sum_{\varphi(Q(w))=\gamma}E(w)^{-s}$.

## 3.1 Sector decomposition (ANS-T36)

**Theorem.** $\mathcal G^{[\gamma]}(s)=|\Gamma|^{-1}\,\mathcal G(s,1)+R_\gamma(s)$, where $R_\gamma$ is holomorphic on a region $\{\sigma>\sigma_c-a(1+|\tau|)^{-A}\}$. Consequently each $\mathcal G^{[\gamma]}$ is singular at $\sigma_c$ and regular at every other point of the critical line.

*Proof.* By orthogonality, $\mathcal G^{[\gamma]}=|\Gamma|^{-1}\sum_{\chi\in\hat\Gamma}\overline{\chi(\gamma)}\,\mathcal G_{\chi\circ\varphi}$. Apply §2.2 to the non-trivial characters. The singularity statements follow from those for $\mathcal G$ (T20, T31). $\square$

**The index-seven quotient.** The Algebraic and Topological Extensions (v1.1, Proposition "index") show that $H=\langle r_p:p\text{ prime}\rangle$ has index $7$, through $\varphi(2)=2$, $\varphi(3)=1$, $\varphi(p)=2\varphi(p+1)$ in $\mathbb Z/7$. Directly: every prime label has class $0$ by construction, as do $r_2$ and $r_3$ ($7\equiv0$), while $\varphi(r_1)=4$; modulo $H$ every prime is a power of $3$ and $3^7\in H$. So T36 gives seven sector functions with the same singular part $\mathcal G/7$. This does not rest on the number seven: the same holds for every finite quotient. What is particular to this quotient is that its characters are trivial on all prime labels, so that the cancellation must come from nonprime labels such as $1$.

## 3.2 Equidistribution of what is proved to be singular (ANS-T37a)

Let $D_j=\sum_w(\log E)^jE^{-\sigma_c}$ and let $D_j^\gamma$ be the part with $\varphi(Q(w))=\gamma$.

**Theorem.** (1) $D_j^\gamma/D_j\to1/|\Gamma|$; the error is at most $C^j j!/D_j$. (2) With $A_\gamma(X)=\#\{w:E(w)\le X,\ \varphi(Q(w))=\gamma\}$ and $A=\sum_\gamma A_\gamma$,
$$\liminf_{X\to\infty}\frac{A_\gamma(X)}{A(X)}\le\frac1{|\Gamma|}\le\limsup_{X\to\infty}\frac{A_\gamma(X)}{A(X)} .$$

In particular, if a sector proportion has a limit, the limit is $1/|\Gamma|$.

*Proof.* (1) All derivatives of $\mathcal G$ and $\mathcal G^{[\gamma]}$ converge uniformly on $\operatorname{Re}s\ge\sigma_c$ (v002), so $D_j^\gamma-D_j/|\Gamma|=(-1)^jR_\gamma^{(j)}(\sigma_c)$, which is at most $C^{j+1}j!$ because $R_\gamma$ is holomorphic near $\sigma_c$. By T27 (v003), $D_j\ge c^jj^{\sigma_cj}$ with $\sigma_c>1$.

(2) Write $\sigma=\sigma_c$, $w_j(X)=X^{-\sigma-1}(\log X)^{j-1}(\sigma\log X-j)$, which is $-\frac d{dX}\big[(\log X)^jX^{-\sigma}\big]$. For $j\ge1$, $(\log E)^jE^{-\sigma}=\int_E^\infty w_j$, and the integrals of $|w_j|$ are summable over words because all $D_i$ are finite. So $D_j^\gamma=\int_1^\infty A_\gamma w_j$, and $D_j=\int_1^\infty Aw_j$. Suppose $A_\gamma\ge(|\Gamma|^{-1}+\varepsilon)A$ for $X\ge X_0$ and set $\Delta=A_\gamma-(|\Gamma|^{-1}+\varepsilon)A$. By (1), $\int\Delta w_j=-\varepsilon D_j+O(C^jj!)$. Take $j$ so large that $e^{j/\sigma}>X_0$. Beyond $e^{j/\sigma}$ the integrand $\Delta w_j$ is non-negative. Below it, $|\Delta|\le CA(e^{j/\sigma})\le C'e^{j}$ and $\int_1^{e^{j/\sigma}}|w_j|=(j/(\sigma e))^j$. Hence $\int\Delta w_j\ge-C''(j/\sigma)^j$. Then $\varepsilon D_j=O(C^jj^j)$, contradicting $D_j\ge c^jj^{\sigma j}$. The lower limit is treated in the same way. $\square$

The statement $A_\gamma(X)\sim A(X)/|\Gamma|$ is **not** proved (ANS-T37, conjecture). The sums $D_j$ at the finite point $\sigma_c$ concentrate on ever larger endpoints, but they do not control every $X$.

# 4. Computations

Finite checks only; parameters and outputs are in `results/`.

- Classes: all $78\,498$ prime labels up to $10^6$ have class $0$; $r_1,r_2,r_3$ have classes $4,0,0$.
- The bound $C\le\min(2A,D)\le\frac23L$ held on $200\,000$ random valuation sequences.
- The remainder in T32a, multiplied by $p^{5/2}$, stays bounded up to $p=100\,003$ for $k\le6$.
- Euler products with the two tail terms of the corollary ($P=200\,000$; uncertified):

| $k$ | 2 | 3 | 4 | 5 | 6 |
|--|--:|--:|--:|--:|--:|
| $\kappa_k$ | 1.853646 | 5.105352 | 19.11923 | 92.6368 | 560.98 |

- $|c_\chi(\sigma_c+i\tau)|<1$ on a grid of $\tau\in[0,500]$ for the six characters of order seven.
- With the exchange set $\{1,2,3,5\}$ no exchange on the good event changed the source.
- Exact sector counts (checked against direct enumeration for $X\le10^5$): the proportions of the seven classes lie between $0.035$ and $0.210$ at $X=10^3$, between $0.136$ and $0.151$ at $10^6$, and between $0.1416$ and $0.1439$ at $10^8$ ($3.8\times10^8$ words). This is consistent with the conjecture and does not prove it.

# 5. Open

- ANS-T33: the singularity at $\sigma_c$.
- ANS-T34: continuation of $G_k$, $k\ge3$.
- ANS-T37: pointwise distribution over sectors, with a rate.
- ANS-T38: complex zeros of $\mathcal G$ and $\mathcal G_\chi$. Nothing is established here beyond the trivial zero-free half-plane where the series is close to $1$.
- ANS-T39: the twists $\chi(q)=q^{i\tau_0}$ at $\tau=\tau_0\ne0$.
