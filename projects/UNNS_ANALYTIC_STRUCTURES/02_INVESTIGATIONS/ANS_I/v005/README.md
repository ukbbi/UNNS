# ANS-I v005 — The critical line and the depth-k functions

Opened 27 November 2026, on the UNNS Research Collective's decision to return to the original analytic functions.
Research notes; reviewed by the UNNS Research Collective (27 November 2026), with one correction to the proof of T32 applied here and in the PDF. The v005 release zip predates the correction. v001-v004 are unchanged.

- `PROOFS.md`, `ANS_I_v005_working_notes.pdf` — continuation across the critical line (T31); depth-k counting (T32, C1).
- `THEOREMS.md` — status register.
- `v005_checks.py`, `depth_count.c` — finite and statistical checks.

## Rerun
    python3 -B v005_checks.py continuation   # about 35 s
    python3 -B v005_checks.py constants
    python3 -B v005_checks.py count          # about 90 s, needs gcc

Outputs are written to `results/`. Recorded software: Python 3.10.12, numpy 2.2.6, mpmath 1.3.0, gcc (Linux).
