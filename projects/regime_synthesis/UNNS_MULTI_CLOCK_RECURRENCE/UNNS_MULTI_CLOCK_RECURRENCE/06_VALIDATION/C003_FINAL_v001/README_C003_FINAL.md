# C003 FINAL v001

One-shot historical boundary evaluation under unchanged `MC_GRAMMAR_v001`.

Canonical ingest:
- `TC_P01_C003.csv` from Fig.1d
- `TC_P01_C003_CTRL.csv` from Fig.1b

Adapter:
- source workbook time is in tau1 units;
- documented tau2/tau1 = 1.618;
- x = time_tau1 / 1.618 (cycles of tau2);
- r = 1.618, so r*x is cycles of tau1.

No interpolation, filtering, sign alignment, or sub-window selection.

The original Phase-I workbook hash is recorded in `C003_FINAL_LOCK_v001.json`.
