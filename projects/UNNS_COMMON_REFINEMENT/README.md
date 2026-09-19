# UNNS Common Refinement

**Research title:** *Common Refinement and Structural Route Closure in the UNNS Substrate*

> **Core question:** When two factorization routes reach the same endpoint, what structural property guarantees that they admit a common deeper refinement?

## Project status

The original Conway/common-refinement investigation is **internally complete at the current audited source state**.

The project has identified the surviving algebraic property, classified finite failure regimes, extracted the finite-to-transfinite mechanism, audited the candidate Conway proof, reproduced the final theorem module independently, and kernel-verified the extracted route-closure induction principle in Lean.

The two primary endpoint documents are:

- `04_PROOF_MAP/output/FINAL_ROUTE_CLOSURE_SYNTHESIS.md`
- `outputs/reports/LEAN_ROUTE_CLOSURE_REPORT.md`

The remaining **external** confirmation layer is independent specialist mathematical review of the Hahn-series / surreal mechanism. That review is not an unfinished computational step in this project.

The next internal research branch is deliberately separate: the STRUC-I / STRUC-PERC-I structural-phenotype experiment. A further branch is the Canonical Refinement Problem.

---

# Research question

Given an endpoint equality

```text
ab = cd
```

when must there exist factors `e, f, g, h` such that

```text
a = ef
b = gh
c = eg
d = fh
```

UNNS reads this as a distinction between **endpoint equivalence** and **structural route closure**:

> Two routes may reach the same endpoint without necessarily possessing a common deeper ancestry.

The project began with positive-integer controls, exact non-refinement systems, and affine monoids, then used those results to audit the candidate Lean proof of Conway's refinement conjecture for omnific integers.

---

# Central result

The decisive cross-regime property is:

> **Primal factor traceability**

For an element `a`, traceability means

```text
a | cd
    ↓
a = ef,   e | c,   f | d
```

which is exactly the standard algebraic notion that `a` is **primal**.

Under the cancellative hypotheses used in the project,

```text
every element is primal
        ⇔
global four-factor refinement
```

Therefore the common structural law is not gcd structure, unique factorization, atomic freeness, support rank, or transfinite descent.

It is

```text
factor traceability  ⇔  route closure
```

The **domain-specific mechanisms differ**; the invariant does not.

Primary references:

- `05_UNNS/definitions/ROUTE_TRACEABILITY_EQUIVALENCE.md`
- `outputs/reports/DECISIVE_COMPARATIVE_SYNTHESIS.md`
- `outputs/records/SURVIVING_PROPERTY_RESULT.json`

---

# Exact finite results

## Positive integers

For positive integers the gcd/coprime construction establishes traceability directly.

Starting from

```text
ab = cd
```

take

```text
e = gcd(a,c)
a = ef
c = eg
gcd(f,g) = 1
```

Then `fb = gd`, so coprimality forces `g | b` and `f | d`, yielding `b = gh` and `d = fh`.

The deterministic control corpus contains **500 verified cases**.

## Exact non-refinement control

The flagship failure system is

```text
H = <2,3>
```

with

```text
2 + 4 = 3 + 3.
```

There is no internal refinement witness. The same equality is an exact primality failure, so here

```text
loss of factor traceability
            =
loss of common refinement.
```

## Rank-one route closure

For a nonzero additive submonoid `H ⊆ N₀`, let

```text
m = min(H \ {0})
γ = gcd(H).
```

Then

```text
H has global refinement
        ⇔
m = γ
        ⇔
H = γN₀.
```

With

```text
RCI(H) = m / γ,
```

one has `RCI(H)=1 ⇔ global common refinement`.

The validation scanned **793 generator families**, including **513** constructive non-refinement families.

## Positive affine route closure

For a positive affine monoid `H`, with atom set `A(H)` and

```text
r = rank(gp(H)),
ARD(H) = |A(H)| - r,
```

the project establishes

```text
global refinement
    ⇔ every atom is prime
    ⇔ H ≅ N₀^r
    ⇔ ARD(H) = 0.
```

Thus lattice saturation or geometric normality alone is not sufficient in higher rank.

---

# Elementwise failure geometry

The later elementwise analysis sharpened the finite comparison.

## Rank one

For nonfree numerical/rank-one controls, the non-primal locus is finite. There is a cofinal all-primal tail, but the surviving finite obstruction core is enough to destroy global refinement.

## Rank at least two

For a positive affine monoid with

```text
rank(H) >= 2
ARD(H) > 0,
```

the project proves the **Persistent Defect-Ray Theorem**:

```text
there exist a and nonzero ρ such that
a + nρ is non-primal for every n >= 0.
```

So higher-rank relation defects need not wash out at larger scale; they can propagate along an infinite affine ray.

