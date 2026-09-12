# TC_INGEST_v001

Validated ingestion layer for the Frey-Rachel 57-qubit discrete-time-crystal data.

## What is established from the supplied files

- `Data.zip` contains 84 binary `.dat` experiment files (Mac metadata excluded).
- Every `.dat` file is exactly 58,140 bytes = 14,535 float32 values.
- The supplied `DTC_qiskit.ipynb` writes `magarray.astype('float32').tofile(...)`.
- Notebook loop order gives the binary shape `5 x 51 x 57` = iteration x Floquet timestep x qubit.
- Iteration 0 is generated at epsilon=0 as a reference run; iterations 1-4 are the requested finite-epsilon runs.
- Filename epsilon codes span 30 values from 0.00 to 1.00.
- The archive contains Brooklyn and Manhattan device runs plus explicitly tagged polarized, Neel, no-disorder and reference-disorder controls.

## Run

```bat
python run_ingest.py Data outputs
python run_benchmark.py Data outputs
```

`Data` should be the extracted folder containing the `.dat` files.

## Outputs

- `manifest.csv` - one row per binary file with decoded metadata and integrity checks.
- `validation.json` - ingestion validation verdict and archive summary.
- `benchmark.csv` - raw physics/recurrence diagnostics per file.
- `phase_scan.csv` - median raw diagnostics by epsilon for standard/unflagged runs.
- `representative_traces.csv` - representative epsilon=0.05 / epsilon=0.5 traces and controls.
- `physics_gate.json` - deliberately limited raw-data sanity gate.
- `fig2_proxy.png` - raw DTC-like versus thermal trace comparison.
- `phase_proxy.png` - raw half-frequency amplitude across epsilon.

## Important boundary

This package does **not** yet claim an exact reproduction of the paper's fully error-mitigated Fig. 2b / Fig. 3 analysis. The supplied notebook contains experiment-generation and raw-data writing code, but not the full plotting/error-mitigation analysis pipeline. The paper describes an empirical measurement correction, reference-run depolarization fit, thresholds, and qubit filtering. That methods-faithful reconstruction is the next validation layer and should be completed before any UNNS chamber is allowed to classify the data.

The `D1_raw`, `D2_raw` and `D2_over_D1_raw` columns are preparatory recurrence diagnostics only. They are **not** a UNNS time-crystal verdict.
