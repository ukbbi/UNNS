# YM-3B Freeze Package

This package freezes the next measured-data refinement experiment for `UNNS_YM_GAP`.

## Status

- YM-3A: complete — `MODEL-REFINEMENT PERSISTENT`
- YM-3B source acquisition/admission: complete
- YM-3B supplementary preregistration: frozen
- YM-3B digitization: not yet performed
- YM-3B CORR-I run: not yet performed

## Primary source

Sakai & Sasaki (2023), Phys. Rev. D 107, 034510, arXiv:2211.15176.

Admitted Class B `0++` effective-mass trajectories:

- beta 6.20 — Figure 9
- beta 6.40 — Figure 10
- beta 6.71 — Figure 11
- beta 6.93 — Figure 12

## Next action

Digitize the four admitted `A1++` ground-state trajectories exactly under
`docs/PREREG_YM3B.md`, reconstruct the normalized eigen-correlator proxies,
perform all admission checks, and only then build the CORR-I batch.

Do not modify CORR-I v0.1.2.
Do not rerun YM-3A.
Do not inspect a partial YM-3B result before all four beta inputs are prepared.
