# Conway Defect-Channel Audit

## Scope and source lock

This audit answers the current project question:

> Which concrete source-level obligations in the candidate Conway proof prevent an analogue of the affine persistent defect ray from surviving through quotient, descent, and transport?

Source repository:

`https://github.com/gaearon/conway-refinement`

Audited commit:

`264445c93b78554c408e99e4e7f663693b4e91ab`

Verified on 2026-09-19: the repository's `main` branch still points to this exact commit.  The analysis below therefore does **not** mix a newer source state into the existing project audit.

The repository author continues to describe the development as candidate / not completed mathematical work.  Accordingly, this file records the structure of the Lean development and the UNNS comparison; it does not claim independent community validation of Conway's conjecture.

## Important interpretive boundary

The Lean source does not use the phrases **persistent defect ray**, **defect channel**, or **UNNS route closure**.  Those phrases belong to this project.

What the source actually proves, under its stated hypotheses, is a chain of exact refinement, factorisation, strict support-class descent, primality, and transport statements.  The claim that this chain *blocks the analogue of a persistent defect channel* is a structural interpretation of those source-level obligations.

---

# 1. The finite obstruction we now have to compare against

The affine theorem established inside this project gives, for every positive affine monoid of rank at least two with `ARD(H)>0`, an atom `a` and nonzero direction `rho` such that

`a + n rho`

is non-primal for every `n>=0`.

The mechanism has three defining features:

1. an exact local non-refinement witness exists;
2. translation by `rho` preserves the obstruction;
3. the obstruction can therefore remain at unbounded structural distance without ever being forced into a simpler terminating regime.

The source-level Conway comparison should therefore ask four questions at every recursive step:

- Is there an **exact local refinement**, or can a local defect remain unresolved?
- Does the residual object have **strictly smaller structural rank**, or can the defect propagate at the same rank?
- Is the terminal/base regime already **primal**, or can a finite residual bad core survive?
- Does the local result **transport back to the ambient object**, or can the defect disappear only in a quotient and return after lifting?

The audited Lean spine answers all four.

---

# 2. Source-level blocker stack

## Blocker A — finite-class primality removes a residual finite bad core

**Proof-map node:** (142) *Primality for finitely many Archimedean support classes*  
**Lean declaration:** `isPrimal_of_supportArchimedeanClasses_finite`  
**File:** `ConwayRefinement/HahnSeries/IntegerPart/FiniteClassPrimality.lean`

The file explicitly states that the proof inducts on the number of Archimedean classes met by the support.  At the leading class it splits the series into a reduced factor and a strict lower-class factor; the reduced factor is primal and the lower factor has fewer support classes and is primal by induction.

Structural function:

`finite support-class complexity -> primal`

This is the precise place where the rank-one analogue of a surviving finite non-primal core is excluded.  In our numerical-monoid controls, conductor saturation gives an eventually primal tail but leaves finitely many bad elements.  Here the finite-class endpoint of the recursion is not merely "small" or "bounded": it is proved **primal**.

**Defect-channel consequence:** a descending obstruction cannot terminate in a finite support-class residue that remains non-primal.

---

## Blocker B — Cauchy-complete common-tail quotients give exact local refinement

**Proof-map node:** (156) *Exact refinement over a Cauchy-complete common-tail quotient*  
**Lean declaration:** `exists_closed_class_refinement_of_complete_tail_quotient`  
**File:** `ConwayRefinement/HahnSeries/IntegerPart/Refinement/LimitTailRefinement.lean`

The source first obtains a cardinal-bounded germ refinement and then restricts at a suitable closed Archimedean ball so that the four refinement equations hold **exactly** there.

Structural function:

`quotient equality + completeness -> exact refinement at a closed class`

This matters because an affine defect ray is sustained by an equality that remains non-refinable at every translated position.  At the selected quotient class, the Conway machinery does the opposite: it constructs an exact four-factor refinement rather than merely an approximate or germ-level compatibility statement.

**Defect-channel consequence:** at the selected structural class, the obstruction is not allowed to persist as an unresolved endpoint equality.

---

## Blocker C — support-class refinement selects a class actually met by the factor

**Proof-map node:** (157) *Refinement at a quotient Archimedean class*  
**Lean declaration:** `exists_closed_class_refinement_at_support_class`  
**File:** `ConwayRefinement/HahnSeries/IntegerPart/Refinement/SupportClassRefinement.lean`

