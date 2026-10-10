# UPI Blinded Secondary Diagnostic

## Role

UPI is not part of the SCR-I-A pruning rule.

The original UPI formulation treats UPI as a diagnostic of recursive/paradox-prone instability rather than proof of inadmissibility. SCR-I-A preserves that status.

## Freeze rule

For every primary pool:

1. complete baseline target evaluation;
2. complete SCR filtering and downstream evaluation;
3. finalize and hash the primary result JSON;
4. only then compute or join UPI diagnostics.

## Allowed secondary analyses

- UPI distribution among survivors vs rejects;
- `P(reject | UPI band)`;
- `P(target | UPI band)`;
- association between UPI and first reject gate;
- association between UPI and downstream evaluation cost;
- multivariate diagnostic analysis controlling for generator mode.

## Forbidden in SCR-I-A

UPI may not:

- reject candidates;
- alter gate thresholds;
- alter gate order;
- define a target;
- select seeds;
- determine stopping;
- enter the primary verdict.

If a strong association is found, UPI-based pruning requires a separately preregistered later experiment.
