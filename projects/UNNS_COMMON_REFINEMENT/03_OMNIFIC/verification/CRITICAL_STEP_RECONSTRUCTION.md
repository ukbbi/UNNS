# Critical Transfinite Step Reconstruction

This reconstruction uses only the theorem statements and the proof body of the audited Lean source,
not the prose proof guide.

Let

\[
\rho(x)
=
\operatorname{orderType}
(\text{nonzero support Archimedean classes of }x).
\]

The central theorem is:

```text
isPrimal_of_finite_classes_and_limit_tail_conditions
```

Its proof performs well-founded induction on \(\rho(x)\).

For a nonzero \(x\) at infinite support-class rank and a divisibility challenge

\[
x\mid bc,
\]

the proof chooses \(d\) so that

\[
xd=bc.
\]

It then invokes:

```text
exists_closed_class_refinement_at_support_class
```

to obtain an exact refinement at a quotient Archimedean class met by the support.

Next:

```text
exists_factor_with_smaller_support_class_orderType
```

produces

\[
x=t\,w
\]

with the strict inequality

\[
\rho(w)<\rho(x).
\]

The proof then invokes:

```text
exists_factor_refinement_of_closed_class_refinement
```

to transport the quotient/local split back to the ambient integer part, producing

\[
t=e_Af_A,
\qquad
e_A\mid b,
\qquad
f_A\mid c.
\]

The strict rank inequality makes the induction hypothesis applicable:

\[
\operatorname{IsPrimal}(w).
\]

Finally:

```text
exists_primalRefinement_of_factor_refinement
```

splices the transported factor split with primality of \(w\), yielding a primal refinement for
\(x\).

Therefore the induction closes and proves

\[
\operatorname{IsPrimal}(x)
\]

for every element.

## Audit conclusion

The central source-level transfinite step is internally coherent and follows the exact structural
spine claimed by the project:

\[
\text{local exact refinement}
+
\text{strict rank descent}
+
\text{ambient transport}
+
\text{inductive residual primality}
\Longrightarrow
\text{current primality}.
\]

This is a successful independent **source-level reconstruction**.

It is not yet an independent Lean re-formalization of the step.
