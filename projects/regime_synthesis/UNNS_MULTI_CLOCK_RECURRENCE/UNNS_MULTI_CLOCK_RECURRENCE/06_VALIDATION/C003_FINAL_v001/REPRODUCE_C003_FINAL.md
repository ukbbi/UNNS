# C003_FINAL_v001 — Reproduction Guide Aligned to the Actual Project Tree

## Actual locations in this project

The uploaded project already contains every file needed for the **normal C003 reproduction**.

```text
UNNS_MULTI_CLOCK_RECURRENCE/
├── 05_METHODS/
│   ├── rep_study_v002.py
│   ├── rep_study_config_v002.json
│   ├── grammar_dev_v001.py
│   ├── grammar_dev_config_v001.json
│   └── mc_grammar_v001.py
│
├── 06_VALIDATION/
│   └── C003_FINAL_v001/
│       ├── C003_FINAL_LOCK_v001.json
│       ├── C003_FINAL_LOCK_SHA256.txt
│       ├── INGEST/
│       │   ├── TC_P01_C003.csv
│       │   └── TC_P01_C003_CTRL.csv
│       ├── run_C003_final.py
│       └── verify_C003_final.py
│
└── 08_OUTPUTS/
    └── C003_FINAL_v001/
        ├── C003_FINAL_QUANT_SHA256.txt
        ├── C003_FINAL_RESULTS.csv
        ├── C003_FINAL_RESULTS.json
        ├── TC_P01_C003_DETAIL.json
        └── TC_P01_C003_CTRL_DETAIL.json
```

The historical Phase-I `rawdata.xls` is **not stored in this project tree**.

Therefore source-workbook regeneration is optional and separate.

---

## Normal reproduction — no external files required

You do **not** need to navigate to the project root first.

The scripts determine the project root automatically from their own location.

From anywhere, run:

```bat
python "D:\...\UNNS_MULTI_CLOCK_RECURRENCE\06_VALIDATION\C003_FINAL_v001\run_C003_final.py"
```

or simply double-click/open a terminal in `C003_FINAL_v001` and run:

```bat
python run_C003_final.py
```

The script reads the actual files at:

```text
05_METHODS/
06_VALIDATION/C003_FINAL_v001/INGEST/
```

and writes only to:

```text
08_OUTPUTS/C003_FINAL_v001/REPRO/
```

The historical one-shot result is never overwritten.

---

## Verify the reproduction

Then run:

```bat
python verify_C003_final.py
```

This automatically reads:

```text
08_OUTPUTS/C003_FINAL_v001/C003_FINAL_QUANT_SHA256.txt
```

and compares it with:

```text
08_OUTPUTS/C003_FINAL_v001/REPRO/
```

A successful reproduction ends with:

```text
PASS: regenerated C003 artifacts match the historical one-shot quantitative lock.
```

---

## Optional source-workbook verification

The project already contains the canonical ingest CSVs, so this is **not required** to
reproduce the frozen grammar result.

If you still have the original Phase-I `rawdata.xls` somewhere outside this project, run:

```bat
python build_C003_ingest.py --source "D:\path\to\rawdata.xls"
```

That script writes only to:

```text
06_VALIDATION/C003_FINAL_v001/REPRO_INGEST/
```

and checks the regenerated source extraction against the locked canonical ingest.

For old `.xls` support, Python may require:

```bat
pip install xlrd
```

Do **not** move `rawdata.xls` into this project merely to satisfy the reproduction script.
It is historical Phase-I source material, whereas this project already contains the locked
canonical C003 ingest.

---

## Expected result

```text
TC_P01_C003
  P_src p      = 1.00
  J_frac       = +0.910688
  M_frac       = +0.596092
  Fourier p    = 0.02
  robust M min = +0.595093
  state        = SOURCE_UNANCHORED

TC_P01_C003_CTRL
  P_src p      = 0.01
  J_frac       = -0.593846
  M_frac       = -0.003958
  Fourier p    = 0.78
  robust M min = -0.558942
  state        = MIXED_ORGANIZATION_WEAK
```

Formal frozen outcome:

```text
C003_REMAINS_OUTSIDE_FROZEN_MULTI_CLOCK_GRAMMAR
```

---

## What must not be changed

Reproduction requires the existing project files exactly as stored:

- `05_METHODS/rep_study_v002.py`
- `05_METHODS/grammar_dev_v001.py`
- `05_METHODS/mc_grammar_v001.py`
- canonical C003 ingest CSVs
- `tau2/tau1 = 1.618`
- all frozen null, threshold and robustness settings

Any altered method or input creates a new experiment, not a reproduction of
`C003_FINAL_v001`.
