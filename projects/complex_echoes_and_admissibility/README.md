# Complex Echoes and Admissibility

**ESC-I — Echo–Admissibility Correspondence Chamber I**

**UNNS Substrate | Mathematical Research and Experimental Validation**

Research manuscript: **Recursive Projection and Structural Admissibility: From Complex Echoes to Predictive Boundaries** (13 October 2026)

## Overview

This project investigates complex-number representations, recursive echo dynamics, and projection-dependent structural admissibility within the UNNS (Unbounded Nested Number Sequences) Substrate.

It develops two earlier UNNS investigations:

1. *Complex Numbers in the UNNS Substrate: Derived Convenience or Foundational Necessity?*
2. *Quadratic Roots Without Complex Numbers via UNNS Echo Cycles*

The original research proposed interpreting complex multiplication, oscillation, and phase through real recursive operators, cyclotomic structures, and lattice inlaying.

ESC-I extends that mathematical setting by asking:

- Which recursive trajectories are periodic, bounded, convergent, or divergent?
- When does finite numerical observation disagree with exact mathematical classification?
- Under which conditions do phase transformations preserve structural behavior?
- How can lattice rounding, collapse, clipping, or state-dependent projection change the fate of a recursive trajectory?
- Can some projected regimes be predicted from explicit structural conditions without simulating the full trajectory?

ESC-I is a focused mathematical experiment, not a replacement for the existing UNNS canonical framework.

## Mathematical Foundation

Complex multiplication can be represented through real two-dimensional operators:

$$
a+bi \longleftrightarrow
\begin{pmatrix}
a & -b\\
b & a
\end{pmatrix}.
$$

The imaginary unit corresponds to the quarter-turn operator

$$
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix},
\qquad J^2=-I.
$$

This establishes an exact real representation of complex multiplication.

ESC-I distinguishes finite cyclotomic phases, bounded nonperiodic rotations, and lattice-projected dynamics.

The main recursive model is

$$
x_{n+1}=\Pi(Tx_n),
$$

where:

- $T$ is a real recursive operator;
- $x_n$ is the current state;
- $\Pi$ is a specified projection, quantization, threshold, clipping, or gating operation.

The resulting structural regime depends on the complete system $(T,\Pi,x_0)$, not necessarily on the spectrum of $T$ alone.

## Research Components

### 1. Echo Classification

The ESC-I chamber provides an exact classifier using rational arithmetic and a finite-horizon trajectory observer.

The initial 15-case benchmark produced:

| Result | Cases |
|---|---:|
| Exact–echo agreement | 13 |
| Echo misses genuine divergence | 1 |
| Echo incorrectly reports periodicity | 1 |

The two disagreements are intentionally constructed observational traps.

The horizon trap demonstrates how a weakly divergent recurrence may appear bounded during finite observation.

The resolution trap demonstrates how a bounded nonperiodic rotation may appear periodic when its per-period residual falls below numerical tolerance.

### 2. Mathematical Theorem Audit

ESC-I revisits the projected-stability and phase-inletting statements of the original complex-number manuscript.

**Theorem A — Phase Inletting**

Distinguishes similarity transformations, commuting phase operators, and more general left-multiplication transformations.

It characterizes real two-dimensional operators for which spectral radius is invariant under planar phase multiplication.

**Theorem B — Projected Growth**

Establishes conditional growth results using explicit perturbation bounds, invariant cones, and an escape radius.

For a dominant expanding eigen-coordinate, a sufficient escape condition is

$$
|u_0|>\frac{h}{|\lambda|-1}.
$$

This is a sufficient guarantee, not a necessary condition for every projected trajectory.

The corrected mathematical statements are accompanied by counterexamples demonstrating why the original unrestricted forms require additional hypotheses.

### 3. Structural Admissibility Rules

The `admissibility.py` module implements rules AR-1, AR-2, and AR-3, followed by the corrected AR-3.1.

The protocol includes frozen rule definitions, SHA-256 hashes, deterministic seeds, exact comparisons, recorded disagreements, and independently generated confirmation cases.

**AR-3.1 confirmation:**

| Measure | Result |
|---|---:|
| Fresh cases | 3,600 |
| Agreements | 2,148 |
| Disagreements | 0 |
| Abstentions | 1,452 |
| Per-step bound violations | 0 |

The original AR-3 quantization conversion was falsified in 92 cases and remains preserved in the historical record.

The corrected AR-3.1 conversion includes the required dominant-eigenvalue factor. Its cone condition is sufficient but conservative.

### 4. Projection Route Dependence — PRD-1

