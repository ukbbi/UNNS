# TC_CTRL_v001

Ordinary/classical period-doubling challenge for the frozen UNNS temporal-closure metric.

## Required layout

Either place the extracted lock beside this package:

```text
Time_crystal\
├── TC_CLOSURE_LOCK_v001\
└── TC_CTRL_v001\
```

or keep the lock as a ZIP:

```text
Time_crystal\
├── TC_CLOSURE_LOCK_v001.zip
└── TC_CTRL_v001\
```

## Run on Windows

Double-click:

`RUN_WINDOWS.bat`

The BAT file accepts either the extracted lock folder or the lock ZIP.

Manual commands:

```bat
python run_controls.py ..\TC_CLOSURE_LOCK_v001 outputs
```

or:

```bat
python run_controls.py ..\TC_CLOSURE_LOCK_v001.zip outputs
```

## Expected primary result

`PASS_CONTROL_CHALLENGE`

The important scientific outcome is expected to be **negative for uniqueness**:

ordinary classical period-doubled dynamics should also produce strong q=2
temporal closure.

That is the point of this challenge.

## Outputs

- `outputs/control_summary.csv`
- `outputs/control_spectra.csv`
- `outputs/noise_sweep.csv`
- `outputs/damping_sweep.csv`
- `outputs/damping_shuffle.csv`
- `outputs/logistic_sweep.csv`
- `outputs/control_validation.json`
- `outputs/control_spectra.png`
- `outputs/noise_sweep.png`
- `outputs/damping_sweep.png`
- `outputs/logistic_q_scan.png`
- `outputs/RUN_LOG.txt`

See `METHOD.md` and `RESULT_SUMMARY.md`.
