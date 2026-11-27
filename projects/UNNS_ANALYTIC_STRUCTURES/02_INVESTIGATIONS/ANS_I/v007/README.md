# ANS-I v007 — Generative scaling and equidistribution

Opened 27 November 2026 after the UNNS Research Collective review of v006. Research notes. Reviewed by the UNNS Research Collective; two clarifications applied (see `00_SCOPE/CHANGELOG.md`).

- `PROOFS.md`, `ANS_I_v007_working_notes.pdf` — exchange comparison, T37, T37b, T40, T41, T42.
- `THEOREMS.md` — status register.
- `v007_checks.py`, `census.c` — finite checks.

## Rerun
    python3 -B v007_checks.py census      # needs gcc; about one minute
    python3 -B v007_checks.py exchange
    python3 -B v007_checks.py depth

Outputs are written to `results/`. Recorded software: Python 3.10.12, numpy 2.2.6, mpmath 1.3.0, gcc 11.4 (Linux). Sampling seed 20261127.