This theorem regroups along the common tail, uses cofinality of the support classes in the quotient, invokes the complete-tail refinement, and normalizes the resulting factors back inside the bounded Hahn integer part.  Crucially, the chosen class is met by the support of the factor being analysed.

Structural function:

`local exactness -> exactness on an occupied structural block`

This prevents the proof from resolving an irrelevant quotient class while leaving the actual support obstruction untouched.

**Defect-channel consequence:** the local repair is attached to a genuine occupied block of the object whose primality is being proved.

---

## Blocker D — factorisation converts local repair into strict structural progress

**Proof-map nodes:**

- (153) *Factorisation at a quotient Archimedean class*
- (152) *Strict decrease of support-class order type*

**Lean declarations:**

- `exists_factor_with_smaller_support_class_orderType`
- `Nonpositive.orderType_nonzeroSupportArchimedeanClasses_lt`

**Files:**

- `ConwayRefinement/HahnSeries/IntegerPart/Refinement/SupportClassFactorization.lean`
- `ConwayRefinement/HahnSeries/SupportArchimedeanClasses.lean`

The retained closed-class restriction is factored off.  The complementary factor `w` is proved to have strictly smaller order type of nonzero Archimedean support classes.

Structural function:

`retain resolved block -> residual rank strictly decreases`

This is the sharpest contrast with the affine persistent ray.  In the affine theorem, translation by `rho` preserves the sign obstruction while allowing the bad family to continue indefinitely.  Here the recursive residual is not permitted to remain at the same support-class complexity:

`rank(w) < rank(a)`.

The induction rank is an ordinal, so a recursive bad channel cannot preserve its rank indefinitely.

**Defect-channel consequence:** there is no source-level analogue of a tangent direction along which the same unresolved structural complexity can be carried forever.

---

## Blocker E — ambient transport prevents a quotient-only repair

**Proof-map node:** (147) *Transport of refinement from a quotient Archimedean class*  
**Lean declaration:** `exists_factor_refinement_of_closed_class_refinement`  
**File:** `ConwayRefinement/HahnSeries/IntegerPart/Refinement/ClosedClassRefinementTransport.lean`

The source identifies the closed quotient-class restriction with an ambient convex restriction, confines the relevant factors to the retained subgroup, and then obtains ambient divisibility of the corresponding right-hand factors.

Structural function:

`quotient refinement -> retained ambient factorisation/divisibility`

This is essential.  Without it, the quotient could be locally refinable while the original ambient equality remained non-refinable.  Such a gap would be exactly where a hidden defect channel could survive the projection/lift cycle.

**Defect-channel consequence:** local resolution is not discarded when returning to the ambient integer part.

---

## Blocker F — the residual cofactor is made primal by well-founded induction

**Proof-map node:** (158) *Transfinite extension of finite-class primality*  
**Lean declaration:** `isPrimal_of_finite_classes_and_limit_tail_conditions`  
**File:** `ConwayRefinement/HahnSeries/IntegerPart/LimitTailPrimality.lean`

The file states its proof architecture directly:

- finite support-class case: primal by hypothesis;
- otherwise split the classes into a nonzero limit initial segment and a finite final segment;
- obtain exact refinement at a quotient class;
- factor off the retained block;
- the complementary factor has strictly smaller support-class order type;
- apply the induction hypothesis to make that complementary factor primal;
- transport the local refinement to the ambient integer part.

Structural function:

`exact local block + strict ordinal descent + primal base -> primal residual closure`

**Defect-channel consequence:** even if an obstruction were imagined to migrate to the residual cofactor after resolving one class, it is forced into a strictly smaller ordinal rank, and the well-founded induction eventually reaches the already-primal finite-class base.

---

## Blocker G — splice the retained factor refinement with primality of the residual factor

**Lean declaration:** `exists_primalRefinement_of_factor_refinement`  
**File:** `ConwayRefinement/Algebra/Divisibility/Refinement.lean`

This generic algebraic lemma takes:

- a factorisation `a = t*w`;
- a refinement of the retained factor `t` across the two branches;
- primality of the complementary factor `w`;

and splices them into a primal refinement for the original divisibility problem.

Structural function:

`resolved retained block + primal residual -> resolved original factor`

This closes the recursive step.  The proof does not merely show that some lower-rank object is primal; it reconstructs primality at the original rank.

**Defect-channel consequence:** descent is not an escape from the original problem.  The lower-rank solution is reassembled into the original structural level.

---

## Blocker H — every element primal is converted to global four-factor refinement

**Lean declarations:**

