# TC_P01_C001 v001 — Adapter Method

## Objective

Convert the uploaded 4T source archive into a neutral TIME-CRYSTAL-I v1.1.0
candidate bundle without changing the chamber or its frozen temporal metric.

## Adapter firewall

The adapter is allowed to:

- read JSON arrays;
- align identical cycle indices;
- stack independent same-observable runs as ensemble coordinates;
- preserve provenance and hashes.

The adapter is not allowed to:

- tell the temporal metric that the expected period is 4;
- align signs to a four-cycle template;
- smooth toward a desired recurrence;
- use a Fourier filter to construct the input;
- tune chamber thresholds;
- convert missing collective/spectral evidence into synthetic evidence.

## Primary coordinate construction

Eight recompilation-result IBM trajectories become:

`X_t = (Z_1(t), ..., Z_8(t))`

for t = 0,...,19.

The filename/device identity is retained only as coordinate provenance.

## Control construction

Seven no-recompilation trajectories are independently stacked into a separate
control bundle and passed through exactly the same chamber protocol.

## Ground truth

Ground truth is stored outside the candidate ZIP under:

`ground_truth/TC_P01_C001_GT.json`

It is not read by the blind run.
