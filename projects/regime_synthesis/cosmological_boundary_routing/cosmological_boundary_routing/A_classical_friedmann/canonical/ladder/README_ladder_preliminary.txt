README — DATASET A PRELIMINARY LADDER AND PATH

PURPOSE

This step converts the validated Dataset A classical Friedmann contraction
trajectory into two complementary structural representations.

1. A sorted scalar ladder for STRUC-PERC-I and STRUC-I.
2. A direction-preserving path retaining contraction order.

INPUT

../../generated_trajectory/validated/
classical_friedmann_approach_validated.csv

CONVERTER

build_classical_friedmann_preliminary_ladder.py

SCALAR RESPONSE COORDINATE

q_A(a) = ln(E(a))

where:

E(a) = |H(a)| / H0

OUTPUTS

classical_friedmann_response_ladder_preliminary.csv

Headerless one-column sorted ladder for STRUC-PERC-I.

classical_friedmann_response_path_preliminary.csv

Direction-preserving path ordered from a = 1 toward a = 1e-8. It retains
scale factor, redshift, signed H, H magnitude, elapsed contraction time,
q_A, and the provisional margin.

classical_friedmann_response_ladder_preliminary_struc_i.csv

The same sorted scalar ladder with the header:

value

for STRUC-I ingestion.

classical_friedmann_response_ladder_preliminary_manifest.txt

Audit record describing the transformation, counts, range, path checks,
recommended chamber settings, and interpretive limits.

LOCATION

Place this README and the converter in:

A_classical_friedmann/
└── canonical/
    └── ladder/

RUN

Open a terminal in:

A_classical_friedmann/canonical/ladder/

Run:

python build_classical_friedmann_preliminary_ladder.py

On Windows, if required:

py build_classical_friedmann_preliminary_ladder.py

EXPECTED RELATION TO DATASET C

Dataset A and Dataset C share:

- the same Planck parameter anchor;
- the same Friedmann magnitude E(a);
- the same 4001 scale-factor samples;
- the same scalar mapping q = ln(E).

Therefore, the sorted Dataset A and Dataset C ladders are expected to be
identical.

This is intentional.

The sorted scalar geometry cannot distinguish expansion from contraction when
the underlying scalar set is the same.

The distinction remains available in:

- signed H;
- path ordering;
- density and margin direction;
- contraction elapsed time;
- alpha deformation;
- later path-sensitive bridge analysis.

STRUC-PERC-I SETTINGS

Input:

classical_friedmann_response_ladder_preliminary.csv

Settings:

Domain adapter: Generic
kappa points: 17
kappa minimum: 0.01
kappa maximum: 1.0

STRUC-I SETTINGS

Input:

classical_friedmann_response_ladder_preliminary_struc_i.csv

Settings:

maximum ladder size: 5000
Monte Carlo runs: 2000
kappa steps: 40
kappa minimum: 0.01
kappa maximum: 1.0

STATUS

The representation is preliminary.

The sorted ladder is intended for direct structural diagnostics.

The direction-preserving path must be retained for Dataset A alpha analysis and
the final A/B/C bridge.

NEXT STEP

Run the converter, inspect the manifest, then run the sorted ladder through
STRUC-PERC-I and STRUC-I under the same settings used for Dataset C.
