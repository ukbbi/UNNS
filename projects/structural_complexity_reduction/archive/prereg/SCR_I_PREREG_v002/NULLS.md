# Null and adversarial controls

- **Identity:** re-evaluate the target oracle on the unchanged pool; labels must match exactly.
- **Rate-matched random pruning:** retain the same N1 as SCR using deterministic control seeds; 100 replicates at N=10,000 and 30 at the other sizes.
- **Order-shuffled gate inputs:** independently permute gate-input fields across candidate IDs while preserving their marginal distributions; 30 replicates at N=10,000.
- **Gate-label permutation:** independently permute each frozen gate's boolean labels across candidate IDs and recompute the conjunction.

Nulls never redefine targets and never influence the primary gate thresholds.
