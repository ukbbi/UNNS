COSMOLOGICAL BOUNDARY ROUTING
UNNS Substrate Research Program
Initial project structure — June 2026

PURPOSE

This folder contains the first controlled test of Cosmological Boundary Routing within the UNNS Substrate program.

The project asks whether singularity-removal models can be represented as admissibility-preserving boundary-routing systems. The central comparison is between:

A. a classical Friedmann trajectory approaching the singular limit a(t) -> 0;
B. a non-singular loop-quantum-cosmology-style bounce trajectory with a(t) >= a_min > 0;
C. a Planck-anchored Lambda-CDM expansion trajectory compatible with observational cosmology.

The goal is not to claim that any one non-singular model is physically established. The goal is to test whether corrected cosmological dynamics preserve a positive structural margin where the classical model approaches an inadmissible boundary.

CORE RESEARCH QUESTION

Using Planck-anchored cosmological parameters, does a non-singular bounce trajectory preserve a positive UNNS boundary margin where the classical Friedmann trajectory collapses toward zero?

SECONDARY QUESTIONS

1. Does the classical trajectory show margin collapse as a(t), density, and curvature approach their singular limits?
2. Does the corrected trajectory retain finite density, finite curvature, and a positive minimum scale factor?
3. Are the pre-boundary, transition, and post-boundary regimes all locally admissible?
4. Do these regimes remain structurally equivalent, or does the transition route the system into a distinct admissible regime?
5. Does the unified ABC bridge show contact, separation, or branching analogous to Stellar Boundary Dynamics?

FOLDER STRUCTURE

A_classical_friedmann/

Contains the classical baseline trajectory generated from the standard Friedmann equations.

Expected contents:
- Planck-anchored parameter file
- trajectory CSV
- model assumptions
- raw and normalized variables
- STRUC-PERC-I input
- alpha-application output
- UNNS structural vector
- validation notes

Minimum variables:
- time or conformal time
- scale factor a(t)
- Hubble parameter H(t)
- density rho(t)
- pressure p(t) or equation-of-state parameter w(t)
- curvature proxy
- normalized boundary margin m(t)

Expected structural role:
The controlled collapse baseline in which the classical trajectory approaches a(t) -> 0 and the structural margin tends toward zero.


B_lqc_bounce/

Contains the non-singular corrected trajectory generated from an effective loop quantum cosmology bounce model.

Expected contents:
- effective corrected Friedmann equation
- critical density parameter
- trajectory CSV
- bounce-location record
- raw and normalized variables
- STRUC-PERC-I input
- alpha-application output
- UNNS structural vector
- validation notes

Minimum variables:
- time
- scale factor a(t)
- Hubble parameter H(t)
- density rho(t)
- correction factor
- critical density rho_c
- curvature proxy
- normalized boundary margin m(t)

Expected structural role:
The candidate boundary-routing regime in which collapse is halted before a = 0, density remains bounded, and the system passes through a finite minimum scale factor.


C_planck_lcdm/

Contains the observationally anchored expansion regime based on Planck 2018 Lambda-CDM best-fit parameters.

Expected contents:
- cosmological parameter table
- generated late-time expansion trajectory
- trajectory CSV
- source and parameter provenance
- raw and normalized variables
- STRUC-PERC-I input
- alpha-application output
- UNNS structural vector
- validation notes

Minimum parameters:
- H0
- Omega_m
- Omega_b
- Omega_Lambda
- Omega_r where used
- scalar spectral index n_s
- scalar amplitude A_s where required

Expected structural role:
The observationally compatible post-boundary expansion regime used to determine whether the corrected transition routes into a viable cosmological state.


ABC_bridge/

Contains pairwise and unified structural comparisons.

Expected analyses:
- A-B bridge
- B-C bridge
- A-C bridge
- unified ABC normalization
- centroid distances
- nearest-neighbor relations
- feature-wise deltas
- branching index
- global routing classification
- final structural interpretation

The unified ABC bridge is authoritative for the global routing geometry. Pairwise bridges are local diagnostics only.

Candidate routing outcomes:
- A_to_B_contact_with_C_continuation
- A_to_B_contact_with_C_branching
- A_to_B_strong_separation
- B_to_C_recovery
- classical_boundary_failure_with_corrected_admissibility


tools/

Contains only reusable project tools.

Expected contents:
- trajectory generators
- parameter loaders
- physical-variable validators
- normalization utilities
- alpha-application integration
- STRUC-PERC-I preparation scripts
- structural-vector exporter
- bridge-analysis scripts
- plotting and report utilities

Do not create a separate generator for every dataset if the same function can be handled through one configurable pipeline. Prefer reusable adapters and a single controlled workflow.


