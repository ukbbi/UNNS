# HIGH-RE CHAMBER EXECUTION PROTOCOL v0.1

Status: frozen before STRUC-I / STRUC-PERC-I high-Re chamber results are observed.

## Source identity

Source bundle: `HIGH_RE_SCALE_LADDERS.zip`

SHA-256:
`2f33fca62b35683272d0c4f822be36973475c085618b42f15d7d2efdd7462415`

All ladder files rebuilt here are byte-identical copies of the frozen `P_SCALE.csv`
populations. Files are renamed only so several samples can be selected conveniently
in the browser chamber interfaces.

No jitter, smoothing, normalization, rescaling, value editing, deduplication, or
multiplicity editing is applied by the rebuild step.

## STRUC-I v1.0.4

Primary group:
- i8192_s00
- i8192_s01
- i8192_s02
- i8192_s03
- i8192_s04
- i32768_s00

Contrast:
- i8192_s05

Run each ladder under the same chamber settings used for Pilot A:
- generic single-column numeric CSV
- kappa min = 0.01
- kappa max = 1.0
- kappa steps = 40
- Monte Carlo primary = 2000

For Pilot-A parity, preserve a 10,000-MC precision validation run with the same
settings. Do not change the ladder or kappa grid between primary and precision runs.

Interpret the chamber-defined regime/state. The preregistered high-Re endpoint is
based on recurrence versus shift of the Pilot-A `P_SCALE` STRUC-I regime, not on
tuning mean A_kappa.

## STRUC-PERC-I v2.5.0

Use the canonical generic adapter with no modification.

The frozen `P_SCALE` populations are intentionally quantized (3 or 4 distinct
values). The canonical generic adapter may therefore reduce them to a very
low-dimensional support. This is not an error and must not be repaired by jittering
or altering duplicate values.

STRUC-PERC-I is secondary/descriptive for this quantized coordinate. STRUC-I is the
cross-chamber regime test used for the registered recurrence/stabilization
interpretation.

## Decision discipline

Do not change:
- the `P_SCALE` population;
- duplicate multiplicities before STRUC-I;
- chamber kappa ranges/steps;
- MC counts after seeing a favorable or unfavorable outcome;
- STRUC-PERC-I's canonical generic adapter.