Primary references:

- `outputs/reports/ELEMENTWISE_ROUTE_REPORT.md`
- `outputs/reports/AFFINE_ELEMENTWISE_REPORT.md`
- `02_NONREF/systems/AFFINE_DEFECT_RAY_THEOREM.md`
- `outputs/reports/AFFINE_DEFECT_RAY_REPORT.md`

---

# Candidate Conway proof: structural anatomy

The audited candidate proof is source-locked to

```text
Repository: gaearon/conway-refinement
Commit:     264445c93b78554c408e99e4e7f663693b4e91ab
```

Its load-bearing structural spine is

```text
finite support-class primality
        ↓
common-tail quotient local refinement
        ↓
occupied support-class selection
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
every element primal
        ↓
four-factor refinement
        ↓
transport to omnific integers
```

The decreasing quantity is the order type of the nonzero support Archimedean classes. The invariant propagated through the induction is `IsPrimal`.

The finite/transfinite comparison is therefore:

```text
positive integers:
    immediate exact repair

rank-one failures:
    finite residual defect core

higher-rank affine failures:
    persistent rank-preserving defect channel

candidate omnific mechanism:
    exact local repair + strictly lower-rank residual + primal base + reconstruction
```

Primary references:

- `03_OMNIFIC/output/STRUCTURAL_DESCENT_ANATOMY.md`
- `04_PROOF_MAP/output/CONWAY_DEFECT_CHANNEL_AUDIT.md`
- `04_PROOF_MAP/output/FINAL_ROUTE_CLOSURE_SYNTHESIS.md`

---

# Route-Closure Induction Proposition

The project isolates the following sufficient construction principle:

```text
primal base
+ exact ambient routed local block
+ strictly lower well-founded residual rank
        ↓
every element primal
        ↓
four-factor refinement
```

The mathematical proposition is recorded in

```text
05_UNNS/definitions/ROUTE_CLOSURE_INDUCTION.md
```

and the independent Lean formalization is

```text
04_PROOF_MAP/lean/RouteClosureInduction.lean
```

The formal module defines `HasWellFoundedRouteClosure` and proves:

```text
forall_isPrimal_of_wellFoundedRouteClosure
hasFourFactorRefinement_of_wellFoundedRouteClosure
```

against the audited Conway algebraic interface.

---

# Lean and verification status

| Verification layer | Status |
|---|---|
| Statement fidelity | **PASS** |
| Axiom / proof-trust audit | **PASS** |
| Exact-commit repository CI build | **PASS** |
| Dependency-spine audit | **PASS** |
| Independent mathematical primality → refinement reconstruction | **PASS** |
| Independent local targeted final-theorem build | **PASS** |
| Critical transfinite-step source reconstruction | **PASS** |
| Independent extracted route-closure induction formalization | **PASS — LEAN KERNEL VERIFIED** |
| Independent specialist mathematical review | **OPEN — external** |

The independent Windows theorem build used Lean 4.31.0:

```text
lake build ConwayRefinement.Surreal.OmnificInteger.Refinement.ConwayRefinement
Build completed successfully (2649 jobs).
```

The independent route-closure induction formalization was then built against the same locked source state:

```text
lake build ConwayRefinement.UNNS.RouteClosureInduction
[837/837] Built ConwayRefinement.UNNS.RouteClosureInduction
Build completed successfully (837 jobs).
```

A cached recheck also completed successfully:

```text
[829/829] Replayed ConwayRefinement.UNNS.RouteClosureInduction
Build completed successfully (829 jobs).
```

### Scope boundary

The kernel-verified `RouteClosureInduction.lean` is an independent formalization of the **extracted induction mechanism** using the public Conway algebraic interfaces. It is not claimed to be a from-scratch reimplementation of the full concrete Hahn-series / surreal infrastructure.

A still stronger exercise would independently rebuild the concrete Hahn/surreal critical step in a separate mini-project. That is not required for the present internal closure and is not being treated as an unfinished project step.

Likewise, `03_OMNIFIC/verification/IndependentEndgame.lean` exists as a separately written endgame proof source; a standalone minimal-environment kernel build of that specific file was not separately executed. This is an optional redundancy check, not a load-bearing open task.

### Strongest current status

> **Mechanically verified candidate proof + independent local final-theorem build + kernel-verified independent formalization of the extracted route-closure induction principle + strong source/statement/axiom audit.**

Independent specialist mathematical review remains open, so the Conway result should still be described as a **candidate formal proof** rather than as independently peer-confirmed mathematics.

Verification references:

