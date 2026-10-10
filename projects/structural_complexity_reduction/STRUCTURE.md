# Canonical Project Structure

```text
structural_complexity_reduction/
├── README.md
├── CTX_SCR.md
├── STRUCTURE.md
├── MANIFEST.md
├── CHANGELOG.md
├── SHA256SUMS.txt
├── RUN_DASHBOARD.bat
├── RUN_VALIDATE_V003.bat
├── RUN_SETUP_V003.bat
├── RUN_SCR_I_A_v003.bat
│
├── SCR_I_PREREG_v003/          # active frozen preregistration
├── archive/
│   ├── prereg/                 # frozen v001/v002 preregistrations
│   └── history/                # decisive v001/v002 transition evidence
├── adapters/                   # active v003 benchmark adapter
├── dashboard/                  # v003 local dashboard
├── docs/                       # current scientific/methodological docs
├── inputs/                     # reserved for future external benchmark inputs
├── references/
│   ├── source_lock/            # only v003 pinned sources
│   └── upi/                    # blinded secondary diagnostic reference
├── scripts/                    # active v003 setup/regression/runner scripts
├── src/
│   ├── scr_i_v003/             # canonical SCR-I-A v003 engine
│   └── diagnostics/            # secondary diagnostics; non-pruning
├── tests/                      # active v003 + UPI tests
└── output/
    ├── PRIMARY_RESULT_v003.json
    ├── gate_audit_v003.csv
    ├── null_results_v003.csv
    ├── timing_trials_v003.csv
    ├── RUN_ENVIRONMENT_v003.json
    ├── RUN_PROGRESS_v003.json
    ├── PRE_FLIGHT_v003.json
    ├── SUMMARY_v003.md
    ├── checkpoints/
    ├── v003_phase1/
    ├── reports/v003/
    └── exports/v003/
```

## Status rule

`SCR_I_PREREG_v003/` and the completed `output/` primary record are frozen. Historical v001/v002 material is preserved only under `archive/` and is not part of the active execution path.
