# High-Re Adapter / Scale-Ladder Stage v0.1

This stage implements the already frozen `jhtdb_high_re` protocol without changing the source selection or object grammar.

## Input

`data/raw/jhtdb/high_re/HIGH_RE_EXPORT/` containing the seven verified 256³ HDF5 velocity samples.

## Transformation

For each sample independently:

1. verify source identity and HDF5 structure;
2. apply exact block means at factors `[1,2,4,8,16]`;
3. calculate boundary-safe velocity-gradient fields;
4. segment `Q >= 1.5 RMS(Q)` with 26-connectivity;
5. remove small and retained-boundary-touching objects under the Pilot-A rule;
6. construct positive-overlap relations only across adjacent scale layers;
7. run canonical STRUC-ROUTE-I v0.1.2 with the frozen 100-null ensemble;
8. extract `P_SCALE` from actual source nodes of eligible scale edges;
9. preserve duplicates and write ascending binary64 values without normalization, jitter, smoothing, or rescaling.

No time edges are constructed. The six `isotropic8192` snapshots are independent samples.

## Endpoint of this stage

Seven byte-frozen `P_SCALE.csv` ladders are produced for independent interrogation by STRUC-I v1.0.4 and STRUC-PERC-I v2.5.0.
