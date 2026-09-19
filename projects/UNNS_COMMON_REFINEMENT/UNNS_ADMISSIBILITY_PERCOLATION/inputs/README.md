# Chamber Inputs

These files are generated from the frozen corpus by `scripts/BUILD_LADDERS.py`.

## STRUC-I

Upload:

`struc_i/ALL_SYSTEM_SPECTRA.csv`

It contains `case_id,value` and is parsed by STRUC-I as one ladder per case.

## STRUC-PERC-I

Use batch mode on all CSV files in:

`struc_perc_i/`

Each file contains one `value` column and exactly 128 levels.

Do not edit these files after `outputs/records/FREEZE_RECORD.json` has been created.
