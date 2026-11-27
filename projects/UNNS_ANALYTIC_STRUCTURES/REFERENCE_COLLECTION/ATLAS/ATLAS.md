---
title: "The Analytic Atlas of the UNNS Substrate"
author: "UNNS Research Collective"
date: "27 November 2026"
---

# How to read the Atlas

The Atlas organizes the results of Analytic Structures of the UNNS Substrate by mathematical phenomenon. It covers ANS-I through v015, ANS-II through v002 and ANS-II-ND through v003. It states nothing new: each mathematical claim is a short account of catalogued results, named by identifier. The exact statements, with all hypotheses, are in the Theorem Compendium, and they govern wherever a summary here is shorter.

Each entry gives the mathematical object, the established structure, what that structure says about generation, further structure and the open boundary. The sections headed **Reading across** are interpretation: they point to parallels and are not theorems. The tables, the connections between entries, the review boundary and the proof sources at the end of each entry are generated from the catalogue.

Status words: *proved* means a written argument exists; review codes say who has checked it (V UNNS Research Collective review, VQ UNNS Research Collective review with a qualification, A proposal checked internally, P no review verdict, B baseline note, N not a proved result). No literature novelty review has been completed.

**Notation.** A letter $N\ge1$ multiplies by $r_N=(N+1)^2/N$ and is admissible at $x$ when $N\mid x$. For a word $w$: multiplier $Q(w)$, minimal source $K(w)$, least endpoint $E(w)=K(w)Q(w)$. Further, $G_k(s)=\sum_{|w|=k}E(w)^{-s}$, $\mathcal G(s,t)=\sum_kt^kG_k(s)$, $B(\sigma)=\sum_Nr_N^{-\sigma}$, and $\sigma_c=1.5463810\ldots$ solves $B(\sigma_c)=1$.

# Four governing mechanisms

The foundational audit of 27 November 2026 singled out four results on which much of the theory turns.

| Mechanism | Result | What it does | Entry |
|---------------------|------------|-------------------------------------|----------|
| Exact admissible composition | ANS-T03 | Turns histories into arithmetic: every word has an exact set of sources and endpoints | ATL-01 |
| Finite-resource saturation | ANS-T15 | Each finite truncation $1\le N\le M$ can be prepared so that random generation continues for ever with positive probability | ATL-02 |
| Unbounded-resource obstruction | ANS-T17 | With all letters available, a random infinite word is almost surely inadmissible from any integer | ATL-02 |
| Quantitative collective suppression | ANS-T23a | Measures the cost of that obstruction at depth $k$ | ATL-04 |

# The shape of the territory

- **Composition** (ATL-01) supplies the arithmetic object.
- The contrast between **finite and infinite alphabets** (ATL-02) fixes the **characteristic exponent** (ATL-03) and the **suppression** below it (ATL-04), which govern the **generated populations** (ATL-05).
- At **fixed depth** the singularities sit at smaller abscissae (ATL-06): **depth two** is understood to its natural boundary (ATL-07), and the singularity at one third has a **local mechanism** whose general form is open (ATL-08).
- **Collective growth** at and below $s=1$ (ATL-09) concerns the passage to large depth where the sum over letters diverges.
- **Extended generation** (ATL-10) adds multipliers that can deplete primes, and **entropy and admissibility** (ATL-11) describes the resulting exponent.

This list is a guide. The cited logical connections are given entry by entry.

# ATL-01: Exact admissible composition

## Mathematical object

A word of letters acting on integers, subject to integrality. The data of a word are its minimal source $K(w)$ and least endpoint $E(w)$.

## Established structure

- **Sources and endpoints are exact progressions.** A word is admissible precisely from the multiples of $K(w)$, with endpoints the multiples of $E(w)$, and both obey a one-letter gcd recurrence (T03). This holds for every integral-image grammar under the stated hypotheses.
- **Prime coordinates.** Each letter shifts the exponent of $p$ by $2v_p(N+1)-v_p(N)$, and the minimal endpoint exponent is a maximum over suffixes (T04).
- **Composition.** With $d=\gcd(E(u),K(v))$ one has $K(uv)=K(u)K(v)/d$ and $E(uv)=E(u)E(v)/d$. Prime by prime this is multiplication in a bicyclic monoid, a classical object. It gives a block factorization of $G_{m+n}$ and the supermultiplicativity $G_{m+n}\ge G_mG_n$ (T47).
- **History series.** Counting histories by endpoint factorizes as $\mathcal Z_H(s,t)=\zeta(s)\,\mathcal G(s,t)$, with Möbius inversion depth by depth (T01, T02). A source weight gives a three-variable series with a closed form on its anti-diagonal (T14).
- **No ordinary Euler product** exists for the nesting grammar at $t=1$ (T06). Grammars with unit denominators, by contrast, have a closed rational form (T08).
- At one step, the in-degree and the root series reduce to classical Dirichlet series (AS-001, AS-002).

## What it reveals

Generation can be studied through two integers per word. The zeta factor records only the free choice of source; the structure specific to the grammar lies in $\mathcal G$. Although the evolution of a prescribed word separates into prime coordinates, the history population does not possess an ordinary Euler product. The ordered letter structure couples the arithmetic contributions when histories are counted.

## Further structure

The recurrence of T03 drives the fixed-depth convergence region (ATL-06) and the decompositions at one third (ATL-08).

## Open boundary

The supermultiplicativity conjecture ANS-C2 for the history counts has finite evidence only.

## Reading across (interpretation)

The prime-by-prime bicyclic structure is a point of contact with algebraic investigations of the Substrate. It is examined in the Cross-Structural Research Map (`CROSS_STRUCTURES/`), whose derived statements are unreviewed and are not part of this Atlas or the catalogue.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS-T03 | Source and endpoint recurrences | PROVED | V |
| ANS-T04 | Prime-coordinate evolution | PROVED | V |
| ANS-T47 | Composition of words, block factorization, supermultiplicativity | PROVED | V |
| ANS-T01 | History Dirichlet factorization | PROVED | V |
| ANS-T06 | No ordinary Euler product | PROVED | V |

