# ANS-I v011 — An exact decomposition of the depth-three function

Opened 27 November 2026 after the UNNS Research Collective review of v010. Research notes. Reviewed by the UNNS Research Collective.

- `PROOFS.md`, `ANS_I_v011_working_notes.pdf` — T45f, T38e, T46f, T46d, conjecture T46e.
- `THEOREMS.md` — status register.
- `v011_checks.py`, `hurwitz_np.py` — finite checks.

## Rerun (in this order; `counts` reads the output of `shifted` and the v008 results)
    python3 -B v011_checks.py grammar
    python3 -B v011_checks.py exponents
    python3 -B v011_checks.py local
    python3 -B v011_checks.py decomposition
    python3 -B v011_checks.py shifted      # about 1 GB memory
    python3 -B v011_checks.py counts

Outputs are written to `results/`. Recorded software: Python 3.10.12, numpy 2.2.6, mpmath 1.3.0 (Linux).
