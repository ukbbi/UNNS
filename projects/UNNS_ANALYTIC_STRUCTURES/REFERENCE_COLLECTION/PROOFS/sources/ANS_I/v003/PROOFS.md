# ANS-I v003 — Critical regularity and prime-coordinate suppression: proofs

Research notes. Uses ANS-I v001 and v002.

## Notation
As in v002. $a>1$, $\beta=1/a$; letters independent with law $\nu_a(N)=r_N^{-a}/B(a)$; $K_k$ the least source of the first $k$ letters; $S_p(j)=\sum_{i\le j}\big(2v_p(N_i+1)-v_p(N_i)\big)$. At the critical point $a=\sigma=\sigma_c$ and $\beta=\beta_c=1/\sigma_c\approx0.6467$.

## 1. Source valuations (used for T23a and T24a)
**Lemma 1.** $v_p(K_k)=\max_{0\le j\le k}\big(-S_p(j)\big)$.

*Proof.* $v_p(K_k)$ is the least $v\ge0$ with $v+S_p(i-1)\ge v_p(N_i)$ for all $i\le k$, that is $\max\{0,\max_i(v_p(N_i)-S_p(i-1))\}$. If $p\mid N_i$ then $p\nmid N_i+1$, so $v_p(N_i)-S_p(i-1)=-S_p(i)$; and a positive maximum of $-S_p$ is first attained at such a step. $\square$

By v002 Lemma B, whose proof applies equally to the full alphabet, there is $\eta=\eta(a)>0$ with $\mathbb E e^{-\eta X_p}\le1$ for every prime $p$. Ville's inequality and Lemma 1 give
$$\Pr(v_p(K_k)\ge r)\le e^{-\eta r}\qquad(r\ge1),\qquad(1)$$
uniformly in $p$ and $k$; the same holds for letters restricted to $N\le M$ and $p\le M$.

## 2. T23a — critical depth bounds
**Theorem.** For $a>1$, $b>0$ and large $k$,
$$\frac{c\,k^{\beta}}{\log k}\le-\log\mathbb E K_k^{-b}\le C\,k^{\beta}.$$
In particular $e^{-Ck^{\beta_c}}\le G_k(\sigma_c)\le e^{-ck^{\beta_c}/\log k}$.

*Proof.* The left inequality is v002 §4. By Jensen, $-\log\mathbb EK_k^{-b}\le b\,\mathbb E\log K_k$. Let $\tau$ be the first step with $p\mid N_\tau$. Before $\tau$, $S_p\ge0$, so on $\{\tau\le k\}$ one has $v_p(K_k)\le v_p(N_\tau)+\sup_{m\ge0}\big(S_p(\tau)-S_p(\tau+m)\big)$, and $v_p(K_k)=0$ otherwise. The supremum is independent of the past at $\tau$ with bounded mean by (1), and $\mathbb E[v_p(N)\mid p\mid N]$ is bounded uniformly in $p$ because $\Pr(p^j\mid N)\le C p^{-aj}$ and $\Pr(p\mid N)\ge cp^{-a}$. Hence $\mathbb E v_p(K_k)\le C\Pr(\tau\le k)\le C'\min(1,kp^{-a})$, and
$$\mathbb E\log K_k\le C'\sum_p\log p\,\min(1,kp^{-a})\le C'\Big(\sum_{p\le k^{\beta}}\log p+k\sum_{p>k^{\beta}}\frac{\log p}{p^{a}}\Big)=O(k^{\beta}).\qquad\square$$

This is the review note's argument, applied on the full alphabet; neither a truncation nor the term $D_p=\lfloor\log M/\log p\rfloor$ is needed.

## 3. T24a — growth suppression without logarithms in the lower estimate
**Lemma 2 (economical preparation).** Let $T=\prod_{p\le M}p^{t_p}$. There is a word $w_T$, admissible from $1$, with $T\mid Q(w_T)$ and $\log Q(w_T)\le2\log T+2\theta(M)$, where $\theta(M)=\sum_{p\le M}\log p$.

*Proof.* Start with demands $d_p=t_p$. Treat the primes $q\le M$ in decreasing order: reserve $n_q=\lceil d_q/2\rceil$ copies of the letter $q-1$, and add $n_qv_r(q-1)$ to $d_r$ for each prime $r<q$. Execute the blocks in increasing order of $q$ (for $q=2$ the letter is $1$). Each copy of $q-1$ consumes $q-1$, which the earlier blocks have supplied in excess of what remains reserved, and contributes $q^2$; so the word is admissible and finally $v_q\ge2n_q-(d_q-t_q)\ge t_q$. For the size let $\Phi=\sum_{q\text{ untreated}}d_q\log q$, initially $\log T$. Treating $q$ changes $\Phi$ by $-d_q\log q+n_q\log(q-1)\le-(d_q-n_q)\log q$, and $\Phi$ ends at $0$. Hence $\sum_q(d_q-n_q)\log q\le\log T$, and since $d_q-n_q\ge(d_q-1)/2$, $\sum d_q\log q\le2\log T+\theta(M)$. Finally $\log Q(w_T)=\sum n_q\log\frac{q^2}{q-1}\le\sum 2n_q\log q\le\sum(d_q+1)\log q\le2\log T+2\theta(M)$. $\square$

