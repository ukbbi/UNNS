# TEL-FINGERPRINT-I Chamber v0.1.0

**Teleportation Route Identity, Closure, and Bifurcation Chamber**

This is a new chamber built from the transferable *fingerprint* concept of GAL-FINGERPRINT-I. It does not modify, overlay, or depend on the galaxy chamber.

## Registered scientific question for this prototype

> Do four correction-conditioned teleportation routes form one reproducible structural fingerprint class over a physically ordered perturbation axis, and if so, where does that class deform, bifurcate, or fragment?

The chamber consumes branch-resolved, physically defined quantum-process invariants. It does **not** accept arbitrary flattened density matrices, detector timestamps, or generic numeric ladders.

## Start

Double-click:

```text
RUN_TEL_FINGERPRINT_I_CHAMBER.bat
```

or open directly:

```text
TEL_FINGERPRINT_I_CHAMBER_v0_1_0.html
```

No server, package installation, or internet connection is required.

## Input

One CSV file in the long schema documented in `INPUT_SCHEMA.md`.

Each `(scenario_id, realization_id, lambda, correction_status, control_type)` group must contain exactly these four routes:

```text
PHI_PLUS
PHI_MINUS
PSI_PLUS
PSI_MINUS
```

The physical perturbation coordinate `lambda` supplies the only ordering. Route labels are never converted to numbers and never determine distance geometry.

## Canonical defect fingerprint

For each branch and perturbation level, the chamber constructs a bounded defect vector from:

```text
branch-probability imbalance
terminal closure defect
process infidelity
normalized Choi mixing
normalized Choi entropy
Choi-entanglement loss
three PTM contraction defects
nonunital displacement
```

All coordinates have frozen physical transformations in `ENGINE_LOCK.json`.

## Core outputs

- route-pair distances at every perturbation level;
- route-class diameter and mean pair distance;
- class topology: `4`, `3+1`, `2+2`, `2+1+1`, or `1+1+1+1`;
- first deformation and first bifurcation coordinates;
- persistence depth and diameter integral;
- leave-one-realization-out scenario retrieval when the corpus supports it;
- route-label permutation invariance;
- deterministic perturbation-grid thinning stability;
- leave-one-coordinate-out sensitivity;
- JSON and CSV exports.

## Bounded verdict language

```text
ROUTE_CLASS_CLOSED
ROUTE_CLASS_PERSISTENT
ROUTE_CLASS_BIFURCATED
ROUTE_CLASS_FRAGMENTED
INITIAL_CLOSURE_NOT_ESTABLISHED
MIXED_REALIZATION_RESPONSE
INSUFFICIENT_EVIDENCE
INVALID_INPUT
```

These are operational fingerprint verdicts under frozen thresholds. They are not claims of teleportation fidelity, quantum advantage, or a universal physical transition.

## Boundary

This chamber analyzes already derived invariants. It does not derive Choi matrices from experimental counts and does not simulate a teleportation protocol. Those are separate source-reconstruction/theory modules whose outputs must satisfy this chamber's schema.

## Provenance

The design deliberately carries over the strongest GAL-FINGERPRINT-I ideas: full-trajectory fingerprints, within-versus-between identity, leave-one-repeat-out retrieval, deterministic perturbation controls, frozen metrics, explicit stop rules, and preserved exports. The galaxy chamber itself remains unchanged.