# SCR Gate Policy

## 1. Purpose

A structural gate is allowed to reduce the candidate space only after it satisfies the SCR admission rule.

## 2. Required gate record

Every active gate must have:

```text
gate_id
source_project
invariant
input representation
decision rule
thresholds
falsifier
expected signature
computational cost method
known scope
known failure modes
version
```

## 3. Independence

The gate must not use:

- reference solution labels;
- downstream solver success/failure;
- post-hoc benchmark outcome statistics;
- information unavailable at the point where pruning is claimed to occur.

## 4. Gate categories

### PRUNING
May remove candidates before the solver.

### DIAGNOSTIC
May be computed and correlated with outcomes but cannot remove candidates.

### CONTROL
Used to measure baseline or null behavior.

### AUDIT
Checks representation, provenance, refinement, or excluded-space integrity.

## 5. Initial SCR-I rule

No inherited UNNS chamber becomes a pruning gate merely because it exists.

A source chamber may be reused only if its invariant is meaningful for the selected benchmark and its implementation can be applied without changing its established meaning.

## 6. UPI

UPI is initially:

```text
category = DIAGNOSTIC
prunes = false
```

Its role is to test independent association with SCR rejection/survival.

## 7. STRUC-I / STRUC-PERC-I

These are candidate reusable instruments where ordered ladder representations are valid.

They must not be conflated:

- perturbative admissibility;
- percolative connectivity.

Their scale conventions and verdict meanings remain distinct.

## 8. Axis V gates

V-3 / V-4 / V-5 provide methodological precedents and may provide actual gates only where the benchmark state has the corresponding topology/spectrum/logical object.

Do not force a benchmark into an Axis V representation solely to obtain pruning.

## 9. Gate order

If multiple gates are active, evaluate and report:

- fixed canonical order;
- order-independent total survivor set if gates are pure predicates;
- marginal/unique reject counts;
- cost under alternate order when early termination changes runtime.

A computationally cheap gate may run first for performance only if this ordering is frozen and does not alter the logical survivor set.

## 10. Gate versioning

Changing any invariant, threshold, encoding, or decision rule requires a new gate/config version.

Bug fixes that change outputs also require a new version and a rerun of affected results.
