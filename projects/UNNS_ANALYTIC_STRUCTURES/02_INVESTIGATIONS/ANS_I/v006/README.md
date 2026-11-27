# ANS-I v006 — Character decomposition and local coupling

Opened 27 November 2026 after the UNNS Research Collective review of v005. Research notes. Reviewed by the UNNS Research Collective; one wording correction applied (see `00_SCOPE/CHANGELOG.md`).

- `PROOFS.md`, `ANS_I_v006_working_notes.pdf` — T32a, T35, T36, T37a.
- `THEOREMS.md` — status register.
- `v006_checks.py`, `sector_count.c` — finite checks.

## Rerun
    python3 -B v006_checks.py algebra
    python3 -B v006_checks.py local        # under a minute
    python3 -B v006_checks.py characters
    python3 -B v006_checks.py sectors      # needs gcc

Outputs are written to `results/`. Recorded software: Python 3.10.12, numpy 2.2.6, mpmath 1.3.0, gcc 11.4 (Linux).
