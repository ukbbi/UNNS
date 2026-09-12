# Physical Window Label Template — Edited Draft Summary

This is a conservative first-pass edit of `tokamark_physical_window_label_template.csv`.

Rules used:

- Full-profile-edge shots: earliest D-alpha sharp change was marked as `LH_TRANSITION` with moderate confidence.
- Full-profile-edge shots: pre-transition baseline rows were added as `L_MODE` when a finite baseline existed.
- Full-profile-edge shots: quiet post-transition intervals before the next major physical marker were added as low-confidence `H_MODE_STABLE` candidates.
- Later physical marker windows were kept `AMBIGUOUS` and excluded until manual review.
- Control/stress-test shots `11768` and `11776` were marked `UNLABELABLE` because they lack critical independent diagnostics.

Label/exclusion counts:

| label_type | excluded_from_validation | count |
|---|---:|---:|
| AMBIGUOUS | True | 54 |
| H_MODE_STABLE | False | 5 |
| LH_TRANSITION | False | 6 |
| L_MODE | False | 6 |
| UNLABELABLE | True | 18 |

Per-shot label counts:

| shot_id | labels |
|---:|---|
| 11768 | UNLABELABLE: 10 |
| 11776 | UNLABELABLE: 8 |
| 11941 | AMBIGUOUS: 9, LH_TRANSITION: 1, L_MODE: 1 |
| 12007 | AMBIGUOUS: 9, H_MODE_STABLE: 1, LH_TRANSITION: 1, L_MODE: 1 |
| 12017 | AMBIGUOUS: 9, H_MODE_STABLE: 1, LH_TRANSITION: 1, L_MODE: 1 |
| 12046 | AMBIGUOUS: 9, H_MODE_STABLE: 1, LH_TRANSITION: 1, L_MODE: 1 |
| 12055 | AMBIGUOUS: 9, H_MODE_STABLE: 1, LH_TRANSITION: 1, L_MODE: 1 |
| 12063 | AMBIGUOUS: 9, H_MODE_STABLE: 1, LH_TRANSITION: 1, L_MODE: 1 |

Output:

`tokamark_physical_window_label_template_EDITED.csv`

Caution: this is a review draft, not definitive H-mode validation.