**Theorem.** With $\sigma=\sigma_c$, $\beta=\beta_c$, any fixed source $x$ and $Z(X)$ any of $N_x(X)$, $A(X)$, $C(X)$:
$$\frac{c(\log X)^{\beta}}{\log\log X}\le-\log\frac{Z(X)}{X^{\sigma}}\le C(\log X)^{\beta}.$$

*Proof.* The left inequality is v002 §6. For the right one it suffices to treat $N_1$. Let $M=\lceil(\log X)^{\beta}\rceil$ and use letters $N\le M$ with law $\nu_M$. Only primes $p\le M$ divide $K_k$, so by (1) $\mathbb E_M\log K_k\le C_1\theta(M)\le C_2M$ for every $k$. Hence $\Pr(\log K_k\le4C_2M)\ge3/4$. Put $Y=\log X-C_3M$ with $C_3$ large (fixed below), let $\mu_M$ be the mean of $\log r_N$, and choose $k=\lfloor(Y-h\sqrt Y)/\mu_M\rfloor$ with $h$ as in v002 §6, so that $Y-2h\sqrt Y-\mu_M\le\log Q(v)\le Y$ with probability at least $3/4$. Both events hold with probability at least $1/2$. There are at most $e^{4C_2M}$ integers $K\le e^{4C_2M}$, so **one value** $K_0$ satisfies
$$\Pr\big(K_k=K_0,\ \log Q(v)\in[Y-2h\sqrt Y-\mu_M,\,Y]\big)\ge\tfrac12e^{-4C_2M}.$$
Apply Lemma 2 to $T=K_0$: $\log Q(w_{K_0})\le8C_2M+2\theta(M)\le C_3M$, which fixes $C_3$ independently of $K_0$. Each such $v$ is admissible from every multiple of $K_0$, so $w_{K_0}v$ is admissible from $1$ and $\log Q(w_{K_0}v)\le C_3M+Y=\log X$. Each $v$ has probability $Q(v)^{-\sigma}/B_M(\sigma)^k$, so
$$N_1(X)\ge\tfrac12e^{-4C_2M}\,e^{\sigma(Y-2h\sqrt Y-\mu_M)}\,B_M(\sigma)^k .$$
The right side is $X^{\sigma}\exp\big(-O(M+\sqrt{\log X}+kM^{1-\sigma})\big)=X^\sigma e^{-O((\log X)^{\beta})}$. $\square$

## 4. T27 — growth of the derivatives
Let $D_j=(-1)^j\mathcal G^{(j)}(\sigma,1)=\sum_w(\log E(w))^jE(w)^{-\sigma}$.

**Theorem.** There are $c,C>0$ with $c^j j^{\sigma j}\le D_j\le(Cj\log j)^{\sigma j}$ for large $j$. Hence $\log D_j=\sigma j\log j+O(j\log\log j)$, $D_j=(j!)^{\sigma+o(1)}$, the Taylor series of $\mathcal G(\cdot,1)$ at $\sigma$ has radius $0$, and $\sigma_c$ is the exact infimal Gevrey order of $\mathcal G(\cdot,1)$ on $\operatorname{Re}s\ge\sigma$ (since $|\mathcal G^{(j)}(s,1)|\le D_j$ there).

*Proof.* Lower bound: $D_j\ge(\tfrac12\log X)^jX^{-\sigma}\big(A(X)-A(\sqrt X)\big)$. Here $A(\sqrt X)=O(X^{\sigma/2})$ and $A(X)\ge X^\sigma e^{-C(\log X)^{\beta}}$ (§3). Take $\log X=j^{\sigma}$.

Upper bound: with $f(L)=A(e^L)e^{-\sigma L}$, partial summation gives $D_j=\int_0^\infty f(L)(\sigma L^j-jL^{j-1})\,dL\le\sigma\int_0^\infty f(L)L^j\,dL$ for $j\ge1$. Here $f$ is bounded, and $f(L)\le C_0e^{-c_0L^{\beta}/\log L}$ for $L\ge L_0$. The range $L\le L_0$ contributes $e^{O(j)}$. Beyond it, bound $L^je^{-c_0L^\beta/\log L}$ by $\sup_L\big[L^je^{-(c_0/2)L^\beta/\log L}\big]\cdot e^{-(c_0/2)L^{\beta}/\log L}$. The bracket is decreasing for $L\ge L_*=(Hj\log j)^{\sigma}$ when $H$ is large, so the supremum is at most $L_*^j$, and the remaining factor is integrable. $\square$

