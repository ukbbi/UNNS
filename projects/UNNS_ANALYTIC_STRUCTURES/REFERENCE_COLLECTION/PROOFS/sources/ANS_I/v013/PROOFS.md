---
title: "ANS-I v013 --- Boundary letters, link roles and depth four"
author: "UNNS Research Collective"
date: "27 November 2026"
---

Research notes. They continue ANS-I v012; notation is as there. All results concern the nesting grammar. New proofs are pending review; no claim of priority is made, and no comprehensive literature review has been done. Throughout, $\sigma=\operatorname{Re}s$ and $z=p^{-s}$.

# 0. Review of v012 and summary

The owner's review found T46g, T46h, T46h-i, T46i, T46j, T46e, T46k and T46l valid, and T46b established for $k=3$. It made the following points, all adopted here. The v012 files are not altered.

1. *Lemma of §4.6:* $I$ must be an **interval** in $(N,2N]$ (part (a) uses an interval estimate). All uses in §§4.7--4.8 are intervals.
2. *T46j:* the bounds (H) are to be required **uniformly in $\operatorname{Im}s$**. Constants growing with $\operatorname{Im}s$ prime by prime need not give polynomial growth of the products. The weights $q_1,r_2$ satisfy the uniform form, since $|z|$ depends only on $\sigma$.
3. *T46h-i:* normal convergence of the binomial tail. For $\sigma>-\frac1{10}$ the prime-power formula gives $|\Phi(M;s)|\ll M^{1/5+\varepsilon}$ on compact sets. So for $n\ge3$ the sum over $M\ge2$ of the $n$-th term is $O(2^{-n})$, while $|\binom{-2s}n|$ grows polynomially in $n$. The finitely many other terms are continued as in v012.
4. *A simplification:* $1+z^3-z^4-z^5=(1-z^2)(1+z^2+z^3)$, hence $D(s,s)=\zeta(4s)\prod_p(1+p^{-2s}+p^{-3s})$.

The review also proposed the margin $\delta=1/700$. It is correct; §1 records a somewhat larger one.

New here: an exact decomposition of $G_k$ at **every** depth by its two end letters (§2); the classification of simultaneously active links (§3); a model in which the maximal link pattern provably gives a pole of order $rt$ at $1/3$, in particular $4$ at depth four (§4); and a precise form of what is still missing for $G_4$ (§5). **No result on the singularity of $G_4$ at $1/3$ is claimed.**

# 1. A larger continuation margin (ANS-T46k-i)

**Proposition.** T46j, and therefore T46k and T46l, hold with $\delta_0=1/200$. So $G_3$ is meromorphic on $\sigma>\frac13-\frac1{200}$.

