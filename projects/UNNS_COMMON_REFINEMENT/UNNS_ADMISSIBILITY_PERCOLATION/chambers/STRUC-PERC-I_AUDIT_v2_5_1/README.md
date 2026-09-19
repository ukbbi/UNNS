# STRUC-PERC-I Audit/Repair v2.5.1

## Identity

This is a **separate derived audit instrument**.

It does not overwrite or replace the frozen parent chamber:

`../STRUC-PERC-I/struc_perc_i_v2_5_0.html`

Parent SHA-256:

`844b84e4f1d681a4363207974061bbee62fdc69904990a9387bdaa2bb8b71200`

Audit/repair chamber:

`struc_perc_i_audit_v2_5_1.html`

SHA-256:

`bc3daa66c3281f1e2679d5d42c153123b49e78b9bdfeb856d93eb18e4c1d5b7c`

## Scope

Exactly three logical changes are introduced.

### 1. Effective-zero IQR fallback

v2.5.0 used:

```text
IQR > 0 ? IQR : median
```

This allowed floating-point residue such as the `AFF04` IQR to act as the physical epsilon scale.

v2.5.1 uses the documented median fallback when:

```text
abs(IQR) / abs(median) <= 1e-12
```

or when IQR is nonpositive.

No nondegenerate IQR case is rescaled.

### 2. Plateau no longer terminates the extension before the exact threshold

v2.5.0 could stop at a temporary giant-component plateau even when the same finite full-pairwise graph would connect at a slightly larger kappa.

v2.5.1 still records the first plateau as a diagnostic marker, but it does not use that marker as an early stop before an eligible exact-connectivity probe.

### 3. Exact connectivity threshold

For sorted gap values `d_(1) <= ... <= d_(n)`, the full threshold graph is connected exactly when every adjacent sorted separation is within epsilon.

Therefore:

```text
kappa_connect_exact
=
max_i (d_(i+1) - d_(i)) / epsilon_scale
```

v2.5.1 computes this value in O(n log n) including the existing sort, displays it, and exports it.

For small/medium ladders the adaptive extension probes that threshold directly. The probe is capped at kappa = 1e6 for computational safety; thresholds beyond the cap are still reported but not force-tested.

## Preserved behavior

The following are unchanged:

- full pairwise gap graph definition;
- base kappa grid;
- four-tier base classification;
- strict no-reset chain logic;
- outlier analysis;
- hard-cap/downsampling policy;
- domain adapters;
- batch input parser;
- parent v2.5.0 raw outputs.

The v2.5.1 batch export adds both `base_verdict` and final `verdict`, plus scale/audit fields, so the effect of the repair remains visible.

## How to run the frozen project audit

Open:

`struc_perc_i_audit_v2_5_1.html`

Use **Batch Mode** with the same 30 files from:

`inputs/struc_perc_i/`

Do not alter the frozen corpus.

Export both new files:

```text
struc_perc_audit_v2_5_1_batch_results.csv
struc_perc_audit_v2_5_1_batch_results.json
```

Keep them separate from the original v2.5.0 raw batch.

## Preflight

`PREFLIGHT_30_CASES.csv` and `VALIDATION.json` record deterministic expectations from the frozen inputs before the browser rerun.

They are validation aids, not substitutes for the v2.5.1 exported batch record.
