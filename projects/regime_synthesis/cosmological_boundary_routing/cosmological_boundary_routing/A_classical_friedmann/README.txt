A_CLASSICAL_FRIEDMANN
Cosmological Boundary Routing
UNNS Substrate Research Program

PURPOSE

This folder contains Dataset A of the Cosmological Boundary Routing project.

Dataset A is the matched classical Friedmann baseline. It represents a contracting classical cosmological trajectory approaching the small-scale-factor singular boundary.

Its role is to provide the non-corrected comparison branch for:

B_lqc_bounce
C_planck_lcdm

The central question is whether the corrected Dataset B trajectory preserves admissibility and avoids the boundary-collapse behaviour exhibited by Dataset A.

DATASET ROLE

Dataset A is:

- classical;
- non-bouncing;
- singularity-approaching;
- Planck-anchored;
- numerically truncated at a finite small-scale-factor cutoff;
- ordered from a = 1 toward a = 1e-8;
- assigned to the contracting branch H < 0.

It is model-generated and must not be described as a direct Planck observation.

PARAMETER ANCHOR

Dataset A uses the same compact Planck 2018 parameter record used by Dataset C:

../C_planck_lcdm/parameters/extracted/
planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.csv

This ensures that Datasets A and C share the same cosmological anchor.

MATCHING POLICY

Dataset A and Dataset C use the same:

- Planck parameter record;
- H0;
- matter density;
- effective radiation density;
- dynamic Lambda closure;
- scale-factor range;
- logarithmic sampling;
- number of samples;
- Friedmann magnitude E(a).

The distinction is trajectory orientation and research role:

Dataset A:
contracting approach toward the classical singular boundary

Dataset C:
observationally anchored expansion away from the small-a regime

FOLDER STRUCTURE

A_classical_friedmann/
├── canonical/
│   ├── alpha/
│   ├── ladder/
│   ├── struc_perc/
│   └── structural_vector/
├── generated_trajectory/
│   ├── diagnostics/
│   ├── raw/
│   └── validated/
├── trajectory_generation/
│   ├── generate_classical_friedmann_approach.py
│   └── README_trajectory_generation.txt
├── provenance.txt
└── README.txt

TRAJECTORY GENERATION

Generator:

trajectory_generation/
generate_classical_friedmann_approach.py

Default outputs:

generated_trajectory/raw/
classical_friedmann_approach_raw.csv

generated_trajectory/diagnostics/
classical_friedmann_approach_diagnostics.txt

DEFAULT SAMPLING

a_start = 1
a_cutoff = 1e-8
samples = 4001
grid = logarithmic in scale factor
ordering = descending
branch = contraction

CLASSICAL DYNAMICS

The trajectory uses:

H(a) = -H0 E(a)

where E(a) is the same Planck-anchored Friedmann magnitude used for Dataset C.

The negative sign identifies the contracting branch.

EXPECTED BEHAVIOUR

As the trajectory approaches the numerical cutoff:

- scale factor decreases;
- contraction elapsed time increases;
- |H| increases;
- total density increases;
- curvature proxy increases;
- radiation fraction grows;
- provisional boundary margin decreases;
- the trajectory approaches the classical singular regime.

The numerical path stops at a = 1e-8 and does not evaluate a = 0.

VALIDATION REQUIREMENTS

The raw trajectory must be validated before canonical processing.

Required checks:

1. 4001 rows are present.
2. No missing or infinite values occur.
3. scale_factor decreases monotonically.
4. contraction_elapsed_time_Gyr increases monotonically.
5. H_signed_km_s_Mpc remains negative.
6. H_magnitude_km_s_Mpc increases monotonically.
7. rho_total_relative_to_rho_crit0 increases monotonically.
8. ricci_scalar_over_6H0sq increases monotonically.
9. boundary_margin_candidate decreases monotonically.
10. present_closure_dynamic equals 1 within numerical precision.

After validation, copy the accepted raw trajectory to:

generated_trajectory/validated/
classical_friedmann_approach_validated.csv

Do not overwrite or delete the raw file.

CANONICAL PROCESSING

After validation, Dataset A follows the same sequence as Dataset C:

validated trajectory
→ preliminary scalar ladder
→ STRUC-PERC-I
→ STRUC-I
→ alpha application
→ 5D structural vector
→ A/B/C bridge comparison

The same scalar mapping, alpha grid, chamber settings, and output conventions must be preserved across A, B, and C.

PROVISIONAL MARGIN STATUS

boundary_margin_candidate is diagnostic only.

It is not yet the final shared UNNS boundary-distance coordinate.

The canonical A/B/C margin must be frozen only after Dataset A and Dataset B are both available for matched comparison.

INTERPRETIVE LIMITS

Dataset A does not prove that the universe physically underwent a classical contraction from a = 1 toward a = 0.

It is a controlled model trajectory used to test the structural consequences of classical singular approach.

It does not by itself establish:

- singularity formation in nature;
- singularity removal;
- cosmological boundary routing;
- a UNNS admissibility result;
- superiority of any corrected cosmological model.

CURRENT STATUS

Folder structure:
CREATED

Provenance record:
CREATED

Trajectory generator:
CREATED

Raw trajectory:
NOT YET GENERATED

Diagnostics:
NOT YET GENERATED

Validation:
NOT YET COMPLETED

Canonical ladder:
NOT YET CREATED

STRUC-PERC-I:
NOT YET RUN

STRUC-I:
NOT YET RUN

Alpha application:
NOT YET RUN

5D vector:
NOT YET CREATED

NEXT STEP

Run:

trajectory_generation/
generate_classical_friedmann_approach.py

Then inspect:

generated_trajectory/diagnostics/
classical_friedmann_approach_diagnostics.txt

and validate:

generated_trajectory/raw/
classical_friedmann_approach_raw.csv
