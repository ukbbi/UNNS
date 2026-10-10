# Frozen run plan

1. Run `RUN_SETUP_V002.bat` and require source lock, prereg validation, adapter regression, and the design-audit certificate to pass.
2. Refresh the dashboard and verify every v002 readiness gate is green.
3. Run `RUN_SCR_I_A_v002.bat` once for the primary experiment. Resume checkpoints are allowed after interruption; scientific definitions are not.
4. Inspect all 15 cells, null controls, negative-space exports, and environment record.
5. Freeze the finalized primary JSON with its SHA-256 sidecar before any UPI analysis.

The v001 primary run remains blocked and is not part of v002 execution.
