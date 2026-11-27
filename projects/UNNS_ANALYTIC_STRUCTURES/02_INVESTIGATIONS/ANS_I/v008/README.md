# ANS-I v008 — Continuation of the depth-k functions

Opened 27 November 2026 after the UNNS Research Collective review of v007. Research notes. Reviewed by the UNNS Research Collective; clarifications applied (see `00_SCOPE/CHANGELOG.md`).

- `PROOFS.md`, `ANS_I_v008_working_notes.pdf` — T34, T34a, T45, T43, T44, T42a.
- `THEOREMS.md` — status register.
- `v008_checks.py`, `depth_count.c` — finite checks.

## Rerun
    python3 -B v008_checks.py identity
    python3 -B v008_checks.py count2     # needs gcc; includes the depth-two constants
    python3 -B v008_checks.py count3     # needs gcc; about two minutes
    python3 -B v008_checks.py laws       # reads ../v007/results/v007_census.json

Outputs are written to `results/`. Recorded software: Python 3.10.12, numpy 2.2.6, mpmath 1.3.0, gcc 11.4 (Linux).
