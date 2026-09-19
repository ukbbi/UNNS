# STRUC-PERC-I Audit v2.5.1 Intake

## Status

**BROWSER RUN COMPLETE — 30 / 30 RESULTS RETAINED**

The v2.5.1 audit instrument was run on the same frozen 30 ladder files used by STRUC-PERC-I v2.5.0.

Raw files retained:

```text
outputs/struc_perc_i/audit_v2_5_1/STRUC_PERC_AUDIT_RESULTS.csv
outputs/struc_perc_i/audit_v2_5_1/STRUC_PERC_AUDIT_RESULTS.json
```

All 30 rows report:

```text
runStatus = COMPLETE
verdict   = FULL_PERCOLATION
```

The JSON and CSV exports agree to export-rounding precision.

## Interpretation boundary

The v2.5.1 result is an **eventual-connectivity audit**, not a new binary classifier.

For any finite gap-value set with a positive finite epsilon scale, the full pairwise threshold graph
must become connected once epsilon reaches the largest adjacent separation in the sorted gap-value
list.

v2.5.1 explicitly computes and probes that exact threshold.

Therefore the final `FULL_PERCOLATION` verdict is expected whenever the exact threshold is finite
and lies within the audit probe cap.

The informative output is primarily:

```text
kappa_connect_exact
```

together with the base-scale verdict and scale mode.

## Threshold span

Across the frozen corpus:

```text
minimum exact threshold = 0
maximum exact threshold = 15.073646 (AFF05)
```

The six `R1_FREE` ladders have:

```text
kappa_connect_exact = 0
```

Their reported `kappa_connect = 0.01` is simply the first tested kappa grid point.

The six `R1_FAIL` ladders have:

```text
kappa_connect_exact = 1
```

under the median fallback.

## Class-level exact connectivity scale

```text
R1_FREE median = 0.000000
R1_FAIL median = 1.000000

AFF_FREE median = 3.132993
AFF_FAIL median = 2.474745

INT_FREE median = 5.138617
```

There is no global monotone ordering by the algebraic `TRACEABLE` / `NON_TRACEABLE` annotation.

## Relation to v2.5.0

The v2.5.0 raw verdicts remain permanent evidence of the original finite/adaptive search policy.

The v2.5.1 exact-threshold audit answers a different question:

```text
v2.5.0:
what happens under its finite/adaptive search policy?

v2.5.1:
at what normalized scale must the finite full-pairwise gap graph connect?
```

Both records are retained.
