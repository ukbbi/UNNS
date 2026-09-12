# TC_CLOSURE_v001

First exploratory UNNS temporal-closure stage for the discrete-time-crystal branch.

## What this stage asks

The physics layer has already been frozen and validated in `TC_PHYS_v001`.

`TC_CLOSURE_v001` now asks a different question:

**Do the physics-validated state trajectories organize themselves into a preferred temporal recurrence depth and a finite recurrence-family basin, without supplying the published DTC transition to the closure metric?**

## Required sibling layout

```text
Time_crystal\
│
├── TC_INGEST_v001\
├── TC_PHYS_v001\
├── TC_CLOSURE_v001\
├── Data.zip
├── DTC_qiskit.ipynb.zip
└── Realization of a discrete time crystal on 57 qubits of a quantum computer.pdf
```

Do not modify `TC_PHYS_v001` before this run.

## Run on Windows

Double-click:

`RUN_WINDOWS.bat`

or open Command Prompt in `TC_CLOSURE_v001` and run:

```bat
python run_closure.py ..\Data.zip ..\TC_PHYS_v001 outputs
```

The program refuses to run if the sibling physics layer does not report a PASS status.

## Core outputs

- `outputs/closure_spectrum.csv`
- `outputs/ladder_closure.csv`
- `outputs/closure_scan.csv`
- `outputs/control_comparison.csv`
- `outputs/basin_sensitivity.csv`
- `outputs/threshold_sensitivity.csv`
- `outputs/closure_result.json`
- `outputs/posthoc_comparison.json`
- `outputs/closure_spectrum.png`
- `outputs/closure_q0_scan.png`
- `outputs/closure_basin.png`
- `outputs/controls.png`
- `outputs/RUN_LOG.txt`

## Firewall

The primary closure result is written before the program reads the physical reference transition for comparison.

The closure metric:
- receives no DTC/thermal labels;
- receives no published epsilon_c;
- searches q=1..10;
- detects its fundamental recurrence q from the closure spectrum itself.

`posthoc_comparison.json` is deliberately separate.

## Status

This is **exploratory v001**, not a prospective preregistration. Its definitions are now explicit and reproducible. If the metric is retained, the strongest next test is to lock it unchanged and apply it to an independent DTC dataset.
