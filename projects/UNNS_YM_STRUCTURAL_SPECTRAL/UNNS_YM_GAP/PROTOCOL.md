# YM-0 Frozen Research Protocol

**Project:** UNNS Yang–Mills Gap / Vacuum Boundary Non-Crossability  
**Protocol version:** 0.1.0  
**Status:** initial freeze candidate

## 1. Research question

Can the absence of arbitrarily low positive-energy Yang–Mills excitations be represented in the UNNS Substrate as a **refinement-stable structural non-crossability boundary** around the vacuum?

The protocol is designed to distinguish four possibilities:

- a genuine refinement-stable structural obstruction;
- a numerical/lattice artifact;
- a representation-dependent structural effect;
- no detectable UNNS distinction between massive and gapless continuation.

## 2. Primary hypothesis

**H1 — Vacuum boundary non-crossability**

A physically admissible non-vacuum Yang–Mills branch cannot be continued arbitrarily close to the vacuum while remaining inside the same frozen UNNS admissibility grammar.

Operationally, the project searches for a positive structural separation

\[
D_{\rm YM}(X,V)\ge \delta>0
\]

that is stable under the predefined refinement program.

## 3. Competing hypothesis

**H0 — Structurally crossable vacuum**

For any proposed positive structural separation, an admissible sequence can be produced whose structural distance to the vacuum decreases toward zero under refinement without a stable UNNS rejection, collapse, or non-generability transition.

H0 is not treated as a weak fallback. It is an explicit adversarial target.

## 4. Unit of analysis

The basic unit is a **gauge-invariant ladder record** built from an ordered observable family.

A ladder is not a raw gauge field configuration. It is a reproducible ordered sequence derived from physical/gauge-invariant observables with documented:

- source ensemble or source publication;
- lattice or continuum parameters;
- physical units or dimensionless normalization;
- ordering variable;
- transformation applied before ladder construction;
- uncertainty information where available.

## 5. Initial observable classes

Eligible classes for YM-1 are:

1. Wilson-loop or Creutz-ratio families;
2. static quark–antiquark potential families;
3. glueball Euclidean correlators and extracted spectral masses;
4. gauge-invariant correlation-length observables;
5. flux-tube or field-energy profiles represented through gauge-invariant composites;
6. transfer-matrix or spectral quantities when the physical interpretation is explicit and reproducible.

A class is not included merely because it is numerically convenient.

## 6. Vacuum reference

The vacuum reference `V` must not be an arbitrary zero vector.

For every observable class, the protocol must document how the vacuum limit is represented. Permitted cases include:

- a mathematically known zero-connected-correlator limit after vacuum subtraction;
- a large-separation/asymptotic limit with explicitly defined normalization;
- a transfer-matrix ground-state reference;
- an empirically estimated vacuum baseline with uncertainty propagated.

If a meaningful vacuum reference cannot be defined for an observable class, that class cannot support the primary vacuum-boundary test.

## 7. Branch construction

Two branch families are required.

### 7.1 Physical branch

A branch derived from real Yang–Mills/lattice observables in a regime that supports finite correlation length or finite nonzero spectral mass.

### 7.2 Adversarial gapless branch

A synthetic or transformed family designed to approach a gapless limit while preserving as many non-gap-related properties of the physical branch as possible.

Adversarial construction may act on:

- correlation length;
- lowest positive spectral scale;
- exponential decay constant;
- long-range tail;
- dimensionless ratios tied to the candidate gap.

The construction must not simply inject random noise or destroy all structure.

## 8. Frozen chamber rule

`STRUC-I` is treated as canonical and is not modified to improve Yang–Mills separation.

Additional analyses may be introduced only as separate adapters, bridge diagnostics, or explicitly versioned auxiliary chambers. Their results must not retroactively redefine the canonical result.

## 9. Primary structural outcome

The central qualitative outcome is whether the attempted gapless continuation remains admissible under refinement.

The primary record for every branch/refinement level must contain:

- branch identity;
- observable class;
- refinement coordinates;
- ladder length;
- normalization;
- canonical chamber verdict;
- structural metrics exported by the canonical chamber;
- distance-to-vacuum proxy used in that experiment;
- uncertainty or resampling summary where defined.

## 10. Non-crossability criterion

A candidate non-crossability boundary is recorded only if all of the following hold:

1. the physical branch remains structurally stable across the specified refinement range;
2. the adversarial gapless branch exhibits a reproducible boundary event;
3. the event is not removed by a permitted change of ladder representation;
4. the event survives at least two independent refinement axes;
5. the inferred boundary location converges, plateaus, or remains positively separated from zero within uncertainty;
6. matched nulls do not reproduce the same effect at a comparable rate.

A one-resolution rejection is insufficient.

## 11. Representation-robustness requirement

At least two independently motivated gauge-invariant observable representations must eventually be tested.

A claim of Yang–Mills vacuum non-crossability may not rest entirely on a single observable family.

Cross-representation agreement means agreement in the **existence and refinement behavior of the obstruction**, not necessarily numerical equality of every UNNS metric.

## 12. Common-refinement requirement

For compatible ladder representations `L_a` and `L_b`, construct or identify a common refinement `R(L_a,L_b)` whenever the data permit.

The project asks whether admissibility classification and vacuum separation are preserved under the maps

\[
L_a \rightarrow R,\qquad L_b \rightarrow R.
\]

A boundary that changes sign, disappears systematically, or moves toward zero under common refinement fails the strong hypothesis.

## 13. Null controls

At minimum, later experimental phases must include:

- order-preserving value shuffles where meaningful;
- phase/randomization nulls for correlator-like data where mathematically legitimate;
- matched smooth massive surrogates;
- matched gapless surrogates;
- noise-amplitude controls;
- finite-size controls;
- normalization controls.

Nulls must be designed to answer a specific confound, not accumulated decoratively.

## 14. Evidence levels

### Level A — Structural indication
Massive and adversarial gapless families separate in the canonical chamber at one resolution.

### Level B — Refinement-stable structural boundary
The separation survives predefined refinement and null controls.

### Level C — Cross-representation non-crossability
The boundary is reproduced in multiple independent gauge-invariant observable families.

### Level D — Quantitative physical bridge
A controlled monotone relation is established between structural separation and a physical spectral/correlation scale.

### Level E — Mathematical mass-gap relevance
The bridge and continuum/refinement results are strong enough to imply a positive lower spectral bound under explicitly stated mathematical assumptions.

The project must state the achieved level and must not describe a lower level as a higher one.

## 15. Stop conditions

A branch experiment is stopped and recorded rather than repaired post hoc if:

- the observable loses its physical meaning under the proposed transformation;
- the vacuum baseline becomes undefined;
- the refinement procedure changes the quantity being tested;
- the canonical chamber input contract is violated;
- the gapless adversary becomes trivial or structurally unrelated to the physical branch.

## 16. Reproducibility

Every computational result must be reproducible from:

- immutable source identifiers or checksums where possible;
- a recorded preprocessing command;
- a versioned script;
- explicit random seed for stochastic nulls;
- a machine-readable run record;
- exported chamber result files.

## 17. What would constitute a successful YM-0 completion?

YM-0 is complete when one first experiment is frozen with:

- one real gauge-invariant observable family;
- one physical branch construction;
- one adversarial gapless construction;
- at least two refinement axes;
- one vacuum-distance definition;
- one matched null family;
- exact pass/fail criteria.

No target data should be tuned to improve those criteria afterward.
