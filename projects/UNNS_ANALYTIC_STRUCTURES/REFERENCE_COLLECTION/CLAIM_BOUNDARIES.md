# Claim boundaries

This page states limits. The exact statements are in the compendium, and they govern.

## Meaning of the labels
- **PROVED**: a written argument exists in a release. It is not a statement about independent review; read the review code.
- **PROVED (implication)** and **PROVED (model)**: a conditional statement, or a statement about a model series that is not the function G_k.
- **CERTIFIED**: a directed-rounding computation. It relies on the correct rounding of MPFR and on the program.
- **COMPUTED**: numerical evidence only.
- **CONJECTURE**: not proved in general; proved cases are named.
- "UNNS Research Collective review" means a verdict supplied or adopted by the Collective; the records under `PROVENANCE/` say where each verdict comes from. Nothing here has had external peer review.
- Finite verification never counts as proof of an infinite statement.

## Boundaries by subject
| Subject | Established | Not established | Entries |
|--|--|--|--|
| Grammar | Results of regions A to I concern the nesting grammar; a few hold for every integral-image grammar with finiteness condition (F), as their statements say | Transfer to other grammars | T03, T01, T11, T25 |
| Classification of grammars | A saturation criterion | An analytic classification | T11 |
| Abscissa | The history series has abscissa sigma_c | A description of the singularity there | T09, T33 |
| At sigma_c | Convergence on the critical surface; no meromorphic continuation through sigma_c; holomorphic continuation across the rest of the critical line | Nature of the singularity | T20, T22, T31, T33 |
| Critical derivatives | Infimal Gevrey order | Membership at exactly that order | T27 |
| Critical decay | Bounds differing by a logarithm in the depth | The exact order. The exact order of the first-introduction event does not give it, since depletion of primes already met is a separate demand | T23, T23a, T28, T28a |
| Counting at the exponent | Z(X) = X^(sigma_c + o(1)), and also Z(X) = o(X^sigma_c): the first fixes the exponent, the second excludes a positive proportion of the pure power | Neither statement alone gives the order of Z(X) | T10, T21 |
| Counting factor | Regular variation of index sigma_c and two-sided stretched-exponential suppression | An asymptotic formula for the slowly varying factor | T24a, T40 |
| Equidistribution | Finite quotients | Rates and quotients beyond the stated ones | T37, T37b |
| Fixed depth | Each G_k is meromorphic on Re s > 1/3, with a pole of order k at 1/2 | Continuation of general G_k to the left of 1/3 | T34, T34b |
| Depth two | Meromorphic on Re s > 0 with natural boundary Re s = 0 | Nothing is claimed beyond that line | T45a |
| Depth two open questions | Maximal meromorphic domain and pole divisor | Classification of the zeros of G_2; the sharp unsmoothed term of order X^(1/3) in A_2(X) | T45a, T45d, ANS-G2Z, ANS-A2S |
| Depth two poles | Pole divisor on Re s > 0. The description of the non-real poles in one corollary assumes the Riemann hypothesis | No statement about the truth of that hypothesis | T45d |
| Depth three | Continuation past 1/3, pole of order two there | Behaviour further left; natural boundary of G_3 | T46e, T46k, T46k-i, T46a |
| Depth four and higher at 1/3 | Decomposition and link bounds; a conditional implication; model computations | The pole-order law (T46b), the weighted middle-word law (T46q), and the combined statement of continuation, pole order and leading coefficient (T46t) | T46m, T46n, T46o, T46p, T46b, T46q, T46t |
| s = 1 | G_k(1)^(1/k) has exact order log k; lower limit of the ratio to log k at least 1.107910..., upper limit at most e^gamma; window bounds for each fixed real tau | Existence or value of the limit; strict inequality below e^gamma; uniformity for tau depending on k | T48, T48a, T49, T50, ANS-LIM |
| Extended grammar, nonnegative drift | Abscissa unchanged; depth and counting bounds under the stated drift hypotheses | Exact suppression order in every case | ANS2-T02, ANS2-T03, ANS2-T09a, ANS2-O3 |
| Extended grammar, negative drift | The abscissa is given by an entropy variational principle and lies strictly below sigma_A | Attainment of the supremum; convergence at the abscissa | ANS2-T16, ANS2N-T01, ANS2N-O1, ANS2N-O2 |
| Example abscissa | Certified interval for the 2/sqrt3 example | Independent rerun of the certificate | ANS2N-T06 |

## Outside the programme's claims
- No result implies or approaches a proof of the Riemann hypothesis.
- No result is claimed new in the literature. The novelty review has not been done.
- No physical interpretation is claimed.
- No reviewed result rests on a cited ancestor without a review verdict. The recorded dependency graph is a lower bound. Results without a review verdict are listed in `PROVENANCE/REVIEW_STATUS.md`.
- Statements M1 to M8 in `CROSS_STRUCTURES/` are new derivations, unreviewed and not catalogued; the counts above do not include them.
- The Atlas summarizes and interprets. Its sections headed "Reading across" are not theorems.
- Mathematical proof status, mathematical review and release acceptance are separate. A verdict recorded here is not a rerun of any computation.