## Recorded open questions

- **ANS-C2:** Conjecture (v001): H(mn) > H(m)H(n) for coprime non-squarefree m, n. Finite evidence only.

## Connected entries (cited dependencies)

- **Uses ATL-03** (The characteristic exponent and its singular point): ANS-T07, ANS-T09.
- **Uses ATL-06** (Fixed-depth singularity architecture): ANS-T12.
- **Used by ATL-02** (Finite saturation and unbounded obstruction): ANS-T11.
- **Used by ATL-06** (Fixed-depth singularity architecture): ANS-T12.
- **Used by ATL-07** (Depth two: an arithmetic singularity hierarchy): ANS-T05, ANS-T13.
- **Used by ATL-08** (The mechanism at one third): ANS-T46m, ANS-T46r, ANS-T46s.

## Review boundary

Without a review verdict: AS-001 (B), AS-002 (B).

Qualified verdicts:

- ANS-T14: The stated convergence regions; not a complete classification for negative source weights.

## All results and proof sources

- **Initial analytic baseline:** AS-001, AS-002.
- **ANS-I v001:** ANS-T03, ANS-T04, ANS-T01, ANS-T02, ANS-T14, ANS-T06, ANS-T08.
- **ANS-I v014:** ANS-T47.

# ATL-02: Finite saturation and unbounded obstruction

## Mathematical object

Random words with independent letters of law proportional to $r_N^{-a}$, with the alphabet either truncated at $N\le M$ or unrestricted, and the question whether an infinite word is admissible from a finite integer.

## Established structure

- **Every prime can be supplied from source 1**, and for every finite truncation $1\le N\le M$ there is a finite preparation word after which the whole infinite random continuation is admissible with probability at least one half (T15).
- **Criterion for other grammars.** Positive weighted drift at every consuming prime of a finite label set gives the corresponding lower growth bound (T11).
- **At the finite critical exponent** $\sigma_M$ the minimal source stabilizes almost surely, $G_k^{(M)}(\sigma_M)$ decreases to a positive constant $c_M$, and $c_M\to0$ as $M\to\infty$ (T26).
- **With the full alphabet** and $a>1$, a random infinite word is almost surely not admissible from any given integer (T17); hence $K_k\to\infty$ almost surely (T18).

## What it reveals

Every finite truncation can sustain indefinite random generation, while unrestricted generation almost surely meets a demand it cannot supply. The positive constants $c_M$ vanishing in the limit measure how the first regime passes into the second. The suppression theory of ATL-04 grows from this difference.

## Further structure

The mechanisms differ. Saturation uses a positive drift in each of finitely many prime coordinates. The obstruction uses fresh primes: a prime not yet present is first met through a consuming letter with probability bounded below, and this needs no independence between prime coordinates.

## Open boundary

A quantitative description of the transition from finite to infinite alphabets (ANS-T30), and an analytic classification of grammars beyond the saturation criterion (ANS-T11).

## Reading across (interpretation)

The pair suggests a test to apply to any alternative history grammar: does positive drift in finitely many coordinates coexist with an obstruction from unboundedly many?

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS-T15 | Source-one generation: every prime reached; saturation | PROVED | V |
| ANS-T17 | Infinite-alphabet admissibility obstruction | PROVED | V |
| ANS-T18 | Divergence of minimal sources | PROVED | V |
| ANS-T26 | Finite-alphabet contrast | PROVED | V |
| ANS-T11 | Saturation criterion for general grammars (classification open) | PROVED | VQ |

## Recorded open questions

- **ANS-T30:** Quantitative finite-to-infinite alphabet transition.
- **ANS-T11:** Analytic classification across grammars (a saturation criterion is proved).

## Connected entries (cited dependencies)

- **Uses ATL-01** (Exact admissible composition): ANS-T03.
- **Uses ATL-03** (The characteristic exponent and its singular point): ANS-T09.
- **Uses ATL-04** (Collective critical suppression): ANS-T23.
- **Used by ATL-03** (The characteristic exponent and its singular point): ANS-T09, ANS-T10, ANS-T19, ANS-T21, ANS-T31.
- **Used by ATL-04** (Collective critical suppression): ANS-T23.

## Review boundary

Every result in this entry has a review verdict.

Qualified verdicts:

- ANS-T11: The saturation criterion only; the general classification remains open.

## All results and proof sources

- **ANS-I v001:** ANS-T15, ANS-T11.
- **ANS-I v002:** ANS-T26, ANS-T17, ANS-T18.

# ATL-03: The characteristic exponent and its singular point

## Mathematical object

The full history series $\mathcal G(s,1)=\sum_kG_k(s)$ and the counting functions $N_x(X)$, $A(X)$, $C(X)$.

## Established structure

- **Growth in depth** is $G_k(\sigma)^{1/k}\to B(\sigma)$ for $\sigma>1$ and infinite for $0\le\sigma\le1$, so the abscissa is $\sigma_c$ (T09; a sufficient criterion is T07).
- **Counting.** For every fixed source, and for the other two counts, $\log Z(X)/\log X\to\sigma_c$ (T10).
- **Probability form.** $G_k(a)/B(a)^k=\mathbb E\,K_k^{-a}$ (T16). At $\sigma_c$ the depth terms tend to zero although their $k$-th roots tend to one (T19).
- **Below a pure power.** $Z(X)=o(X^{\sigma_c})$ (T21).
- **The singular point.** $\mathcal G(s,1)$ has no meromorphic continuation through $\sigma_c$ (T20), yet converges on the whole critical surface under the stated condition and is infinitely differentiable up to the line $\operatorname{Re}s=\sigma_c$ (T22).
- **The rest of the line is regular.** The function continues holomorphically across every point $\sigma_c+i\tau$ with $\tau\ne0$; the line is not a natural boundary (T31).

## What it reveals

