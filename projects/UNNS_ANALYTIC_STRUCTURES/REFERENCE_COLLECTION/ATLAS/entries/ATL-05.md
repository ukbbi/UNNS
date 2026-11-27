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
