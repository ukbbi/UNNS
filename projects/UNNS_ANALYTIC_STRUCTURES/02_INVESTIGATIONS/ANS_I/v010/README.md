# ANS-I v010 — Arithmetic singularity hierarchies

Opened 27 November 2026 after the UNNS Research Collective review of v009. Research notes. Reviewed by the UNNS Research Collective.

- `PROOFS.md`, `ANS_I_v010_working_notes.pdf` — T45c, T45d, T45e, T38b-d, T46c.
- `THEOREMS.md` — status register.
- `v010_checks.py`, `scipy_free.py` (Hurwitz zeta, numpy only) — finite checks.

## Rerun
    python3 -B v010_checks.py exponents
    python3 -B v010_checks.py zeros
    python3 -B v010_checks.py identity
    python3 -B v010_checks.py kloosterman
    python3 -B v010_checks.py summatory      # about 30 s, about 1 GB memory

Outputs are written to `results/`. Recorded software: Python 3.10.12, numpy 2.2.6, mpmath 1.3.0 (Linux).
