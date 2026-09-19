# UNNS Common Refinement

**Research title:** *Common Refinement and Structural Route Closure in the UNNS Substrate*

> **Core question:** When two factorization routes reach the same endpoint, what structural property guarantees that they admit a common deeper refinement?

---

## Research question

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

For an element `a`, traceability means:

```text
a | cd
    ↓
a = ef,   e | c,   f | d
```

This is exactly the standard algebraic notion that `a` is **primal**.

Under the cancellative hypotheses used in the project:

```text
every element is primal
        ⇔
global four-factor refinement
```

So the common structural law is **not** gcd structure, unique factorization, atomic freeness, support rank, or transfinite descent.

It is:

```text
factor traceability  ⇔  route closure
```

The **domain-specific mechanisms differ**; the invariant does not.

**Primary references**

- `05_UNNS/definitions/ROUTE_TRACEABILITY_EQUIVALENCE.md`
- `outputs/reports/DECISIVE_COMPARATIVE_SYNTHESIS.md`
- `outputs/records/SURVIVING_PROPERTY_RESULT.json`

---

# Integer control regime

For positive integers, the refinement square follows from the classical gcd/coprime mechanism.

Starting with

```text
ab = cd
```

set

```text
e = gcd(a,c)
a = ef
c = eg
gcd(f,g) = 1
```

Then

```text
fb = gd
```

and coprimality forces

```text
g | b
f | d
```

so

```text
b = gh
d = fh
```

The gcd is therefore the **mechanism establishing traceability**, not the cross-domain invariant.

The deterministic control corpus contains **500 verified positive-integer cases**.

**Primary exact chamber**

```text
chambers/REF-I/REF_I.py
```

**Quick test**

```bash
python chambers/REF-I/REF_I.py 6 10 12 5
```

---

# Exact non-refinement controls

The flagship failure system is

```text
H = <2,3>
```

with

```text
2 + 4 = 3 + 3
```

There is no internal refinement witness.

The same example is also an exact primality failure: the atom `2` participates in the combined route `3 + 3` but cannot be routed into either `3` individually.

Therefore:

```text
loss of factor traceability
            =
loss of common refinement
```

**References**

- `02_NONREF/systems/NONREF_THEORY.md`
- `02_NONREF/output/counterexamples.csv`
- `outputs/reports/PHASE2_REPORT.md`

---

# Rank-one route-closure theorem

For a nonzero additive submonoid `H ⊆ N₀`, let

```text
m = min(H \ {0})
γ = gcd(H)
```

The project establishes:

```text
H has global refinement
        ⇔
m = γ
        ⇔
H = γN₀
```

Define the **Route-Closure Index**

```text
RCI(H) = m / γ
```

Then:

```text
RCI(H) = 1  ⇔  global common refinement
```

The implementation validation scanned **793 generator families** and verified the constructive counterexample mechanism throughout the tested non-refinable families.

**Reference**

- `02_NONREF/systems/RANK1_ROUTE_CLOSURE_THEOREM.md`

---

# Positive affine route-closure theorem

For a positive affine monoid `H`, let `A(H)` be its atom set and let

```text
r = rank(gp(H))
```

Define the **Atom-Relation Defect**

```text
ARD(H) = |A(H)| - r
```

In the finite positive-affine setting treated here:

```text
global refinement
    ⇔ every atom is prime
    ⇔ H ≅ N₀^r
    ⇔ ARD(H) = 0
```

This shows that **lattice saturation or geometric normality alone is not enough**: atomic relations can destroy factor traceability even in geometrically well-behaved monoids.

**References**

- `02_NONREF/systems/AFFINE_ROUTE_CLOSURE_THEOREM.md`
- `02_NONREF/output/affine_examples.csv`
- `outputs/reports/AFFINE_ROUTE_CLOSURE_REPORT.md`

---

# Candidate Conway proof: structural anatomy

The audited candidate proof is pinned to:

```text
Repository: gaearon/conway-refinement
Commit:     264445c93b78554c408e99e4e7f663693b4e91ab
```

Its load-bearing structural spine is:

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

The decisive decreasing quantity is the **order type of the nonzero support Archimedean classes**.

The invariant propagated through the argument is:

```text
IsPrimal(x)
```

The structural summary is therefore:

> **Rank decreases while factor traceability survives.**

**References**

- `03_OMNIFIC/output/STRUCTURAL_DESCENT_ANATOMY.md`
- `03_OMNIFIC/output/CONWAY_STRUCTURAL_SPINE.md`

---

# Verification status of the candidate Conway proof

A dedicated verification protocol has been executed against the pinned commit.

| Verification layer | Status |
|---|---|
| Statement fidelity | **PASS** |
| Axiom / proof-trust audit | **PASS** |
| Exact-commit repository CI build | **PASS** |
| Dependency-spine audit | **PASS** |
| Independent mathematical primality → refinement reconstruction | **PASS** |
| Independent local targeted final-theorem build | **PASS** |
| Critical transfinite-step source reconstruction | **PASS** |
| Independent Lean re-formalization of the critical step | **OPEN** |
| Independent specialist mathematical review | **OPEN** |