The review note's argument gives the limit $\log D_j/(j\log j)\to\sigma_c$; the bounds above add the error terms.

## 5. T28a — the first-introduction event has exact order $k^{\beta}/\log k$
A prime *occurs* in $N$ if it divides $N(N+1)$. Let $S_i$ be the set of primes not occurring in $N_1,\dots,N_{i-1}$, and let $\mathcal I_k$ be the event that no $N_i$ ($i\le k$) is divisible by a prime of $S_i$: every prime met in the first $k$ letters is introduced through $N+1$ only.

**Theorem.** For $a>1$,
$$e^{-Ck^{\beta}/\log k}\le\Pr(\mathcal I_k)\le e^{-ck^{\beta}/\log k}.$$

*Proof.* Upper bound: this is v002 §4 with a success counted as fatal. In its notation $\mathbf 1_{Z_k=0}(1-c_0)^{-F_k}$ is a supermartingale, so $\Pr(Z_k=0)\le\Pr(F_k<J)+(1-c_0)^J$ with $J=\lceil m/20\rceil$.

Lower bound: let $\mathsf A_i=\{N:\text{no }p\in S_i\text{ divides }N\}$ and let $\mathsf Q$ be the law in which $N_i$ is drawn from $\nu_a$ conditioned on $\mathsf A_i$. Then $\Pr(\mathcal I_k)=\mathbb E_{\mathsf Q}\prod_{i\le k}\nu_a(\mathsf A_i)$. Always $1\in\mathsf A_i$, so $\nu_a(\mathsf A_i)\ge\rho=\nu_a(1)$ and $\log\nu_a(\mathsf A_i)\ge-\nu_a(\mathsf A_i^c)/\rho$. Jensen's inequality and $\nu_a(\{N:q\mid N\})\le Cq^{-a}$ give
$$-\log\Pr(\mathcal I_k)\le\rho^{-1}\,\mathbb E_{\mathsf Q}\sum_{i\le k}\nu_a(\mathsf A_i^c)\le C'\sum_qq^{-a}\,\mathbb E_{\mathsf Q}\min(k,T_q),\qquad(2)$$
where $T_q$ is the first step whose letter involves $q$.

**Claim:** $\mathbb E_{\mathsf Q}T_q\le Aq^{a}$ for all primes $q$. For $q=2$ the letter $1$ has conditional probability at least $\rho$. For $q\ge3$, once every prime $r\mid q-1$ has occurred, the letter $q-1$ belongs to $\mathsf A_i$, involves $q$, and has conditional probability at least $\nu_a(q-1)\ge c_1q^{-a}$. Hence $\mathbb E_{\mathsf Q}T_q\le\sum_{r\mid q-1}\mathbb E_{\mathsf Q}T_r+q^a/c_1$. Moreover $\sum_{r\mid q-1}r\le5q/7$ (sum over distinct primes): it is $2$ if $q-1$ is a power of $2$, and otherwise $q\ge7$, the odd primes sum to at most their product $\le(q-1)/2$, and $2+(q-1)/2\le5q/7$. Therefore $\sum_rr^a\le q^a\sum_rr/q\le\frac57q^a$, and induction gives the claim with $A\ge\max\{7/(2c_1),\,1/(2^a\rho)\}$. $\square$

By the claim the right side of (2) is at most $C''\sum_q\min(1,kq^{-a})\le C''\big(\pi(k^{\beta})+k\sum_{q>k^{\beta}}q^{-a}\big)=O(k^{\beta}/\log k)$. $\square$

**Consequence.** Counting first introductions, the mechanism of the upper bound in T23a, cannot give more than $k^\beta/\log k$: the event that every introduction is harmless really is that likely. $\mathcal I_k$ does not imply $K_k=1$, because a prime already introduced can later be demanded beyond its stock.

## 6. T28 — exact order (open)
**Conjecture.** $-\log\mathbb E K_k^{-b}\asymp k^{\beta}/\log k$.

Proved: it lies between $ck^{\beta}/\log k$ and $Ck^{\beta}$. What is missing is control of repeated demands: under a law that keeps $K_k$ small, one needs the exponent of each small prime in the state to stay supplied. Under $\mathsf Q$ the introductions are handled by §5, but the drift of the individual prime coordinates under $\mathsf Q$ is not controlled.
