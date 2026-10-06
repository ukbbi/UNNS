# BATTELLI_CTRL

Secondary unsmoothed structural control for `UNNS_VACUUM_CONTINUITY`.

Merge this package into the project root.

The admitted values are stored individually as:

```text
data/derived/battelli_2019/B1_POS.csv
data/derived/battelli_2019/B2_POS.csv
data/derived/battelli_2019/B3_POS.csv
```

For canonical STRUC-I v1.0.4, load instead:

```text
data/derived/battelli_2019/BATTELLI_STRUC_I.csv
```

This is only a parser-compatible grouped wrapper around the same three ladders; it changes no numerical value.

They exclude only `d_t=0`, because the Battelli source states that its missing logarithmic renormalization differs between `d_t=0` and `d_t>0`.

Run order:

1. Read `stage2/BATTELLI_CTRL_FREEZE.md`.
2. Optionally run `RUN_BATTELLI_EXTRACT.bat` to reproduce the included extraction from the local arXiv archive.
3. Run canonical STRUC-I v1.0.4 on `BATTELLI_STRUC_I.csv` (it loads B1/B2/B3 as three independent ladders).
4. Run canonical STRUC-PERC-I v2.5.0 Batch Mode on the same ladders.
5. Save exports in the prepared `output/battelli_ctrl/` folders and upload them.

Do not modify either canonical chamber.