PRD-1 investigates projection-aware prediction in a restricted two-dimensional spectral frame.

Projection families include:

- Dead-zone thresholding
- Saturation and clipping
- Lattice rounding
- State-gated zeroing
- Linear kernel projections as controls

**Primary results:**

| Measure | Result |
|---|---:|
| Nonlinear cases | 4,197 |
| Rule R predictions issued | 3,978 |
| Analytically supported | 3,159 |
| Finite-horizon-consistent only | 819 |
| Abstentions | 219 |
| Observed contradictions | 0 |

The projection-aware classical comparator issued 1,778 certified predictions. Its lower coverage reflects its restricted access to projection information, not an inherent limitation of classical mathematics.

Rule R evaluates closed-form conditions without step-by-step orbit simulation. The experiment does not establish superiority over classical analysis using equivalent information.

The original PRD-1 comparator mapping error, subsequent correction, and exploratory fresh-seed results remain documented.

### 5. Independent Verification

ESC-I includes separately implemented verification scripts.

**AR-3.1:** The independent checker tests the corrected quantization bound without importing the main chamber modules.

**PRD-1:** The standalone checker independently implements the tested projection families and their prediction conditions.

The independent PRD-1 sample contains:

| Component | Cases |
|---|---:|
| Nonlinear cases | 1,600 |
| Nonlinear predictions checked | 1,525 |
| Nonlinear abstentions | 75 |
| Linear controls | 800 |
| Total cases | 2,400 |
| Contradictions | 0 |

Independent implementation and exact finite-horizon corroboration do not constitute formal proof of every asymptotic assertion or independent scientific peer review.

## Project Structure

```text
complex_echoes_and_admissibility/
├── admissibility.py
├── chamber.html
├── esc_i.py
├── independent_check_ar31.py
├── test_esc_i.py
├── RUN_EXAMPLE.bat
├── README.md
├── REPRODUCE.md
├── output/
├── PRD1_VERIFY/
└── synthesis/
```

**Main components**

- `esc_i.py` — exact rational classifier, echo observer, and experimental challenges.
- `admissibility.py` — theorem audit, admissibility rules, AR-3.1 confirmation, and PRD-1.
- `chamber.html` — interactive offline experimental interface.
- `test_esc_i.py` — automated chamber tests.
- `independent_check_ar31.py` — independent quantization-bound verification.
- `PRD1_VERIFY/` — standalone independent PRD-1 verification package.
- `output/` — numerical reports and experimental records.
- `synthesis/` — synthesis manuscript, scientific figures, generation scripts, and supporting records.
- `REPRODUCE.md` — detailed reproduction instructions.

Generated Python cache files are not research artifacts and need not be version-controlled.

## Reproduction

The core chamber uses Python and its standard library.

From the project root, run:

```bat
python test_esc_i.py
```

Run the original echo experiment:

```bat
python esc_i.py
```

Run the admissibility experiments:

```bat
python admissibility.py --out output
```

Run the independent AR-3.1 checker:

```bat
python independent_check_ar31.py
```

For independent PRD-1 verification:

```bat
cd PRD1_VERIFY
python independent_check_prd1.py
```

The interactive chamber can be opened locally using `chamber.html`.

The synthesis figures are generated using `synthesis/make_figures.py`, which requires Matplotlib.

Consult `REPRODUCE.md` and the individual verification README for the complete procedures, dependencies, seeds, expected outputs, and interpretation of each verification level.

## Synthesis Manuscript

**Recursive Projection and Structural Admissibility: From Complex Echoes to Predictive Boundaries**

UNNS Research Collective, 13 October 2026.

The 25-page synthesis includes:

- The original complex-number research context
- Real recursive representations and phase structure
- Exact echo classification
- Mathematical theorem audit and corrected results
- ESC-I chamber architecture
- Structural admissibility rules
- PRD-1 experiments
- Independent verification
- Relationship to canonical UNNS research
- The complex-number question revisited
- Limitations and open questions
- Mathematical proofs, counterexamples, and reproducibility records

Six original scientific figures illustrate the mathematical representations, dynamical regimes, observational traps, projection-dependent routing, and PRD-1 coverage.

The manuscript and supporting materials are maintained in `synthesis/`.

## Relationship to Canonical UNNS Research

ESC-I is part of the broader UNNS Substrate research program.

Its admissibility certificates are mathematically distinct from the predicates implemented by the canonical structural instruments.

**STRUC-I v1.0.4**

Evaluates perturbative ladder admissibility using rank inversions and vulnerability-derived budgets.

