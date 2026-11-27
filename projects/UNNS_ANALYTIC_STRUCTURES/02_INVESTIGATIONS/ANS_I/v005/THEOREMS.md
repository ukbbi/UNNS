# ANS-I v005 — register

PROVED means a written proof in `PROOFS.md`. Nesting grammar throughout. Finite checks: `results/`.

| ID | Result | Status | Origin | Review |
|---|---|---|---|---|
| ANS-T31 | G(s,1) and Z_H(s,1) continue holomorphically to {sigma > sigma_c - a min(tau^2, \|tau\|^-A), tau != 0}; sigma_c is the only singular point on the critical line (resolves the line part of ANS-T29) | PROVED | internal | UNNS Research Collective review: valid |
| ANS-T32 | A_k(X) ~ kappa_k sqrt(X) log^(k-1) X / (2^(k-1) (k-1)!), kappa_k finite with Euler product | PROVED | internal | UNNS Research Collective review: valid after correction (applied) |
| ANS-C1 | (2 sigma - 1)^k G_k(sigma) -> kappa_k (conjectured in v001; corollary of T32) | PROVED | conjecture v001; proof: internal | UNNS Research Collective review: valid |
| ANS-T33 | Do the continuations above and below sigma_c agree to its left? Nature of the singularity | OPEN | | |
| ANS-T34 | Continuation of G_k, k >= 3, to the left of Re s = 1/2 | OPEN | | |

## Computed observations (not theorems)
| Observation | Values |
|---|---|
| kappa_k, k = 2..6 | 1.85365, 5.1053, 19.119, 92.64, 561.0 |
| c_p(k) - 1 against binom(k,2) p^(-3/2) | ratios 0.99-1.08 at p = 101; within 0.013 of 1 at p = 10007 |
| exact A_k(X) / leading term | 0.82 (k=2, 1e12), 0.50 (k=3, 1e10), 0.21 (k=4, 1e9) |
