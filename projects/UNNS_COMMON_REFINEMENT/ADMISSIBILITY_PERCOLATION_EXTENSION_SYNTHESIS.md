# Admissibility–Percolation Extension Synthesis

## Extension to `UNNS_COMMON_REFINEMENT`

**Parent project:** `UNNS_COMMON_REFINEMENT`  
**Extension project:** `UNNS_ADMISSIBILITY_PERCOLATION`  
**Status:** cross-project synthesis complete  
**Scope:** interpretive extension of the common-refinement result; no change to the parent algebraic theorem

---

## 1. Parent result that remains unchanged

The central algebraic conclusion of `UNNS_COMMON_REFINEMENT` remains:

```text
global primal factor traceability
        <=>
global four-factor refinement
```

under the cancellative hypotheses used in the project.

The parent investigation established that common refinement is controlled by exact factor-routing
structure: every factor must be traceable through a competing product decomposition.

That result is not weakened or replaced by the later chamber work.

The new project addresses a different question:

> What happens to systems with known route-closure status when they are examined through independent
> UNNS notions of perturbative admissibility and gap-space percolative connectivity?

---

## 2. Why the extension was necessary

The common-refinement project identified exact route defects in non-refining systems.

Without further testing, it would be easy to overinterpret such defects as generic structural
failure.

The admissibility–percolation branch tested that possibility directly using two frozen UNNS
instruments:

```text
STRUC-I v1.0.4
    perturbative ladder admissibility

STRUC-PERC-I v2.5.0
    gap-space percolative connectivity

STRUC-PERC-I Audit v2.5.1
    exact finite-graph connectivity-threshold audit
```

The 30-system corpus retained independently established algebraic annotations from the parent
project, but those annotations were not used as chamber definitions.

This separation is essential.

---

## 3. First extension result: route failure does not imply inadmissibility

STRUC-I classified all 30 frozen ladders as:

```text
Geometric Persistence
Stable Structure
```

with:

```text
mean_Ak = 1.0
min_Ak  = 1.0
```

This includes both:

```text
algebraically route-closed systems
and
algebraically route-defective systems
```

Therefore:

> **Loss of primal factor traceability does not, by itself, imply failure of perturbative
> admissibility.**

This is the first major extension of the parent result.

A system can fail to possess a common algebraic refinement route while its ordered numerical
realization remains completely admissible under the STRUC-I perturbation criterion.

The route defect is therefore specific.

It is not automatically:

- loss of ordering stability;
- collapse of the ladder;
- a structural-boundary transition;
- perturbative inadmissibility.

---

## 4. Second extension result: route failure does not imply failure of eventual connectivity

The original STRUC-PERC-I v2.5.0 batch produced:

```text
25 FULL_PERCOLATION
 4 HARD_FRAGMENTATION
 1 TAIL_FRAGMENTATION
```

Those five non-full outcomes triggered a dedicated audit because STRUC-I had already found all 30
ladders fully admissible.

The separately versioned `STRUC-PERC-I Audit v2.5.1` showed that all 30 finite gap graphs eventually
reach full connectivity once their exact normalized connectivity threshold is explicitly probed.

Therefore:

> **Loss of primal factor traceability also does not, by itself, imply failure of eventual
> gap-space connectivity.**

Again, the algebraic defect survives as a distinct structural property rather than becoming a
generic collapse of the host representation.

---

## 5. The important percolation variable is scale, not eventual yes/no connectivity

The v2.5.1 audit revealed an important limitation of an unbounded binary percolation question.

For a finite full-pairwise threshold graph, eventual connectivity becomes expected once the
threshold is allowed to reach the largest adjacent separation in the sorted gap-value set.

So the informative quantity is not simply:

```text
does the finite gap graph eventually connect?
```

but rather:

```text
at what normalized scale does it connect?
```

The retained observable is:

```text
kappa_connect_exact
```

Across the pilot corpus it spans:

```text
0
to
15.073646
```

Thus systems that are equally admissible under STRUC-I can require very different structural scales
to become connected in gap space.

---

## 6. Rank-one result: a clean secondary signature

The most striking repeated distinction appears in rank one.

All six free rank-one controls have:

```text
kappa_connect_exact = 0
```

All six nonfree rank-one controls have:

```text
kappa_connect_exact = 1
```

At the same time, both classes have:

```text
STRUC-I mean_Ak = 1
STRUC-I min_Ak  = 1
```

So in rank one:

```text
same perturbative admissibility
different exact percolation scale
different algebraic route-closure status
```

This provides a concrete example of a **secondary structural signature** of the algebraic
free/nonfree distinction.

But it is not a universal classifier.

---

## 7. Higher-rank result: the rank-one pattern does not globalize

The affine systems do not preserve the same ordering.

For the frozen pilot corpus:

```text
AFF_FREE:
    median kappa_connect_exact ≈ 3.133
    mean   kappa_connect_exact ≈ 5.794

AFF_FAIL:
    median kappa_connect_exact ≈ 2.475
    mean   kappa_connect_exact ≈ 3.225
```

The route-closed affine class is therefore not uniformly easier to connect than the route-defective
affine class.

