# CORR-I Gapless Family v0.0.1

This is the next CORR-I falsification control.

## Run these four files

Upload each separately to the unchanged `corr_i_v011.html`:

1. `p05.csv`
2. `p2.csv`
3. `p4.csv`
4. `p8.csv`

Do **not** rerun the previous `p=1` control; its result is already recorded.

## Family definition

For each p,

`C_p(t) = (1 + theta_p t)^(-p)`

with

`theta_p = exp(0.3474/p) - 1`.

This is the Laplace transform of the positive Gamma spectral density

`rho_p(E) = E^(p-1) exp(-E/theta_p) / (Gamma(p) theta_p^p)`

on `E >= 0`.

Therefore every member is genuinely **gapless**, while all are matched so that

`log[C(0)/C(1)] = 0.3474`

and all use the same `t/a = 0..10` window as the AT20 massive control.

## Why p=8 matters

As p increases, this gapless family becomes increasingly exponential-like on
the finite observation window. The p=8 case is therefore an intentionally hard
control: it remains exactly gapless, but it should move closer to the massive
CORR-I response.

## Preregistered expected contraction ratios

- p=0.5: 0.500947
- p=1.0: 0.326916  (already run)
- p=2.0: 0.178612
- p=4.0: 0.084534
- p=8.0: 0.037668

Massive plateau control reference:

- massive: 0.007688

The expected trend is progressive approach toward the massive response as p
increases, while all exact spectra remain gapless.

## Files

- `p05.csv`, `p2.csv`, `p4.csv`, `p8.csv` — chamber-ready inputs.
- matching `*_meff.csv` files — effective-mass trajectories.
- `EXPECTED.csv` / `EXPECTED.json` — preregistered chamber expectations.
- `metadata.json` — construction and interpretation.
- `build_family.py` — reproducible builder.
- `manifest.json` — SHA-256 manifest.
