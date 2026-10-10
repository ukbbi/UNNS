# Frozen target oracle — Chamber LIII viability

The v002 target is the pinned Chamber LIII v3.1.0 `simulateLIIProtocol(mechanism, replicates)` followed by `isEmpiricallyViable` with 20 replicates and pass-rate threshold 0.85.

For each candidate, six boolean checks are evaluated:

1. `regimeStability >= 0.95` under the source's replicate rules;
2. `delta_kappa < 0.5`;
3. `kappa > 0`;
4. `locality_score < 0.20` (the viability bound, deliberately looser than G4's 0.10);
5. `temporal_signature_valid OR NOT has_bifurcation`;
6. `gammaCritStd < 0.15 OR no gammaCrit samples`.

The source pass rate is the fraction of these six checks that pass. Since 5/6 = 0.8333… < 0.85, a target-positive candidate must pass **all six checks**.

### Exact deterministic treatment of the gamma-critical check

When a candidate has a bifurcation, the source generates each gamma-critical replicate as `0.5 + noise` with `noise ∈ [-0.05, 0.05)`. Any finite sample drawn from an interval of width 0.1 has population standard deviation at most 0.05, which is strictly below the source threshold 0.15. Therefore `gamma_crit_consistent` is mathematically guaranteed true for this source implementation. v002 does not consume an unseeded RNG for a check whose outcome cannot change; it records the check as true and preserves source-equivalent classification.

### Independence from the SCR filter

The target is not G1, G2, G3, or G4 and does not require their conjunction. In particular, the viability locality bound is 0.20 whereas G4 is 0.10, and viability permits non-bifurcating mechanisms that G3 rejects. This deliberate non-equivalence makes exact target preservation a genuine falsifiable requirement.
