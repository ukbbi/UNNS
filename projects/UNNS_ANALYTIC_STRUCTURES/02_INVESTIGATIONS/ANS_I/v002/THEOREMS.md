# ANS-I v002 — register

PROVED means a written proof in `PROOFS.md`. T22-T24 and T26 passed the UNNS Research Collective's mathematical review on 26 November 2026; sharper bounds are in v003. Finite checks: `results/critical_checks.json`.

| ID | Result | Status | Origin of the argument | Review |
|---|---|---|---|---|
| ANS-T16 | G_k(a)/B(a)^k = E[K_k^-a] | PROVED | UNNS Research Collective's review note (a = sigma_c) | checked internally |
| ANS-T17 | Critical random words are a.s. inadmissible from any integer | PROVED | review note | checked internally |
| ANS-T18 | K_k -> infinity a.s. | PROVED | review note | checked internally |
| ANS-T19 | G_k(sigma_c) -> 0 with G_k^(1/k) -> 1 | PROVED | review note | checked internally |
| ANS-T20 | No meromorphic continuation through sigma_c | PROVED | review note | checked internally |
| ANS-T21 | N_x, A, C are o(X^sigma_c) | PROVED | review note | checked internally |
| ANS-T22 | On |t|B(a) = 1, a > 1: F converges absolutely iff Re(s+u) > 0; G(sigma_c,1) finite; G and Z_H are C-infinity up to Re s = sigma_c | PROVED | internal | UNNS Research Collective review: valid |
| ANS-T23 | -log(G_k(a)/B(a)^k) = k^(1/a + o(1)) | PROVED up to logarithmic factors; exact order OPEN | internal | UNNS Research Collective review: valid |
| ANS-T24 | N_x, A, C = X^sigma_c exp(-(log X)^(1/sigma_c + o(1))) | PROVED up to log log factors; exact order OPEN | internal | UNNS Research Collective review: valid |
| ANS-T25 | Other nesting grammars | OPEN | | |
| ANS-T26 | Finite alphabets: G_k -> c_M > 0, blow-up c_M/(mu_M delta), c_M -> 0 | PROVED | internal (extends the comparison in the review note) | UNNS Research Collective review: valid, clarification added |

## Computed observations (not theorems)
| Observation | Value |
|---|---|
| -log G_k(sigma_c) / k^(1/sigma_c), Monte Carlo, 200,000 words | about 1.7 to 1.95 for k <= 10; noisy beyond k = 20 |
| G(sigma_c,1), exact G_1, G_2 plus Monte Carlo terms | about 1.28 |
| -log(A(X)/X^sigma_c) / (log X)^(1/sigma_c), exact census | falls from 1.44 (10^3) to 1.35 (10^7) |

## Open
1. Exact order of -log G_k(sigma_c): is it comparable to k^(1/sigma_c) without logarithms? Does the ratio have a limit?
2. The same for -log(A(X)/X^sigma_c) against (log X)^(1/sigma_c).
3. Analytic continuation across any other point of Re s = sigma_c, or a natural boundary.
4. Region of F for Re(s+u) < 0 inside |t|B < 1 (from v001).
5. T25: the arguments look adaptable to x (N+1)^d / N with the exponent 1/(a(d-1)); not written or checked. The Chebyshev step in T24 needs the resulting exponent to exceed 1/2.
