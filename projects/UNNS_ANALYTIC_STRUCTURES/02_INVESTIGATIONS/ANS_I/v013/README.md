# ANS-I v013 — Boundary letters, link roles and depth four

Opened 27 November 2026 after the UNNS Research Collective review of v012. Research notes. Reviewed by the UNNS Research Collective.

- `PROOFS.md`, `ANS_I_v013_working_notes.pdf` — v012 corrections; T46k-i, T46m, T46n, T46o, T46p, conjecture T46q.
- `THEOREMS.md` — status register.
- `v013_checks.py` — finite checks.

## Rerun
    python3 -B v013_checks.py recursion
    python3 -B v013_checks.py local
    python3 -B v013_checks.py numeric
    python3 -B v013_checks.py roles
    python3 -B v013_checks.py model
    python3 -B v013_checks.py margins

Outputs are written to `results/`. Recorded software: Python 3.10.12, numpy 2.2.6, mpmath 1.3.0, sympy 1.14.0 (Linux).
