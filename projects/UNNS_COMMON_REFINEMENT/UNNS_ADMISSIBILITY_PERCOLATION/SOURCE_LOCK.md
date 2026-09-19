# SOURCE LOCK

## Current project identity

Project:

`UNNS_ADMISSIBILITY_PERCOLATION`

Former provisional identity:

`UNNS_TRACEABILITY_PHENOTYPE`

The rename is documented in `RENAME_RECORD.md`.

## Parent project

Repository: `ukbbi/UNNS`

Parent path:

`projects/UNNS_COMMON_REFINEMENT/`

Reference `main` commit:

`d7dcea26b39c2ddfe01d55f8d658d0a8503fb771`

Primary parent references:

- `README.md`
- `04_PROOF_MAP/output/FINAL_ROUTE_CLOSURE_SYNTHESIS.md`
- `outputs/reports/LEAN_ROUTE_CLOSURE_REPORT.md`
- `05_UNNS/definitions/ROUTE_TRACEABILITY_EQUIVALENCE.md`
- `02_NONREF/systems/RANK1_ROUTE_CLOSURE_THEOREM.md`
- `02_NONREF/systems/AFFINE_ROUTE_CLOSURE_THEOREM.md`
- `02_NONREF/systems/AFFINE_DEFECT_RAY_THEOREM.md`

The parent repository is reference material for this local branch.

## Frozen chambers

### STRUC-I v1.0.4

Role:

`Universal Ladder Admissibility`

Core quantity:

`A_kappa = fraction of perturbations satisfying inv <= nu(V)`

Native taxonomy:

- Geometric Persistence
- Structural Boundary
- Structural Instability

`rho` is a secondary structural-pressure analytic.

SHA256:

`df0919cd2c11d1e21c7d39ed200f2d5ffad7e0c0a6496bc21001ddd9267fa3ae`

### STRUC-PERC-I v2.5.0

Role:

`Full PRP Percolation Analyzer / Vulnerability Graph Engine`

Graph:

```text
vertices = gap values Delta_i

edge(i,j) exists when:
abs(Delta_i - Delta_j) <= epsilon

epsilon = kappa * IQR(Delta)
```

with median fallback when IQR is zero.

Native verdicts:

- FULL_PERCOLATION
- GIANT_COMPONENT_PERCOLATION
- TAIL_FRAGMENTATION
- HARD_FRAGMENTATION

The chamber marks the sufficient percolation-to-admissibility direction as an open conjecture.

SHA256:

`844b84e4f1d681a4363207974061bbee62fdc69904990a9387bdaa2bb8b71200`

Both chamber files remain immutable for this experiment.

## Derived audit instrument

STRUC-PERC-I Audit/Repair v2.5.1

Path:

`chambers/STRUC-PERC-I_AUDIT_v2_5_1/struc_perc_i_audit_v2_5_1.html`

Parent SHA-256:

`844b84e4f1d681a4363207974061bbee62fdc69904990a9387bdaa2bb8b71200`

Derived SHA-256:

`bc3daa66c3281f1e2679d5d42c153123b49e78b9bdfeb856d93eb18e4c1d5b7c`

This child instrument does not alter the frozen parent chamber.