The exponent is the one that independent letters would give, $B(\sigma_c)=1$: admissibility does not move it. Admissibility changes the nature of the singularity and pushes the counts below the pure power. The singularity is smooth from the right and still not meromorphic.

## Further structure

The continuation of T31 comes from cancellation inside each $G_k$; the word series itself does not converge absolutely to the left of the line.

## Open boundary

The nature of the singularity at $\sigma_c$, including whether continuations above and below it agree to its left (ANS-T33), and the analogous theory for higher-degree and other nesting grammars (ANS-T25).

## Reading across (interpretation)

A smooth non-meromorphic singularity is a second kind of obstruction, different in nature from the natural boundary of ATL-07.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS-T09 | Growth in depth and the sharp boundary sigma_c | PROVED | V |
| ANS-T10 | Growth exponent of every counting function | PROVED | V |
| ANS-T20 | No meromorphic continuation through sigma_c | PROVED | V |
| ANS-T22 | Convergence on the critical surface; smooth singularity | PROVED | V |
| ANS-T31 | Holomorphic continuation across the critical line away from sigma_c | PROVED | V |
| ANS-T21 | Strict growth suppression | PROVED | V |

## Recorded open questions

- **ANS-T33:** Nature of the singularity at sigma_c; whether the continuations above and below agree to its left.
- **ANS-T25:** Higher-degree and other nesting grammars.

## Connected entries (cited dependencies)

- **Uses ATL-02** (Finite saturation and unbounded obstruction): ANS-T15, ANS-T18.
- **Uses ATL-04** (Collective critical suppression): ANS-T23.
- **Used by ATL-01** (Exact admissible composition): ANS-T14.
- **Used by ATL-02** (Finite saturation and unbounded obstruction): ANS-T11.
- **Used by ATL-04** (Collective critical suppression): ANS-T24.
- **Used by ATL-05** (Generated populations and typical histories): ANS-T35, ANS-T36, ANS-T37, ANS-T37a, ANS-T40.

## Review boundary

Every result in this entry has a review verdict.

## All results and proof sources

- **ANS-I v001:** ANS-T07, ANS-T09, ANS-T10.
- **ANS-I v002:** ANS-T16, ANS-T19, ANS-T20, ANS-T21, ANS-T22.
- **ANS-I v005:** ANS-T31.

# ATL-04: Collective critical suppression

## Mathematical object

The negative moments $\mathbb E\,K_k^{-b}$ of the minimal source, the ratio $Z(X)/X^{\sigma_c}$ and the derivatives of $\mathcal G(s,1)$ at $\sigma_c$. Write $\beta=1/a$, and $\beta=1/\sigma_c$ at the critical exponent.

## Established structure

- **Depth.** For $a>1$ and large $k$, $ck^{\beta}/\log k\le-\log\mathbb E\,K_k^{-b}\le Ck^{\beta}$ (T23a, sharpening T23).
- **Counting.** $c(\log X)^{\beta}/\log\log X\le-\log\big(Z(X)/X^{\sigma_c}\big)\le C(\log X)^{\beta}$ (T24a, sharpening T24; second proof of one inequality in T24b).
- **Derivatives.** The $j$-th derivative magnitude $D_j$ satisfies $c^jj^{\sigma_cj}\le D_j\le(Cj\log j)^{\sigma_cj}$, so $\sigma_c$ is the infimal Gevrey order on the closed half-plane (T27).
- **First introductions.** The probability that every new prime among the first $k$ letters arrives only through $N+1$ has exact order $\exp(-\Theta(k^{\beta}/\log k))$ (T28a).

## What it reveals

The cost of admissibility at depth $k$ is stretched-exponential, with exponent fixed by the letter law. One quantity appears three times: as decay in depth, as a deficit in counting and as the growth of derivatives.

## Further structure

The two sides of the depth estimate have different sources. That the suppression is at least $ck^{\beta}/\log k$ comes from fresh primes. That it is at most $Ck^{\beta}$ comes from Jensen's inequality and a bound, for each prime, on the demand that can build up after the prime is first consumed.

## Open boundary

The exact order of the decay: the conjecture T28 states $-\log\mathbb E\,K_k^{-b}\asymp k^{\beta}/\log k$. T28a settles the first introductions only. Preventing harmful first introductions does not prevent depletion of primes met earlier, which is why T28a does not resolve T28. Membership at exactly the Gevrey order $\sigma_c$ is also open (T27).

## Reading across (interpretation)

The gap between T28a and T28 isolates repeated demands on small primes. The prime-resource questions of ATL-09 and ATL-11 have the same character in other settings.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS-T23a | Strengthened critical depth bounds | PROVED | V |
| ANS-T24a | Growth suppression without logarithms in the lower estimate | PROVED | V |
| ANS-T27 | Critical derivative growth; infimal Gevrey order sigma_c | PROVED | VQ |
| ANS-T28a | Exact order of the first-introduction event | PROVED | V |
| ANS-T28 | Exact order of the critical decay | CONJECTURE | N |

## Connected entries (cited dependencies)

- **Uses ATL-02** (Finite saturation and unbounded obstruction): ANS-T15, ANS-T17.
- **Uses ATL-03** (The characteristic exponent and its singular point): ANS-T21.
- **Used by ATL-02** (Finite saturation and unbounded obstruction): ANS-T26.
- **Used by ATL-03** (The characteristic exponent and its singular point): ANS-T22.
- **Used by ATL-05** (Generated populations and typical histories): ANS-T37a, ANS-T37b, ANS-T42a.
- **Used by ATL-09** (Collective growth at and below s = 1): ANS-T48.
- **Used by ATL-10** (Extended generation and prime-resource balance): ANS2-T02, ANS2-T03, ANS2-T04, ANS2-T07, ANS2-T09a.
- **Used by ATL-11** (Entropy and admissibility): ANS2N-T04b.

## Review boundary

Without a review verdict: ANS-T28 (N).

Qualified verdicts:

- ANS-T27: Valid for the infimal Gevrey order; membership at exactly that order is open.

## All results and proof sources

- **ANS-I v002:** ANS-T23, ANS-T24.
- **ANS-I v003:** ANS-T23a, ANS-T24a, ANS-T27, ANS-T28a, ANS-T28.
- **ANS-I v004:** ANS-T24b.

# ATL-05: Generated populations and typical histories

## Mathematical object

The histories counted up to endpoint $X$, sorted by a homomorphism of $\mathbb Q_{>0}$ onto a finite abelian group $\Gamma$ (the sector of a word is the image of $Q(w)$).

## Established structure

- **Analytic input.** Twisted series continue across the critical line except for the characters $q\mapsto q^{i\tau}$ (T35); each sector function equals $\mathcal G/|\Gamma|$ plus a function holomorphic across the line (T36).
- **Equidistribution.** Critical log-moments equidistribute (T37a); $A_\gamma(X)\sim A(X)/|\Gamma|$, and likewise from each fixed source (T37); at fixed depth the sector ratio at $\sigma_c$ converges exponentially fast (T37b).
- **Regular variation.** $A(X)=X^{\sigma_c}L(X)$ with $L$ slowly varying, and likewise for $N_x$ (T40). The bounds of T24a apply to this factor.
- **Replication.** $C(X)\sim\zeta(\sigma_c)A(X)$ (T41).
- **Typical history.** $\log Q/\log X\to1$, $\log K=o(\log X)$, depth over $\log X$ tends to $1/\lambda_c$, and block frequencies tend to the product weights $r_N^{-\sigma_c}$ (T42), with concentration bounds (T42a).
- **Limit laws.** The normalized endpoint has density $\sigma_cu^{\sigma_c-1}$ (T43), and sector, replication factor and endpoint become independent (T44).

## What it reveals

A typical generated history has the letter and block frequencies of an independent sequence, although admissibility strongly suppresses the total number of histories. The suppression acts on the size of the population; the stated frequency laws are unaffected by it. This establishes convergence of empirical block frequencies, rather than independence of letters at arbitrary prescribed positions in the conditioned history population.

## Further structure

All of this passes through the holomorphic continuation of ATL-03 and the characters of the multiplier group.

## Open boundary

An asymptotic formula for the slowly varying factor is not available. Twists $q^{i\tau_0}$ at the matching height $\tau=\tau_0\ne0$ are open (ANS-T39).

## Reading across (interpretation)

The limit weights $r_N^{-\sigma_c}$ describe a weighted history population and are a candidate point of contact with generative information geometry.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS-T37 | Counting equidistribution over finite quotients | PROVED | V |
| ANS-T40 | Regular variation with index sigma_c | PROVED | V |
| ANS-T41 | Asymptotic arithmetic replication | PROVED | V |
| ANS-T42 | Typical-history laws | PROVED | V |
| ANS-T43 | Limit law of normalized endpoints | PROVED | V |
| ANS-T44 | Joint limit law of sector, replication factor and endpoint | PROVED | V |

## Recorded open questions

- **ANS-T39:** Twists q^(i tau0) at tau = tau0 != 0.

## Connected entries (cited dependencies)

- **Uses ATL-03** (The characteristic exponent and its singular point): ANS-T10, ANS-T20, ANS-T22, ANS-T31.
- **Uses ATL-04** (Collective critical suppression): ANS-T23a, ANS-T24a, ANS-T27.
- **Uses ATL-06** (Fixed-depth singularity architecture): ANS-T12.

## Review boundary

Every result in this entry has a review verdict.

## All results and proof sources

- **ANS-I v006:** ANS-T35, ANS-T36, ANS-T37a.
- **ANS-I v007:** ANS-T37, ANS-T37b, ANS-T40, ANS-T41, ANS-T42.
- **ANS-I v008:** ANS-T42a, ANS-T43, ANS-T44.

# ATL-06: Fixed-depth singularity architecture

## Mathematical object

$G_k(s)$ for a fixed depth $k$, its restrictions to words whose source is divisible by $D$, and the counting function $A_k(X)$.

## Established structure

- **Region of convergence.** The weighted sum over words of length $k$ converges exactly in the stated region; in particular $G_k$ has abscissa $1/2$ at every depth (T12).
- **Counting.** $A_k(X)\sim\kappa_k\sqrt X(\log X)^{k-1}/(2^{k-1}(k-1)!)$, with $\kappa_k$ an Euler product (T32); as a corollary, $(2\sigma-1)^kG_k(\sigma)\to\kappa_k$ at $1/2$ (C1). The local factors have the expansion $1+\binom k2p^{-3/2}+\binom k3p^{-2}+O_k(p^{-5/2})$ (T32a).
- **Continuation.** Every $G_k$ is meromorphic on $\operatorname{Re}s>1/3$, with a single pole there, at $1/2$, of order exactly $k$ (T34), also for every source restriction (T34b).
- **Full main term.** $A_k(X)=\sqrt X\,P_{k-1}(\log X)$ with a power saving (T34a).

## What it reveals

At fixed depth $k$, the principal pole has order $k$, one order per letter position. Arithmetic coupling changes its leading coefficient and generates additional singularity structures.

## Further structure

To the left of $1/3$ the picture depends on depth: ATL-07 treats depth two and ATL-08 the singularity at one third.

## Open boundary

Zeros and poles of the complete functions (ANS-T38). Continuation of general $G_k$ to $1/3$ and beyond is part of ATL-08.

## Reading across (interpretation)

The abscissae $1/2$ at fixed depth and $\sigma_c$ for the whole series show that the infinite sum over depths creates a singularity that no single depth has.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS-T12 | Convergence region at fixed depth | PROVED | V |
| ANS-T32 | Fixed-depth counting asymptotic and the constants kappa_k | PROVED | VQ |
| ANS-T34 | Every G_k is meromorphic on Re s > 1/3 | PROVED | V |
| ANS-T34a | Full counting polynomial with power saving | PROVED | V |
| ANS-T34b | Exact pole order k at one half for every restriction | PROVED | V |

