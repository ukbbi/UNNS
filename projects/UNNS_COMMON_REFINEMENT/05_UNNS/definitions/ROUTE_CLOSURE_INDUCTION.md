# Well-Founded Route-Closure Induction

## Status

**Proved in this project as a narrow algebraic proposition.**

This is not a new replacement for pre-Schreier theory and not a new generic UNNS framework.
Its purpose is to isolate the smallest local-to-global proof principle that is actually shared by
our integer baseline and the audited Conway proof architecture, and to show exactly why the affine
failure systems cannot satisfy the same mechanism globally.

---

# 1. Algebraic setting

Let `M` be a commutative cancellative monoid.  Write divisibility multiplicatively.

An element `a` is **primal** if, whenever

\[
a\mid bc,
\]

there are `a_1,a_2` with

\[
a=a_1a_2,\qquad a_1\mid b,\qquad a_2\mid c.
\]

Assume a rank map

\[
\rho:M\to W
\]

into a set equipped with a well-founded strict relation `≺`.

Let `B\subseteq M` be a designated base regime.

---

# 2. Proposition

## Well-Founded Route-Closure Induction Proposition

Assume:

### Base closure
Every element of `B` is primal.

### Exact routed-block reduction
For every `a\notin B` and every divisibility

\[
a\mid bc,
\]

there exist elements

\[
t,w,e,f\in M
\]

such that

\[
a=tw,
\]

\[
t=ef,
\]

\[
e\mid b,\qquad f\mid c,
\]

and

\[
\boxed{\rho(w)\prec\rho(a).}
\]

Then every element of `M` is primal.
Consequently, in the cancellative commutative setting,

\[
\boxed{M\text{ has four-factor refinement}.}
\]

---

# 3. Proof

Proceed by well-founded induction on `rho(a)`.

Fix `a` and assume every element with strictly smaller rank is primal.
We prove `a` primal.

If `a\in B`, this is the base-closure hypothesis.

Now assume `a\notin B` and let

\[
a\mid bc.
\]

By exact routed-block reduction there are `t,w,e,f` with

\[
a=tw,\qquad t=ef,
\]

\[
e\mid b,\qquad f\mid c,
\]

and

\[
\rho(w)\prec\rho(a).
\]

Write

\[
b=e b_1,
\qquad
c=f c_1.
\]

Since `a\mid bc`, choose `q` with

\[
bc=aq.
\]

Substituting the decompositions gives

\[
e f b_1c_1=e f wq.
\]

Cancellation yields

\[
b_1c_1=wq,
\]

so

\[
w\mid b_1c_1.
\]

Because `rho(w)≺rho(a)`, the induction hypothesis says that `w` is primal.  Therefore

\[
w=w_1w_2
\]

with

\[
w_1\mid b_1,
\qquad
w_2\mid c_1.
\]

Hence

\[
a=tw=(ef)(w_1w_2)=(e w_1)(f w_2),
\]

while

\[
e w_1\mid b,
\qquad
f w_2\mid c.
\]

Thus `a` is primal.

Well-founded induction proves every element primal.  The established algebraic equivalence then
converts every-element primality into four-factor refinement. ∎

---

# 4. Additive translation used by the affine controls

For a commutative cancellative additive monoid, replace

`a | b*c`

by

`a <=_H b+c`,

replace factorisations by sums, and replace the routed block condition by

\[
a=t+w,\qquad t=e+f,\qquad e\le_H b,\qquad f\le_H c,\qquad \rho(w)\prec\rho(a).
\]

The same cancellation-and-induction proof applies verbatim.  This is the form relevant to the
rank-one and higher-rank affine failure systems in this project.

---

# 5. Why this is not just a renaming of pre-Schreier

The conclusion

\[
\forall a\;\operatorname{IsPrimal}(a)
\]

is exactly the pre-Schreier/decomposition-monoid state relevant to four-factor refinement.
The proposition does **not** claim a new characterization of that state.

Its additional content is proof-theoretic and structural:

\[
\boxed{
\text{primal base}
+
\text{exact routed local block}
+
\text{strictly lower residual rank}
\Longrightarrow
\text{global primality}.
}
\]

It identifies a sufficient mechanism for obtaining the surviving algebraic property.

The distinction matters because the project has explicit non-refinable systems in which:

- many individual elements are nevertheless primal;
- rank-one defects eventually disappear above a conductor;
- higher-rank affine defects can propagate forever along a ray.

Therefore “some local primality” or “eventual primality” is not enough.  The proposition requires a
repair step for **every non-base divisibility**, plus irreversible descent to a base that is already
route-closed.

---

# 6. Ordinary integers as the immediate-repair realization

For positive integers, take the base

\[
B=\{1\}
\]

and let

\[
\rho(a)=\Omega(a),
\]

the total number of prime factors counted with multiplicity.

Given

\[
a\mid bc,
\]

let

\[
e=\gcd(a,b),\qquad f=a/e.
\]

Writing `b=e b_1`, one has

\[
\gcd(f,b_1)=1.
\]

Since `a|bc`, cancellation gives `f|b_1c`; coprimality then forces

\[
f\mid c.
\]

Now choose

