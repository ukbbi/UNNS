# UNNS Common Refinement

**Research title:** Common Refinement and Structural Route Closure in the UNNS Substrate

## Research question

Given an endpoint equality

[
ab=cd,
]

when must there exist a common deeper factorization

[
a=ef,qquad
b=gh,qquad
c=eg,qquad
d=fh?
]

UNNS reads this as a distinction between **endpoint equivalence** and **structural route closure**:
two routes may reach the same endpoint without necessarily possessing a common deeper ancestry.

The project began with positive-integer controls, exact non-refinement systems, and affine monoids,
then used those results to audit the candidate Lean proof of Conway's refinement conjecture for
omnific integers.

---

## Central result

The decisive cross-regime property is

[
oxed{	ext{primal factor traceability}.}
]

For an element (a), traceability means

[
amid cd
Longrightarrow
a=ef,qquad emid c,qquad fmid d.
]

This is exactly the standard algebraic notion that (a) is **primal**.

Under the cancellative hypotheses used in the project,

[
oxed{
orall a,operatorname{IsPrimal}(a)
iff
	ext{global four-factor refinement}.
}
]

So the common structural law is not gcd structure, unique factorization, atomic freeness, support
rank, or transfinite descent.

It is:

[
oxed{
	ext{factor traceability}
iff
	ext{route closure}.
}
]

The domain-specific mechanisms differ; the invariant does not.

See:

- `05_UNNS/definitions/ROUTE_TRACEABILITY_EQUIVALENCE.md`
- `outputs/reports/DECISIVE_COMPARATIVE_SYNTHESIS.md`
- `outputs/records/SURVIVING_PROPERTY_RESULT.json`

---

## Integer control regime

For positive integers, the refinement square follows from the classical gcd/coprime mechanism.

Starting with

[
ab=cd,
]

set

[
e=gcd(a,c),qquad a=ef,qquad c=eg,qquad gcd(f,g)=1.
]

Then

[
fb=gd,
]

so coprimality forces

[
gmid b,qquad fmid d,
]

and hence

[
b=gh,qquad d=fh.
]

The gcd is therefore the **mechanism** establishing traceability, not the cross-domain invariant.

The deterministic control corpus contains 500 verified positive-integer cases.

Primary exact chamber:

`chambers/REF-I/REF_I.py`

Quick test:

```text
python chambers/REF-I/REF_I.py 6 10 12 5
```

---

## Exact non-refinement controls

The flagship failure system is

[
H=langle2,3angle,
]

with

[
2+4=3+3.
]

There is no internal refinement witness.

The same example is also an exact primality failure: the atom (2) participates in the combined
route (3+3) but cannot be routed into either (3) individually.

Thus the project identifies the failure mechanism as

[
oxed{
	ext{loss of factor traceability}
=
	ext{loss of common refinement}.
}
]

See:

- `02_NONREF/systems/NONREF_THEORY.md`
- `02_NONREF/output/counterexamples.csv`
- `outputs/reports/PHASE2_REPORT.md`

---

## Rank-one route-closure theorem

For a nonzero additive submonoid

[
Hsubseteqmathbb N_0,
]

let

[
m=min(Hsetminus{0}),
qquad
gamma=gcd(H).
]

The project establishes

[
oxed{
H	ext{ has global refinement}
iff
m=gamma
iff
H=gammamathbb N_0.
}
]

Define the Route-Closure Index

[
operatorname{RCI}(H)=rac{m}{gamma}.
]

Then

[
operatorname{RCI}(H)=1
iff
	ext{global common refinement}.
]

The implementation validation scanned 793 generator families and verified the constructive
counterexample mechanism throughout the tested non-refinable families.

See:

`02_NONREF/systems/RANK1_ROUTE_CLOSURE_THEOREM.md`

---

## Positive affine route-closure theorem

For a positive affine monoid (H), let (mathcal A(H)) be its atom set and let

[
r=operatorname{rank}operatorname{gp}(H).
]

Define the Atom-Relation Defect

