# TC_PHYS_v001

Physics-validation stage for the UNNS time-crystal branch.

This package reconstructs the Frey–Rachel 57-qubit discrete-time-crystal analysis from the supplied raw `.dat` corpus before any UNNS temporal-closure metric is introduced.

## Purpose

The package has one job:

`raw experimental data -> published-physics reconstruction -> physics gate`

It does **not** calculate UNNS closure, admissibility, STRUC-I, or STRUC-PERC-I quantities.

## Input

Use the supplied `Data.zip` directly. The program also accepts an extracted directory containing the `.dat` files.

Each data record is decoded as:

`[5 iterations, 51 Floquet timesteps, 57 qubits]`

Iteration 0 is the epsilon=0 reference run. Iterations 1–4 are the finite-epsilon target runs.

## Run on Windows

Put `Data.zip` beside this folder, then double-click:

`RUN_WINDOWS.bat`

Or from Command Prompt:

`python run_phys.py Data.zip outputs`

## Main outputs

- `outputs/fig2_reproduction.png`
- `outputs/transition_variance.png`
- `outputs/transition_decay.png`
- `outputs/file_metrics.csv`
- `outputs/epsilon_scan.csv`
- `outputs/qubit_filter.csv`
- `outputs/mitigation_sensitivity.csv`
- `outputs/representative_traces.csv`
- `outputs/physics_validation.json`
- `outputs/RUN_LOG.txt`

## Default published thresholds

- `W0 = 0.15`
- `Wf / W0 = 2/3`

The code also runs a small threshold-sensitivity grid.

## Important methodological status

The supplied Qiskit notebook contains circuit generation/execution and binary data writing, but not the separate complete figure-analysis/error-mitigation program. Therefore this package is a transparent reconstruction from the paper's Methods equations and stated thresholds, not a byte-identical recreation of unpublished code.

See `METHOD.md` for every operational choice.
