# UNNS Common Refinement

**Research title:** Common Refinement and Structural Route Closure in the UNNS Substrate

## Central question
Under what structural conditions does equality of endpoints force the existence of a common deeper admissible route?

## Current state
Phase 1 is implemented and frozen for the positive-integer control regime.

Pipeline:

`ab = cd`  
→ `REF-I exact witness`  
→ `canonical prime-valuation ladder encoding`  
→ `STRUC-I / STRUC-PERC-I secondary diagnostics`

See:
- `01_INTEGER/theory/PHASE1_PROTOCOL.md`
- `outputs/reports/PHASE1_REPORT.md`
- `outputs/records/PHASE1_RESULT.json`

## Quick test
`python chambers/REF-I/REF_I.py 6 10 12 5`


## Phase 2 — exact non-refinement controls

Implemented in `02_NONREF/`.

Flagship:
`H=<2,3>`, with `2+4=3+3`, has `D_R=1`.
All ambient refinement witnesses require the missing exponent `1`.

See:
- `02_NONREF/systems/PHASE2_PROTOCOL.md`
- `02_NONREF/systems/NONREF_THEORY.md`
- `02_NONREF/output/counterexamples.csv`
- `outputs/reports/PHASE2_REPORT.md`


## Rank-One Route Closure theorem

The `02_NONREF` stage has now produced an exact classification for additive submonoids of `N0`:

`global common refinement ⇔ min_positive = gcd(H)`.

See `02_NONREF/systems/RANK1_ROUTE_CLOSURE_THEOREM.md`.

The project root remains `UNNS_COMMON_REFINEMENT`; this is a development inside the existing research structure, not a renamed phase project.


## Higher-rank affine criterion

The project now contains an exact extension beyond rank one:

`global refinement ⇔ ARD=0`

for positive affine monoids, where

`ARD = number of atoms - rank of the generated group`.

See `02_NONREF/systems/AFFINE_ROUTE_CLOSURE_THEOREM.md`.


## Omnific finite-to-transfinite bridge

The project now contains a source-grounded map between the positive-affine theorem and the
candidate Conway proof architecture.

The provisional five-condition schema is:

`I + P + D + L + R -> Transfinite Route Closure`

It is intentionally recorded as an unproved schema, with falsification tests required next.

See:
`03_OMNIFIC/definitions/OMNIFIC_BRIDGE.md`
and
`05_UNNS/models/TRC_I.md`.


## TRC-I falsification suite

The project now contains five explicit omission countermodels for the provisional
Transfinite Route-Closure schema.

All five roles are independently load-bearing inside the formal test framework.

Sufficiency of all five together remains open.

See `05_UNNS/models/TRC_I_COUNTERMODELS.md`.


## Stratified Refinement System theorem

TRC-I has now been formalized as the SRS Route-Closure Theorem:

`I + P + D + L + R => global route closure`

inside the explicitly defined category of Stratified Refinement Systems.

The theorem is proved by transfinite induction.

The next task is the exact realization audit against the candidate Conway proof.

See:
- `05_UNNS/models/STRATIFIED_REFINEMENT_SYSTEM.md`
- `05_UNNS/models/SRS_ROUTE_CLOSURE_THEOREM.md`


## SRS–Conway audit correction

A source-level audit found that the candidate Conway proof does **not** instantiate the current
SRS axioms literally.

The SRS theorem remains valid as an abstract theorem, but Conway realization is marked
`NOT ESTABLISHED`.

The candidate proof is more faithfully organized around transfinite proof of global primality
(pre-Schreier), followed by the equivalence with four-factor refinement.

See `03_OMNIFIC/output/SRS_CONWAY_AUDIT.md`.


## Primal Descent System

The audited Conway proof is now represented by the `PDS` abstraction:

`F + Q + D + T -> global primality -> four-factor refinement`.

This is separate from the earlier SRS theorem.

See:
- `05_UNNS/models/PRIMAL_DESCENT_SYSTEM.md`
- `05_UNNS/models/PDS_ROUTE_CLOSURE_THEOREM.md`
- `03_OMNIFIC/definitions/PDS_CONWAY_REALIZATION.md`


## Decisive synthesis: the surviving property

The integer, non-refinement, affine, and omnific branches now identify the same exact structural
separator:

`factor traceability = primality`.

Under the cancellative hypotheses used here:

`global four-factor refinement <-> every element is primal`.

The proof mechanisms differ by domain; the invariant does not.

See:
- `05_UNNS/definitions/ROUTE_TRACEABILITY_EQUIVALENCE.md`
- `03_OMNIFIC/output/CONWAY_STRUCTURAL_SPINE.md`
- `outputs/reports/DECISIVE_COMPARATIVE_SYNTHESIS.md`

## Reproducing the decisive synthesis

On Windows run `scripts\RUN_SYNTHESIS.bat`.

The canonical builder is `scripts/BUILD_SYNTHESIS.py`. It validates the pinned upstream evidence
before reproducing the decisive synthesis byte-for-byte. See `scripts/README_SYNTHESIS.md`.

## Structural Descent Anatomy

The stage-by-stage proof anatomy for the candidate omnific refinement construction is recorded in:

`03_OMNIFIC/output/STRUCTURAL_DESCENT_ANATOMY.md`

It tracks the decreasing structural rank, the surviving factor-traceability invariant, the
admissibility mechanism at each transition, and the obstruction to non-refinable branches.

## Conway verification

The pinned candidate proof has been checked with a dedicated verification protocol covering
statement fidelity, proof trust, exact-commit CI build evidence, dependency-spine reconstruction,
and independent endgame reconstruction.

See:
- `03_OMNIFIC/verification/CONWAY_VERIFICATION_PROTOCOL.md`
- `outputs/reports/CONWAY_VERIFICATION_REPORT.md`
- `04_PROOF_MAP/output/CONWAY_VERIFICATION_MATRIX.csv`

For a fresh independent Windows rebuild, run:
`scripts\RUN_CONWAY_VERIFY.bat`


## Independent local theorem build

The final Conway refinement theorem module was rebuilt successfully on an independent Windows
machine at the pinned commit using Lean 4.31.0:

`Build completed successfully (2649 jobs).`

See `03_OMNIFIC/verification/LOCAL_BUILD_EVIDENCE.md`.
