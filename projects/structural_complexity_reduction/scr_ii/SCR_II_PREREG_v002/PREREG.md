# SCR-II Preregistration v002

## Status

**FROZEN BEFORE ANY v002 PRIMARY SEED IS GENERATED OR SOLVED**

Project: Structural Complexity Reduction (SCR)  
Phase: SCR-II — solution-preserving computational transfer  
Benchmark: `ROUTE_CSP_I / v002`

## Reason for v002

v001 was closed before primary execution because all calibration and design-audit instances contained only one exact solution, derived from the planted structural backbone.

v002 removes that degeneracy.

## Central question

Can the unchanged frozen UNNS route-structural filter reduce search on unseen discrete instances while preserving a genuinely nontrivial exact solution set whose arithmetic definition is independent of structural-filter survival?

## Primary preservation rule

For every primary instance:

\[
S_{SCR}=S_{baseline}.
\]

Exact set equality is mandatory. One lost exact solution is a primary preservation failure.

## Independence constraints

The v002 generator must obey all of the following:

1. structural metadata are generated first from a structural RNG stream;
2. arithmetic cost/checksum fields are generated from a separate arithmetic RNG stream;
3. the arithmetic anchor bit string is generated independently of structural-filter survival;
4. arithmetic target selection may not inspect G1–G4 or any structural survivor set;
5. deterministic acceptance/rejection of a candidate instance may use only exact baseline solution count/density;
6. no primary seed may be used to tune the arithmetic family, multiplicity band, grammar, thresholds, or nulls.

## Multiplicity freeze

The exact solution-density acceptance band is frozen as:

\[
0.02 \le |S_{solution}|/2^d \le 0.04.
\]

This band was selected using new v002 calibration seeds only.

Arithmetic family:

- checksum modulus: `5`;
- branch costs: integers in `[1,1000]`;
- terminal seal: final branch bit;
- cost window centered on an arithmetic anchor route;
- cost half-width: `round(0.025 * d * 1000)`;
- maximum arithmetic attempts per structural skeleton: `64`.

A structural skeleton is generated once per seed. Only arithmetic fields/targets are resampled across attempts.

## Depths

Calibration depths: `8, 10, 12`.  
Primary transfer depths: `14, 16, 18`.

## Primary hypotheses

### H1 — Exact preservation
All v002 primary exact solutions survive structural filtering.

### H2 — Material node reduction
Median node-expansion reduction is at least 25% at each primary depth.

### H3 — Net computational gain
Median end-to-end time gain is at least 1.10× at depths 16 and 18, including filter overhead.

### H4 — Out-of-scale transfer
The structural grammar and arithmetic family are frozen before the depth-14/16/18 primary grid.

## Verdict hierarchy

1. `PRESERVATION_FAIL`
2. `NO_MATERIAL_REDUCTION`
3. `REDUCTION_WITHOUT_NET_GAIN`
4. `COMPUTATIONAL_TRANSFER_CONFIRMED`
5. `TRANSFER_WITH_SCALING_SIGNAL` (exploratory only)

## Design-audit rule

The v002 design audit may record solution preservation diagnostically, but **that diagnostic is not permitted to modify the frozen benchmark**.

A negative design-preservation diagnostic is not an implementation failure if:

- multiplicity is in-band;
- generation is deterministic;
- filter arithmetic blindness passes;
- exact baseline/native solver agreement passes.

This prevents iterative redesign until a positive outcome is obtained.
