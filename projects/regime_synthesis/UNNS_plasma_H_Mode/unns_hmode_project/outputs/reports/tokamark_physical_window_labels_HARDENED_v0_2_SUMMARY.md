# HARDENED v0.2 H-Mode-Stable Evidence Recovery Summary

## Rule used

Accept `H_MODE_STABLE` only when all of the following are true:

```text
H_evidence_score >= 7
at least three internal physical evidence families score 2
profile evidence score >= 2
power/density context score >= 2
```

No UNNS audit columns were used for label acceptance. Because no external reference was supplied, accepted windows are `2_SUPPORTED`, not `3_EXTERNALLY_ANCHORED`.

## Accepted H_MODE_STABLE windows

```text
12007_MANUAL_H_MODE_STABLE_001
12017_MANUAL_H_MODE_STABLE_001
12046_MANUAL_H_MODE_STABLE_001
12055_MANUAL_H_MODE_STABLE_001
12063_MANUAL_H_MODE_STABLE_001
```

## Counts

```text
review candidates: 5
accepted H_MODE_STABLE: 5
updated label rows: 5
eligible rows in v0.2: 17
eligible label counts: {'L_MODE': 6, 'LH_TRANSITION': 6, 'H_MODE_STABLE': 5}
```

## Next command

```powershell
python components\tokamark_physical_window_label_analyzer.py --labels outputs\reports\tokamark_physical_window_labels_HARDENED_v0_2.csv --out-dir outputs\reports --prefix tokamark_physical_window_label_analysis_HARDENED_v0_2
```

## Interpretation caution

This restores five `H_MODE_STABLE` windows based on internal physical diagnostic evidence. It is stronger than v0.1 but still not externally anchored. The next analyzer run must determine whether the H-vs-L alignment returns under v0.2 labels.
