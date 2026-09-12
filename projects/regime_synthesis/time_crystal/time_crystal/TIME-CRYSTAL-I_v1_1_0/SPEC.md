# TIME-CRYSTAL-I v1.1.0 — Chamber Specification

## Chamber principle

**Temporal recurrence is necessary but not sufficient.**

Within the quantum many-body domain, TIME-CRYSTAL-I recognizes the following
hierarchy:

`temporal closure -> recurrence rigidity -> collective order -> many-body spectral breadth`

The chamber deliberately preserves the falsification history that led to this
architecture.

## Why the chamber has four sectors

### Temporal sector

Established by the frozen `TC_CLOSURE_v001` metric.

It identifies recurrence depth and temporal closure, but classical period-2 and
period-4 attractors prove that this sector is not DTC-specific.

### Rigidity sector

Captures persistence across perturbations and initial states.

`TC_RIGIDITY_v001` showed that recurrence rigidity is still not uniquely
time-crystalline: ideal classical two-cycles can equal or exceed MBL-DTC data on
trajectory-level rigidity axes.

### Collective sector

Requires many-site evidence such as finite-size pair order, correlation
spreading/localization, and broad initial-state behavior.

Pair order and localization are retained as meaningful physical structure, but
their explicit classical counterexamples prevent them from being treated as
standalone DTC identifiers.

### Spectral sector

Represents experimentally measured many-body eigenstate / quantum-typicality
breadth.

This is domain-specific. A classical periodic attractor has no directly
equivalent Hilbert-space typicality coordinate and must be marked `N/A`, not
assigned an artificial failure value.

## Verdict hierarchy

### NO_TEMPORAL_ORDER
Temporal recurrence is not supported.

### TEMPORAL_RECURRENCE
A recurrence family exists, but higher rigidity is not established.

### RIGID_RECURRENCE
Recurrence persists under state/perturbation variation, but no quantum
many-body claim is established.

### COLLECTIVE_TEMPORAL_ORDER
A quantum many-body system has temporal recurrence, rigidity, and collective
order, but the spectral/eigenstate sector is not fully supported.

### MANY_BODY_TIME_CRYSTAL_ADMISSIBLE
All four quantum many-body sectors are supported.

### INSUFFICIENT_DOMAIN_EVIDENCE
A quantum many-body candidate reaches the rigidity gate, but required
collective/spectral evidence has not been tested.

## Domain logic

A classical record is never rejected because a Hilbert-space quantity is `N/A`.

This is a central chamber rule, not a convenience.

## Frozen dependency

The chamber expects the temporal closure lineage to descend from:

`TC_CLOSURE_LOCK_v001`

Frozen metric SHA-256:

`06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553`

## Initial validation corpus

The v1.1.0 package validates the hierarchy against:

- Frey–Rachel 57-qubit DTC;
- Mi et al. MBL-DTC;
- Mi prethermal DTC-like control;
- Mi thermal control;
- exact classical period-2;
- classical logistic period-2;
- classical logistic period-4;
- damped transient period-2;
- classical chaos;
- IID random control.

The expected verdicts are encoded in `run_chamber.py` and asserted during the
build/run.
