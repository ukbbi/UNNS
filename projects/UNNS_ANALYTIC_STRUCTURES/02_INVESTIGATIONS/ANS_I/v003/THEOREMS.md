# ANS-I v003 — register

PROVED means a written proof in `PROOFS.md`. Finite checks: `results/v003_checks.json`.

| ID | Result | Status | Origin | Review |
|---|---|---|---|---|
| ANS-T23a | -log E[K_k^-b] <= C k^beta (with v002: >= c k^beta / log k) | PROVED | UNNS Research Collective review note | checked internally |
| ANS-T24a | -log(Z(X)/X^sigma_c) <= C (log X)^beta_c, Z = N_x, A, C | PROVED | internal | UNNS Research Collective review: valid (renewed review with v007) |
| ANS-T25 | Higher-degree nesting grammars | OPEN | | |
| ANS-T27 | c^j j^(sigma j) <= D_j <= (C j log j)^(sigma j); infimal Gevrey order sigma_c | PROVED | statement: UNNS Research Collective; proof with error terms: internal | UNNS Research Collective review: valid as infimal order (recorded with the v006 review) |
| ANS-T28 | Exact order: -log E[K_k^-b] comparable to k^beta / log k | CONJECTURE | internal | |
| ANS-T28a | Probability that every new prime arrives through N+1 is exp(-order k^beta / log k) | PROVED | internal | pending |
| ANS-T29 | Continuation along the critical line | OPEN | UNNS Research Collective | |
| ANS-T30 | Quantitative finite-to-infinite alphabet transition | OPEN | UNNS Research Collective | |

## Computed observations (statistical; not theorems)
| Observation | Values |
|---|---|
| mean log K_k / k^beta_c, k = 100, 300, 1000, 3000 | see results; rising slowly from about 4.2 to 4.8 |
| mean first-occurrence time / q^sigma_c under the conditioned law, q <= 23 | 0.3 to 0.7 |
| mean rejected draws / (k^beta / log k), k = 100, 500, 2000 | 8.8, 8.3, 7.7 |