- `hasFourFactorRefinement_iff_forall_isPrimal`
- `hasFourFactorRefinement_of_decompositionMonoid`

**File:** `ConwayRefinement/Algebra/Divisibility/Refinement.lean`

At the omnific endpoint:

**Lean declarations:**

- `signedSmallSupportIntegerPart_isPrimal`
- `signedSmallSupportIntegerPart_decompositionMonoid`
- `conwayRefinement`

**File:** `ConwayRefinement/Surreal/OmnificInteger/Refinement/ConwayRefinement.lean`

The candidate proof first proves every element of the signed small-support Hahn integer part primal, packages that as a `DecompositionMonoid`, obtains four-factor refinement, and transports it through the signed normal-form equivalence to the omnific-integer formulation.

Structural function:

`elementwise route traceability -> global common refinement -> Oz transport`

**Defect-channel consequence:** once every element is primal, the algebraic equivalence established in the repository rules out any remaining four-corner non-refinement witness in the target structure.

---

# 3. The exact comparison with the affine persistent defect ray

| Affine persistent defect mechanism | Conway candidate mechanism |
|---|---|
| exact non-refinement witness exists | exact local refinement is produced at a selected support class |
| translation preserves the obstruction | factorisation forces strict decrease of support-class order type |
| bad family can remain at the same structural complexity | recursive cofactor cannot remain at the same ordinal rank |
| no terminal repair is forced | finite support-class base is primal |
| obstruction survives in the ambient monoid | quotient refinement is transported back to ambient divisibility |
| therefore an infinite non-primal ray survives | induction + splice prove the original element primal |

The crucial distinction is not simply **finite versus transfinite**.  It is:

`rank-preserving defect propagation`

versus

`exact local repair + strictly rank-decreasing residual + primal base + ambient reconstruction`.

That is the strongest source-grounded answer currently available to the project's central comparison question.

---

# 4. What each hypothesis is doing

The source audit now lets us assign specific structural jobs rather than treating the hypotheses as one undifferentiated technical package.

### Finite-class primality
Prevents a terminal finite obstruction core.

### Cauchy completeness of the common-tail quotient
Supplies the local refinement mechanism at limit support complexity.

### Common-tail fraction-field condition
Lets the quotient refinement be normalized inside the bounded integer part rather than only in a larger ambient field.

### Cofinality / occupied support-class selection
Ensures the refined block is structurally relevant to the series under analysis.

### Strict support-class order-type decrease
Provides irreversible progress of the recursion.

### Convex-support and transport lemmas
Prevent the local solution from being an artefact of quotienting.

### Primality/refinement splice
Reconstructs the original factor from the resolved block and lower-rank residual.

No one of these alone is the surviving property.  The surviving property remains **primality / pre-Schreier factor traceability**.  These are the source-level mechanisms that establish it in the omnific setting.

---

# 5. Revised UNNS conclusion

The earlier project formulation

`well-founded descent + route traceability -> common refinement`

was too compressed, because it did not explain why an obstruction cannot persist at a limit stage or survive projection/lifting.

The source-grounded formulation is now:

`exact local refinement`

`+ retained-block factorisation`

`+ strict well-founded residual descent`

`+ primal terminal/base regime`

`+ ambient transport and splice`

`=> global primal traceability`

`=> four-factor refinement`.

In compact UNNS language:

> **Persistent route defects are excluded when every occupied structural obstruction admits an exact local resolution whose unresolved residue is forced to lower well-founded rank, the terminal regime is already route-closed, and the local resolution transports back to the ambient structure.**

This is an **interpretive proposition extracted from the audited proof architecture**, not a new theorem claimed independently of its concrete hypotheses.

---

# 6. What has now been answered

The question posed after the affine defect-ray theorem was:

> Where, concretely, does the Conway proof prevent an analogous persistent non-primal channel from surviving?

The answer is not one line of Lean.  It is a closed source-level loop:

`finite-class primality`

`-> exact common-tail quotient refinement`

`-> support-class selection`

`-> retained-block factorisation`

`-> strict order-type decrease`

`-> ambient transport`

`-> primal residual by induction`

`-> splice`

`-> every element primal`

`-> four-factor refinement`.

The affine ray survives because it has a direction along which the obstruction is invariant.  The candidate Conway proof supplies no analogous rank-preserving recursive direction: every recursive residual is forced to strictly lower support-class order type, and the descent terminates in a primal base.

That is the concrete structural difference the project was looking for.
