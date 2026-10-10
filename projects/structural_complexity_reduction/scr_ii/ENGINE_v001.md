# SCR-II Engine v001

## Scope

This is the executable engine for the frozen `SCR_II_PREREG_v001` / `ROUTE_CSP_I` benchmark.

It implements:

- deterministic instance generation;
- exact exhaustive baseline enumeration;
- frozen G1→G4 structural pruning;
- exact solution-set equality checks;
- N1/N2/N3 controls;
- C1 solver-native arithmetic preprocessing;
- calibration-only N1 rate estimation;
- design-audit firewall checks;
- checkpointed/resumable primary execution.

## Scientific firewall

The structural filter receives a stripped structural view containing only:

- initial symbol and phase;
- per-option route symbol;
- per-option phase;
- per-option discontinuity marker;
- branch ID.

It cannot access checksum, cost, terminal seal, or exact-solution labels.

Unit tests mutate every arithmetic solution field and assert unchanged structural behavior.

## G3 note

The frozen preregistration specifies suffix reachability but does not define a restricted terminal structural subset. The engine therefore treats every structurally valid terminal state as accepting. G3 remains a grammar-reachability check and may be non-discriminating in v001. This is documented rather than silently inventing an additional acceptance rule.

## Before primary execution

Run:

1. `RUN_SCR_II_VALIDATE.bat`
2. `RUN_SCR_II_CALIBRATION.bat`
3. `RUN_SCR_II_AUDIT.bat`

or use `RUN_SCR_II_SETUP.bat`.

The primary runner refuses to start without frozen calibration and audit artifacts.

## Primary rerun protection

Once `output/primary/PRIMARY_RESULT_v001.json` exists, the engine refuses a second primary run.
