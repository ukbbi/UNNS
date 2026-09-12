# TC_EXT_MI_v001

External validation of the frozen UNNS temporal-closure metric on the
independent Mi et al. time-crystal dataset.

## Required sibling layout

```text
Time_crystal\
│
├── TC_CLOSURE_LOCK_v001\
├── TC_EXT_MI_v001\
└── DTC_Data.zip
```

## Run on Windows

Double-click:

`RUN_WINDOWS.bat`

or run:

```bat
python run_validate.py ..\DTC_Data.zip ..\TC_CLOSURE_LOCK_v001 outputs
```

## Main outputs

- `outputs/external_validation.json`
- `outputs/external_summary.csv`
- `outputs/external_spectra.csv`
- `outputs/initial_state_pairwise.csv`
- `outputs/fig2d_closure_spectra.png`
- `outputs/fig3a_closure_spectra.png`
- `outputs/family_contrast_comparison.png`
- `outputs/initial_state_pairwise.png`
- `outputs/RUN_LOG.txt`

## Important

This package must not contain a modified copy of the closure metric.

The runner verifies the frozen metric SHA-256 before every analysis.
