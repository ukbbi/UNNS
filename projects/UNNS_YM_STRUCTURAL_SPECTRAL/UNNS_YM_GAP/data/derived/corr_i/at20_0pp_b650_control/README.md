# CORR-I AT20 0++ Plateau Control v0.0.1

This is the **second, controlled representation** of the AT20 beta=6.50
0++ ground state for CORR-I v0.1.1.

## Primary input

Upload:

`corr.csv`

to `corr_i_v011.html`.

It is an exact single-exponential control anchored to the paper's published
mass estimate:

`aM = 0.3474(22)`.

The construction is:

`C_control(t) = exp(-0.3474 t)`, with `C_control(0)=1`.

The time support is `t/a = 0..10`, intentionally matching the first
Figure-7 digitized proxy so the two chamber responses can be compared without
changing the support length.

## Why this is controlled

The paper reports a well-defined early 0++ effective-mass plateau and explicitly
describes the later rise as a statistical fluctuation. This representation
therefore removes the plotted fluctuations and holds the effective mass at the
published best estimate.

It is **not** the authors' raw correlator and must not be described as such.

## Uncertainty

The published mass uncertainty ±0.0022 is retained in `mass_band.csv` as a
fully correlated model band. It is deliberately not turned into a pointwise
`sigma` column, because doing that would falsely treat a fitted mass uncertainty
as independent correlator errors.

CORR-I should therefore remain in `RELATIVE_LIMITS_DESCRIPTIVE` mode.

## Files

- `corr.csv` — primary chamber-ready control.
- `meff.csv` — constant effective-mass representation.
- `mass_band.csv` — central and ±1σ mass-model curves.
- `compare_first_proxy.csv` — direct comparison with the first proxy, when available.
- `EXPECTED.json` — expected CORR-I v0.1.1 baseline/envelope values.
- `VERIFY.json` — construction checks.
- `build_control.py` — reproducible builder.
- `metadata.json` — provenance and interpretation boundary.
- `manifest.json` — SHA-256 manifest.

## Intended comparison

Compare this run against the first real-data proxy:

`0pp_b650_fig7_proxy`

The scientific question is not whether this ideal control passes positivity
(it should), but whether the near-zero compatibility-envelope behavior remains
qualitatively similar after the Figure-7 fluctuations are removed.
