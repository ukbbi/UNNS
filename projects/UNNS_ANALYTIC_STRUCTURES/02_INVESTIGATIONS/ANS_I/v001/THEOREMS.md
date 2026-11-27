# ANS-I v001 — theorem register

Status values: PROVED, VERIFIED_FINITE, COMPUTED, CONJECTURE, OPEN, REFUTED. Proofs are in `PROOFS.md`; checks are in `results/verification.json`. Every PROVED entry awaits independent review. No literature novelty review has been performed.

| ID | Result | Domain | Status | Finite check | Prior source / relation |
|---|---|---|---|---|---|
| ANS-T01 | History Dirichlet factorization Z_H = zeta G, with exact region | integral-image grammars with (F) | PROVED | coefficientwise via T02 | Monograph Thm 19.2 (unweighted, coefficient level) |
| ANS-T02 | Depth-resolved Moebius inversion | same | PROVED | VERIFIED_FINITE, all n <= 10^7 (nesting); controls to 2*10^4 | Monograph Thm 19.2 |
| ANS-T03 | Recurrences for E(wb), K(wb); predecessor recursion | same | PROVED | VERIFIED_FINITE, words with E <= 10^5 | Monograph Lemma 4.2 (least source/endpoint) |
| ANS-T04 | Prime-coordinate law, closed (maximum) form | nesting | PROVED | VERIFIED_FINITE, words with E <= 10^5 | valuation of T03 |
| ANS-T05 | Depth-two double sum, Hurwitz representation, continuation to Re s > 1/3 | nesting | PROVED | VERIFIED_FINITE at s = 3 (truncated, tail bounded) | classical gcd expansion applied to T03 |
| ANS-T06 | No ordinary Euler product for Z_H or G at t = 1 | nesting | PROVED | exact witnesses | H(36) = 6 as in monograph Ch. 6-7 |
| ANS-T07 | Sufficient convergence criterion, B(2) < 1 | nesting | PROVED | partial sums | |
| ANS-T08 | Closed form when all denominators are 1 | such grammars | PROVED | VERIFIED_FINITE to 2*10^4 | classical |
| ANS-T09 | G_k^(1/k) -> B(sigma); sharp abscissa sigma_c with B(sigma_c) = 1 | nesting | PROVED (boundary surface itself OPEN) | drift, restricted ratios; sigma_c COMPUTED | answers open question O01 |
| ANS-T10 | log A(X)/log X, log C(X)/log X -> sigma_c | nesting | PROVED (finer asymptotics OPEN) | COMPUTED to 10^7; convergence slow | |
| ANS-T11 | Analytic classification across grammars | integral-image | OPEN; saturation criterion PROVED | nine controls | |
| ANS-T12 | Fixed-depth region a + b > 1; abscissa of G_k is 1/2 | nesting, a > 0, b >= 0 | PROVED | | |
| ANS-T13 | Depth-two double pole, constant kappa, A_2(X) ~ (kappa/2) sqrt(X) log X | nesting | PROVED (uses Delange) | COMPUTED to 10^8 | |
| ANS-T14 | Source-weighted series F(s,u,t): all-history factorization, anti-diagonal closed form, convergence region | factorization: (F); region: nesting | PROVED (b < 0 sufficiency and boundary OPEN) | records replayed, E <= 10^5 | proposed extension F(s,u,t) |
| ANS-T15 | Every source's history count grows as X^(sigma_c + o(1)); all primes reachable from 1 | nesting | PROVED | prime words < 1000; orbit counts to 10^7 | |

## Observations and conjectures (not theorems)

| ID | Statement | Status |
|---|---|---|
| ANS-C1 | (2 sigma - 1)^k G_k(sigma) -> kappa_k as sigma -> 1/2+, kappa_k the mean of prod gcd(E,N_i)^(1/2) over profinitely uniform labels | CONJECTURE (k = 1, 2 proved) |
| ANS-C2 | H(mn) > H(m)H(n) for coprime non-squarefree m, n | CONJECTURE; holds for all 16,176 such pairs with mn <= 10^5 |
| ANS-N1 | A_2(X)/sqrt(X) = (kappa/2) log X + c + o(1), c = -4.5451 | COMPUTED; gap behaves like X^(-1/6) to 10^8 |
