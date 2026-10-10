# Frozen SCR-I-A Gate Set

## Source role

SCR-I-A does not invent new gates. It reuses the P3/P4 gate family as a frozen upstream filter.

## G1 — Geometric curvature consistency

Primary predicate:

```text
curvature_method == "turning_angle"
```

No relaxation is used in the primary SCR-I-A filter.

## G2 — Baseline separability

Primary predicate:

```text
delta_kappa > 0.05
```

## G3 — Bifurcation capability, P4 baseline soft band

Primary predicate:

```text
if has_bifurcation is false:
    FAIL
else if sharpness >= 0.10:
    PASS only if temporal_signature_valid is true
else if sharpness < 0.08:
    FAIL
else:
    PASS only if temporal_quality >= 0.70
```

## G4 — Locality consistency

Primary predicate:

```text
locality_score < 0.10
```

## Conjunction

```text
PASS_SCR = G1 AND G2 AND G3 AND G4
```

## Early termination

Primary gate order:

```text
G1 → G2 → G3 → G4
```

A candidate is rejected as soon as the first active gate fails. For scientific auditing, all four gate verdicts should also be computed in a separate non-timed audit pass so gate overlap can be reconstructed without contaminating timed early-termination cost.

## No target leakage

The filter may consume only candidate structural fields required by G1–G4. It must not consume:

- baseline/Mode-C target label;
- downstream regime label;
- downstream coverage result;
- downstream final utility/emergence label.

If leakage occurs, the run is invalid.

## Gate provenance

Thresholds correspond to the P4 baseline gate profile pinned in `SOURCE_LOCK.md`.
