# YM1A-G1 — Next Stage

The physical branch and the adversarial/null families are now frozen.

The next task is to run the canonical `STRUC-I` chamber on:

1. the physical baseline (`epsilon=1`);
2. the primary common-offset gapless family;
3. the matched upward massive control;
4. the ratio-preserving scale null;
5. the gap-only null.

## Required material

Before building the G1 runner, the project needs the exact canonical `STRUC-I`
input contract and executable/script version currently used in the UNNS project.

`STRUC-I` itself must not be modified.

The G1 adapter should only:

- convert each five-coordinate row into the exact canonical ladder format;
- preserve `family`, `epsilon`, `k`, `level`, `beta`, and source identifiers;
- execute the chamber reproducibly;
- collect the existing chamber verdict and metrics;
- identify `k_i*` using the already frozen G0 rule;
- write a complete cross-refinement boundary record.

No chamber thresholds are to be fitted to the YM1A result.
