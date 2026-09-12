README — DATASET C PLANCK LCDM TRAJECTORY GENERATION

PURPOSE

This step generates the Planck-anchored flat Lambda-CDM expansion trajectory
for Dataset C of the Cosmological Boundary Routing project.

The generator reads only the compact extracted parameter record:

../parameters/extracted/
planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.csv

It does not parse the original Planck GetDist files again.

FILES

Place these files in:

C_planck_lcdm/trajectory_generation/

- generate_planck_lcdm_trajectory.py
- trajectory_config.txt
- README_trajectory_generation.txt

EXPECTED INPUT

C_planck_lcdm/parameters/extracted/
planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.csv

EXPECTED OUTPUTS

C_planck_lcdm/generated_trajectory/raw/
planck_lcdm_trajectory_raw.csv

C_planck_lcdm/generated_trajectory/diagnostics/
planck_lcdm_trajectory_diagnostics.txt

LAMBDA HANDLING

The extracted Planck value is retained as:

Omega_Lambda_planck

The trajectory generator separately computes:

Omega_Lambda_dynamic = 1 - Omega_m - Omega_r

Omega_Lambda_dynamic is used in the Friedmann equation so that the explicitly
included radiation density does not push the present-day closure sum above one.

The original Planck value is never overwritten.

RADIATION HANDLING

Omega_r is the effective relativistic radiation density derived during the
parameter-extraction step.

It includes photons and an effective relativistic-neutrino contribution. It is
adequate for the first controlled radiation-matter-Lambda trajectory but is not
a precision treatment of the massive-neutrino transition.

SAMPLING

Default scale-factor range:

a_min = 1e-8
a_max = 1
samples = 4001

The grid is logarithmic in scale factor.

The generated cosmic-time column measures elapsed time from a_min. It does not
claim to integrate from an exact physical a = 0 state.

RUN

Open a terminal in:

C_planck_lcdm/trajectory_generation/

Run:

python generate_planck_lcdm_trajectory.py

On Windows, if needed:

py generate_planck_lcdm_trajectory.py

No external Python packages are required.

MAIN OUTPUT COLUMNS

- sample_index
- redshift
- scale_factor
- cosmic_time_from_a_min_Gyr
- lookback_from_present_Gyr
- H_km_s_Mpc
- E_of_a
- Omega_m_planck
- Omega_r_effective
- Omega_Lambda_planck
- Omega_Lambda_dynamic
- present_closure_planck_plus_radiation
- present_closure_dynamic
- rho_m_relative_to_rho_crit0
- rho_r_relative_to_rho_crit0
- rho_lambda_relative_to_rho_crit0
- rho_total_relative_to_rho_crit0
- fractional density components
- Ricci-curvature proxy
- provisional margin components
- boundary_margin_candidate

MARGIN STATUS

boundary_margin_candidate is provisional.

It is currently the minimum of:

- normalized scale-factor distance
- inverse total-density pressure
- inverse Ricci-curvature pressure

This column is included for inspection only. It is not yet the canonical UNNS
boundary-margin definition and must not be used as a final theoretical result.

VALIDATION

After execution, confirm:

1. The raw trajectory CSV exists.
2. The diagnostics TXT exists.
3. Omega_Lambda_planck remains unchanged.
4. Omega_Lambda_dynamic is explicitly recorded.
5. present_closure_dynamic equals one within numerical precision.
6. H(a=1) equals the extracted H0.
7. E(a=1) equals one.
8. The integrated age is close to the extracted Planck age.
9. Density and H increase toward small scale factor.
10. No NaN, infinity, or negative E(a)^2 occurs.

NEXT STEP

After validating the raw trajectory, copy or transform the accepted result into:

generated_trajectory/validated/

Only the validated trajectory should then be used to construct:

canonical/ladder/
canonical/alpha/
canonical/struc_perc/
canonical/structural_vector/
