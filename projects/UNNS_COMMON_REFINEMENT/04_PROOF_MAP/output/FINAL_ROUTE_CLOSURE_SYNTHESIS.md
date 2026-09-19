# Final Route-Closure Synthesis

## Common Refinement and Structural Route Closure in the UNNS Substrate

**Project:** `UNNS_COMMON_REFINEMENT`  
**Status:** original Conway/common-refinement structural investigation internally complete at the current audited source state  
**Conway source lock:** `gaearon/conway-refinement` commit `264445c93b78554c408e99e4e7f663693b4e91ab`  
**Formal closure:** extracted route-closure induction principle independently formalized and Lean-kernel verified

---

# 1. Original question

The project began with the contrast between

`ab = cd`

and the stronger existence of a common refinement

```text
a = ef
b = gh
c = eg
d = fh
```

The central research question was:

> **What structural property survives the transition from ordinary integers to omnific integers that keeps the refinement square admissible?**

That question is now answered at both the algebraic and mechanism levels.

---

# 2. Final answer — algebraic level

The surviving algebraic property is

**Every-element primality / pre-Schreier factor traceability.**

In the relevant cancellative commutative setting,

```text
every element primal
        <=>
four-factor refinement
```

Thus factor traceability is not merely correlated with route closure. It is the exact algebraic state corresponding to global route closure.

This equivalence is classical algebra. The project contribution is the cross-regime structural identification and the analysis of how different domains establish or fail that state.

---

# 3. Final answer — mechanism level

The successful regimes do not obtain primal traceability by the same mechanism. What they share is a local-to-global construction pattern:

```text
exact routed local block
+ strictly simpler unresolved residue
+ route-closed terminal regime
+ ambient reconstruction
=> global traceability
```

This is isolated as the **Well-Founded Route-Closure Induction Proposition** in

`05_UNNS/definitions/ROUTE_CLOSURE_INDUCTION.md`.

Its extracted algebraic induction skeleton has also been independently formalized in

`04_PROOF_MAP/lean/RouteClosureInduction.lean`

and kernel-verified against the locked Conway algebraic interface.

---

# 4. Four-regime comparison

## A. Positive integers — immediate repair

The gcd/coprime mechanism routes the full factor in one step.

Structural form:

```text
local split -> residual unit -> done
```

There is no defect core and no persistent defect channel.

## B. Rank-one nonfree monoids — finite residual defect core

The rank-one theorem gives global refinement only for the free lattice ray. Elementwise analysis shows that nonfree numerical monoids may have a cofinal all-primal tail while retaining a finite non-primal core.

Structural form:

```text
finite obstruction core + cofinal primal tail
```

Eventual safety does not imply global route closure.

## C. Higher-rank nonfree positive affine monoids — persistent defect channel

For

```text
rank(H) >= 2
ARD(H) > 0
```

the project proves the Persistent Defect-Ray Theorem:

```text
there exist a and nonzero rho such that
for every n >= 0:
    a + n*rho is non-primal
```

Structural form:

```text
local relation defect -> rank-preserving propagation -> no terminal repair
```

The obstruction can survive indefinitely along a legitimate monoid direction.

## D. Omnific candidate proof — exact repair plus forced descent

The audited source architecture is

```text
finite-class primality
-> exact common-tail quotient refinement
-> occupied support-class selection
-> retained-block factorisation
-> strict support-class order-type decrease
-> ambient transport
-> primal lower-rank residual
-> splice
-> every-element primality
-> four-factor refinement
```

The unresolved residual is forbidden from propagating at unchanged structural rank.

Structural form:

```text
exact repair -> lower-rank residue -> primal base -> reconstruction
```

---

# 5. Decisive contrast

The project now distinguishes four behaviors of a potential route defect:

```text
positive integers:
    defect eliminated immediately

rank-one failures:
    defect survives only in a finite residual core

higher-rank affine failures:
    defect propagates indefinitely at persistent structural complexity

candidate omnific mechanism:
    every unresolved residual is forced to strictly lower well-founded complexity
    until it reaches a primal base
```

This is the strongest finite-to-transfinite structural distinction established by the project.

---

# 6. Why well-founded descent is not the invariant

The project originally considered whether well-founded structural descent might itself be the common law.

That is rejected.

Descent is a **mechanism**, not the final property. A decreasing complexity measure is useless if local routing fails, if descent terminates in a non-primal base, or if a quotient repair cannot be reconstructed in the ambient system.

The sufficient pattern requires:

1. an exact routed local block;
2. a complementary residual;
3. strict decrease of a well-founded rank on that residual;
4. a terminal/base regime that is already primal;
5. ambient reconstruction of the local routing.

The final algebraic state remains:

**Global primal factor traceability.**

---

# 7. What UNNS adds

UNNS should not rename “every element primal” as if it were a new algebraic theorem.

The useful UNNS contribution is the separation of:

### Endpoint level
Two routes reach the same terminal result.

