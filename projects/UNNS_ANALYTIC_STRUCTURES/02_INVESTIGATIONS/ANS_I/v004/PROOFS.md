# ANS-I v004 — First-passage proof of the counting estimate

Research notes. Notation of ANS-I v001–v003: nesting letters with law $\nu_\sigma$, $\sigma=\sigma_c$, $\beta=1/\sigma$. This is the argument of ANS-II v001 §5 with no adjoined multipliers.

**Statement** (right inequality of ANS-T24a). For any fixed source $x$ and $Z(X)$ any of $N_x(X)$, $A(X)$, $C(X)$: $-\log\big(Z(X)/X^\sigma\big)\le C(\log X)^\beta$.

*Proof.* A word admissible from $1$ is admissible from $n$ with endpoint multiplied by $n$, so $N_n(X)\ge N_1(X/n)$; also $N_1\le A\le C$. Treat $N_1$. Let $M=\lceil(\log X)^\beta\rceil$ and draw letters from $\nu_\sigma$ restricted to $N\le M$; let $B_M<1$ be the restricted value of $B(\sigma)$. Only primes at most $M$ divide $K$, so by the tail bound (1) of v003 and monotone convergence $\mathbb E\log K_\infty\le C_1M$, and $\Pr(\log K_\infty\le4C_1M)\ge3/4$.

Let $L_k=\log Q_k$, $Y=\log X-C_2M$ with $C_2$ large, and let $\tau$ be the first $k$ with $L_k>Y-H$. The increments $\xi=\log r_N$ are at least $\log4$ and have tails bounded uniformly in $M$ by an integrable function. A unit interval contains at most $1+1/\log4$ of the $L_k$, so
$$\Pr(L_\tau>Y)\le\Big(1+\frac1{\log4}\Big)\sum_{h\ge0}\Pr(\xi>H+h)\le\frac14$$
for a constant $H$. With probability at least $1/2$ both events hold, and $\tau\le\bar k=Y/\log4+1$. First-passage words $v$ form a prefix-free set with $\Pr(v)=Q(v)^{-\sigma}B_M^{-|v|}$. There are at most $e^{4C_1M}$ possible values of $K(v)$, so some value $K^\ast$ satisfies $\Pr(K(v)=K^\ast,\ L_\tau\le Y)\ge\tfrac12e^{-4C_1M}$, and the number of such words is at least $\tfrac12e^{-4C_1M}e^{\sigma(Y-H)}B_M^{\bar k}$. Prefix each by the preparation word $w^\ast$ of v003 Lemma 2 for $T=K^\ast$, with $\log Q(w^\ast)\le2\log K^\ast+2\theta(M)$. Then $w^\ast v$ is admissible from $1$, and its endpoint is at most $X$ once $C_2M\ge8C_1M+2\theta(M)$. Finally $-\log B_M=O(M^{1-\sigma})$ and $\bar kM^{1-\sigma}=O((\log X)^\beta)$. $\square$

**What changes.** The proof in v003 §3 fixes the word length and uses a central-limit window of width $\sqrt{\log X}$, which is of smaller order than $(\log X)^\beta$ because $\sigma<2$. The first-passage stopping time needs no variance or window and no condition $\sigma<2$.

**What does not change.** The estimate is the same. The gap between $(\log X)^\beta/\log\log X$ and $(\log X)^\beta$, and the exact depth order (ANS-T28), are untouched.
