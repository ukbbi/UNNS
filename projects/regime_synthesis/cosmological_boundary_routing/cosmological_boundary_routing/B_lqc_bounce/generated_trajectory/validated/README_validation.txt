README — DATASET B TRAJECTORY VALIDATION
Cosmological Boundary Routing
B_lqc_bounce / generated_trajectory / validated

PURPOSE

This folder contains the accepted validated copy of Dataset B:

lqc_bounce_trajectory_validated_v2_2.csv

Dataset B is the effective loop-quantum-cosmology contraction–bounce–expansion trajectory used in the Cosmological Boundary Routing comparison.

The validated file is copied from:

../raw/
lqc_bounce_trajectory_raw_v2_2.csv

The raw file must remain unchanged.

The validated filename records that version 2.2 passed the current numerical, branch-structure, bounce, density-bound, hybrid-sampling, and time-integration checks and is approved for downstream structural processing.

MODEL

The trajectory uses the effective equation:

H^2 = H0^2 * rho_rel * (1 - rho_rel / rho_c_rel)

with:

rho_c = 0.41 * rho_Planck

The background radiation–matter–Lambda density model and Planck parameter anchor are the same as those used for Datasets A and C.

TRAJECTORY STRUCTURE

The validated trajectory contains:

contraction
→ exact finite bounce
→ expansion

Total rows:
4001

Branch rows:

contraction:
2000

exact bounce:
1

expansion:
2000 additional post-bounce rows, with the bounce row included as the first expansion-side row in the stored sequence

Exact bounce index:
2000

VALIDATION STATUS

Dataset B trajectory generation:
PASS

Exact bounce condition:
PASS

Branch orientation:
PASS

Density boundedness:
PASS

Finite curvature representation:
PASS

Hybrid sampling:
PASS

Time integration:
PASS

Validated copy:
APPROVED FOR DOWNSTREAM PROCESSING

EXACT BOUNCE CHECK

At the unique bounce row:

a_bounce:
2.46836418015e-32

H_signed_km_s_Mpc:
0

H_magnitude_km_s_Mpc:
0

rho_over_rho_c:
1

lqc_correction_factor:
0

E_lqc_of_a:
0

The scale factor remains strictly positive at the bounce.

The bounce row is identified only by:

x_bounce_distance = 0

and:

is_exact_bounce = yes

No other row is treated as the exact bounce.

CRITICAL DENSITY

Present critical density:

rho_crit0 =
8.51306131693e-27 kg m^-3

Effective LQC critical density:

rho_c =
2.11348788763e96 kg m^-3

Relative critical density:

rho_c / rho_crit0 =
2.48264144817e122

The stored density satisfies:

rho / rho_c <= 1

throughout the complete trajectory.

HYBRID SAMPLING

Version 2.2 uses two matched sampling regions.

Near-bounce region:

coordinate:
x = sqrt(1 - rho/rho_c)

sampling:
logarithmic in x

transition condition:
rho/rho_c = 0.01

near-bounce points per branch:
801

Outer region:

coordinate:
scale factor a

sampling:
logarithmic in a

outer points per branch:
1201

After removing the duplicated transition row:

points per branch:
2001

complete trajectory rows:
4001

The transition scale factor is:

a_transition =
7.80565290404e-32

RESOLUTION CHECK

Rows with:

rho/rho_c >= 0.01

across the full trajectory:

1601

Outer-region rows across both branches:

2400

This confirms that the accepted trajectory resolves both:

- the quantum-corrected region near the bounce;
- the long outer cosmological evolution toward a = 1.

TIME-INTEGRATION CHECK

Integrated time from the bounce to a = 1:

13.7989388794 Gyr

Extracted Planck age reference:

13.79731 Gyr

Difference:

approximately 0.001629 Gyr

The branch time is finite and physically reasonable for the selected effective model and numerical grid.

BRANCH MONOTONICITY

Contraction branch:

- time_relative_to_bounce_Gyr increases toward zero;
- scale factor decreases toward a_bounce;
- H_signed_km_s_Mpc remains negative;
- rho_over_rho_c increases toward one;
- distance_to_bounce_Gyr decreases toward zero.

Expansion branch:

- time_relative_to_bounce_Gyr increases away from zero;
- scale factor increases away from a_bounce;
- H_signed_km_s_Mpc remains positive after the exact bounce;
- rho_over_rho_c decreases away from one;
- distance_to_bounce_Gyr increases away from zero.

Complete trajectory:

- time ordering is continuous through the bounce;
- exactly one row has H = 0;
- exactly one row has rho/rho_c = 1;
- density never exceeds rho_c;
- scale factor never reaches zero.

NEAR-BOUNCE PRECISION NOTE