[
operatorname{ARD}(H)
=
|mathcal A(H)|-r.
]

In the finite positive-affine setting treated here,

[
oxed{
	ext{global refinement}
iff
	ext{every atom is prime}
iff
Hcongmathbb N_0^r
iff
operatorname{ARD}(H)=0.
}
]

This shows that lattice saturation or geometric normality alone is not enough: atomic relations can
destroy factor traceability even in geometrically well-behaved monoids.

See:

- `02_NONREF/systems/AFFINE_ROUTE_CLOSURE_THEOREM.md`
- `02_NONREF/output/affine_examples.csv`
- `outputs/reports/AFFINE_ROUTE_CLOSURE_REPORT.md`

---

## Candidate Conway proof: structural anatomy

The audited candidate proof is pinned to:

```text
gaearon/conway-refinement
commit 264445c93b78554c408e99e4e7f663693b4e91ab
```

The source-level proof spine is:

```text
finite support-class primality
    ↓
support-class stratification
    ↓
common-tail quotient local refinement
    ↓
retained-block factorization
    ↓
strict decrease of support-class order type
    ↓
primality of the residual by induction
    ↓
ambient transport
    ↓
primal splice
    ↓
global primality
    ↓
four-factor refinement
    ↓
transport to omnific integers
```

The decisive decreasing quantity is

[
ho(x)
=
operatorname{orderType}
(	ext{nonzero support Archimedean classes of }x),
]

while the invariant propagated through the argument is

[
operatorname{IsPrimal}(x).
]

The structural summary is therefore:

[
oxed{
	ext{rank decreases while factor traceability survives}.
}
]

See:

- `03_OMNIFIC/output/STRUCTURAL_DESCENT_ANATOMY.md`
- `03_OMNIFIC/output/CONWAY_STRUCTURAL_SPINE.md`

---

## Verification status of the candidate Conway proof

A dedicated verification protocol has been executed against the pinned commit.

Current status:

| Verification layer | Status |
|---|---|
| Statement fidelity | **PASS** |
| Axiom / proof-trust audit | **PASS** |
| Exact-commit repository CI build | **PASS** |
| Dependency-spine audit | **PASS** |
| Independent mathematical primality→refinement reconstruction | **PASS** |
| Independent local targeted final-theorem build | **PASS** |
| Critical transfinite-step source reconstruction | **PASS** |
| Independent Lean re-formalization of the critical step | **OPEN** |
| Independent specialist mathematical review | **OPEN** |

The independent Windows build used Lean 4.31.0 and successfully ran:

```text
lake build ConwayRefinement.Surreal.OmnificInteger.Refinement.ConwayRefinement
```

with:

```text
Build completed successfully (2649 jobs).
```

The exact-commit CI also completed the full repository build and audited 13,114 project declarations,
whose transitive axiom closure reduced to:

```text
propext
Classical.choice
Quot.sound
```

The strongest justified status is therefore:

[
oxed{
	ext{mechanically verified candidate proof}
+
	ext{independent local theorem build}
+
	ext{strong source-level audit}
}
]

Full independent mathematical confirmation remains incomplete until the critical transfinite step is
re-formalized independently and the proof receives specialist mathematical review.

See:

- `03_OMNIFIC/verification/CONWAY_VERIFICATION_PROTOCOL.md`
- `03_OMNIFIC/verification/LOCAL_BUILD_EVIDENCE.md`
- `03_OMNIFIC/verification/CRITICAL_STEP_RECONSTRUCTION.md`
- `outputs/reports/CONWAY_VERIFICATION_REPORT.md`
- `outputs/records/CONWAY_VERIFICATION_RESULT.json`
- `04_PROOF_MAP/output/CONWAY_VERIFICATION_MATRIX.csv`

---

## Reproducible decisive synthesis

The cross-regime synthesis is mechanically reproducible.

Windows runner:

```text
scripts\RUN_SYNTHESIS.bat
```

Canonical builder:

```text
python scripts/BUILD_SYNTHESIS.py
```

