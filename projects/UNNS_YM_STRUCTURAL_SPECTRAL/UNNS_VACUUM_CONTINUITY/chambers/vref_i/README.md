# VREF-I/A Chamber

**Purpose:** refinement / continuum-scaling calibration for the frozen VREF-I representation.

**This chamber is not the Structural Vacuum Continuity test.**

## Inputs

The chamber expects the three admitted source tables at:

```text
data/raw/baker_2022/anc/
├── EX_NP_xl0.128_beta6.240.dat
├── EX_NP_xl0.128_beta6.544.dat
└── EX_NP_xl0.128_beta6.769.dat
```

Their SHA-256 hashes are frozen in `VREF_A_CONFIG.json`. A mismatch stops the run.

## Run on Windows

From the project root, double-click:

```text
RUN_VREF_A.bat
```

or run:

```bat
py -3 chambers\vref_i\vref_a.py --project-root .
```

Install dependencies if needed:

```bat
py -3 -m pip install -r chambers\vref_i\requirements.txt
```

## Validation-only mode

This verifies source hashes, column format, symmetry, ordering, and support without computing VREF metrics:

```bat
py -3 chambers\vref_i\vref_a.py --project-root . --validate-only
```

## Synthetic self-test

```bat
py -3 chambers\vref_i\vref_a.py --self-test
```

## Frozen outputs

```text
output/tables/VREF_A_GRID.csv
output/tables/VREF_A_PROFILE.csv
output/tables/VREF_A_WINDOWS.csv
output/tables/VREF_A_REFINEMENT.csv
output/tables/VREF_A_LOO.csv
output/reports/VREF_A_REPORT.md
output/reports/VREF_A_RUN.json
output/figures/VREF_A_PROFILE.png
output/figures/VREF_A_DISTANCE.png
```

## Possible verdicts

- `CALIBRATION-VALID`
- `CALIBRATION-SENSITIVE`
- `CALIBRATION-INVALID`

The chamber is explicitly prohibited from returning `CONTINUITY-SUPPORTED` or `ISOLATION-SUPPORTED`.