## Recorded open questions

- **ANS-T38:** Complex zeros (and poles) of the complete functions G, G_chi.

## Connected entries (cited dependencies)

- **Uses ATL-01** (Exact admissible composition): ANS-T03.
- **Used by ATL-01** (Exact admissible composition): ANS-T47.
- **Used by ATL-05** (Generated populations and typical histories): ANS-T35.
- **Used by ATL-07** (Depth two: an arithmetic singularity hierarchy): ANS-T45.
- **Used by ATL-08** (The mechanism at one third): ANS-T46k, ANS-T46m.

## Review boundary

Every result in this entry has a review verdict.

Qualified verdicts:

- ANS-T32: Valid after a correction to the limiting step, which has been applied.

## All results and proof sources

- **ANS-I v001:** ANS-T12.
- **ANS-I v005:** ANS-T32, ANS-C1.
- **ANS-I v006:** ANS-T32a.
- **ANS-I v008:** ANS-T34, ANS-T34a.
- **ANS-I v009:** ANS-T34b.

# ATL-07: Depth two: an arithmetic singularity hierarchy

## Mathematical object

$G_2(s)=\sum_{a,b\ge1}\big[\gcd((a+1)^2,b)/((a+1)^2(b+1)^2)\big]^s$ and the integer exponents $e_n$ obtained by expanding its Euler factor in powers of $p^{-s}$.

## Established structure

- **First continuation.** A Hurwitz-zeta representation gives continuation to $\operatorname{Re}s>1/3$ and the double pole at $1/2$, with $A_2(X)\sim(\kappa/2)\sqrt X\log X$ (T05, T13).
- **Factorization.** $G_2$ is meromorphic on $\operatorname{Re}s>1/5$ with a simple pole at $1/3$ (T45), and on $\operatorname{Re}s>0$, where the line $\operatorname{Re}s=0$ is a natural boundary (T45a).
- **Pole divisor.** On the positive real axis the poles are at $1/n$ with $e_n>0$, of order $e_n$ (T45d). Examples: orders $2,1,1,1$ at $1/2,1/3,1/7,1/8$ (T45b) and order two at $1/12$ (T45c).
- **Exponents.** $nc_n=-2R^n\cos n\theta+O(\tau(n)R^{n/2})$ for the stated algebraic $R>1$ and $\theta$, each sign of $e_n$ has density one half (T45e), and the normalized exponents follow an arcsine law (T45f).
- **Zeta zeros.** For $e_n<0$, all but a small set of critical-line zeros $\rho$ give poles at $\rho/n$ (T38d; cases T38a, T38b), with lower bounds (T38c) and asymptotic populations on the lines $\operatorname{Re}s=1/(2n)$ (T38e).

The description of **all** non-real poles in the second corollary of T45d assumes the Riemann hypothesis. The other statements listed here are recorded without it.

## What it reveals

A single coupling between two letters produces an unbounded hierarchy of singularities, accumulating on a natural boundary, with orders governed by one cubic polynomial.

## Further structure

The signs of the exponents decide whether a given $n$ contributes poles on the real axis or poles at rescaled zeta zeros.

## Open boundary

The maximal meromorphic domain and the pole divisor are established. Two questions about depth two remain unresolved: the classification of the zeros of $G_2$ (ANS-G2Z), and a rigorous sharp, unsmoothed secondary counting term of order $X^{1/3}$ in $A_2(X)$ (ANS-A2S). They are preserved as mathematical questions, not active investigations. The corresponding hierarchy at higher depth is also open (ATL-08).

## Reading across (interpretation)

The natural boundary is a candidate point of contact with structural obstruction theory. The poles at rescaled zeta zeros reflect zeta factors in the formula; they carry no information about where those zeros lie.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS-T45 | Depth two to Re s > 1/5 with a simple pole at 1/3 | PROVED | V |
| ANS-T45a | Depth two: meromorphic on Re s > 0 with natural boundary | PROVED | V |
| ANS-T45d | Depth two: exact pole divisor on Re s > 0 | PROVED | V |
| ANS-T45e | Depth two: asymptotics and sign densities of the Euler exponents | PROVED | V |
| ANS-T38d | Depth two: vertical pole family for every negative exponent | PROVED | V |
| ANS-T38e | Depth two: pole populations on the lines Re s = 1/(2n) | PROVED | V |

## Recorded open questions

- **ANS-G2Z:** Classification of the zeros of G_2 (the maximal meromorphic domain and the pole divisor are established). ID is a label of this collection.
- **ANS-A2S:** Rigorous sharp, unsmoothed secondary counting term of order X^(1/3) in A_2(X) (recorded as not proved in ANS-I v008; a smoothed form holds). ID is a label of this collection.

## Connected entries (cited dependencies)

- **Uses ATL-01** (Exact admissible composition): ANS-T03.
- **Uses ATL-06** (Fixed-depth singularity architecture): ANS-T34.
- **Used by ATL-08** (The mechanism at one third): ANS-T46b, ANS-T46h-i, ANS-T46k, ANS-T46s.

## Review boundary

Every result in this entry has a review verdict.

## All results and proof sources

- **ANS-I v001:** ANS-T13, ANS-T05.
- **ANS-I v008:** ANS-T45.
- **ANS-I v009:** ANS-T45a, ANS-T45b, ANS-T38a.
- **ANS-I v010:** ANS-T45d, ANS-T45c, ANS-T45e, ANS-T38d, ANS-T38b, ANS-T38c.
- **ANS-I v011:** ANS-T45f, ANS-T38e.

# ATL-08: The mechanism at one third

## Mathematical object

The singularity of $G_k$ at $s=1/3$, produced by primes shared between an earlier letter through $N+1$ and a later letter through $N$.

## Established structure: depth three

