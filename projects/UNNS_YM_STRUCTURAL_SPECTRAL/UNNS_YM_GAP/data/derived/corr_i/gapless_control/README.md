# CORR-I Gapless Control v0.0.1

This is the next falsification experiment for CORR-I v0.1.1.

## Primary chamber input

Upload:

`corr.csv`

to the unchanged `corr_i_v011.html`.

Do not change the chamber defaults.

## Control definition

The control has a strictly positive spectral density

`rho(E) = (1/theta) exp(-E/theta), E >= 0`

with

`theta = 0.415382765261008`.

Its Euclidean correlator is exactly

`C(t) = 1 / (1 + theta t)`.

Because the spectral support extends all the way to `E=0`, this control has
**no positive mass gap**. Its long-time tail is power-law:

`C(t) ~ 1/(theta t)`,

and its effective mass tends to zero.

## Matching to the massive AT20 control

The control is not arbitrarily scaled. `theta` was chosen so that

`log[C(0)/C(1)] = 0.3474`,

matching the first-interval mass scale of the AT20 beta=6.50 0++ plateau
control. Both inputs use the same `t/a = 0..10` support and `C(0)=1`.

Thus the principal intentional difference is spectral character:

- massive control: `C(t)=exp(-0.3474 t)`
- gapless control: `C(t)=1/(1+theta t)`

## What should happen

The gapless baseline should remain positive-spectral consistent but should
**not** develop a constant effective-mass plateau.

Under CORR-I v0.1.1 defaults the expected near-zero compatibility envelope is
much less contractive than for the massive control.

Expected approximate values:

- gapless `alpha_max(mu/mref=1)` = 0.062298972
- gapless `alpha_max(mu/mref=1e-3)` = 0.020366537
- gapless contraction ratio = 0.32691611

For comparison, the already-run massive plateau control had a contraction
ratio about `0.00768765`.

The point of the experiment is to see whether the **actual frozen chamber run**
reproduces this qualitative separation.

## Files

- `corr.csv` — upload this.
- `meff.csv` — effective-mass trajectory.
- `EXPECTED.json` — preregistered expected chamber behavior.
- `VERIFY.json` — analytic/numerical construction checks.
- `metadata.json` — provenance and interpretation.
- `build_gapless.py` — reproducible input builder.
- `manifest.json` — SHA-256 manifest.

This is a synthetic control, not Yang-Mills data and not evidence by itself
for or against the Yang-Mills mass gap.
