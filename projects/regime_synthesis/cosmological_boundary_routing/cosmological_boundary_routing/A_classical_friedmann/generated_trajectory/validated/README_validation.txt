README — DATASET A TRAJECTORY VALIDATION
Cosmological Boundary Routing
A_classical_friedmann / generated_trajectory / validated

PURPOSE

This folder contains the accepted validated copy of the Dataset A classical Friedmann contraction trajectory.

Validated file:

classical_friedmann_approach_validated.csv

Raw source:

../raw/classical_friedmann_approach_raw.csv

The raw file must remain unchanged. The validated filename records that the trajectory passed the current numerical and physical checks and is approved for downstream structural processing.

VALIDATION STATUS

Dataset A trajectory generation:
PASS

Physical monotonicity:
PASS

Dynamic closure:
PASS

Finite-value validation:
PASS

Validated copy:
APPROVED FOR DOWNSTREAM PROCESSING

KEY TRAJECTORY PROPERTIES

Trajectory role:
classical singular approach

Evolution direction:
contraction

Scale-factor range:
a = 1 to a = 1e-8

Sampling:
4001 logarithmically spaced points

Branch definition:
H(a) = -H0 E(a)

Initial state:

a = 1
H_signed = -67.32178 km s^-1 Mpc^-1
boundary_margin_candidate approximately 0.395864

Terminal numerical cutoff:

a = 1e-8
H_signed approximately -6.46306468673e15 km s^-1 Mpc^-1
boundary_margin_candidate approximately 1.08501108519e-28

The trajectory approaches the classical small-a singular regime but does not evaluate a = 0.

PARAMETER CONSISTENCY

H0:
67.32178 km s^-1 Mpc^-1

Omega_m:
0.3157967

Omega_r_effective:
9.21617990232e-05

Omega_Lambda_planck:
0.6842033

Omega_Lambda_dynamic:
0.684111138201

Dynamic flat closure:
1.0

Dynamic closure residual:
0.000000e+00

The trajectory uses the same Planck-anchored parameter record and dynamic Lambda convention as Dataset C.

VALIDATED CHECKS

The accepted trajectory satisfies all of the following:

1. The CSV contains 4001 data rows.
2. The expected 31 columns are present.
3. No missing values occur.
4. No non-finite values occur.
5. E(a)^2 remains positive.
6. H_signed_km_s_Mpc remains negative.
7. scale_factor decreases monotonically.
8. redshift increases monotonically.
9. contraction_elapsed_time_Gyr is non-decreasing.
10. H_magnitude_km_s_Mpc increases monotonically.
11. rho_total_relative_to_rho_crit0 increases monotonically.
12. ricci_scalar_over_6H0sq increases monotonically.
13. boundary_margin_candidate decreases monotonically.
14. present_closure_dynamic remains equal to one within numerical precision.

ELAPSED-TIME PRECISION NOTE

Near the final numerical cutoff, contraction_elapsed_time_Gyr can appear unchanged across adjacent rows.

This occurs because the remaining time increments become smaller than the printed decimal precision relative to the accumulated value near 13.7969 Gyr.

This is a representation-precision effect, not a failure of the physical integration.

For late-stage resolution, use:

time_to_numerical_cutoff_Gyr

This column retains the remaining interval information closer to a = 1e-8.

FILES

validated/
├── classical_friedmann_approach_validated.csv
└── README_validation.txt

RELATED FILES

Raw trajectory:

../raw/
classical_friedmann_approach_raw.csv

Diagnostics:

../diagnostics/
classical_friedmann_approach_diagnostics.txt

Generator:

../../trajectory_generation/
generate_classical_friedmann_approach.py

Parameter source:

../../../C_planck_lcdm/parameters/extracted/
planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.csv

VALIDATED FILE POLICY

The validated trajectory is currently an exact copy of the accepted raw output.

Do not:

- modify the raw trajectory;
- manually edit values in the validated trajectory;
- overwrite the validated file with an unreviewed regeneration;
- change the Planck anchor without regenerating and revalidating Dataset A;
- treat boundary_margin_candidate as the final canonical UNNS margin.

If the generator, parameter source, sampling range, branch convention, or numerical precision changes, the trajectory must be regenerated and validated again.

INTERPRETIVE STATUS

This validation establishes that Dataset A is numerically coherent and suitable for structural analysis.

It does not establish:

- that the universe physically followed this contracting path;
- that a classical singularity was observed;
- that singularity removal has been demonstrated;
- that cosmological boundary routing has been established;
- that the provisional margin is canonical.

Dataset A is a controlled classical baseline for comparison with:

B_lqc_bounce
C_planck_lcdm

DOWNSTREAM USE

Only the validated copy should be used for:

- preliminary scalar ladder construction;
- STRUC-PERC-I analysis;
- STRUC-I admissibility testing;
- alpha-grid application;
- 5D structural-vector export;
- A/B/C bridge analysis.

Expected downstream folders:

../../canonical/ladder/
../../canonical/struc_perc/
../../canonical/alpha/
../../canonical/structural_vector/

CURRENT STATUS

Raw trajectory:
COMPLETE

Diagnostics:
COMPLETE

Validation:
PASS

Validated copy:
APPROVED

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

Construct the preliminary Dataset A scalar ladder using the same response coordinate used for Dataset C:

q_A(a) = ln(E(a))

The ladder should preserve the matched sampling and use the validated Dataset A trajectory as its sole input.
