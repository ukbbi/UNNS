# Data Plan

## 1. Principle

The first corpus must be built from **gauge-invariant physical observables** and must permit a meaningful refinement study.

The project should prefer data for which raw or near-raw numerical values, ensemble parameters, uncertainties, and lattice spacings are available.

## 2. Priority order

### Priority A — Glueball correlators / spectra

Why useful:

- direct connection to positive spectral masses;
- natural vacuum subtraction;
- exponential decay provides an explicit massive-vs-gapless deformation axis;
- several operator channels can provide representation robustness.

Desired fields:

- Euclidean separation/time;
- correlator value;
- covariance or uncertainty;
- lattice spacing;
- volume;
- coupling/action metadata;
- operator/channel;
- extracted mass where supplied.

### Priority B — Static potential / Wilson-loop derived observables

Why useful:

- gauge-invariant;
- natural scale-setting and confinement information;
- multiple lattice spacings often available;
- enables comparison with earlier UNNS confinement work.

Desired fields:

- separation;
- potential or force observable;
- uncertainty;
- lattice spacing;
- volume;
- action/coupling;
- scale-setting information.

### Priority C — Gauge-invariant flux-tube profiles

Why useful:

- links directly to prior UNNS boundary/closure work;
- supports spatial ladder construction;
- provides an independent representation from spectral correlators.

Desired fields:

- transverse/longitudinal coordinate;
- gauge-invariant field-energy or action-density observable;
- uncertainty;
- source separation;
- lattice spacing;
- volume.

## 3. Inclusion criteria

A dataset may enter the primary corpus only if:

- the observable is gauge-invariant or its gauge-independent physical status is explicitly justified;
- numerical values are recoverable reproducibly;
- ordering and units are known;
- essential lattice/ensemble metadata are available;
- a vacuum or asymptotic reference can be defined;
- the data can support at least one refinement comparison or can be paired with a compatible dataset that does.

## 4. Exclusion criteria

Exclude from the primary test:

- plots that cannot be digitized with adequate accuracy and have no tabulated source;
- isolated best-fit masses without underlying correlator or scale context;
- gauge-dependent field components used without a gauge-invariant bridge;
- data with unknown lattice spacing/volume when refinement interpretation depends on them;
- mixtures of incompatible actions or normalizations presented as one branch without an explicit conversion.

## 5. Raw-data policy

`data/raw/` is immutable.

No cleaned, rescaled, interpolated, or vacuum-subtracted file should overwrite a raw source file.

For each raw source, store or record:

- canonical filename;
- source citation/identifier;
- retrieval date;
- checksum where practical;
- license/usage note where relevant.

## 6. Derived-data policy

All transformations go to `data/derived/`.

Each derived table should record:

- source filename(s);
- transformation script/version;
- normalization;
- units;
- filtering;
- interpolation rule if used;
- uncertainty handling.

## 7. Ladder construction

Candidate ladder encodings include:

### Correlator ladder

\[
L_C = \{C(t_1),C(t_2),\ldots,C(t_n)\}
\]

after a frozen dimensionless normalization.

### Effective-mass ladder

\[
L_m = \{m_{\rm eff}(t_1),m_{\rm eff}(t_2),\ldots\}
\]

where the effective-mass definition is specified before comparison.

### Potential ladder

\[
L_V = \{V(r_1),V(r_2),\ldots,V(r_n)\}
\]

or a dimensionless force/Creutz-ratio representation.

### Profile ladder

\[
L_P = \{\rho(x_1),\rho(x_2),\ldots,\rho(x_n)\}.
\]

Multiple ladder encodings may be retained, but one encoding must be designated primary for each preregistered experiment.

## 8. First adversarial gapless construction

For a positive massive correlator that is well represented over a selected window by

\[
C(t)\sim A e^{-mt},
\]

construct a controlled family

\[
C_\lambda(t)
\]

with a gap proxy `m(λ)` decreasing toward zero while preserving:

- initial amplitude normalization;
- sample locations;
- noise model/covariance scale where feasible;
- monotonicity and positivity constraints appropriate to the chosen observable.

The transformation must be fully specified in the experiment record before the final target run.

A second adversary should later use a long-range/power-law tail rather than merely reducing an exponential mass parameter.

## 9. Metadata schema

Every primary data record should be mappable to:

```text
source_id
observable_class
theory_group
dimension
action
beta_or_coupling
lattice_spacing
volume
operator_channel
ordering_variable
value
uncertainty
units
vacuum_reference
notes
```

Fields not applicable to a dataset are explicitly marked, not silently dropped.

## 10. First acquisition target

The preferred first experiment is a published pure-gauge glueball correlator or spectral dataset with:

- more than one lattice spacing;
- documented volume;
- accessible numerical correlator values or reproducible tables;
- at least one clearly identified lowest positive mass channel.

This gives the cleanest initial bridge between a physical gap proxy and a structural ladder.
