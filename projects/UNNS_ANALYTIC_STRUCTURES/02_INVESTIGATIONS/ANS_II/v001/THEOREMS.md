# ANS-II v001 — register

PROVED means a written proof in `PROOFS.md`. Review: the UNNS Research Collective's independent mathematical review of v001 (recorded 26 November 2026) found every PROVED entry valid, T04 for the infimal Gevrey order and T07 with the event defined precisely; both qualifications and two clarifications of the counting proof are now in the text. The verdicts are conditional on the ANS-I lemmas used (see Dependencies). The reviewer separately re-evaluated the 2/sqrt3 bound at a = 2.062, theta = 0.08 (sum 0.999777937 < 1); the reviewer did not rerun the check suite. Constants and finite checks: `results/ansii_checks.json`.

| ID | Result | Hypothesis | Status |
|---|---|---|---|
| ANS2-T00 | Z_C = alpha_C^-s Z_H on a valuation-type class | nesting letters only | PROVED |
| ANS2-L1 | v_p(K) = max_j -floor(phi_p + S_p(j)) | any torsion multipliers > 1 | PROVED |
| ANS2-L2 | All torsion classes are comparable, K_phi / K_0 / R K_phi | same | PROVED |
| ANS2-T01 | Z_phi = zeta G_phi | same | PROVED |
| ANS2-T02 | Depth bounds k^beta/log k to k^beta; abscissa sigma_A; critical convergence | positive drift (D) | PROVED |
| ANS2-T03 | X^sigma_A exp(-(log X)^beta) up to log log, all counting functions | (D) | PROVED |
| ANS2-T04 | Derivative bounds; smooth singular point; infimal Gevrey order sigma_A (membership at order sigma_A open) | (D) | PROVED |
| ANS2-T05 | Abscissa strictly below the characteristic root | some drift negative | PROVED |
| ANS2-T06 | First-letter identity between classes | non-negative exponents | PROVED |
| ANS2-T07 | Event I_k (every prime dividing a nesting letter occurred earlier through N or N+1): probability exp(-order k^beta/log k) | any a > 1 | PROVED |
| ANS2-T08 | Dependence on multiplier size; 2^(1/d) asymptotic | (D) where an abscissa is meant | PROVED |
| ANS2-O1 | Exact abscissa under negative drift | | OPEN |
| ANS2-O2 | Zero drift | | OPEN |
| ANS2-O3 | Exact suppression order in the extensions | | OPEN |
| ANS2-O4 | Coupled class operators (planned v002) | | OPEN |

Dependencies: ANS-I v002 Lemmas A, B and section 4; ANS-I v003 Lemma 2 and section 5 (v003 proofs themselves await review). Novelty: unreviewed.

## Computed exponents
| Adjoined | Order | characteristic root | 1/root | Drift condition |
|---|---|---|---|---|
| none | | 1.546381 | 0.646671 | holds |
| sqrt2 | 2 | 1.834059 | 0.545239 | holds (exponents >= 0) |
| sqrt3 | 2 | 1.725995 | 0.579376 | holds |
| cube root of 2 | 3 | 1.947885 | 0.513377 | holds |
| fifth root of 2 | 5 | 2.113318 | 0.473190 | holds |
| sqrt2, sqrt3 | 2 x 2 | 2.171224 | 0.460570 | holds |
| 2 | 1 | 1.680811 | 0.594951 | holds |
| 2^(3/2) | 2 | 1.618266 | 0.617945 | holds |
| 3/sqrt2 | 2 | 1.666547 | 0.600043 | holds (computed drift signs) |
| 2/cbrt3 | 3 | 1.849399 | 0.540716 | holds (computed drift signs; margin 0.03) |
| 2/sqrt3 | 2 | 2.100608 | not an exponent | fails at p = 3; abscissa <= 2.062 |
