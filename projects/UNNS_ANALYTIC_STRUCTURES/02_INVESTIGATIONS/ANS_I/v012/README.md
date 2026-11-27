# ANS-I v012 — Continuation of the depth-three function past 1/3

Opened 27 November 2026 after the UNNS Research Collective review of v011. Research notes. Reviewed by the UNNS Research Collective; clarifications are recorded in v013.

- `PROOFS.md`, `ANS_I_v012_working_notes.pdf` — T46g, T46h (checked), T46h-i, T46i, T46j, T46e, T46k, T46l.
- `THEOREMS.md` — status register.
- `v012_checks.py` — finite checks.

## Rerun (`leading` reads the v011 results)
    python3 -B v012_checks.py algebra
    python3 -B v012_checks.py representation
    python3 -B v012_checks.py margins
    python3 -B v012_checks.py lemma
    python3 -B v012_checks.py remainder
    python3 -B v012_checks.py shifted      # about 1 GB memory
    python3 -B v012_checks.py leading

Outputs are written to `results/`. Recorded software: Python 3.10.12, numpy 2.2.6, mpmath 1.3.0, sympy 1.14.0 (Linux).
