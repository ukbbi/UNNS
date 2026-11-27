# ANS-I v007 — register

PROVED means a written proof in `PROOFS.md`. Nesting grammar throughout. Finite checks: `results/`.

| ID | Result | Status | Origin | Review |
|---|---|---|---|---|
| ANS-T37 | A_gamma(X) ~ A(X)/\|Gamma\|, and the same for each fixed source, for every finite quotient | PROVED | UNNS Research Collective's proposed proof; details and fixed source checked internally | UNNS Research Collective review: valid |
| ANS-T40 | A(lambda X)/A(X) -> lambda^sigma_c, same for N_x: A = X^sigma_c times a slowly varying factor | PROVED | UNNS Research Collective's proposed proof | UNNS Research Collective review: valid |
| ANS-T41 | C(X) ~ zeta(sigma_c) A(X), with equal sector shares | PROVED | UNNS Research Collective; majorant written out internally | UNNS Research Collective review: valid |
| ANS-T37b | G_k sector ratio at sigma_c = 1/\|Gamma\| + O(e^(-c'k)) | PROVED | UNNS Research Collective | UNNS Research Collective review: valid |
| ANS-T42 | Typical histories: log Q ~ log X, log K = o(log X), depth ~ log X / lambda_c, block frequencies -> product of r_N^(-sigma_c) | PROVED | internal | UNNS Research Collective review: valid |
| ANS-T33 | Singularity at sigma_c | OPEN | UNNS Research Collective | |
| ANS-T34 | Continuation of G_k, k >= 3 | OPEN | UNNS Research Collective | |
| ANS-T38 | Complex zeros | OPEN | UNNS Research Collective | |
| ANS-T39 | Twists q^(i tau0) at tau0 != 0 | OPEN | internal | |

The bounds on the slowly varying factor use T24a (v003; found valid in the UNNS Research Collective review of v007); T24 (v002, reviewed) gives them up to a factor (log log X)^2.

## Computed observations (not theorems)
| Observation | Values at X = 1e8 | Proven limit |
|---|---|---|
| A(2X)/A(X) | 2.455 | 2.921 |
| C(X)/A(X) | 4.82 | 2.446 |
| largest order-seven sector deviation | 0.0013 | 0 |
| mean depth / log X (not yet approaching) | 0.432 | 0.337 |
| share of letter 1 | 0.244 | 0.117 |
