README — DATASET A CLASSICAL FRIEDMANN BASELINE
Cosmological Boundary Routing

PURPOSE

Dataset A is the matched classical Friedmann trajectory approaching the
small-scale-factor singular boundary.

It uses the same Planck-anchored parameters, effective radiation convention,
dynamic Lambda closure, scale-factor range, sample count, and logarithmic grid
as Dataset C.

The key differences are:

- Dataset A is ordered from a = 1 toward a = 1e-8;
- Dataset A uses the contracting branch H < 0;
- density, curvature, and |H| increase toward the numerical cutoff;
- the provisional boundary margin decreases toward zero.

Dataset A is the classical non-corrected comparison trajectory for the later
A/B/C boundary-routing analysis.

FOLDER STRUCTURE

A_classical_friedmann/
├── trajectory_generation/
│   ├── generate_classical_friedmann_approach.py
│   └── README_trajectory_generation.txt
├── generated_trajectory/
│   ├── raw/
│   ├── validated/
│   └── diagnostics/
├── canonical/
│   ├── ladder/
│   ├── alpha/
│   ├── struc_perc/
│   └── structural_vector/
├── provenance.txt
└── README.txt

PARAMETER SOURCE

The generator reads the compact Dataset C Planck parameter record directly:

../C_planck_lcdm/parameters/extracted/
planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.csv

This preserves the matched A/C cosmological anchor.

DEFAULT SAMPLING

a_start = 1
a_cutoff = 1e-8
samples = 4001
grid = logarithmic in scale factor
ordering = descending
branch = contraction

OUTPUTS

generated_trajectory/raw/
classical_friedmann_approach_raw.csv

generated_trajectory/diagnostics/
classical_friedmann_approach_diagnostics.txt

RUN

Open a terminal in:

A_classical_friedmann/trajectory_generation/

Run:

python generate_classical_friedmann_approach.py

On Windows, if required:

py generate_classical_friedmann_approach.py

EXPECTED BEHAVIOUR

scale factor:
monotonic decreasing

contraction elapsed time:
monotonic increasing

signed Hubble parameter:
negative

Hubble magnitude:
monotonic increasing

total density:
monotonic increasing

curvature proxy:
monotonic increasing

provisional boundary margin:
monotonic decreasing

INTERPRETIVE LIMIT

The numerical trajectory stops at a = 1e-8.

It approaches the classical singular limit but does not evaluate a = 0.

The boundary_margin_candidate remains provisional and must not be treated as
the final shared UNNS boundary-distance coordinate.

Dataset A and Dataset C share the same classical Friedmann magnitude E(a).
Dataset A is the contracting approach branch; Dataset C is the observationally
anchored expansion branch. This role distinction must remain explicit.

NEXT STEP

Run the generator, inspect the diagnostics, validate the trajectory, and copy
the accepted raw CSV into:

generated_trajectory/validated/
classical_friedmann_approach_validated.csv

Only after validation should the Dataset A ladder and alpha-grid stages begin.
