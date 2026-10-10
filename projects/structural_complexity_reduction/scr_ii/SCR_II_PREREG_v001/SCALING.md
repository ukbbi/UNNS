# Scaling protocol

## Calibration

Depths: 8, 10, 12.  
Calibration may be used only to:

- verify nonempty solution sets;
- verify deterministic generation;
- estimate expected run time;
- calibrate N1 pruning probability by depth;
- detect implementation defects.

Calibration may not alter Γ_route or the frozen primary thresholds.

## Primary transfer

Depths: 14, 16, 18.

Ten primary seeds are frozen per depth.

## Exploratory scaling signal

After primary completion, fit median node expansions by depth.

Report `TRANSFER_WITH_SCALING_SIGNAL` only if:

- primary level 4 is already achieved;
- `Δα >= 0.05`;
- SCR node reduction does not decrease from d=14 to d=18 by more than 5 percentage points.

This label is empirical only and is not a complexity-class claim.
