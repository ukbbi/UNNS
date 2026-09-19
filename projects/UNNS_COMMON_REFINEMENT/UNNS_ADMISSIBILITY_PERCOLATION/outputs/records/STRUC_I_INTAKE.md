# STRUC-I Intake Record

## Status

**STRUC-I COMPLETE — RAW OUTPUT RETAINED — STRUC-PERC-I PENDING**

This is an intake/descriptive record only. It is **not** the final cross-chamber synthesis.

## Run validation

The retained STRUC-I output is internally consistent:

- chamber: STRUC-I v1.0.4;
- input: `ALL_SYSTEM_SPECTRA.csv`;
- 30 ladders;
- 128 levels per ladder;
- no subsampling;
- 40 kappa steps from 0.01 to 1.0;
- 2000 Monte Carlo runs;
- CSV profile count: 1200 rows = 30 x 40;
- JSON and CSV summary metrics agree to rounding precision.

No rerun of STRUC-I is required.

## Primary admissibility result

All 30 ladders were classified:

```text
Geometric Persistence
Stable Structure
```

and all 30 have:

```text
mean_Ak = 1.0
min_Ak  = 1.0
```

Therefore every frozen ladder is fully admissible across the tested STRUC-I scale range under the
chamber's perturbation criterion.

This result spans source systems with different exact algebraic route-closure properties.

The correct interpretation is:

> algebraic route closure and STRUC-I perturbative admissibility are distinct structural notions.

STRUC-I should not be described as a traceability classifier.

## Structural-pressure diagnostic

The secondary `rho` diagnostic varies even though `A_kappa` remains 1.

### Rank-one source families

`R1_FREE`:

- mean of ladder `mean_rho`: 0.017582
- median: 0.017579
- mean of `max_rho`: 0.248634

`R1_FAIL`:

- mean of ladder `mean_rho`: 0.017443
- median: 0.017459
- mean of `max_rho`: 0.245224

These rank-one values are practically coincident.

So the secondary STRUC-I pressure diagnostic does not recover the independent free/nonfree
algebraic distinction in this encoding.

### Affine source families

`AFF_FREE`:

- mean of ladder `mean_rho`: 0.096075
- median: 0.070981
- mean of `max_rho`: 0.311340

`AFF_FAIL`:

- mean of ladder `mean_rho`: 0.065531
- median: 0.058163
- mean of `max_rho`: 0.280980

The affine pressure diagnostic is heterogeneous rather than ordered by algebraic annotation.

For example, `AFF06` has:

```text
mean_rho = 0.253125
max_rho  = 0.462500
```

whereas `AFN05` and `AFN06` have:

```text
mean_rho = 0.013363
mean_rho = 0.013463
```

respectively.

Thus `rho` should not be interpreted as a monotone proxy for factor traceability.

## What the STRUC-I result establishes for this branch

At the frozen primary encoding:

1. all 30 ladders are perturbatively admissible;
2. all 30 remain in the same core STRUC-I regime/state;
3. secondary pressure varies, but not in a simple algebraic-label order.

The next scientific question is therefore not whether STRUC-I classifies traceability.

It is:

> How will the percolative connectivity structure of these already-admissible ladders compare with
> their STRUC-I result?

## Next step

Run STRUC-PERC-I v2.5.0 in **Batch Mode** on all 30 files in:

`inputs/struc_perc_i/`

Keep the frozen PRP controls unchanged.

After completion export both:

- `struc_perc_batch_results.csv`
- `struc_perc_batch_results.json`

Do not change the corpus, adapter, STRUC-I input, or completed STRUC-I raw output before the
cross-chamber comparison.
