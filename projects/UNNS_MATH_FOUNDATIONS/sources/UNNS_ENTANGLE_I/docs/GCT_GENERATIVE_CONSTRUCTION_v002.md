# GCT v002 — Joint Generative Structure

The construction is deliberately minimal and exposes every assumed ingredient.

## Grammar (candidate, not canonical UNNS)

- **Alphabet** Σ: paired branch labels (+,+), (+,−), (−,+), (−,−), a joint parity z∈{±1}, and an unobserved common sign g∈{±1}.
- **Generation R:** choose a measurement context (a,b); update z with a context-dependent two-state refresh recursion.
- **Constraints C:** normalized probabilities; global sign symmetry; rotation/swap/axis-reversal covariance; perfect aligned anticorrelation; operational no-signalling.
- **Ordering O:** supply a,b → update joint parity → select global sign g → reveal local outcomes A=g and B=gz.

The word *admissibility* in this construction means that each nonzero joint event is allowed. It is deliberately weaker than a specified probability measure.

## Crucial missing selector

The transition law must be supplied with C(a,b). Different legitimate values of this function generate different correlations. Even the unique stationary distribution of each recursion does not yield a unique observable probability law across all contexts.

A candidate physical UNNS derivation would need to **derive C from independent generative rules**, rather than postulating it in the recursion. At present no source-grounded canonical UNNS rule is known here that makes this selection.

## Relationship to locality

The distribution of the independent source variable g and the update random seed may be measurement-independent. But the parity update jointly reads a,b. Therefore the resulting construction is not a Bell-local mechanism merely because both outcomes arise from one source. The use of a joint context is exposed rather than hidden.

No superluminal communication is claimed: operational no-signalling follows from unbiased marginals. This is not evidence that the physical mechanism is locally implementable.

## What the construction proves

A formal theorem about possible generative correlation rules, **not** a uniquely quantum mechanism, not a Born-rule derivation, and not evidence that UNNS has explained entanglement.