Check-only mode:

```text
python scripts/BUILD_SYNTHESIS.py --check
```

Pinned canonical inputs:

`scripts/SYNTHESIS_INPUTS.json`

The build validates the integer baseline, rank-one failure controls, affine controls, and audited
Conway evidence before regenerating the approved synthesis artifacts byte-for-byte.

See:

- `scripts/README_SYNTHESIS.md`
- `outputs/records/SYNTHESIS_BUILD.json`
- `outputs/reports/SYNTHESIS_REPRODUCIBILITY.md`

---

## Role of the chambers

The chamber roles are now sharply separated.

### REF-I

`REF-I` is the exact algebraic witness/failure layer.

### STRUC-I and STRUC-PERC-I

These remain **secondary structural diagnostics only**.

They must not be used to prove:

- primality;
- route closure;
- the rank-one theorem;
- the affine theorem;
- Conway refinement.

A legitimate future experiment is to ask whether algebraic loss of factor traceability has a stable
perturbative/percolative structural phenotype, but such chamber results would remain orthogonal to
the theorem proof.

---

## Historical abstractions

During the investigation, broader transfinite abstractions were built and audited. Those exercises
helped separate a genuine invariant from proof-specific machinery.

The key correction was:

[
oxed{
	ext{well-founded descent is a mechanism, not the common law}.
}
]

The mature project therefore centers the exact algebraic traceability/refinement equivalence rather
than the earlier provisional transfinite schemas.

---

## Project structure

```text
UNNS_COMMON_REFINEMENT/
├── 01_INTEGER/        positive-integer controls
├── 02_NONREF/         exact failure systems, rank-one and affine theorems
├── 03_OMNIFIC/        Conway bridge, structural anatomy, verification
├── 04_PROOF_MAP/      dependency and realization maps
├── 05_UNNS/           structural definitions and theorem interpretations
├── 06_TESTS/          adversarial and validation tests
├── chambers/          REF-I, STRUC-I, STRUC-PERC-I
├── outputs/           reports and machine-readable result records
├── refs/              source and terminology records
├── scripts/           reproducible builders and verification runners
├── manuscript/        manuscript-oriented material
├── CLEAN_STATE.md
├── MANIFEST.md
└── README.md
```

Temporary verification clones under `scripts/CONWAY_VERIFY_TMP/` are intentionally ignored by Git.

---

## What has been established

At the current project state:

1. Positive integers provide an exact successful refinement control.
2. Explicit additive monoids provide exact non-refinement controls.
3. Rank-one additive submonoids of (mathbb N_0) are classified by (m=gamma).
4. Positive affine refinement is characterized by prime atoms / atomic independence / (operatorname{ARD}=0).
5. Across successful and failed regimes, the exact separator is primal factor traceability.
6. The candidate omnific proof is structurally understood as a transfinite construction of that traceability.
7. The decisive comparative synthesis is reproducible.
8. The pinned candidate Conway theorem module has passed an independent local Lean build.

---

## Current frontier

The project no longer needs more examples to identify the surviving property.

The two strongest theorem-confirmation tasks still open are:

1. **independent Lean re-formalization of the critical transfinite induction step**;
2. **independent specialist mathematical review of the Hahn-series / surreal mechanism**.

Beyond theorem confirmation lies a stronger research problem:

> If common refinement exists, is there a structurally privileged or canonical refinement?

That **Canonical Refinement Problem** is a distinct next stage and should not be conflated with the
already-solved existence/traceability question.

---

## Status discipline

This repository distinguishes carefully between:

- classical algebraic facts;
- project-specific theorems and classifications;
- computational validation;
- source-level proof audit;
- candidate-proof dependence;
- UNNS structural interpretation.

In particular, the equivalence between global primality / pre-Schreier structure and four-factor
refinement is classical algebra. The project contribution is the exact UNNS identification of that
property as **structural route traceability**, together with the comparative finite-to-transfinite
synthesis and its reproducible audit trail.
