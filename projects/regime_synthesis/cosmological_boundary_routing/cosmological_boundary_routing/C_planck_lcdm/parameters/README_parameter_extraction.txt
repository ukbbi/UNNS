README — PLANCK 2018 CANONICAL PARAMETER EXTRACTION
Cosmological Boundary Routing
Dataset C — C_planck_lcdm

PURPOSE

This step converts the official Planck 2018 GetDist outputs for the selected baseline Lambda-CDM model into a compact, reproducible parameter record for Dataset C.

The selected model is:

base_plikHM_TTTEEE_lowl_lowE

This is the non-lensing baseline Planck 2018 flat six-parameter Lambda-CDM model constrained by:

- high-multipole TT
- high-multipole TE
- high-multipole EE
- low-multipole temperature
- lowE polarization

The extraction step produces one machine-readable CSV file and one human-readable TXT file. These outputs become the sole parameter inputs for the first generated Dataset C expansion trajectory.

INPUT FILES

Place the following files in the same folder as the extraction script:

base_plikHM_TTTEEE_lowl_lowE.minimum
base_plikHM_TTTEEE_lowl_lowE.margestats
base_plikHM_TTTEEE_lowl_lowE.paramnames
extract_planck_2018_parameters.py

Recommended folder:

C_planck_lcdm/
└── parameters/
    ├── base_plikHM_TTTEEE_lowl_lowE.minimum
    ├── base_plikHM_TTTEEE_lowl_lowE.margestats
    ├── base_plikHM_TTTEEE_lowl_lowE.paramnames
    ├── extract_planck_2018_parameters.py
    └── README_parameter_extraction.txt

ROLE OF EACH INPUT FILE

.minimum

Contains the best-fit parameter point.

These values are used as the canonical deterministic parameter set for generating the first Dataset C Lambda-CDM trajectory.

.margestats

Contains marginalized posterior means, standard deviations, and confidence limits.

These values are retained for documentation, later uncertainty propagation, and Monte Carlo robustness analysis.

.paramnames

Contains the mapping between Planck/GetDist parameter names and human-readable or LaTeX-style labels.

This prevents ambiguity in the extracted parameter record.

SCRIPT

File:

extract_planck_2018_parameters.py

The script:

1. verifies that all three required input files exist;
2. parses the Planck best-fit values from the .minimum file;
3. parses posterior means and 68% limits from the .margestats file;
4. maps source parameter names using .paramnames;
5. extracts the canonical cosmological parameters;
6. derives A_s from logA;
7. derives omega_r and Omega_r using the adopted radiation-density approximation;
8. writes the compact CSV record;
9. writes the human-readable TXT record;
10. stops with an explicit error if required files or parameters are missing.

PARAMETERS EXTRACTED

Directly extracted parameters:

H0
omegabh2
omegach2
Omega_m
Omega_Lambda
n_s
ln(10^10 A_s)
tau
sigma8
age

Derived parameters:

A_s
omega_r
Omega_r

The script records for each parameter:

- output parameter name
- original Planck source parameter
- label
- best-fit value
- posterior mean
- standard deviation
- lower 68% limit
- upper 68% limit
- confidence-limit type
- unit
- direct or derived status
- derivation formula where applicable
- canonical-use designation

CANONICAL VALUE POLICY

For the first deterministic Dataset C trajectory:

Use:
best_fit

Source:
base_plikHM_TTTEEE_lowl_lowE.minimum

Do not use posterior means as the main trajectory input in this first pass.

Posterior means and 68% limits are included only for:

- verification
- uncertainty documentation
- later robustness testing
- future Monte Carlo trajectory generation

DERIVED QUANTITIES

A_s

Derived from:

A_s = exp(logA) × 10^-10

where:

logA = ln(10^10 A_s)

omega_r

Derived using:

omega_gamma = 2.469 × 10^-5 × (T_CMB / 2.7255 K)^4

