# SCR-I Falsification Rules

The benchmark-specific preservation unit must be frozen before primary execution.

For SCR-I-A v003, primary structural preservation fails when any frozen basin/class requirement fails: basin recall <1, too few target survivors in a basin, geometric coverage <0.95, centroid drift >0.125, excessive unclustered target fraction, or incomplete adequately populated phenotype-stratum recall.

Candidate-level target identity loss alone does **not** falsify v003 because candidate identity is not the frozen preservation unit.

Computational-gain claims fail if filter cost cancels downstream saving. Structural-specificity claims fail if matched controls perform equivalently on the claimed distinguishing metric.

Observed v003 outcome:

- N=2,500: `REPRESENTATION_LOSS` in 5/5 cells;
- N=10,000: `STRUCTURAL_COMPRESSION_PRESERVED` in 5/5;
- N=40,000: `STRUCTURAL_COMPRESSION_PRESERVED` in 5/5.

The scale threshold is retained as part of the result, not tuned away.