- An exact decomposition expresses $G_3$ through a shifted series $V$, a remainder $R$ and $G_2$ (T46d). Models of one linked letter have only a simple pole at $1/3$ (T46c, T46f).
- Square-divisor identities (T46g) lead to the continuation of the remainder (T46h, T46i), whose first component has a natural boundary at $\operatorname{Re}s=0$ (T46h-i). A theorem on shifted series (T46j) then gives the continuation and residue of $V$ (T46e); positivity of its constants was proved in advance (T46e-i).
- $G_3$ has a pole of order **exactly two** at $1/3$, with an explicit leading coefficient near $-0.75916$ (T46k); the continuation reaches $\operatorname{Re}s>1/3-1/200$ (T46k-i), and smoothed counts have a second term of size $X^{1/3}\log X$ (T46l).

## Established structure: arbitrary depth

- For every $k\ge2$, on $\operatorname{Re}s>1/2$, $G_k$ decomposes by its end letters into a weighted middle-word sum $M_k$, a remainder and $G_{k-1}$ (T46m). Overlaps in the weight obey an exact identity (T46r).
- At one prime at most $\lfloor k^2/4\rfloor$ links can be active (T46n). A model with $r$ supplying and $t$ receiving letters has a pole of order exactly $rt$ (T46o).
- For a role pattern $R$ the local expectation is $1+L(R)/p+O(p^{-4/3})$, where $L(R)$ counts links; the resulting formula reproduces the proved leading coefficients at $k=2,3$ and in the model (T46s).
- Stated conditions on $M_k$, the remainder and $G_{k-1}$ would imply the pole order at depth $k$ (T46p). They are not established for any $k\ge4$.

## What it reveals

Under the role-pattern measure, each eligible supplier-to-receiver link contributes to the first-order coefficient $L(R)/p$ of the local expectation. The maximal link count is attained by a balanced complete bipartite pattern, with all suppliers preceding all receivers. This mechanism reproduces the proved singularities at depths two and three and in the comparison model. Its extension to the full history series at arbitrary depth remains conjectural.

## Further structure

Three statements of different strength are kept apart:

| Identifier | Content | Proved |
|----------------|----------------------------------------------------|--------------|
| T46b | $G_k$ has a pole at $1/3$ of order $\lfloor k^2/4\rfloor$ | $k=2,3$ |
| T46q | $M_k$ has a pole of order exactly $\lfloor k^2/4\rfloor-1$ | $k=2,3$ |
| T46t | Continuation near $1/3$, pole order $\lfloor k^2/4\rfloor$ and the leading coefficient | $k=2,3$ |

In the second row, order zero at $k=2$ denotes regularity, not a pole: $M_2=1$ is regular and nonzero at $\frac13$.

## Open boundary

Depth four and beyond at and past $\operatorname{Re}s=1/3$, and depth three further left (ANS-T46); singularities and natural boundaries at higher depth (ANS-T46a). ANS-I v014 records that no viable route to the continuation of $G_4$ past $\frac13$ has been established.

## Reading across (interpretation)

The quadratic growth of the conjectured order with depth is a candidate point of contact with generative geometry. Models are not the functions $G_k$.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS-T46k | Depth three: pole of order exactly two at 1/3 | PROVED | V |
| ANS-T46m | Every depth: decomposition by end letters | PROVED | V |
| ANS-T46s | Role patterns: local expectation and agreement with proved coefficients | PROVED | V |
| ANS-T46b | Pole of order floor(k^2/4) at 1/3 | PROVED for k <= 3; CONJECTURE for k >= 4 | V |
| ANS-T46q | Weighted middle-word sum: pole order floor(k^2/4)-1 | CONJECTURE (k = 2, 3 proved) | N |
| ANS-T46t | General continuation, pole order floor(k^2/4) and leading coefficient at 1/3 | CONJECTURE (k = 2, 3 proved) | N |

## Recorded open questions

- **ANS-T46:** Depth k >= 4 at and beyond Re s = 1/3; depth three further to the left.
- **ANS-T46a:** Singularities and natural boundaries at higher depth.

## Connected entries (cited dependencies)

- **Uses ATL-01** (Exact admissible composition): ANS-T03, ANS-T47.
- **Uses ATL-06** (Fixed-depth singularity architecture): ANS-T12, ANS-T34.
- **Uses ATL-07** (Depth two: an arithmetic singularity hierarchy): ANS-T45, ANS-T45a.

## Review boundary

Without a review verdict: ANS-T46q (N), ANS-T46t (N).

Qualified verdicts:

- ANS-T46h-i: A normal-convergence clarification was requested and added in ANS-I v013.
- ANS-T46j: Two scope clarifications were requested and made in ANS-I v013.

## All results and proof sources

- **ANS-I v010:** ANS-T46c.
- **ANS-I v011:** ANS-T46f, ANS-T46d, ANS-T46e-i.
- **ANS-I v012:** ANS-T46g, ANS-T46h, ANS-T46h-i, ANS-T46i, ANS-T46j, ANS-T46e, ANS-T46k, ANS-T46l.
- **ANS-I v013:** ANS-T46k-i, ANS-T46m, ANS-T46n, ANS-T46o, ANS-T46p, ANS-T46q.
- **ANS-I v014:** ANS-T46r, ANS-T46s.
- **ANS-I v009:** ANS-T46b.
- **ANS-I v015:** ANS-T46t.

# ATL-09: Collective growth at and below s = 1

## Mathematical object

$G_k(s)^{1/k}$ for real $s>1/2$, with particular attention to $1/2<s\le1$ and the window near $1$. For $s\le1$ one has $B(s)=\infty$ and the radius of convergence of $\sum_kG_k(s)t^k$ is zero. For $s\le1/2$ the fixed-depth sums already diverge.

## Established structure

