README — DATASET C TRAJECTORY VALIDATION
Cosmological Boundary Routing
C_planck_lcdm / generated_trajectory / validated

PURPOSE

This folder contains the accepted validated copy of the Planck-anchored Lambda-CDM trajectory for Dataset C.

The validated file is:

planck_lcdm_trajectory_validated.csv

It is copied from:

../raw/planck_lcdm_trajectory_raw.csv

The raw source file remains unchanged and must be preserved as the original generator output.

VALIDATION STATUS

The trajectory passed the first numerical and physical validation stage.

Validated checks:

- parameter extraction completed successfully;
- Omega_Lambda_planck preserved unchanged;
- Omega_Lambda_dynamic computed explicitly;
- dynamic flat closure equals 1;
- closure residual equals 0 within numerical precision;
- 4001 logarithmically spaced samples produced;
- scale-factor range is a = 1e-8 to a = 1;
- no missing values;
- no infinite values;
- E(a)^2 remains positive and finite;
- E(a = 1) = 1;
- H(a = 1) = H0;
- cosmic time increases monotonically;
- scale factor increases monotonically;
- H decreases monotonically across the stored expansion trajectory;
- total relative density decreases monotonically;
- integrated age is consistent with the extracted Planck age.

KEY VALIDATION VALUES

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

Planck Lambda plus explicit radiation:
1.00009216179902

Dynamic flat closure:
1.0

Dynamic closure residual:
0.000000e+00

Integrated age from a_min:
13.7969074704 Gyr

Extracted Planck age:
13.79731 Gyr

Age difference:
-0.000402529568408 Gyr

Sampling:

a_min = 1e-8
a_max = 1
samples = 4001
grid = logarithmic in scale factor

FILES

validated/
├── planck_lcdm_trajectory_validated.csv
└── README_validation.txt

RELATED FILES

Raw trajectory:

../raw/planck_lcdm_trajectory_raw.csv

Diagnostics:

../diagnostics/planck_lcdm_trajectory_diagnostics.txt

Generator:

../../trajectory_generation/generate_planck_lcdm_trajectory.py

Parameter source:

../../parameters/extracted/
planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.csv

VALIDATED FILE POLICY

The validated file is currently an exact copy of the raw trajectory.

The change in filename records approval for downstream use.

Do not:

- modify the raw source file;
- overwrite the validated file with an unreviewed regeneration;
- manually edit individual trajectory values;
- treat the provisional boundary margin as canonical;
- use the validated file without preserving this validation record.

If the generator, parameter record, sampling range, or physical assumptions change, the trajectory must be regenerated and revalidated.

INTERPRETIVE STATUS

This validation confirms that Dataset C is numerically coherent and suitable for downstream structural processing.

It does not yet establish:

- a cosmological boundary-routing result;
- singularity removal;
- a canonical UNNS margin;
- a bridge classification;
- a STRUC-PERC verdict.

The column:

boundary_margin_candidate

is provisional.

It may be inspected, but it must not be treated as the final UNNS boundary-distance coordinate until the shared definition is frozen across Datasets A, B, and C.

DOWNSTREAM USE

Only the validated trajectory should be used for:

- canonical ladder construction;
- alpha application;
- STRUC-PERC-I preparation;
- structural-vector export;
- bridge comparison.

The next downstream folders are:

../../canonical/ladder/
../../canonical/alpha/
../../canonical/struc_perc/
../../canonical/structural_vector/

CURRENT STATUS

Raw trajectory:
COMPLETE

Diagnostics:
COMPLETE

First validation:
PASS

Validated copy:
APPROVED FOR DOWNSTREAM PROCESSING

Canonical margin:
NOT YET FROZEN

Dataset A:
NOT YET GENERATED

Dataset B:
NOT YET GENERATED

ABC bridge:
NOT YET STARTED

NEXT STEP

Generate Dataset A, the matched classical Friedmann baseline, using the same Planck parameter record and compatible sampling conventions.

The shared canonical margin should be frozen only after Dataset A and Dataset B are available for direct comparison.