Near the exact bounce, some adjacent rows can contain repeated printed scale_factor values.

This is a floating-point representation effect.

The bounce scale is approximately:

2.47e-32

and the smallest relative changes in a near the bounce can become comparable to double-precision resolution.

The near-bounce rows remain structurally distinct through:

- x_bounce_distance;
- rho_over_rho_c;
- lqc_correction_factor;
- E_lqc_of_a;
- time_relative_to_bounce_Gyr;
- distance_to_bounce_Gyr.

The stored density ratio and the density reconstructed from scale factor remain consistent to approximately:

3.4e-12 relative error or better.

Therefore, repeated printed scale-factor values near the bounce do not invalidate the accepted trajectory.

For near-bounce analysis, use:

x_bounce_distance

and:

rho_over_rho_c

as the primary resolution coordinates rather than relying only on printed scale_factor differences.

FILES

validated/
├── lqc_bounce_trajectory_validated_v2_2.csv
└── README_validation.txt

RELATED FILES

Accepted raw trajectory:

../raw/
lqc_bounce_trajectory_raw_v2_2.csv

Accepted diagnostics:

../diagnostics/
lqc_bounce_trajectory_diagnostics_v2_2.txt

Accepted generator:

../../trajectory_generation/
generate_lqc_bounce_trajectory_v2_2.py

Rejected earlier runs should remain separately archived and must not be used as validated inputs.

PARAMETER SOURCE

../../../C_planck_lcdm/parameters/extracted/
planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.csv

VALIDATED FILE POLICY

Do not:

- modify the raw v2.2 trajectory;
- manually edit values in the validated CSV;
- overwrite the validated file with an unreviewed regeneration;
- substitute outputs from v1, v2.1, or other rejected runs;
- change rho_c without recording the new convention and repeating validation;
- treat boundary_margin_candidate as the final shared UNNS boundary coordinate.

If any of the following change, Dataset B must be regenerated and revalidated:

- Planck parameter source;
- rho_c convention;
- transition ratio;
- near-bounce point count;
- outer point count;
- x_min;
- a_outer;
- effective LQC equation;
- time-integration method.

INTERPRETIVE STATUS

This validation establishes that Dataset B is a numerically coherent effective LQC bounce trajectory suitable for downstream structural analysis.

It demonstrates within the selected model that:

- contraction reaches a finite positive minimum scale factor;
- H changes sign through an exact bounce;
- density remains bounded by rho_c;
- the path continues into expansion;
- the trajectory avoids numerical passage through a = 0.

It does not by itself establish:

- that loop quantum cosmology is the correct physical theory;
- that a cosmological bounce occurred in nature;
- observational confirmation of singularity removal;
- a final UNNS boundary-routing result;
- a final shared A/B/C margin.

PROVISIONAL MARGIN STATUS

boundary_margin_candidate remains diagnostic only.

At the exact bounce, the current provisional definition reaches zero because the density-to-bounce component is defined as:

1 - rho/rho_c

This zero identifies the effective turning surface under the present diagnostic construction.

It must not yet be interpreted as the final canonical UNNS boundary-distance coordinate.

The shared A/B/C margin will be frozen only after matched structural comparison across all three validated datasets.

DOWNSTREAM USE

Only the validated v2.2 trajectory should be used for:

- direction-preserving bounce-path construction;
- preliminary scalar ladder construction;
- STRUC-PERC-I analysis;
- STRUC-I admissibility testing;
- alpha-grid application;
- 5D structural-vector export;
- orientation-sensitive A/B/C bridge construction.

Expected downstream folders:

../../canonical/ladder/
../../canonical/struc_perc/
../../canonical/alpha/
../../canonical/structural_vector/

CURRENT STATUS

Raw v2.2 trajectory:
COMPLETE

Diagnostics v2.2:
COMPLETE

Validation:
PASS

Validated copy:
APPROVED

Canonical ladder:
NOT YET CREATED

Direction-preserving bounce path:
NOT YET CREATED

STRUC-PERC-I:
NOT YET RUN

STRUC-I:
NOT YET RUN

Alpha application:
NOT YET RUN

5D vector:
NOT YET CREATED

A/B/C bridge:
NOT YET STARTED

NEXT STEP

Construct the Dataset B preliminary structural representations while preserving the full path:

contraction
→ bounce
→ expansion

The next conversion must not discard:

- branch identity;
- time orientation;
- signed H;
- exact bounce index;
- rho/rho_c;
- x_bounce_distance.

A sorted scalar ladder may be produced for direct STRUC-PERC-I and STRUC-I comparison, but a direction-preserving bounce-path file must also be retained for alpha analysis and the final orientation-sensitive A/B/C bridge.
