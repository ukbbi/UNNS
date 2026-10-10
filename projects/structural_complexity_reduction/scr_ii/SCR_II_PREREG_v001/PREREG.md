# SCR-II Preregistration v001

## Status

**FROZEN BEFORE PRIMARY EXECUTION**

Project: Structural Complexity Reduction (SCR)  
Phase: SCR-II — solution-preserving computational transfer  
Benchmark: `ROUTE_CSP_I`

## Primary question

Can the frozen UNNS route-structural grammar reduce search effort on unseen layered discrete problems while preserving the complete exact solution set and lowering total computational cost?

## Primary hypotheses

### H1 — Exact preservation
For every primary instance,

\[
S_{solution}^{SCR}=S_{solution}^{baseline}.
\]

One lost exact solution is a primary preservation failure.

### H2 — Material search reduction
At each primary depth `d ∈ {14,16,18}`, the median node-expansion reduction must be at least 25%.

### H3 — Net computational gain
At depths 16 and 18, median end-to-end gain

\[
G_{time}=T_{baseline}/T_{SCR}
\]

must be at least 1.10×, with all structural-filter overhead included.

### H4 — Out-of-scale transfer
The grammar is frozen using only calibration depths `{8,10,12}` and must not be changed before testing `{14,16,18}`.

## Primary outcome hierarchy

1. `PRESERVATION_FAIL` — any exact solution is lost on any primary instance.
2. `NO_MATERIAL_REDUCTION` — preservation passes, but H2 fails.
3. `REDUCTION_WITHOUT_NET_GAIN` — H1/H2 pass, H3 fails.
4. `COMPUTATIONAL_TRANSFER_CONFIRMED` — H1, H2, H3, H4 all pass.
5. `TRANSFER_WITH_SCALING_SIGNAL` — level 4 plus the exploratory scaling criterion in `SCALING.md`.

Null superiority is secondary and cannot rescue failure of H1–H4.

## Prohibited adaptations after freeze

After this preregistration is frozen, the following may not change based on calibration or primary outcomes:

- primary depths;
- primary seeds;
- Γ_route transition matrix;
- boundary rule;
- persistence rule;
- gate order;
- checksum modulus;
- downstream solution predicate;
- primary success thresholds;
- null definitions.

Implementation bugs may be repaired only if the scientific rule is unchanged and the repair is recorded.
