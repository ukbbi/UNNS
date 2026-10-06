# CORR-I AT20 0++ Pilot Input v0.0.1

This package is the first actual Yang-Mills input prepared for CORR-I.

## Files

- `meff.csv` — digitized AT20 Figure 7 effective-mass point estimates for the beta=6.50 0++ ground state.
- `corr.csv` — chamber-ready normalized correlator proxy reconstructed from those effective masses.
- `metadata.json` — provenance, reconstruction rule, and limitations.
- `build_proxy.py` — reproducibly rebuilds `corr.csv` from `meff.csv`.
- `manifest.json` — SHA-256 manifest.

## Run in CORR-I

Upload:

`corr.csv`

into `corr_i_v011.html`.

The file intentionally has no `sigma` column. CORR-I should therefore report the
descriptive relative-deviation compatibility envelope rather than a diagonal-error envelope.

## Reconstruction

Set C(0)=1 and use

C(n+1) = C(n) exp[-aM_eff(n+1/2)].

No smoothing, interpolation, plateau replacement, or removal of the large-t
statistical rise has been performed.

## Important status

This is a published-figure reconstruction, not raw lattice correlator data.
It is suitable for the first CORR-I pilot and chamber validation against real
published Yang-Mills information, but it must not be described as the authors'
original C(t) dataset.