*Proof.* Keep the argument of v012 §4 and change four parameters:
$$\mathcal S:\max(m,n)\le(ab)^{\mathsf K},\quad\mathsf K=\tfrac74;\qquad\text{H\"older exponents }h=\tfrac65,\ h'=6;\qquad\tau=\tfrac1{14};$$
and $\theta=\frac2{25}$ in place of $\theta=\frac12$ (the first row keeps $\theta=\frac34$). The sets $\mathcal A,\mathcal B$ are defined with $(ab)^{\mathsf K}$. The following are all the places where the parameters enter.

- *Moments.* In (F2) use $\sum F^{h}$ and $\sum G^{h'}$. Needed: $(-2\sigma_0+\tau)k<0$ for $k=h,h'$; for $F$ at $p^2$, $2\big((\sigma_0+\tau)h-1\big)<-1$; for $G$ at $p^2$, $2\tau h'-2<-1$; for $p^j$, $j\ge3$, $(2-j)\sigma_0h'+j\tau h'-j<-1$.
- *Set $\mathcal S$.* Now $M_0\le(ab)^{2\mathsf K+1}$, so the dyadic bound is $Y^{1-3\sigma-\tau/(2\mathsf K+1)+\varepsilon}$; here $\tau/(2\mathsf K+1)=\frac1{63}>\frac3{200}$. The second part needs $2\sigma-6\mathsf K\delta_0>\frac12$.
- *Counting lemma.* Unchanged. Its hypothesis $N\ge\sqrt u/2$ still holds because $\mathsf K\ge1$.
- *Sets $\mathcal A,\mathcal B$.* The exponents of $(a,b,m)$ become $\big(\frac12-3\sigma-\mathsf K\sigma(1-\theta),\,-2\sigma-\mathsf K\sigma(1-\theta),\,\frac12-4\sigma-\sigma\theta\big)$ in the first row and $\big(-2\sigma-\mathsf K\sigma(1-\theta),\,-\mathsf K\sigma(1-\theta),\,-3\sigma-\sigma\theta\big)$ in the second. In the second shift term they are $\big(-\mathsf K\sigma(1-\theta),\,-2\sigma-1-\mathsf K\sigma(1-\theta),\,-3\sigma-1-\sigma\theta\big)$.
- *Principal parts.* The bound is $a^{-1+3\mathsf K\delta_0}b^{-2\sigma+3\mathsf K\delta_0}m^{-\sigma-1+3\delta_0}$.

All required inequalities were verified in exact fractions at $\sigma=\frac13,\frac13\pm\delta_0$ (`margins`); each is linear in $\sigma$. The other ingredients allow this range: $P(z)\ne0$ uniformly for $\sigma>\frac3{10}$, and $R$ continues to $\sigma>\frac27$. $\square$

The value $1/200$ is not optimised either.

# 2. The decomposition by end letters (ANS-T46m)

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

*Proof.* By (1), $E^{-s}=(a(P+1))^{-2s}E(\mu)^{-s}g^sh^s$. As in v011, $\sum_{a\ge1}a^{-2s}\gcd(N,a^2)^s=\zeta(2s)\Phi(N)$. The letter $a-1$ requires $a\ge2$, so we subtract the term $a=1$, where $h=1$; what is subtracted is $\sum(P+1)^{-2s}E(\mu)^{-s}g^s=\sum E(\mu P)^{-s}=G_{k-1}(s)$. Therefore
$$G_k=\zeta(2s)\sum_{|\mu|=k-2}E(\mu)^{-s}\sum_{P\ge1}(P+1)^{-2s}f_\mu(P)\;-\;G_{k-1}.$$
Writing $f_\mu(P)=\sum_{q\mid P}\Lambda_\mu(q)$,
$$\sum_{P\ge1}(P+1)^{-2s}f_\mu(P)=\zeta(2s)\sum_q\frac{\Lambda_\mu(q)}{q^{2s}}+\sum_q\frac{\Lambda_\mu(q)\,\Delta(s,q)}{q^{2s}}.$$
Now $f_\mu(P)=\prod_pf_p(v_pP)$ with $f_p(j)=p^{s\min(j,v)}\Phi\big(p^{u+j-\min(j,v)}\big)$, $u=v_pK(\mu)$, $v=v_pE(\mu)$. So $\sum_q\Lambda_\mu(q)q^{-2s}=\prod_p\sum_j\big(f_p(j)-f_p(j-1)\big)z^{2j}$ with $f_p(-1)=0$. The terms $1\le j\le v$ give $(1-z)\Phi(p^u)\sum_{j=1}^vz^j=(z-z^{v+1})\Phi(p^u)$, and the terms $j=v+i$ give $z^vc_u$. With $j=0$ the factor is $L(u,v)$. Since $\prod_pL_0=\zeta(3s)H(s)$, the product is $\zeta(3s)H(s)\,\Omega(K(\mu),E(\mu))$.

*Convergence.* $K(\mu)\le\prod x\le E(\mu)$, because each letter multiplies the endpoint by at least $(x+1)^2/x>x+1$. Next $|\Lambda_\mu(q)|\ll(qK)^\varepsilon\gcd(q,E)^\sigma$, and $\sum_q\gcd(q,E)^\sigma q^{-2\sigma+\varepsilon}\ll E^{\varepsilon'}$ for $\sigma>\frac12$. Also $\Delta$ is bounded and $\Omega\ll E^\varepsilon$. So all sums are dominated by $G_{k-2}(\sigma-\varepsilon'')$, which converges (T12). $\square$

**Cases.** $k=2$: $M_2=1$, giving T45. $k=3$: $\mu=M$, $K=M$, $E=(M+1)^2$ and $\Omega=w_1(M)\,w_2(M+1)$, giving T46d.

**What the theorem says.** The two end letters can be summed out at any depth. The link between them is the Euler product $\zeta(3s)H(s)$ of depth two. Everything else is a sum over middle words, and in both $M_k$ and $R_k$ a middle word enters only through the pair $(K,E)$ of its source and endpoint. With $\Omega=1$, $M_k$ would be $G_{k-2}$. At a prime with $(v_pK,v_pE)=(1,0)$ or $(0,2)$ the factor of $\Omega$ is $(1+z+z^2)/(1+z^2+z^3)=1+z+O(z^3)$.

The theorem is not a closed recursion in $G_k$: the weight depends on the middle word.

# 3. Links and roles (ANS-T46n)

Write a word as $x_1\cdots x_k$ and $a_i=x_i+1$. A prime $p$ activates the link $(i,j)$, $i<j$, when $p\mid a_i$ and $p\mid x_j$. Since $\gcd(x_i,a_i)=1$, at one prime a letter can supply ($p\mid a_i$, role S) or receive ($p\mid x_i$, role R), not both. So the sets of links active at one prime are contained in the sets $\{(i,j):i\in S,\ j\in R,\ i<j\}$ for assignments of roles.

**Proposition.** The largest such set has $\lfloor k^2/4\rfloor$ links. It requires all S letters to precede all R letters, with $\lfloor k/2\rfloor$ or $\lceil k/2\rceil$ letters of role S: one assignment for even $k$, two for odd $k\ge3$ (the first letter taken as S and the last as R).

*Proof.* With $r$ letters of role S there are at most $r(k-r)$ pairs, with equality exactly when every S precedes every R. $\square$

| depth four: roles of letters 1--4 | links | number |
|--|--|--|
| S S R R | 13, 14, 23, 24 | 4 |
| S S S R | 14, 24, 34 | 3 |
| S R R R | 12, 13, 14 | 3 |
| S R S R | 12, 14, 34 | 3 |

**Where the six links sit in T46m** (middle word $x\,y$, $a_2=x+1$, $a_3=y+1$):

| link | place in the decomposition |
|--|--|
| 14 | the separate factor $\zeta(3s)H(s)$ |
| 23 | the gcd in $E(xy)^{-s}=(a_2a_3)^{-2s}\gcd(y,a_2^2)^s$ |
| 12, 13 | $\Omega$, through the primes of $K(xy)=xy/\gcd(y,a_2^2)$ |
| 24, 34 | $\Omega$, through the primes of $E(xy)$ |

This classifies which links can act together **at one prime**. At different primes a letter may play both roles, and the proposition says nothing about which analytic factors are independent.

At depth three the two maximal assignments are SSR and SRR. The residue in v012 is likewise a sum of two terms; this is an agreement of number, not a derivation.

# 4. A model with the maximal pattern (ANS-T46o)

Keep only the links from $r$ supplying letters to $t$ later receiving letters:
$$F_{r,t}(s)=\sum_{a\in\mathbb N^r}\ \sum_{x\in\mathbb N^t}\ \prod_ia_i^{-2s}\prod_j(x_j+1)^{-2s}\,\gcd\Big(\prod_jx_j,\;\big(\prod_ia_i\big)^2\Big)^s.$$

**Theorem.** For $\sigma>\frac12$,
$$F_{r,t}(s)=\sum_{i=0}^t\zeta(2s)^{r+t-i}\,\zeta(3s)^{r(t-i)}\,Q_i(s),$$
with every $Q_i$ holomorphic on $\sigma>\frac14$. Hence $F_{r,t}$ is meromorphic there, with poles only at $\frac12$, of order exactly $r+t$, and at $\frac13$, of order **exactly $rt$**. Moreover $Q_0(\frac13)>0$, and $\lim_{s\to1/3}(s-\frac13)^{rt}F_{r,t}=\zeta(\frac23)^{r+t}\,Q_0(\frac13)\,3^{-rt}$.

*Proof.* Since $\gcd(X,n^2)^s=\sum_{d\mid X,\ \rho(d)\mid n}J_s(d)$, we have $F_{r,t}=\sum_dJ_s(d)\,A(d)\,B(d)$, where $A(d)=\sum_{\rho(d)\mid n}\tau_r(n)n^{-2s}$ and $B(d)=\sum_{d\mid\prod x_j}\prod(x_j+1)^{-2s}$; for $\sigma>\frac12$ the terms are $O(d^{-2\sigma+\varepsilon})$. The rearrangements below are absolute there, because $\gcd(d,\prod y_l)\le\prod\gcd(d,y_l)$ and $\sum_yy^{-2\sigma-1}\gcd(d,y)^{2\sigma}\ll d^\varepsilon$. Here $A(d)=\rho(d)^{-2s}\zeta(2s)^r\,g_r(\rho(d))$, with $g_r$ multiplicative and
$$g_r(p^e)=(1-z^2)^r\sum_{j\ge0}\binom{e+j+r-1}{r-1}z^{2j},\qquad g_r(p)=r+O(z^2).$$
In $B$ write $(x+1)^{-2s}=x^{-2s}+\delta(x)$, $\delta(x)=O_s(x^{-2\sigma-1})$, and expand. If $i$ factors are $\delta(y_l)$, put $Y=\prod y_l$ and $h=t-i$. For $h\ge1$ the remaining sum is $\zeta(2s)^hq^{-2s}g_h(q)$ with $q=d/\gcd(d,Y)$; for $h=0$ it is $[\,d\mid Y\,]$. Thus
$$F_{r,t}=\sum_{i=0}^t\binom ti\zeta(2s)^{r+t-i}\sum_{y\in\mathbb N^i}\Big(\prod\delta(y_l)\Big)D_{t-i}(Y),$$
where $D_0(Y)=\sum_{d\mid Y}J_s(d)\rho(d)^{-2s}g_r(\rho(d))$ and, for $h\ge1$,
$$D_h(Y)=\sum_dJ_s(d)\,\rho(d)^{-2s}g_r(\rho(d))\,q^{-2s}g_h(q),\qquad q=\frac d{\gcd(d,Y)}.$$

For $h\ge1$, $D_h(Y)=\prod_pE_p(v_pY)$ with
$$E_p(\ell)=\sum_{v\ge0}J_s(p^v)\,z^{2\lceil v/2\rceil}g_r(p^{\lceil v/2\rceil})\,z^{2\max(v-\ell,0)}g_h(p^{\max(v-\ell,0)}),$$
and $J_s(p^v)=z^{-v}(1-z)$ for $v\ge1$. On compact subsets of $\sigma>\frac14$: first, $E_p(0)=1+\sum_{v\ge1}(1-z)z^{2\lceil v/2\rceil+v}g_rg_h=1+rhz^3+O(z^4)$; second, $|E_p(\ell)|\le C(\ell+1)^C$, since the terms $v\le\ell$ are polynomially bounded and the others carry $|z|^{2(v-\ell)}$. Hence
$$D_h(Y)=\zeta(3s)^{rh}\prod_p(1-z^3)^{rh}E_p(v_pY),$$
where the product converges to a holomorphic function of size $O(Y^\varepsilon)$: its factors are $1+O(z^4)$ for $p\nmid Y$. Also $D_0(Y)=O(Y^\varepsilon)$, as $|J_s(d)\rho(d)^{-2s}|\le C^{\omega(d)}$. Therefore the sums over $y$ converge normally, which gives the formula with holomorphic $Q_i$.

At real $s$ every term of $E_p(0)$ is positive, so $Q_0(\frac13)>0$ and $Q_0(\frac12)>0$. The terms $i\ge1$ have lower orders at both points, and $\zeta(\frac23)\ne0$. $\square$

**Depth four.** $F_{2,2}$ carries exactly the links 13, 14, 23, 24 of the maximal assignment, and has a pole of order **four** at $\frac13$, with leading coefficient $\approx0.0068448$.

**Limits.** $F_{r,t}$ is a model. The letters are given fixed roles, so the links inside the two groups, and letters acting in both roles at different primes, are absent. It is not a part of a decomposition of $G_{r+t}$ with the remaining terms controlled. It shows that the maximal link pattern really produces order $rt$ when nothing interferes; it proves nothing about $G_k$ itself. (For $r=t=1$, $F_{1,1}=G_2+\zeta(2s)-1$.)

# 5. What depth four still needs

**Proposition (ANS-T46p, proved implication).** Let $k\ge3$. Suppose $M_k$ and $R_k$ continue meromorphically to a neighbourhood of $\frac13$, that $M_k$ has there a pole of order exactly $\lfloor k^2/4\rfloor-1$, and that the pole order of $R_k$ is less than $\lfloor k^2/4\rfloor$. Suppose also that $G_{k-1}$ continues there with pole order less than $\lfloor k^2/4\rfloor$. Then $G_k$ has a pole of order exactly $\lfloor k^2/4\rfloor$ at $\frac13$.

*Proof.* In T46m, $\zeta(2s)^2H(s)$ is holomorphic and non-zero at $\frac13$ and $\zeta(3s)$ has a simple pole. $\square$

**Conjecture (ANS-T46q).** $M_k$ has a pole of order exactly $\lfloor k^2/4\rfloor-1$ at $\frac13$.

Since $\lfloor k^2/4\rfloor-1=\lfloor(k-2)^2/4\rfloor+(k-2)$, this says that the weight $\Omega$ raises the order of $G_{k-2}$ by one for each middle letter. It holds for $k=2$ ($M_2=1$) and $k=3$ (v012). This is the form in which depth four can now be tested, and it is a candidate for an induction on depth; no induction step is proved.

For $k=4$,
$$M_4(s)=\sum_{x,y\ge1}\big((x+1)(y+1)\big)^{-2s}\gcd\big(y,(x+1)^2\big)^s\,\Omega(K,E),$$
and the conjectured order is $3$. Neither the continuation of $M_4$ past $\frac13$ nor its order is proved. v012 treated one pair of adjacent integers; here there are two pairs, coupled by $\gcd(y,(x+1)^2)$ and by primes common to both, and estimates uniform in the coupling modulus would be needed. The continuation of $R_4$ is open as well. $G_4$ itself is known to continue to $\sigma>\frac13$ (T34), not beyond.

# 6. Computations

Finite and floating-point checks only. Parameters and outputs are in `results/`.

- Formula (1) and $K(\mu)$: exact integers; all words of length $3,4,5$ with letters up to $30,14,7$, and $20\,000$ random words at each length $4,5,6,8,12$. No failure.
- $\Phi$ and $L(u,v)$ against truncated series ($u,v\le8$; $v\le10$ for $\Phi$): error below $10^{-14}$. $L(u,0)$ and $L(0,2\beta)$ reproduce the weights of v011.
- Last-letter identity at $s=1.5$ for eight middle words: differences below $2.2\cdot10^{-9}$ (truncation).
- First-letter identity for $G_4$ at $s=2$, both sides truncated at letters $\le20,40,80$: differences $-1.8\cdot10^{-7}$, $-2.8\cdot10^{-8}$, $-3.6\cdot10^{-9}$.
- Role assignments enumerated for $k\le16$.
- $F_{r,t}$ at $s=1.5$ for $(1,1),(1,2),(2,2)$: formula against direct sums at three cut-offs; the differences decrease steadily, to $9\cdot10^{-7}$, $6\cdot10^{-6}$ and $2.3\cdot10^{-4}$. Local factors $1+rtz^3+O(z^4)$ for four pairs.
- Margins of §1 in exact fractions.

None of these tests a continuation.

# 7. Open

- ANS-T46q and the continuation of $M_4$, $R_4$ past $\frac13$; hence T46b for $k=4$.
- A general principle for the order of the weighted sums $M_k$.
- ANS-T33 (unrestricted depth). Not addressed in this release.
- The largest half-plane for $G_3$; sharp counting terms; zeros; ANS-T38 for the complete functions; ANS-T39.