**STRUC-PERC-I v2.5.0**

Investigates full pairwise vulnerability-graph connectivity, spanning, and fragmentation across scale intervals.

**ESC-I**

Classifies and certifies selected properties of projected recursive trajectories.

The three instruments share a conceptual emphasis on generative routes, boundaries, and structural persistence, but do not implement interchangeable mathematical predicates.

ESC-I establishes no equivalence between projected-orbit classifications, STRUC-I ladder admissibility, and STRUC-PERC-I connectivity.

Its results should not be interpreted as independent confirmation of the Universal Structural Law or as closing the open percolation-to-admissibility sufficiency question.

### Canonical Reference Sources

UNNS canonical results:

https://github.com/ukbbi/UNNS/tree/33f8d542483bb4dca5375c3ac72f233779fe304f/canonical

Universal Structural Law / STRUC-I corpus:

https://github.com/ukbbi/UNNS/tree/33f8d542483bb4dca5375c3ac72f233779fe304f/universal-structural-law-struc-i-corpus

STRUC-I v1.0.4 source:

https://github.com/ukbbi/UNNS/blob/33f8d542483bb4dca5375c3ac72f233779fe304f/projects/UNNS_YM_STRUCTURAL_SPECTRAL/UNNS_VACUUM_CONTINUITY/chambers/struc_i_v104.html

STRUC-PERC-I v2.5.0 source:

https://github.com/ukbbi/UNNS/blob/33f8d542483bb4dca5375c3ac72f233779fe304f/projects/UNNS_COMMON_REFINEMENT/chambers/STRUC-PERC-I/struc_perc_i_v2_5_0.html

Axis V admissibility-gate methodology:

https://github.com/ukbbi/UNNS/blob/33f8d542483bb4dca5375c3ac72f233779fe304f/canonical/axis_v_admissibility_gate/axis_v_methodology_guide.md

Common Refinement:

https://github.com/ukbbi/UNNS/tree/33f8d542483bb4dca5375c3ac72f233779fe304f/projects/UNNS_COMMON_REFINEMENT

## Original Complex-Number Research

**Complex Numbers in the UNNS Substrate: Derived Convenience or Foundational Necessity?**

https://ukbbi.github.io/UNNS/docs/unns-complex_numbers/Complex%20Numbers%20in%20the%20UNNS%20Substrate.pdf

**Quadratic Roots Without Complex Numbers via UNNS Echo Cycles**

https://ukbbi.github.io/UNNS/docs/unns-complex_numbers/Quadratic%20Roots%20Without%20Complex%20Numbers%20via%20UNNS%20Echo%20Cycles.pdf

These papers provide the foundational motivation for ESC-I. The later chamber refines specific mathematical statements while preserving the original research direction.

## Scientific Significance

ESC-I demonstrates that exact recursive classification and projection-dependent structural prediction can be studied using explicit mathematical rules, controlled counterexamples, and reproducible computational verification.

Its principal contributions are:

1. A systematic distinction between complex representation, exact recurrence, and finite observational echo behavior.
2. Corrected hypotheses for phase invariance and projected growth.
3. Quantitative conditions for escape and invariant-cone persistence.
4. Projection-aware predictions for several nonlinear operator families.
5. A preserved research history documenting falsification, correction, confirmation, and independent corroboration.
6. A specialized mathematical connection between complex-number representations and the wider UNNS route-and-boundary interpretation.

These results are compatible with established algebra, dynamical-systems theory, numerical analysis, and perturbation theory. They do not establish a new universal mathematical or physical law.

## Open Research Questions

The principal foundational question remains:

**Can complex-compatible algebraic structure emerge from independently specified UNNS generative-admissibility constraints without assuming a rotation operator or complex structure in advance?**

Additional open directions include:

- Necessary and sufficient projection-persistence conditions.
- Higher-dimensional recursive operators.
- Jordan blocks and complex dominant spectral pairs.
- Family-independent orbit-regime certificates.
- Formal verification of generalized results.
- Explicit mathematical bridges between projected recurrences and canonical UNNS ladder admissibility.

The completed ESC-I experimental cycle supplies a reproducible foundation for such future work without treating unresolved questions as established results.

## Research Status

**ESC-I experimental cycle: completed.**

The synthesis manuscript consolidates the mathematical audit, corrected results, experimental evidence, historical falsifications, and independent verification.

The present findings are established within their stated mathematical and computational domains. Generalized generative-selection and cross-instrument equivalence claims remain open.

---

**UNNS Substrate Research Program**

https://unns.tech

Repository: https://github.com/ukbbi/UNNS
