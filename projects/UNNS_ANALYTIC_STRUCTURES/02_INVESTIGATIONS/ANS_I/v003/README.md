# ANS-I v003 — Critical regularity and prime-coordinate suppression

**State:** working research notes, open for review. No report or manuscript. v001 unchanged; v002 received two proof clarifications and a corrected sampler description.

## Run
    python v003_checks.py      (Python 3.8+ with sympy; reads ../v001 and ../v002; a few seconds)

## Where things stand (sigma = sigma_c, beta = 1/sigma)
- Depth: exp(-C k^beta) <= G_k(sigma) <= exp(-c k^beta / log k).
- Counting: exp(-C (log X)^beta) <= Z(X)/X^sigma <= exp(-c (log X)^beta / log log X).
- Derivatives: D_j = (j!)^(sigma + o(1)).
- First introductions: exact order k^beta / log k.

Files: PROOFS.md, THEOREMS.md, v003_checks.py, results/.
