# ANS-II-ND v003 — The half-weight threshold

Research notes, not a manuscript. Continues ANS-II-ND v002.

- `PROOFS.md` — the UNNS Research Collective's ND-T12 and ND-T13 checked; the location of the moment defect; an average bound for the weights; computed observations and a labelled heuristic.
- `THEOREMS.md` — register and status.
- `nd3_checks.py` — checks and computed observations; results in `results/nd3_checks.json`.
- `ANS_II_ND_v003_working_notes.pdf` — the notes in PDF.

Run (Python 3.10+, numpy, sympy): `python -B nd3_checks.py` (checks, under a minute), `python -B nd3_checks.py families` (under a minute), `python -B nd3_checks.py large 600000` and `... large 1500000` (a few minutes in total, about 2 GB memory or less). It imports `../../v002/rate.py` and `../v002/nd2_checks.py` (which imports `../v002/certify.py`, needing gmpy2).

**Main outcome.** Attainment holds exactly when the divisibility of N+1 by each fixed prime is not lost in the limit. Whether a weight can exceed 1/2 remains open.
