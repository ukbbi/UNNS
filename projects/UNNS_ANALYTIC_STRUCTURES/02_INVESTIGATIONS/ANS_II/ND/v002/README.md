# ANS-II-ND v002 — Attainment and infinite prime-coordinate dynamics

Research notes, not a manuscript. Continues ANS-II-ND v001.

- `PROOFS.md` — the UNNS Research Collective's ND-T07 and ND-T08 checked; a variational inequality at the candidate law; the depletion–surplus inequality and attainment criterion; the restriction on decay of the weights.
- `THEOREMS.md` — register and status.
- `certify.py` — the v001 certificate with validity checks on the trial weights.
- `nd2_checks.py` — checks and computed observations; results in `results/nd2_checks.json`.
- `ANS_II_ND_v002_working_notes.pdf` — the notes in PDF.

Run (Python 3.10+, numpy, sympy, gmpy2): `python -B nd2_checks.py` (about a minute), or the parts `certificate` and `analysis` separately. It imports `../../v002/rate.py` and compares with `../v001/results/nd_checks.json`.

**Main outcome.** The full-alphabet optimum is attained whenever the optimal weights stay below 1/2 at the depleting primes. Whether the weights can reach 1/2 is open.
