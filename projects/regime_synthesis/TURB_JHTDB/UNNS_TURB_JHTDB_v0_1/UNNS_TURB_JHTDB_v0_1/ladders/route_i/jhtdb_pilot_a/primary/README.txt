JHTDB PILOT A — PRIMARY ROUTE-DERIVED LADDERS
================================================

D_STITCH.csv
  Full source-object scale-time stitching-defect population.
  Selection: finite NODES.stitch_defect.

P_TIME.csv
  Temporal persistence on actual sources of eligible time relations.

P_SCALE.csv
  Scale persistence on actual sources of eligible scale relations.

All duplicates and full binary64 numerical content are preserved.
No normalization, rescaling, smoothing, jitter or deduplication is applied.

Run order:
  1. D_STITCH -> STRUC-I
  2. D_STITCH -> STRUC-PERC-I
  3. P_TIME   -> STRUC-I
  4. P_TIME   -> STRUC-PERC-I
  5. P_SCALE  -> STRUC-I
  6. P_SCALE  -> STRUC-PERC-I