omega_r = omega_gamma × (1 + 0.22710731766 × N_eff)

The script uses:

T_CMB = 2.7255 K
N_eff = 3.046

unless N_eff is explicitly present in the source file.

Omega_r

Derived from:

Omega_r = omega_r / h^2

where:

h = H0 / 100

These radiation-density values are derived project inputs, not directly quoted Planck table values.

RUNNING THE SCRIPT

Open a terminal or command prompt in:

C_planck_lcdm/parameters/

Run:

python extract_planck_2018_parameters.py

On Windows, if required:

py extract_planck_2018_parameters.py

The script uses only the Python standard library. No external packages are required.

EXPECTED OUTPUT FILES

planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.csv

Purpose:
Machine-readable canonical parameter record for trajectory-generation scripts.

planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.txt

Purpose:
Human-readable audit record containing values, intervals, units, provenance notes, and derivations.

Both files are written into the same folder as the script unless another output directory is explicitly supplied.

OPTIONAL COMMAND-LINE USE

To read the Planck files from another folder:

python extract_planck_2018_parameters.py --input-dir PATH_TO_PARAMETERS

To write outputs into another folder:

python extract_planck_2018_parameters.py --input-dir PATH_TO_PARAMETERS --output-dir PATH_TO_OUTPUT

VALIDATION CHECKS

After execution, confirm that:

1. both output files exist;
2. the CSV contains one row for every required direct and derived parameter;
3. H0, Omega_m, Omega_Lambda, n_s, sigma8, and age are populated;
4. A_s is marked as derived;
5. omega_r and Omega_r are marked as derived;
6. the best-fit column is populated for all canonical parameters;
7. posterior means and 68% limits appear for directly tabulated parameters;
8. no source file has been modified.

EXPECTED PLANCK BASELINE VALUES

The exact values must come from the local official source files.

As a general verification only, the selected Planck 2018 baseline combination is expected to be close to:

H0 ≈ 67.3 km s^-1 Mpc^-1
Omega_m ≈ 0.316
Omega_Lambda ≈ 0.684
n_s ≈ 0.966
sigma8 ≈ 0.812
age ≈ 13.8 Gyr

These are not hard-coded targets. They are only sanity checks.

OUTPUT HANDLING

Keep the official Planck source files unchanged.

Recommended structure after successful extraction:

C_planck_lcdm/
├── source_planck_2018/
├── parameters/
│   ├── official source copies
│   ├── extract_planck_2018_parameters.py
│   ├── README_parameter_extraction.txt
│   ├── planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.csv
│   └── planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.txt
├── generated_trajectory/
├── canonical/
└── provenance.txt

The CSV output should become the only parameter source read by the first Dataset C trajectory generator.

Do not make the trajectory generator parse the original Planck GetDist files again.

This separation preserves:

- source integrity
- reproducibility
- auditability
- clear distinction between official data and project-derived data

INTERPRETIVE STATUS

This extraction step does not generate a cosmological trajectory.

It only freezes the observationally anchored parameter set for Dataset C.

The resulting compact parameter record supports the next step:

generation of the Planck-anchored Lambda-CDM expansion trajectory.

It does not provide direct observational evidence for:

- a cosmological bounce
- singularity removal
- a pre-Big-Bang phase
- a UNNS admissibility boundary

Those questions belong to later comparisons between:

A_classical_friedmann
B_lqc_bounce
C_planck_lcdm

SUCCESS CRITERION

This step is complete when:

- the script runs without error;
- both output files are created;
- all required direct and derived parameters are present;
- the best-fit values are frozen as canonical Dataset C inputs;
- the outputs are preserved beside the extraction script;
- the original Planck files remain unchanged.

NEXT STEP

Use:

planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.csv

to generate the first Dataset C Lambda-CDM expansion trajectory with columns such as:

time
redshift
scale_factor
H
rho_m
rho_r
rho_Lambda
rho_total
curvature_proxy
boundary_margin_candidate
