# VREF-I/B Chamber

Primary Structural Vacuum Accessibility test using the frozen `CEA_2017_SU3` extraction.

## Prerequisites

The deterministic extraction must already have produced:

```text
data/derived/cea_2017/CEA17_VREF_B_POINTS.csv
data/derived/cea_2017/CEA17_VREF_B_EXTRACT.json
```

Install the additional fitting dependency once:

```text
INSTALL_VREF_B_DEPS.bat
```

## Validation without scientific fitting

```bat
py -3.12 chambers\vref_i\vref_b.py --project-root . --validate-only
```

## Run

Double-click:

```text
RUN_VREF_B.bat
```

## Outputs

```text
output/tables/VREF_B_COMMON.csv
output/tables/VREF_B_WINDOWS.csv
output/tables/VREF_B_FITS.csv
output/tables/VREF_B_REFINEMENT.csv
output/reports/VREF_B_REPORT.md
output/reports/VREF_B_RUN.json
output/figures/VREF_B_PROFILE.png
output/figures/VREF_B_DISTANCE.png
```

The chamber implements the already frozen `PREREG_VREF_B.md` plus `VREF_B_BUILD_FREEZE.md`. It must not be retuned after execution.