### Traceability level
Every factor can be routed through a decomposition; algebraically, every element is primal.

### Mechanism level
Traceability is established by admissible exact repairs whose unresolved residue cannot remain structurally stationary and whose terminal regime is already closed.

This mechanism-level reading allows one to compare finite obstruction cores, persistent defect channels, and rank-lowering transfinite repair without confusing those mechanisms with the algebraic invariant itself.

---

# 8. Route-Closure Induction Proposition

The project can state:

> **Route-Closure Induction Proposition.** In a commutative cancellative monoid equipped with a well-founded structural rank, suppose a designated base regime is primal. Suppose further that every divisibility involving a non-base element admits an exact ambient routed factor block whose complementary factor has strictly lower structural rank. Then every element is primal, and hence every product equality admits four-factor refinement.

The proposition is proved mathematically in

`05_UNNS/definitions/ROUTE_CLOSURE_INDUCTION.md`.

The extracted proposition is formalized in Lean as:

```text
UNNS.CommonRefinement.forall_isPrimal_of_wellFoundedRouteClosure
UNNS.CommonRefinement.hasFourFactorRefinement_of_wellFoundedRouteClosure
```

in

`04_PROOF_MAP/lean/RouteClosureInduction.lean`.

---

# 9. Lean kernel closure of the extracted mechanism

The independent formal module was compiled in a local Windows checkout of the exact locked Conway repository, using Lean 4.31.0.

Command:

```text
lake build ConwayRefinement.UNNS.RouteClosureInduction
```

Observed full target build:

```text
[837/837] Built ConwayRefinement.UNNS.RouteClosureInduction
Build completed successfully (837 jobs).
```

Cached recheck:

```text
[829/829] Replayed ConwayRefinement.UNNS.RouteClosureInduction
Build completed successfully (829 jobs).
```

This closes the previously open internal task of formalizing the **extracted route-closure induction principle**.

Scope boundary: this does not claim a from-scratch reimplementation of the complete concrete Hahn-series / surreal infrastructure. It verifies the independently extracted induction mechanism against the public algebraic interfaces used by the audited Conway source.

Primary evidence:

- `outputs/reports/LEAN_ROUTE_CLOSURE_REPORT.md`
- `outputs/records/LEAN_ROUTE_CLOSURE_RESULT.json`
- `outputs/records/ROUTE_CLOSURE_KERNEL_VERIFICATION.md`
- `outputs/records/ROUTE_CLOSURE_KERNEL_CHECK.txt`
- `outputs/records/ROUTE_CLOSURE_KERNEL_EVIDENCE.png`

---

# 10. Final answer to the original research question

The original question was:

> What structural property survives the transition from ordinary integers to omnific integers that keeps the refinement square admissible?

The answer is two-layered.

## Property

**Global factor traceability: every element is primal.**

## Successful construction pattern

```text
exact local routing
+ well-founded reduction of the unresolved residue
+ primal terminal closure
+ ambient reconstruction
```

The integers realize the pattern immediately; the candidate omnific proof realizes it transfinally.

The failure systems show why this distinction matters:

- rank one can leave a finite unresolved core;
- higher rank can support an infinite persistent defect ray.

The strongest justified UNNS conclusion is therefore:

> **Global route closure is the absence of any structural defect capable of surviving every admissible exact repair and well-founded reduction.**

This is a UNNS interpretation of the proven comparison, not a replacement definition of algebraic primality.

---

# 11. Project closure status

The original Conway/common-refinement structural-comparison objective is now **internally complete** at the locked source state.

Completed internal layers include:

- exact integer controls;
- exact non-refinement controls;
- rank-one classification;
- positive affine classification;
- elementwise primal/non-primal analysis;
- persistent affine defect-ray theorem;
- source-locked Conway structural audit;
- reproducible decisive synthesis;
- independent local final-theorem build;
- independent mathematical endgame reconstruction;
- source-level critical-step reconstruction;
- kernel-verified independent formalization of the extracted route-closure induction principle.

The remaining confirmation layer is **external**:

- independent specialist mathematical review of the Hahn-series / surreal realization.

A still stronger from-scratch reimplementation of the concrete Hahn/surreal critical step could be pursued as an external-strengthening exercise, but it is not treated as unfinished internal work.

---

# 12. New research branches beyond closure

The following are new branches, not missing steps of the original investigation:

1. **Structural phenotype branch**  
   Test whether exact algebraic loss of primal factor traceability has a reproducible perturbative/percolative signature under frozen STRUC-I and STRUC-PERC-I diagnostics.

2. **Canonical Refinement Problem**  
   If common refinement exists, determine whether there is a structurally privileged refinement.

3. **Optional non-affine extension**  
   Seek systems that separate the route-closure induction mechanism from other ways of obtaining pre-Schreier structure.

These branches should be versioned as extensions of the completed existence/traceability investigation rather than used to reopen it.