\[
t=a,
\qquad
w=1.
\]

Then

\[
t=ef,
\qquad
 e\mid b,
\qquad
 f\mid c,
\]

and, for `a>1`,

\[
\rho(1)=0<\rho(a).
\]

Thus the integer mechanism satisfies the proposition in one step: the residual is already the unit.

This recovers the project baseline

`gcd decomposition -> coprime residuals -> forced cross-routing`

as an **immediate-repair** instance of the induction principle.

---

# 7. Rank-one failure systems

For a nonfree rank-one affine/numerical monoid, the project proved:

- global refinement fails;
- the non-primal set is finite;
- every sufficiently large element is primal.

So the system contains a large route-closed region, but some finite obstruction core survives.

That means the route-closure induction hypotheses cannot hold globally.
At least one non-primal core element must fail the exact routed-block reduction to a strictly lower
residual ending in a primal base.

This is the precise reason that

\[
\text{cofinal primality}
\not\Rightarrow
\text{global route closure}.
\]

The conductor removes new large-scale defects, but it does not repair the residual finite core.

---

# 8. Higher-rank affine failure systems

For positive affine monoids with

\[
\operatorname{rank}H\ge2,
\qquad
\operatorname{ARD}(H)>0,
\]

the project proved the persistent defect-ray theorem:

\[
\exists a,\rho\ne0\quad
\forall n\ge0:
\quad a+n\rho\notin P(H).
\]

Thus non-primality can propagate indefinitely while remaining inside legitimate monoid directions.

By the proposition's contrapositive, no global choice of:

- primal base,
- exact routed-block reduction for every non-base obstruction, and
- well-founded strictly decreasing residual rank

can exist for such a monoid.

The defect ray is therefore a concrete obstruction to the **mechanism**, not merely to the final
pre-Schreier state.

---

# 9. Omnific candidate proof as the transfinite realization

At audited source commit

`264445c93b78554c408e99e4e7f663693b4e91ab`,

the candidate Conway proof has exactly the ingredients needed by the proposition, in a much more
technical realization.

Use as structural rank the order type of the nonzero Archimedean support classes.

The source supplies:

1. **base closure** — finite support-class elements are primal;
2. **exact local route repair** — exact refinement at a quotient support class;
3. **retained-block factorisation** — factor off the resolved closed-class block;
4. **strict residual descent** — the complementary factor has strictly smaller support-class order type;
5. **ambient routing** — quotient factors are transported back to ambient divisibility;
6. **splice** — local routed factors plus primality of the residual reconstruct primality of the original element.

The proposition therefore captures the algebraic induction skeleton of the source-level proof without
replacing its analytic/order-theoretic hypotheses.

It does **not** assert that Cauchy completeness, common-tail fraction-field control, convex support,
or the transport lemmas are dispensable.  Those source facts are precisely what establish the
abstract routed-block premise in the concrete Hahn/omnific setting.

---

# 10. UNNS statement

The narrow UNNS conclusion supported by the project is now:

\[
\boxed{
\begin{gathered}
\text{endpoint divisibility}\
+\ \text{exact ambient route repair on a retained block}\
+\ \text{strict well-founded descent of the unresolved residue}\
+\ \text{route-closed terminal regime}
\\[1mm]
\Longrightarrow\ \text{global factor traceability}\
\Longrightarrow\ \text{common refinement}.
\end{gathered}}
\]

This is stronger as an explanatory structural principle than simply saying “every element is
primal,” because it identifies a sufficient mechanism by which that state can be forced.

But the algebraic invariant itself remains unchanged:

\[
\boxed{
\text{global route closure}
\iff
\text{every-element primality}
}
\]

in the relevant cancellative setting.

The project should therefore keep two layers distinct:

- **surviving property:** primal/pre-Schreier factor traceability;
- **route-closure mechanism:** exact local repair + strict well-founded residual descent + primal base + ambient reconstruction.

That separation is the final answer to the original Conway/UNNS comparison question at the present
stage.

---

# 11. Lean realization

The proposition above is now mirrored by:

`04_PROOF_MAP/lean/RouteClosureInduction.lean`.

The formalization deliberately uses the same algebraic objects as the audited Conway source rather
than introducing a second UNNS-specific refinement predicate.

Its formal interface is:

```text
HasWellFoundedRouteClosure
  + WellFounded r
  -> forall a, IsPrimal a
  -> HasFourFactorRefinement R
```

The proof's splice step is the Conway repository theorem
`exists_primalRefinement_of_factor_refinement`, and the final conversion is
`hasFourFactorRefinement_iff_forall_isPrimal`.

Because the source theorem is formulated for `CommMonoidWithZero` with `IsCancelMulZero`, the Lean
version explicitly places `0` in the base regime.  This is the formal zero-case counterpart of the
prose proposition's cancellative-monoid setting.

The formal source is locked to commit:

`264445c93b78554c408e99e4e7f663693b4e91ab`.

The present runtime does not provide Lean/lake, so this file is recorded as source-interface aligned
but not kernel-compiled here.  See `outputs/reports/LEAN_ROUTE_CLOSURE_REPORT.md` for the exact
verification status and compile command.
