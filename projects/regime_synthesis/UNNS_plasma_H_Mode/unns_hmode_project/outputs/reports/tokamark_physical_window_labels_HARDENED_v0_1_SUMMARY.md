# TokaMark Physical Window Labels — HARDENED v0.1 Summary

This is a conservative hardened copy of `tokamark_physical_window_labels_HARDENING_REVIEW.csv`.

## Rule applied

- Accepted only `L_MODE` and `LH_TRANSITION` rows that were initially marked `ACCEPT`.
- Kept all `H_MODE_STABLE` rows excluded as `NEEDS_EXTERNAL_REFERENCE`.
- Kept all `AMBIGUOUS` rows excluded.
- Kept all `UNLABELABLE` rows excluded.
- Did not use `m_edge_conf` or any UNNS audit-only column to accept physical labels.

## Counts

- Rows: `89`
- Shots: `8`
- Eligible rows: `12`

### Label counts

| label_type | count |
|---|---:|
| AMBIGUOUS | 54 |
| UNLABELABLE | 18 |
| L_MODE | 6 |
| LH_TRANSITION | 6 |
| H_MODE_STABLE | 5 |

### Eligible label counts

| label_type | count |
|---|---:|
| L_MODE | 6 |
| LH_TRANSITION | 6 |

## Next command

```powershell
python components\tokamark_physical_window_label_analyzer.py ^
  --labels outputs\reports\tokamark_physical_window_labels_HARDENED_v0_1.csv ^
  --out-dir outputs\reports ^
  --prefix tokamark_physical_window_label_analysis_HARDENED_v0_1
```

## Expected consequence

Because `H_MODE_STABLE` remains excluded, this conservative hardened pass should weaken or fail the previous physical-window alignment gate unless stronger evidence is added later. That is acceptable and honest.