The independent Windows build used **Lean 4.31.0** and successfully ran:

```bash
lake build ConwayRefinement.Surreal.OmnificInteger.Refinement.ConwayRefinement
```

with:

```text
Build completed successfully (2649 jobs).
```

The exact-commit CI also completed the full repository build and audited **13,114 project declarations**, whose transitive axiom closure reduced to:

```text
propext
Classical.choice
Quot.sound
```

### Current strongest justified status

> **Mechanically verified candidate proof + independent local theorem build + strong source-level audit**

Full independent mathematical confirmation remains incomplete until:

1. the critical transfinite step is re-formalized independently in Lean;
2. the proof receives specialist mathematical review.

**Verification references**

- `03_OMNIFIC/verification/CONWAY_VERIFICATION_PROTOCOL.md`
- `03_OMNIFIC/verification/LOCAL_BUILD_EVIDENCE.md`
- `03_OMNIFIC/verification/CRITICAL_STEP_RECONSTRUCTION.md`
- `outputs/reports/CONWAY_VERIFICATION_REPORT.md`
- `outputs/records/CONWAY_VERIFICATION_RESULT.json`
- `04_PROOF_MAP/output/CONWAY_VERIFICATION_MATRIX.csv`

---

# Reproducible decisive synthesis

The cross-regime synthesis is mechanically reproducible.

**Windows runner**

```bat
scripts\RUN_SYNTHESIS.bat
```

**Canonical builder**

```bash
python scripts/BUILD_SYNTHESIS.py
```

**Check-only mode**

```bash
python scripts/BUILD_SYNTHESIS.py --check
```

Pinned canonical inputs:

```text
scripts/SYNTHESIS_INPUTS.json
```

The build validates the integer baseline, rank-one failure controls, affine controls, and audited Conway evidence before regenerating the approved synthesis artifacts byte-for-byte.

**References**

- `scripts/README_SYNTHESIS.md`
- `outputs/records/SYNTHESIS_BUILD.json`
- `outputs/reports/SYNTHESIS_REPRODUCIBILITY.md`

---

# Role of the chambers

The chamber roles are deliberately separated.

### REF-I

`REF-I` is the **exact algebraic witness/failure layer**.

### STRUC-I and STRUC-PERC-I

These remain **secondary structural diagnostics only**.

They must not be used to prove:

- primality;
- route closure;
- the rank-one theorem;
- the affine theorem;
- Conway refinement.

A legitimate future experiment is to ask whether algebraic loss of factor traceability has a stable perturbative or percolative structural phenotype. Such chamber results would remain orthogonal to theorem proof.

---

# Historical abstractions

During the investigation, broader transfinite abstractions were built and audited. Those exercises were useful because they separated a genuine invariant from proof-specific machinery.

The key correction was:

> **Well-founded descent is a mechanism, not the common law.**

The mature project therefore centers the exact algebraic **traceability ⇔ refinement** equivalence rather than the earlier provisional transfinite schemas.

---

# Project structure

```text
UNNS_COMMON_REFINEMENT/
├── 01_INTEGER/        positive-integer controls
├── 02_NONREF/         exact failures, rank-one and affine theorems
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

Temporary verification clones under

```text
scripts/CONWAY_VERIFY_TMP/
```

are intentionally ignored by Git.

---

# What has been established

1. **Positive integers** provide an exact successful refinement control.
2. **Explicit additive monoids** provide exact non-refinement controls.
3. **Rank-one additive submonoids of N₀** are classified by `m = γ`.
4. **Positive affine refinement** is characterized by prime atoms / atomic independence / `ARD = 0`.
5. Across successful and failed regimes, the exact separator is **primal factor traceability**.
6. The candidate omnific proof is structurally understood as a **transfinite construction of traceability**.
7. The decisive comparative synthesis is **reproducible**.
8. The pinned candidate Conway theorem module has passed an **independent local Lean build**.

---

# Current frontier

The project no longer needs more examples to identify the surviving property.

The two strongest theorem-confirmation tasks still open are:

1. **Independent Lean re-formalization of the critical transfinite induction step**
2. **Independent specialist mathematical review of the Hahn-series / surreal mechanism**

Beyond theorem confirmation lies a stronger research problem:

> **If common refinement exists, is there a structurally privileged or canonical refinement?**

That **Canonical Refinement Problem** is a distinct next stage and should not be conflated with the already-solved existence/traceability question.

---

# Status discipline

This repository distinguishes carefully between:

- classical algebraic facts;
- project-specific theorems and classifications;
- computational validation;
- source-level proof audit;
- candidate-proof dependence;
- UNNS structural interpretation.

In particular, the equivalence between global primality / pre-Schreier structure and four-factor refinement is classical algebra.

The project contribution is the exact UNNS identification of that property as **structural route traceability**, together with the comparative finite-to-transfinite synthesis and its reproducible audit trail.