MINIMUM VIABLE DATASET

Dataset A:
One classical Friedmann trajectory integrated toward a small scale factor.

Dataset B:
One effective loop quantum cosmology bounce trajectory using matched initial conditions or matched low-density behavior.

Dataset C:
One Planck-anchored Lambda-CDM expansion trajectory.

The three datasets must use compatible sampling, shared variable definitions, explicit normalization, and documented parameter provenance.


UNNS VARIABLES AND METRICS

Each regime should be converted into an ordered ladder and evaluated using:

- kappa_connect
- giant ratio
- tail dominance
- admissibility persistence
- anisotropic persistence
- collapse-onset radius
- mean and variance of GR
- normalized boundary margin
- bridge distance
- branching index

The boundary margin must not be defined only as a(t). A composite margin should also be tested using finite-density and finite-curvature conditions.

Candidate normalized margin:

m(t) = minimum of:
- normalized scale-factor distance from zero
- normalized density distance from the critical or divergent limit
- normalized curvature distance from the divergent limit

The exact canonical definition must be documented before bridge comparison.


MODEL-COMPARISON REQUIREMENTS

A and B should be matched as closely as possible in their low-density regime.

The comparison should separate:
- model choice
- parameter choice
- sampling effects
- normalization effects
- physical correction effects

The LQC-style correction should recover the classical Friedmann behavior sufficiently far from the bounce. Otherwise, any structural separation may reflect incompatible model setup rather than genuine boundary routing.


EXPECTED FIRST TEST

Classical baseline:
- a(t) approaches zero
- density and curvature increase without bound or toward the imposed numerical cutoff
- structural margin approaches zero

Corrected bounce:
- a(t) reaches a positive minimum
- density remains bounded by rho_c
- curvature remains finite
- structural margin remains positive
- the trajectory continues into expansion

Planck-anchored expansion:
- late-time expansion remains compatible with the selected cosmological parameter set
- the post-transition trajectory occupies an observationally viable regime


SUCCESS CRITERIA

The pilot experiment succeeds if it can show all of the following:

1. The classical trajectory approaches structural margin collapse.
2. The corrected trajectory avoids the classical singular boundary.
3. The corrected trajectory remains internally admissible under the selected UNNS tests.
4. The corrected and observationally anchored regimes can be compared in a common bridge space.
5. The ABC bridge yields a reproducible routing classification.
6. The result is robust to reasonable changes in sampling and normalization.


INTERPRETIVE LIMITS

This project does not by itself prove:
- that loop quantum cosmology is the correct theory of the early universe;
- that the Big Bang hot phase did not occur;
- that a particular quantum correction is uniquely selected;
- that UNNS replaces general relativity or observational cosmology.

The project tests a narrower structural claim:

A cosmological singularity-removal model may preserve admissibility by preventing the trajectory from crossing the classical singular boundary and routing it into a distinct, non-singular regime.


RELATION TO RECENT UNNS RESEARCH

This project extends Stellar Boundary Dynamics.

Stellar Boundary Dynamics showed that:
- catastrophic transition need not destroy admissibility;
- internal admissibility does not imply cross-regime equivalence;
- a catastrophic boundary may route structure into multiple non-equivalent downstream regimes.

Cosmological Boundary Routing applies the same logic to the classical singular limit.

The stellar pattern was:

pre-collapse support state
-> post-collapse relaxation
-> spectroscopic redistribution

The cosmological pattern is:

classical high-curvature approach
-> corrected non-singular transition
-> observationally viable expansion

The intended theoretical contribution is to determine whether cosmological singularity removal is another instance of admissible boundary routing.


INITIAL WORKFLOW

1. Freeze the physical equations and parameter set.
2. Generate Dataset A.
3. Generate Dataset B with matched low-density behavior.
4. Generate Dataset C from Planck-anchored Lambda-CDM parameters.
5. Validate all trajectories physically.
6. Harmonize sampling and columns.
7. Apply alpha.
8. Produce canonical ladders.
9. Run STRUC-PERC-I.
10. Export structural vectors.
11. Run A-B, B-C, A-C, and unified ABC bridge comparisons.
12. Review scale dependence and normalization.
13. Record the final routing classification.
14. Only then assess the theoretical interpretation.


CURRENT STATUS

Project structure created.
README initialized.
No trajectory data generated yet.
No canonical margin definition frozen yet.
No bridge result available yet.

NEXT STEP

Create the shared parameter and schema specification before generating any trajectory.

Recommended first file:
tools/cosmology_schema_and_parameters.txt

This file should define:
- equations
- units
- parameter values
- time variable
- sampling grid
- output columns
- normalization rules
- singular cutoff
- bounce parameters
- margin definition candidates