- At $s=1$ the growth has exact order $\log k$: $\log k-\log\log k+O(1)\le G_k(1)^{1/k}\le(e^{\gamma}\zeta(2)+o(1))\log k$, and for $1/2<s<1$ it is at least $c_sk^{1-s}$ (T48).
- The constants are sharpened on both sides (T49 below, T48a above):
$$\boxed{1.107910\ldots\le\liminf_{k\to\infty}\frac{G_k(1)^{1/k}}{\log k}\le\limsup_{k\to\infty}\frac{G_k(1)^{1/k}}{\log k}\le e^{\gamma}}$$
- Under growth constants $0<c_-\le c_+<\infty$, the exponential generating function $\sum_kG_k(1)t^k/k!$ is entire of order one and infinite type, with matching maximum-modulus bounds (T48b).
- Two-sided bounds hold in the window $s=1+\tau/\log k$ for every fixed real $\tau$ as $k\to\infty$ (T50). No uniform statement for a growing parameter $\tau=\tau(k)$ is established.

## What it reveals

Without admissibility the value at $s=1$ would be infinite. With it, the growth rate is finite and of size $\log k$, which is also the total weight of the letters up to a fixed power of $k$.

## Further structure

The lower constant above one uses letters beyond the base range whose prime factors are small, counted with the Dickman function (T49).

## Open boundary

Existence and value of $\lim G_k(1)^{1/k}/\log k$ (ANS-LIM), including whether the upper limit is strictly below $e^{\gamma}$. A heuristic recorded in v015, which assumes an equidistribution that is not proved, suggests a value below $e^{\gamma}$.

## Reading across (interpretation)

The constraint here is a balance between primes supplied by $N+1$ and consumed by $N$, the same bookkeeping as in ATL-10. The variational principle of ATL-11 gives a broader context for this reading. No theorem in the collection carries it over to $s=1$: those results assume $a>1$ in the extended grammar.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS-T48 | Growth of G_k at s = 1 of exact order log k | PROVED | V |
| ANS-T48a | Upper constant e^gamma | PROVED | V |
| ANS-T49 | Lower constant 1.1079 | PROVED | V |
| ANS-T50 | Growth bounds in the window around s = 1 | PROVED | VQ |

## Recorded open questions

- **ANS-LIM:** Existence and value of lim G_k(1)^(1/k)/log k. A heuristic (v015, unproved) suggests a value below e^gamma. No separate ID in the releases; ANS-LIM is a label of this collection.

## Connected entries (cited dependencies)

- **Uses ATL-04** (Collective critical suppression): ANS-T23, ANS-T23a.

## Review boundary

Every result in this entry has a review verdict.

Qualified verdicts:

- ANS-T48b: The bounding constants satisfy 0 < c_- <= c_+ < infinity.
- ANS-T50: Fixed real tau as k tends to infinity; no uniform statement for tau = tau(k).

## All results and proof sources

- **ANS-I v014:** ANS-T48.
- **ANS-I v015:** ANS-T48a, ANS-T48b, ANS-T49, ANS-T50.

# ATL-10: Extended generation and prime-resource balance

## Mathematical object

The nesting grammar with finitely many further multipliers $\alpha_j>1$ having a rational power. States fall into finitely many torsion classes. The **drift** $\mu_p(a)$ is the mean change of the exponent of $p$ per letter under the law proportional to $\mu(\ell)^{-a}$; $\sigma_A$ solves $B_A(\sigma_A)=1$.

## Established structure

- **Foundations.** Source formula, comparison of classes, factorization $\mathcal Z_\varphi=\zeta\,\mathcal G_\varphi$ and invariance on valuation-type classes (L1, L2, T01, T00).
- **Positive drift.** Depth bounds, counting bounds, derivative bounds and infimal Gevrey order $\sigma_A$ transfer from the nesting theory (T02, T03, T04); first introductions keep their order (T07). The exponent depends on the real values of the multipliers (T08).
- **Operators.** A first-letter identity (T06), one-letter formulae for any signs and a closed countable operator system for $\operatorname{Re}s>1$, with its realizations (T14, T10 to T13, T15).
- **Growth rate in general.** $\lim\mathcal G_{\varphi,k}(a)^{1/k}=\rho_A(a)$, the minimum of an explicit convex function. The abscissa $\sigma^\ast$ solves $\rho_A=1$, is the same in every class, equals $\sigma_A$ if all drifts at $\sigma_A$ are nonnegative and is strictly smaller if one is negative (T16; earlier bound T05).
- **Boundary cases.** If some drifts vanish at $\sigma_A$ and the others are positive, the series is finite at the abscissa (T09). If all drifts are nonnegative, depth bounds of the form $ck^{\beta}/\log k$ to $Ck^{\beta}$ still hold (T09a).
- **Example.** An interval for the abscissa with multiplier $2/\sqrt3$ (C16, floating point; certified as ANS2N-T06).

## What it reveals

The sign of the drift decides whether admissibility changes only lower-order behaviour or changes the exponent itself. If no drift is negative, the exponent stays at the characteristic root $\sigma_A$, as in the original grammar; if some prime is depleted on average, it lies strictly below that root.

## Further structure

T16 expresses the effect of depletion as a minimization over prime weights, developed in ATL-11.

## Open boundary

Exact suppression order in the extensions, behaviour at the abscissa under negative drift, the spectrum and continuation of the transfer operators, and whether a drift can vanish exactly at $\sigma_A$ (ANS2-O3, O5, O6, O7).

## Reading across (interpretation)

The dichotomy is a candidate point of contact with admissibility and arithmetic dynamics, and with the study of alternative history grammars.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS2-L1 | Source formula in extended grammars | PROVED | V |
| ANS2-T02 | Positive drift: depth bounds and abscissa | PROVED | V |
| ANS2-T16 | Growth rate, abscissa, drift dichotomy | PROVED | V |
| ANS2-T05 | Negative drift: abscissa below the characteristic root | PROVED | V |
| ANS2-T13 | Closed countable operator system | PROVED | V |

## Recorded open questions

- **ANS2-O3:** Exact suppression order in the extensions.
- **ANS2-O5:** Behaviour at the abscissa under negative drift (carried on as ANS2N-O2).
- **ANS2-O6:** Spectrum and continuation of the transfer operators.
- **ANS2-O7:** Does any extension have a drift exactly zero at sigma_A?

