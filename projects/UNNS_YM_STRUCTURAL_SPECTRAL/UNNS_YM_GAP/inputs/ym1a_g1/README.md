# YM1A-G1 chamber-ready inputs

Every CSV contains exactly one header (`value`) and six ordered scalar values:

1. explicit vacuum node = 0
2. five positive YM1A spectral levels after the frozen G0.1 transformation

`baseline/` contains the eight physical measured ladders.
Each deformation family contains K01..K10 for all eight lattice levels.

The formal epsilon=0 endpoint is deliberately NOT included as a chamber input,
because it makes c1 degenerate with the vacuum. It remains recorded under
`nulls/ym1a_g01/g01_endpoint.csv`.

Use the canonical chamber defaults and do not modify the chamber HTML files.