This rules out a simple global law such as:

```text
more algebraic route closure
    ->
lower percolation threshold
```

The rank-one relation is real within the tested controls, but it should not be promoted to a general
UNNS law.

---

## 8. Three structural coordinates now need to be distinguished

The combined projects support a cleaner UNNS architecture.

### Coordinate 1 — Algebraic route closure

Question:

```text
Can competing factorization routes be reconciled by an exact common refinement?
```

Native property:

```text
primal factor traceability
```

Failure means:

```text
exact route obstruction
```

### Coordinate 2 — Perturbative admissibility

Question:

```text
Does the ordered ladder remain inside its structural vulnerability budget under perturbation?
```

Native STRUC-I observable:

```text
A_kappa
```

Failure means:

```text
perturbative structural inadmissibility
```

### Coordinate 3 — Percolative connectivity scale

Question:

```text
At what normalized scale does the gap-vulnerability graph become connected?
```

Native retained observable:

```text
kappa_connect_exact
```

Difficulty means:

```text
larger connectivity scale
```

These coordinates can interact, but they are not equivalent.

The extension establishes:

```text
route closure
    !=
perturbative admissibility
    !=
percolation connectivity scale
```

---

## 9. Sharpened interpretation of a route defect

The parent project could already say:

> A non-refinement system contains a structural route defect.

The extension permits a sharper statement:

> **A route defect can exist inside a perturbatively admissible and eventually percolating
> structure.**

That means a route defect is not necessarily a collapse of the entire structural organization.

It is specifically an obstruction in the admissible routing of decomposition.

Other forms of structural organization can remain intact.

This is an important conceptual gain for UNNS because it separates:

```text
failure of one structural relation
from
failure of the structure as a whole
```

---

## 10. Refined UNNS failure taxonomy

The combined work supports at least three distinct failure notions.

### Route failure

```text
no exact common refinement
loss of primal factor traceability
```

### Admissibility failure

```text
perturbation-induced inversion load exceeds the allowed vulnerability budget
```

### Connectivity difficulty / failure within a chosen scale horizon

```text
gap-space graph remains fragmented or requires a larger normalized scale to connect
```

These should not be conflated.

A system may exhibit one without exhibiting the others.

---

## 11. What this adds to `UNNS_COMMON_REFINEMENT`

The extension does not alter the algebraic endpoint.

It adds five clarifications.

### A. It localizes the meaning of the route defect

The route defect is an exact decomposition-routing obstruction, not a synonym for generic structural
instability.

### B. It prevents overgeneralization

Non-refinement does not automatically mean non-admissibility or permanent fragmentation.

### C. It embeds common refinement into a broader structural state space

The parent result becomes one coordinate of a multidimensional UNNS structural description.

### D. It identifies a new secondary observable

`kappa_connect_exact` can carry structural information even when STRUC-I admissibility is saturated.

### E. It shows that secondary signatures can be domain-specific

The rank-one free/nonfree contrast appears cleanly in connectivity scale, while higher-rank affine
systems do not obey the same monotone relation.

---

## 12. Combined cross-project conclusion

The strongest justified combined statement is:

> **Primal factor traceability governs exact algebraic route closure, but route closure is not a
> universal proxy for structural admissibility or percolative connectivity. A system may be
> algebraically route-defective while remaining perturbatively admissible and eventually connected
> in gap space. The algebraic defect can nevertheless leave secondary geometric signatures, as the
> exact rank-one connectivity-scale contrast demonstrates.**

In compact form:

```text
UNNS_COMMON_REFINEMENT:
    identifies the exact law of algebraic route closure

UNNS_ADMISSIBILITY_PERCOLATION:
    locates that law inside a broader structural landscape
```

The combined lesson is therefore not that one chamber supersedes another.

It is that UNNS structure is **multi-coordinate**.

Exact routing, perturbative admissibility, and connectivity scale measure different aspects of how a
structure can persist, fail, or remain organized.

---

## 13. Recommended parent-project postscript

The following concise postscript can be added to the parent project's final synthesis:

> **Postscript — admissibility and percolation extension.** Subsequent frozen-chamber testing showed
> that exact loss of primal factor traceability does not, by itself, imply perturbative
> inadmissibility or failure of eventual gap-space connectivity. Route closure should therefore be
> treated as an independent structural coordinate rather than as a universal proxy for stability.
> In rank-one controls, however, the free/nonfree distinction produced a reproducible difference in
> exact connectivity scale, showing that algebraic route structure can leave secondary geometric
> signatures without determining admissibility. Higher-rank affine controls did not preserve the
> same monotone ordering, so that secondary relation is domain-dependent rather than universal.

---

## 14. Status

This synthesis closes the interpretive bridge between the two projects.

It does not claim a new algebraic theorem.

It records a cross-chamber empirical/structural result based on the frozen 30-system pilot and the
separately versioned percolation audit.

Future work, if pursued, should treat:

- bounded-scale percolation;
- exact connectivity-threshold geometry;
- component-growth profiles;
- route-closure status;

as separate but potentially interacting structural coordinates.
