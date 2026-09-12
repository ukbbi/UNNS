README — ABC ROUTE PROFILES V1.1
Cosmological Boundary Routing
A–B–C Orientation-Sensitive Bridge

PURPOSE

This step derives two reproducible datasets from the accepted Bridge v1.1 interval file:

ABC_orientation_sensitive_bridge_v1_1.csv

The derived outputs preserve branch-resolved routing information, especially for Dataset B, whose full-path signed means cancel by symmetry.

SCRIPT

ABC_bridge/tools/
build_abc_route_profiles_v1_1.py

INPUT

ABC_bridge/outputs/
ABC_orientation_sensitive_bridge_v1_1.csv

OUTPUTS

ABC_bridge/outputs/
ABC_orientation_sensitive_route_profile_v1_1.csv

ABC_bridge/outputs/
ABC_orientation_sensitive_phase_summary_v1_1.csv

PROFILE PHASES

The source bridge rows are mapped into five interpretation phases:

A_terminal_approach

B_pre_bounce_approach

B_turning_surface

B_post_bounce_recession

C_boundary_recession

This phase split prevents Dataset B from being summarized only by its cancelling full-path signed means.

ROUTE-PROFILE DATASET

File:

ABC_orientation_sensitive_route_profile_v1_1.csv

Purpose:

This file provides binned route profiles across the shared dimensionless route coordinate.

Ordinary phases are divided into up to 50 equal-width route-coordinate bins.

The ordinary phases are:

A_terminal_approach

B_pre_bounce_approach

B_post_bounce_recession

C_boundary_recession

The B turning-surface intervals are not merged into neighboring bins.

They are retained as one dedicated profile:

B_turning_surface

Each route-profile row records:

- profile phase;
- dataset identity;
- route phase;
- route-bin index and label;
- interval count;
- route-coordinate minimum, maximum, and mean;
- margin-decreasing fraction;
- margin-increasing fraction;
- turning-surface crossing fraction;
- mean signed flow;
- mean absolute flow;
- Dataset B rho/rho_c profile;
- Dataset B x_bounce_distance profile.

The profiled signed-flow channels are:

- signed route step;
- signed Delta ln(a);
- normalized signed Delta ln(a);
- signed H flow;
- normalized signed H flow;
- signed density flow;
- normalized signed density flow;
- signed curvature flow;
- normalized signed curvature flow;
- signed margin flow;
- normalized signed margin flow.

PHASE-SUMMARY DATASET

File:

ABC_orientation_sensitive_phase_summary_v1_1.csv

Purpose:

This file provides one summary row for each of the five route phases.

It records:

- interval count;
- route-coordinate range;
- mean normalized signed Delta ln(a);
- mean normalized signed H flow;
- mean normalized signed density flow;
- mean normalized signed curvature flow;
- mean normalized signed margin flow;
- mean absolute normalized flows;
- margin-decreasing fraction;
- margin-increasing fraction;
- number of turning-surface crossing intervals.

The phase-summary file is the preferred source for interpreting Dataset B because it preserves:

pre-bounce approach

turning surface

post-bounce recession

as separate structural phases.

REPRODUCIBILITY

Run from:

ABC_bridge/tools/

Command:

python build_abc_route_profiles_v1_1.py

Default input:

../outputs/ABC_orientation_sensitive_bridge_v1_1.csv

Default outputs:

../outputs/ABC_orientation_sensitive_route_profile_v1_1.csv

../outputs/ABC_orientation_sensitive_phase_summary_v1_1.csv

The default number of route bins is:

50

A different bin count can be requested with:

python build_abc_route_profiles_v1_1.py --bins NUMBER

Example:

python build_abc_route_profiles_v1_1.py --bins 100

The B turning-surface profile remains separate regardless of the ordinary-phase bin count.

FOLDER PLACEMENT

ABC_bridge/
├── tools/
│   └── build_abc_route_profiles_v1_1.py
├── outputs/
│   ├── ABC_orientation_sensitive_bridge_v1_1.csv
│   ├── ABC_orientation_sensitive_route_profile_v1_1.csv
│   └── ABC_orientation_sensitive_phase_summary_v1_1.csv
└── README_ABC_route_profiles_v1_1.txt

DEPENDENCIES

Python 3

pandas

numpy

Install missing dependencies with:

python -m pip install pandas numpy

PROVENANCE

The route-profile and phase-summary datasets are not independent raw data.

They are derived deterministically from:

ABC_orientation_sensitive_bridge_v1_1.csv

The derivation consists of:

1. phase mapping;
2. route-coordinate grouping;
3. equal-width binning for ordinary phases;
4. dedicated preservation of the B turning surface;
5. aggregation of signed and absolute flow statistics.

No physical values are invented or manually inserted.

The derived files can be regenerated at any time from the accepted Bridge v1.1 interval dataset.

INTERPRETIVE STATUS

The route-profile dataset is suitable for:

- plotting signed route dynamics;
- comparing terminal approach and boundary recession;
- displaying Dataset B branch symmetry;
- locating turning-surface behavior;
- preparing the consolidated Cosmological Boundary Routing synthesis.

The phase-summary dataset is suitable for:

- branch-resolved numerical comparison;
- result records;
- tables;
- route-topology interpretation.

INTERPRETIVE LIMITS

The shared route coordinate is path intrinsic.

It is not yet a physical metric distance on the admissibility manifold.

The normalized flows use dataset-specific Q90 scales inherited from Bridge v1.1.

They compare direction and relative within-path response, not absolute physical amplitudes between cosmological models.

boundary_margin_candidate remains provisional.

CURRENT STATUS

Bridge v1.1 interval dataset:
COMPLETE

Route-profile generator:
COMPLETE

Route-profile dataset:
COMPLETE

Phase-summary dataset:
COMPLETE

Branch-resolved Dataset B interpretation:
PRESERVED

Reproducibility:
PASS

NEXT STEP

Use:

ABC_BRIDGE_V1_1_RESULT.txt

ABC_orientation_sensitive_route_profile_v1_1.csv

ABC_orientation_sensitive_phase_summary_v1_1.csv

together with the direct STRUC-PERC-I, STRUC-I, and alpha results for Datasets A, B, and C to prepare the consolidated Cosmological Boundary Routing synthesis.