## Connected entries (cited dependencies)

- **Uses ATL-04** (Collective critical suppression): ANS-T23, ANS-T24a, ANS-T27, ANS-T28a.
- **Used by ATL-11** (Entropy and admissibility): ANS2N-T01, ANS2N-T02, ANS2N-T04a, ANS2N-T04b, ANS2N-T05, ANS2N-T06.

## Review boundary

Every result in this entry has a review verdict.

Qualified verdicts:

- ANS2-T04: Valid for the infimal Gevrey order.
- ANS2-T07: Valid with the precise event definition, now in the text.
- ANS2-T15: Bounded only when the norm is finite (in the text).

## All results and proof sources

- **ANS-II v001:** ANS2-T00, ANS2-L1, ANS2-L2, ANS2-T01, ANS2-T02, ANS2-T03, ANS2-T04, ANS2-T05, ANS2-T06, ANS2-T07, ANS2-T08.
- **ANS-II v002:** ANS2-T14, ANS2-T10, ANS2-T11, ANS2-T12, ANS2-T13, ANS2-T15, ANS2-T16, ANS2-T09, ANS2-T09a, ANS2-C16.

# ATL-11: Entropy and admissibility

## Mathematical object

Probability laws $\pi$ on the letters, with entropy $H(\pi)$ and a resource functional $\Lambda(\pi)$ that charges the logarithm of the multiplier and the depletion of primes. A law is resource-neutral when no prime drift is negative. The dual variables are prime weights $\theta_p$ with optimum $\theta^\ast$, giving a candidate law $\nu^\ast$.

## Established structure

- **Variational principle.** For $a>1$, with the suprema taken over **finitely supported** probability laws $\pi$: $\log\rho=\sup_\pi[H-a\Lambda]$, also over resource-neutral laws, and for multipliers above one $\sigma^\ast=\sup_\pi H/\Lambda$; depletion is never optimal (T01, using weights controlled in T02). Attainment by a probability law on the complete alphabet is a separate result, subject to the criteria below.
- **Counting.** The three counting functions have the exponent $\sigma^\ast$ for any signs of the drifts (T04a, T04b). Certified example (T06).
- **Optimal law.** Finite optimal laws converge to $\nu^\ast$; criteria for attainment (T03, T07, T08) and a variational inequality (T09) lead to the depletion-surplus inequality: $\nu^\ast$ attains if it is neutral, and in particular if all weights are below one half (T10).
- **Shape of the weights.** They vanish identically or are supported on infinitely many primes (T05). Under negative drift, "all weights below one half" and "weights tend to zero" cannot both hold, in the setting of T11.
- **At the threshold.** Constraints on large weights (T12a, T12), the exceptional decay case (C12), bounds for the moment defect and its location at single primes (T13, T14), and a bound on average weight (T15).

## What it reveals

The exponent of a depleting grammar is an entropy rate under a balance condition at every prime. Whether the optimum is achieved by a law is a question about how weight behaves at individual primes.

## Further structure

Failure of attainment, if it occurs, requires a depleted prime with weight at least one half, on the boundary of the domain (T10) and visible in the mean divisibility of $N+1$ at that prime (T14).

## Open boundary

Whether the supremum is always attained; convergence and suppression at the abscissa; lower-order factors of the counts; decay of the weights; whether a weight can reach one half; and whether the logarithmic average of the weights vanishes (ANS2N-O1 to O6).

## Reading across (interpretation)

This principle is the broadest statement in the collection about balancing prime resources, and a natural frame for the questions of ATL-04 and ATL-09. It is a frame only: its hypotheses differ from theirs. It is also a candidate point of contact with generative information geometry.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS2N-T01 | Entropy-admissibility variational principle | PROVED | V |
| ANS2N-T03 | Optimal law and attainment criterion | PROVED | VQ |
| ANS2N-T10 | Depletion-surplus inequality | PROVED | V |
| ANS2N-T14 | Location of the defect | PROVED | VQ |

## Recorded open questions

- **ANS2N-O1:** Is the entropy supremum always attained?
- **ANS2N-O2:** Convergence of G at the abscissa, and suppression there.
- **ANS2N-O3:** Lower-order factors of the counting functions.
- **ANS2N-O4:** Decay of the optimal weights (remaining case: maximum exactly 1/2).
- **ANS2N-O5:** Can an optimal weight reach or exceed 1/2?
- **ANS2N-O6:** Is the logarithmic average of the optimal weights zero?

## Connected entries (cited dependencies)

- **Uses ATL-04** (Collective critical suppression): ANS-T24a.
- **Uses ATL-10** (Extended generation and prime-resource balance): ANS2-C16, ANS2-L1, ANS2-T16.

## Review boundary

Every result in this entry has a review verdict.

Qualified verdicts:

- ANS2N-T03: Convergence valid; attainment is open.
- ANS2N-T06: Method valid and stored result reviewed; no independent rerun.
- ANS2N-T07: Valid; its hypothesis is superseded by ANS2N-T10.
- ANS2N-T09: Valid; a proof clarification is recorded in ANS-II-ND v003.
- ANS2N-C12: Valid under its hypotheses.
- ANS2N-T14: Proof-writing clarification: in the final Fatou step use a limit superior for the drift difference, or a further convergent subsequence. The theorem is unaffected; the release file is not edited.

## All results and proof sources

- **ANS-II-ND v001:** ANS2N-T02, ANS2N-T01, ANS2N-T03, ANS2N-T04a, ANS2N-T04b, ANS2N-T05, ANS2N-T06.
- **ANS-II-ND v002:** ANS2N-T07, ANS2N-T08, ANS2N-T09, ANS2N-T10, ANS2N-T11.
- **ANS-II-ND v003:** ANS2N-T12a, ANS2N-T12, ANS2N-C12, ANS2N-T13, ANS2N-T14, ANS2N-T15.
