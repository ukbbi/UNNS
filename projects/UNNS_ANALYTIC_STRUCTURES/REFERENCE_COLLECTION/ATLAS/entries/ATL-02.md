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
