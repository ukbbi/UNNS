README — PRELIMINARY DATASET C STRUC-PERC LADDER

PURPOSE

This step converts the validated multi-column Planck-Lambda-CDM trajectory
into a controlled one-column scalar ladder suitable for STRUC-PERC-I v2.5.0.

The full validated trajectory must not be loaded directly into STRUC-PERC-I,
because the analyzer would mix physically different columns into one sorted
number sequence.

INPUT

../../generated_trajectory/validated/
planck_lcdm_trajectory_validated.csv

CONVERTER

build_planck_lcdm_preliminary_ladder.py

SCALAR COORDINATE

q_C(a) = ln(E(a))

where:

E(a) = H(a) / H0

This coordinate is dimensionless, finite, physically meaningful, and available
for later matched A/B/C construction.

OUTPUTS

planck_lcdm_response_ladder_preliminary.csv

A headerless one-column CSV containing one scalar ladder value per row.

planck_lcdm_response_ladder_preliminary_manifest.txt

An audit record describing the source, transformation, counts, numerical range,
recommended STRUC-PERC settings, and interpretive limits.

LOCATION

Place all three files in:

C_planck_lcdm/
└── canonical/
    └── ladder/
        ├── build_planck_lcdm_preliminary_ladder.py
        ├── README_ladder_preliminary.txt
        ├── planck_lcdm_response_ladder_preliminary.csv
        └── planck_lcdm_response_ladder_preliminary_manifest.txt

RUN

Open a terminal in:

C_planck_lcdm/canonical/ladder/

Run:

python build_planck_lcdm_preliminary_ladder.py

On Windows, if needed:

py build_planck_lcdm_preliminary_ladder.py

STRUC-PERC-I RUN

Load:

planck_lcdm_response_ladder_preliminary.csv

Use:

Domain adapter: Generic
kappa points: 17
kappa minimum: 0.01
kappa maximum: 1.0

Then run FULL PRP and export the compact STRUC-PERC dataset ZIP.

Store that ZIP in:

../struc_perc/direct/

STATUS

This ladder is PRELIMINARY.

It supports an initial Dataset C structural diagnostic, but it is not yet the
frozen shared canonical ladder definition for Datasets A, B, and C.

The authoritative A/B/C run must later use:

- the same sampling grid;
- the same scalar mapping;
- the same alpha convention;
- the same STRUC-PERC settings.

NEXT STEP AFTER DIRECT RUN

Preserve the direct STRUC-PERC export under:

canonical/struc_perc/direct/

Then apply the established project alpha transformation in a separate,
documented step and run the alpha-applied ladder under identical settings.
