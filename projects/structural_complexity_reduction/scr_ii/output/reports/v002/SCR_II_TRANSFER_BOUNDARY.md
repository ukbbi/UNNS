# SCR-II Transfer Boundary

## Statement

SCR-II v002 identifies an empirical transfer boundary for Structural Complexity Reduction:

> **A structural filter may be computationally valid only to the extent that the target set or observable to be preserved is structurally coupled to the grammar used for reduction.**

The v002 result does not prove this statement as a universal theorem. It establishes it as the operative boundary supported by the present SCR evidence.

## What crossed the boundary

The v002 arithmetic exact-solution predicate was deliberately generated independently of structural-filter survival.

The structural filter then achieved:

\[
R_{node,median} = 0.999405,
\]

and

\[
G_{time,median} = 151.691\times,
\]

but exact solution-set preservation failed in **30/30** primary cells.

Thus:

\[
\text{large search contraction} \not\Rightarrow \text{valid complexity reduction}.
\]

## Structural alignment as a necessary empirical condition

The relevant distinction is not simply between “structured” and “unstructured” problems. It is between:

### Aligned reduction

The pruning grammar and the target being preserved arise from, constrain, or measure the same underlying generative organization.

In that case, removal of structurally non-generable states may be legitimate.

### Unaligned reduction

The pruning grammar is imposed on a target defined independently of that grammar.

In that case, the filter has no reason to preserve the target set. SCR-II v002 demonstrates this regime directly.

## Formal decomposition

Let:

- \(S_N\) = nominal search space;
- \(S_G\) = states admitted by the structural grammar;
- \(S_T\) = target/solution set.

A structural filter returns approximately:

\[
S_{effective} = S_N \cap S_G.
\]

Valid exact-solution preservation requires:

\[
S_T \subseteq S_G,
\]

or, in approximate/observable settings, an explicitly preregistered preservation relation between \(S_T\) and \(S_G\).

SCR-II v002 deliberately removed that relation. Empirically,

\[
|S_T \cap S_G| \ll |S_T|.
\]

Across the 30-cell grid:

\[
|S_T| = 106,417,
\]

while only

\[
|S_T \cap S_G| = 17
\]

exact solutions were retained by the structural arm.

The weighted retained fraction is only **0.0160%**.

## Why this strengthens SCR rather than weakens it

Without SCR-II, a large pruning ratio could be misinterpreted as evidence that structural admissibility universally reduces computational complexity.

SCR-II rules out that interpretation.

The stronger SCR proposition is:

> **Structural Complexity Reduction is a relation between a frozen grammar and a target whose generative or dynamical organization is demonstrably connected to that grammar. It is not universal pre-computation pruning.**

This makes future SCR claims falsifiable.

## Operational requirement for future phases

Before claiming SCR in a new domain, the project should establish three independent objects:

1. a frozen structural grammar \(G\);
2. an independently measured or solved target \(T\);
3. a preregistered preservation relation \(P(G,T)\).

The target must not be constructed from the grammar merely to guarantee preservation, but neither should it be deliberately unrelated. The scientifically informative regime is **coupled but independently measured**.

## Recommended next phase

The next phase should move from synthetic arithmetic independence to a domain where:

- admissible states arise from a physical or generative mechanism;
- target observables are measured or solved independently;
- structural grammar is frozen without access to target outcomes;
- exact or tolerance-bounded preservation is testable;
- conventional problem-aligned controls are included.

That is the proper domain for testing whether SCR can produce genuine, transferable computational advantage.
