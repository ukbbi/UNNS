# Open problems and conjectures

Recorded for preservation. Sequential ANS-I development is paused at v015.

## Conjectures

### ANS-T28: Exact order of the critical decay

**Status:** CONJECTURE. Source: ANS-I v003.

**Conjecture.** $-\log\mathbb E K_k^{-b}\asymp k^{\beta}/\log k$.

Proved: it lies between $ck^{\beta}/\log k$ and $Ck^{\beta}$. What is missing is control of repeated demands: under a law that keeps $K_k$ small, one needs the exponent of each small prime in the state to stay supplied. Under $\mathsf Q$ the introductions are handled by §5, but the drift of the individual prime coordinates under $\mathsf Q$ is not controlled.

### ANS-T46b: Pole of order floor(k^2/4) at 1/3

**Status:** PROVED for k <= 3; CONJECTURE for k >= 4. Source: ANS-I v009.

**Conjecture (ANS-T46b).** For $k\ge2$, $G_k$ has a pole at $s=1/3$ of order $\lfloor k^2/4\rfloor$.

This gives order $1$ at $k=2$ (proved, T45), order $2$ at $k=3$ and order $4$ at $k=4$. A proof needs (i) continuation past $1/3$, (ii) equidistribution, with a power saving, of the least elements above, which involves inverses modulo $P_{\rm out}$ and so estimates of Kloosterman type, and (iii) a non-vanishing check on the leading coefficient. The depth-three counts of v008 are compatible with order $2$ but do not test it.

### ANS-T46q: Weighted middle-word sum: pole order floor(k^2/4)-1

**Status:** CONJECTURE (k = 2, 3 proved). Source: ANS-I v013.

**Conjecture (ANS-T46q).** $M_k$ has a pole of order exactly $\lfloor k^2/4\rfloor-1$ at $\frac13$.

Since $\lfloor k^2/4\rfloor-1=\lfloor(k-2)^2/4\rfloor+(k-2)$, this says that the weight $\Omega$ raises the order of $G_{k-2}$ by one for each middle letter. It holds for $k=2$ ($M_2=1$) and $k=3$ (v012). This is the form in which depth four can now be tested, and it is a candidate for an induction on depth; no induction step is proved.

### ANS-T46t: General continuation, pole order floor(k^2/4) and leading coefficient at 1/3

**Status:** CONJECTURE (k = 2, 3 proved). Source: ANS-I v015.

Following the review: **for every $k\ge2$, $G_k$ continues meromorphically to a neighbourhood of $\frac13$, has there a pole of order exactly $\ell_k=\lfloor k^2/4\rfloor$, and its leading Laurent coefficient is**
$$\zeta(\tfrac23)^k\,3^{-\ell_k}\sum_{L(R)=\ell_k}C_R .$$
Status: CONJECTURE for $k\ge4$; proved for $k=2,3$ (T45, T46k, T46s-ii).

## Open questions

### A. Generation: recurrences, composition and factorization

| ID | Question |
|----------|----------------------------------------|
| ANS-C2 | Conjecture (v001): H(mn) > H(m)H(n) for coprime non-squarefree m, n. Finite evidence only. |

### B. Convergence and growth in depth

| ID | Question |
|----------|----------------------------------------|
| ANS-T11 | Analytic classification across grammars (a saturation criterion is proved). |

### C. The critical exponent

| ID | Question |
|----------|----------------------------------------|
| ANS-T25 | Higher-degree and other nesting grammars. |
| ANS-T30 | Quantitative finite-to-infinite alphabet transition. |
| ANS-T33 | Nature of the singularity at sigma_c; whether the continuations above and below agree to its left. |
| ANS-T39 | Twists q^(i tau0) at tau = tau0 != 0. |

### E. Fixed depth: continuation and counting

| ID | Question |
|----------|----------------------------------------|
| ANS-T38 | Complex zeros (and poles) of the complete functions G, G_chi. |

### F. Depth two

| ID | Question |
|----------|----------------------------------------|
| ANS-G2Z | Classification of the zeros of G_2 (the maximal meromorphic domain and the pole divisor are established). ID is a label of this collection. |
| ANS-A2S | Rigorous sharp, unsmoothed secondary counting term of order X^(1/3) in A_2(X) (recorded as not proved in ANS-I v008; a smoothed form holds). ID is a label of this collection. |

### H. Arbitrary depth at one third

| ID | Question |
|----------|----------------------------------------|
| ANS-T46 | Depth k >= 4 at and beyond Re s = 1/3; depth three further to the left. |
| ANS-T46a | Singularities and natural boundaries at higher depth. |

### I. Collective growth at and below s = 1

| ID | Question |
|----------|----------------------------------------|
| ANS-LIM | Existence and value of lim G_k(1)^(1/k)/log k. A heuristic (v015, unproved) suggests a value below e^gamma. No separate ID in the releases; ANS-LIM is a label of this collection. |

### J. Extended generation: torsion multipliers

| ID | Question |
|----------|----------------------------------------|
| ANS2-O3 | Exact suppression order in the extensions. |
| ANS2-O5 | Behaviour at the abscissa under negative drift (carried on as ANS2N-O2). |
| ANS2-O6 | Spectrum and continuation of the transfer operators. |
| ANS2-O7 | Does any extension have a drift exactly zero at sigma_A? |

### K. Negative drift: entropy and attainment

| ID | Question |
|----------|----------------------------------------|
| ANS2N-O1 | Is the entropy supremum always attained? |
| ANS2N-O2 | Convergence of G at the abscissa, and suppression there. |
| ANS2N-O3 | Lower-order factors of the counting functions. |
| ANS2N-O4 | Decay of the optimal weights (remaining case: maximum exactly 1/2). |
| ANS2N-O5 | Can an optimal weight reach or exceed 1/2? |
| ANS2N-O6 | Is the logarithmic average of the optimal weights zero? |

## Where attempts stopped (recorded in the releases)

- Depth four: no viable analytical route was found (ANS-I v014, section 4).
- Growth at s = 1: a necessary condition, and an unproved heuristic against the upper constant e^gamma (ANS-I v015, section 5).
- Attainment: reduced to weights at least 1/2 at depleting primes (ANS-II-ND v002 and v003).

The earlier list `01_THEORY/OPEN.md` is the historical record; parts of it are superseded.
