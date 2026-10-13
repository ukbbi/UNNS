# PRD-1 Independent Verification

Standalone reproduction package for the ESC-I PRD-1 rule checks. This checker **does not import** `admissibility.py`, `esc_i.py`, or other ESC-I code.

## Requirements

- Windows 10/11 (for the `.bat` launcher), or any OS able to run Python.
- Python 3.9 or later (standard library only; no `pip install`).

## Run on Windows

1. Extract the ZIP into any local folder.
2. Double-click `RUN_VERIFY.bat` (or open Command Prompt in this folder and run `RUN_VERIFY.bat`).
3. Read the console summary and the newly created `RUN_RESULT.json`.

## Run on macOS / Linux / terminal

```sh
python3 independent_check_prd1.py
```

The checker writes `RUN_RESULT.json` **next to the script**, leaving the bundled historical result unchanged. A nonzero exit code indicates detected contradictions, linear-control mismatches, or a runtime failure.

## Expected outcome (seed 20261014)

- 2,400 cases: 400 each for dead-zone, clipping, lattice rounding, state-gating, and two linear controls.
- 1,525 nonlinear predictions checked; 75 nonlinear abstentions.
- 800 linear-control checks.
- 0 reported contradictions and 0 linear-control mismatches.

Compare the summary in `RUN_RESULT.json` with `INDEPENDENT_PRD1_RESULT.json`. The original `INDEPENDENT_PRD1_AUDIT.md` explains what was and was not established.

## Scientific scope

The checker uses exact rational arithmetic for 200-step nonlinear trajectories and separately checks closed-form linear controls. These runs are **falsification checks, not computer-verified proofs of all asymptotic claims**. It uses a distinct sample and seed rather than replaying all cases in the ESC-I main report. A second researcher re-running this script reproduces the same implementation; fully independent scientific verification also requires reviewing the mathematics or writing a separate checker.

## Included files

- `independent_check_prd1.py` — portable standalone implementation (output path adjusted for this package)
- `INDEPENDENT_PRD1_RESULT.json` — historical expected summary, unmodified
- `INDEPENDENT_PRD1_AUDIT.md` — historical audit, unmodified
- `RUN_VERIFY.bat` — Windows launcher
- `README.md` — these instructions