- `03_OMNIFIC/verification/CONWAY_VERIFICATION_PROTOCOL.md`
- `03_OMNIFIC/verification/LOCAL_BUILD_EVIDENCE.md`
- `03_OMNIFIC/verification/CRITICAL_STEP_RECONSTRUCTION.md`
- `04_PROOF_MAP/lean/RouteClosureInduction.lean`
- `outputs/reports/CONWAY_VERIFICATION_REPORT.md`
- `outputs/reports/LEAN_ROUTE_CLOSURE_REPORT.md`
- `outputs/records/CONWAY_VERIFICATION_RESULT.json`
- `outputs/records/LEAN_ROUTE_CLOSURE_RESULT.json`
- `outputs/records/ROUTE_CLOSURE_KERNEL_VERIFICATION.md`

---

# Reproducible decisive synthesis

The cross-regime synthesis remains mechanically reproducible.

Windows runner:

```bat
scripts\RUN_SYNTHESIS.bat
```

Canonical builder:

```bash
python scripts/BUILD_SYNTHESIS.py
```

Check-only mode:

```bash
python scripts/BUILD_SYNTHESIS.py --check
```

Pinned inputs:

```text
scripts/SYNTHESIS_INPUTS.json
```

Primary reproducibility records:

- `outputs/records/SYNTHESIS_BUILD.json`
- `outputs/reports/SYNTHESIS_REPRODUCIBILITY.md`

---

# Role of the chambers

The chamber roles remain deliberately separated.

## REF-I

`REF-I` is the **exact algebraic witness/failure layer**.

## STRUC-I and STRUC-PERC-I

These remain **secondary structural diagnostics only**. They must not be used to prove:

- primality;
- route closure;
- the rank-one theorem;
- the affine theorem;
- Conway refinement.

The next planned internal research branch is:

> **Does exact algebraic loss of primal factor traceability have a reproducible perturbative or percolative structural phenotype under frozen STRUC-I and STRUC-PERC-I diagnostics?**

That chamber branch is new work. It does not reopen the completed existence/traceability investigation.

---

# Historical abstractions

Broader transfinite abstractions developed during the investigation helped distinguish the invariant from proof-specific machinery.

The mature correction is:

> **Well-founded descent is a mechanism, not the common law.**

The common law is primal factor traceability / route closure.

SRS and PDS remain retained historical/formal abstractions where useful, but the mature project should not reintroduce superseded generic unification claims.

---

# Project endpoint

For the original Conway/common-refinement investigation, use the following as the authoritative internal endpoint:

```text
04_PROOF_MAP/output/FINAL_ROUTE_CLOSURE_SYNTHESIS.md
outputs/reports/LEAN_ROUTE_CLOSURE_REPORT.md
outputs/records/FINAL_SYNTHESIS_RESULT.json
outputs/records/LEAN_ROUTE_CLOSURE_RESULT.json
```

The original structural-comparison objective is closed at this source state.

---

# Research branches beyond the endpoint

These are **new branches**, not unfinished steps of the original investigation.

1. **Structural phenotype branch** — frozen STRUC-I / STRUC-PERC-I diagnostics on exact traceability success/failure corpora.
2. **Canonical Refinement Problem** — if common refinement exists, determine whether any refinement is structurally privileged.
3. **Optional algebraic extension** — seek non-affine systems that separate the route-closure induction mechanism from other ways of obtaining pre-Schreier structure.
4. **External confirmation** — independent specialist mathematical review of the Hahn-series / surreal realization.

---

# Project structure

```text
UNNS_COMMON_REFINEMENT/
├── 01_INTEGER/        positive-integer controls
├── 02_NONREF/         exact failures, rank-one and affine theorems
├── 03_OMNIFIC/        Conway bridge, structural anatomy, verification
├── 04_PROOF_MAP/      dependency maps, synthesis, Lean formalization
├── 05_UNNS/           retained structural definitions and models
├── 06_TESTS/          validation and falsification tests
├── chambers/          REF-I, STRUC-I, STRUC-PERC-I
├── outputs/           reports and machine-readable records
├── refs/              source and terminology records
├── scripts/           reproducible builders and verification runners
├── manuscript/        manuscript-oriented material
├── CLEAN_STATE.md
├── MANIFEST.md
└── README.md
```

---

# Status discipline

This project distinguishes carefully between:

- classical algebraic facts;
- project-specific theorems and classifications;
- computational validation;
- source-level proof audit;
- kernel-verified formalization;
- candidate-proof dependence;
- external specialist confirmation;
- UNNS structural interpretation.

In particular, the equivalence between global primality / pre-Schreier structure and four-factor refinement is classical algebra.

The project contribution is the exact UNNS identification of that property as **structural route traceability**, the finite-to-transfinite comparison of how route defects disappear or persist, and the reproducible formal/audit trail supporting that synthesis.