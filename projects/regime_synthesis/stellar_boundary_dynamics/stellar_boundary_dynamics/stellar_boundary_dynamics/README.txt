README.txt
STELLAR_BOUNDARY_DYNAMICS_I
Astrophysical Boundary Dataset — A/B/C Structural Pipeline

PROJECT:
stellar_boundary_dynamics

PURPOSE:
This folder contains the working dataset and pipeline for a three-layer
structural study of stellar boundary dynamics.

The task was to test whether a catastrophic astrophysical boundary can be
represented as linked structural ladders across three related but different
data regimes:

A — pre-supernova radial stellar structure
B — post-collapse supernova light curves
C — post-collapse spectral time series

The central question:

Can a massive-star boundary event be represented as a transition from a
pre-boundary support/composition structure into multiple post-boundary
observable relaxation regimes?

In practical terms, the pipeline asks whether:

1. pre-supernova radial profiles,
2. supernova brightness-response curves,
3. spectral element-line evolution,

can all be converted into comparable structural ladders, processed through
STRUC-PERC-I, alpha-application, normalization review, and finally compared
through bridge geometry.

This README summarizes the complete work performed in this folder.

==============================================================================
TOP-LEVEL FOLDER STRUCTURE
==============================================================================

stellar_boundary_dynamics/
  A_mesa_precollapse_tracks/
  B_supernova_light_curves/
  C_spectral_time_series/
  AB_bridge/
  BC_bridge/
  tools/

A_mesa_precollapse_tracks/
  Phase A: pre-supernova radial profile structures.

B_supernova_light_curves/
  Phase B: observed post-collapse light-curve response trajectories.

C_spectral_time_series/
  Phase C: observed post-collapse spectral line-evolution trajectories.

AB_bridge/
  Bridge between Phase A and Phase B.

BC_bridge/
  Bridge between Phase B and Phase C.

tools/
  Shared bridge/comparison scripts placed at the parent dataset level.

==============================================================================
PHASE A — PRE-SUPERNOVA RADIAL PROFILES
==============================================================================

Folder:
A_mesa_precollapse_tracks/

Purpose:
Phase A represents the pre-boundary side of the stellar system.

The original idea was to use MESA pre-collapse tracks. Since local MESA execution
was unavailable, we used public precomputed pre-supernova profile data from
Zenodo 5556959:

Different to the core: the pre-supernova structures of massive single and
binary-stripped stars.

Selected Phase A files:
  profile_single_M12.09_128net.data
  profile_single_M19.98_128net.data

These were treated as real terminal/pre-supernova radial profile snapshots, not
as MESA inlist scaffolds and not as full time-resolved history.data tracks.

Main Phase A objects:
  A1_12M
  A2_20M

Phase A pipeline:

1. Inspect pre-supernova .data profile structure.
2. Convert profile .data files into radial profile ladders.
3. Convert profile ladders into STRUC-PERC-I canonical inputs.
4. Convert canonical inputs into numeric STRUC-PERC-I ladders.
5. Run numeric ladders through STRUC-PERC-I.
6. Interpret STRUC-PERC-I results.
7. Apply alpha-deformation to canonical inputs.
8. Produce alpha-grids and first-pass 5D vectors.
9. Perform normalization review.
10. Produce A_5D_VECTOR_SUMMARY_v2.csv for bridge work.

Important Phase A scripts:
  tools/a_presupernova_profile_to_ladder.py
  tools/a_profile_ladder_to_struc_perc_i.py
  tools/a_alpha_apply.py
  tools/a_alpha_normalization_review.py

Important Phase A outputs:

A_mesa_precollapse_tracks/ladders/
  A1_12M_presupernova_profile_ladder.csv
  A2_20M_presupernova_profile_ladder.csv

A_mesa_precollapse_tracks/struc_perc_i/canonical_inputs/
  A1_12M_struc_perc_input.csv
  A2_20M_struc_perc_input.csv

A_mesa_precollapse_tracks/struc_perc_i/numeric_ladders/
  A1_12M_numeric_ladder.txt
  A2_20M_numeric_ladder.txt

A_mesa_precollapse_tracks/struc_perc_i/
  struc_perc_batch_results.csv
  struc_perc_batch_results.json

A_mesa_precollapse_tracks/alpha_application/grids/
  A1_12M_alpha_grid.csv
  A2_20M_alpha_grid.csv

A_mesa_precollapse_tracks/alpha_application/vectors/
  A1_12M_5d_vector.csv
  A2_20M_5d_vector.csv

A_mesa_precollapse_tracks/alpha_application/normalization_review/
  A_ALPHA_NORMALIZATION_REVIEW.csv
  A_5D_VECTOR_SUMMARY_v2.csv
  A_NORMALIZATION_REVIEW_INTERPRETATION.txt

Phase A STRUC-PERC-I result:
Both real pre-supernova radial-profile ladders returned FULL_PERCOLATION.

A1_12M:
  FULL_PERCOLATION
  kappa_connect = 2
  tailDominance = 0

A2_20M:
  FULL_PERCOLATION
  kappa_connect = 1
  tailDominance = 0

Phase A interpretation:
The selected pre-supernova radial structures are internally connected under
STRUC-PERC-I. They are valid as pre-boundary radial support/composition ladders.

Phase A caution:
The profiles are real pre-supernova radial snapshots, not full time-series
stellar evolution histories.

Normalization review:
Both A objects required scale review because composition response dominated the
raw alpha-vector scale. Therefore, A-B comparison must use:

  A_5D_VECTOR_SUMMARY_v2.csv

not the raw v1 vector summary.

==============================================================================
PHASE B — SUPERNOVA LIGHT CURVES
==============================================================================

Folder:
B_supernova_light_curves/

Purpose:
Phase B represents post-collapse brightness-response trajectories.

Data source:
Open Supernova Catalog / AstroCats-derived supernova JSON light-curve data.

Phase B pilot/full object set:
  SN1987A
  SN1993J
  SN1999em
  SN2011dh
  SN2012aw
  SN2013ej

Phase B pipeline:

1. Collect raw Open Supernova Catalog / AstroCats JSON files.
2. Convert raw photometry into light-curve ladders.
3. Compress light-curve ladders into STRUC-PERC-I canonical inputs.
4. Extract numeric ladders for STRUC-PERC-I.
5. Run numeric ladders through STRUC-PERC-I.
6. Interpret STRUC-PERC-I results.
7. Apply alpha-deformation.
8. Produce alpha-grids and first-pass 5D vectors.
9. Perform normalization review.
10. Produce B_5D_VECTOR_SUMMARY_v2.csv for bridge work.

Important Phase B scripts:
  tools/osc_to_b_ladder.py
  tools/b_ladder_to_struc_perc_i.py
  tools/b_struc_input_to_numeric_ladders.py
  tools/b_alpha_apply.py
  tools/b_alpha_normalization_review.py

Important Phase B outputs:

B_supernova_light_curves/ladders/
  B_SN1987A_light_curve_ladder.csv
  B_SN1993J_light_curve_ladder.csv
  B_SN1999em_light_curve_ladder.csv
  B_SN2011dh_light_curve_ladder.csv
  B_SN2012aw_light_curve_ladder.csv
  B_SN2013ej_light_curve_ladder.csv

B_supernova_light_curves/struc_perc_i/canonical_inputs/
  B_SN1987A_struc_perc_input.csv
  B_SN1993J_struc_perc_input.csv
  B_SN1999em_struc_perc_input.csv
  B_SN2011dh_struc_perc_input.csv
  B_SN2012aw_struc_perc_input.csv
  B_SN2013ej_struc_perc_input.csv

B_supernova_light_curves/struc_perc_i/numeric_ladders/
  B_SN1987A_numeric_ladder.txt
  B_SN1993J_numeric_ladder.txt
  B_SN1999em_numeric_ladder.txt
  B_SN2011dh_numeric_ladder.txt
  B_SN2012aw_numeric_ladder.txt
  B_SN2013ej_numeric_ladder.txt

B_supernova_light_curves/alpha_application/normalization_review/
  B_ALPHA_NORMALIZATION_REVIEW.csv
  B_5D_VECTOR_SUMMARY_v2.csv
  B_NORMALIZATION_REVIEW_INTERPRETATION.txt

Phase B STRUC-PERC-I result:
All six Phase B light-curve ladders reached FULL_PERCOLATION.

Phase B interpretation:
The light-curve response layer forms connected post-collapse brightness
trajectories.

Phase B special case:
SN2012aw emerged as the main high-tail / high-kappa special object in the
light-curve layer.

Normalization review:
Most B objects required scale review. The bridge layer must use:

  B_5D_VECTOR_SUMMARY_v2.csv

not the raw v1 vector summary.

==============================================================================
PHASE C — SPECTRAL TIME SERIES
==============================================================================

Folder:
C_spectral_time_series/

Purpose:
Phase C represents post-collapse spectral element-line evolution.

Data source:
WISeREP public spectra.

Pilot objects:
  C1_SN1993J
  C2_SN2012aw

Why these two:
  SN1993J was the closest Phase B object to A2_20M in the A-B bridge.
  SN2012aw was the strongest special/outlier case in Phase B and the A-B bridge.

Phase C pipeline:

1. Collect public WISeREP spectra for SN1993J and SN2012aw.
2. Preserve raw spectra and WISeREP metadata.
3. Convert spectra into spectral line-window ladders.
4. Convert line ladders into STRUC-PERC-I canonical inputs.
5. Extract numeric spectral ladders.
6. Run numeric ladders through STRUC-PERC-I.
7. Interpret STRUC-PERC-I results.
8. Apply alpha-deformation.
9. Produce alpha-grids and first-pass 5D vectors.
10. Perform normalization review.
11. Produce C_5D_VECTOR_SUMMARY_v2.csv for bridge work.

Target spectral features:
  H_alpha
  H_beta
  He_I_5876
  O_I_7774
  Ca_II_NIR
  Si_II_6355
  Fe_II_5169
  Ni_Co_decay_proxy

Important Phase C scripts:
  tools/c_spectra_to_line_ladder.py
  tools/c_line_ladder_to_struc_perc_i.py
  tools/c_alpha_apply.py
  tools/c_alpha_normalization_review.py

Important Phase C outputs:

C_spectral_time_series/ladders/
  C1_SN1993J_spectral_line_ladder.csv
  C2_SN2012aw_spectral_line_ladder.csv

C_spectral_time_series/struc_perc_i/canonical_inputs/
  C1_SN1993J_struc_perc_input.csv
  C2_SN2012aw_struc_perc_input.csv

C_spectral_time_series/struc_perc_i/numeric_ladders/
  C1_SN1993J_numeric_ladder.txt
  C2_SN2012aw_numeric_ladder.txt

C_spectral_time_series/alpha_application/grids/
  C1_SN1993J_alpha_grid.csv
  C2_SN2012aw_alpha_grid.csv

C_spectral_time_series/alpha_application/vectors/
  C1_SN1993J_5d_vector.csv
  C2_SN2012aw_5d_vector.csv

C_spectral_time_series/alpha_application/normalization_review/
  C_ALPHA_NORMALIZATION_REVIEW.csv
  C_5D_VECTOR_SUMMARY_v2.csv
  C_NORMALIZATION_REVIEW_INTERPRETATION.txt

Phase C line ladder extraction:
  C1_SN1993J: 100 spectra parsed, 685 ladder rows.
  C2_SN2012aw: 85 spectra parsed, 560 ladder rows.

Phase C STRUC-PERC-I result:
Both spectral numeric ladders returned FULL_PERCOLATION.

C1_SN1993J:
  FULL_PERCOLATION
  kappa_connect ≈ 201.404839
  tailDominance ≈ 0.570046
  n = 685

C2_SN2012aw:
  FULL_PERCOLATION
  kappa_connect ≈ 3992.353937
  tailDominance ≈ 0.959429
  n = 198

Phase C interpretation:
Both spectral line-evolution ladders are internally connected, but SN2012aw is
much more extreme in kappa_connect and tailDominance.

Normalization review:
Both Phase C objects required scale review.

C1_SN1993J:
  scale_review_needed = yes
  high_tail_attention = no
  high_kappa_attention = no
  max_channel = flux

C2_SN2012aw:
  scale_review_needed = yes
  high_tail_attention = yes
  high_kappa_attention = yes
  max_channel = flux

The safe bridge file is:

  C_5D_VECTOR_SUMMARY_v2.csv

Scientific caution:
Spectral line-window proxies are structural spectral features. They are not
direct abundance measurements, radiative-transfer outputs, or nucleosynthesis
yield reconstructions.

==============================================================================
A-B BRIDGE — PRE-COLLAPSE PROFILE VS LIGHT CURVE
==============================================================================

Folder:
AB_bridge/

Purpose:
Compare the Phase A pre-supernova radial-profile vector domain against the Phase
B post-collapse light-curve vector domain.

Inputs:
AB_bridge/inputs/
  A_5D_VECTOR_SUMMARY_v2.csv
  B_5D_VECTOR_SUMMARY_v2.csv

Important script:
  tools/ab_bridge_compare.py

Outputs:
AB_bridge/comparisons/
  AB_VECTOR_PAIRWISE_COMPARISON.csv
  AB_DOMAIN_CENTROID_COMPARISON.csv
  AB_OBJECT_RANKING.csv

AB_bridge/summaries/
  AB_BRIDGE_SUMMARY.csv
  AB_BRIDGE_INTERPRETATION.txt
  AB_BRIDGE_RESULT_RECORD.txt

Main A-B result:
  centroid distance = 0.584026232738
  separation label = weak_separation

Closest A-B pair:
  A2_20M <-> B_SN1993J
  distance = 0.232685521403

Most separated A-B pair:
  A1_12M <-> B_SN2012aw
  distance = 2.0846018436

Interpretation:
Pre-supernova radial structure and post-collapse light-curve response are not
identical, but they are not strongly separated. They form a weakly separated
pre-boundary to post-boundary structural bridge.

Key object roles:
  SN1993J = contact-like bridge object.
  SN2012aw = persistent outlier / high-tail candidate.

==============================================================================
B-C BRIDGE — LIGHT CURVE VS SPECTRAL LINE EVOLUTION
==============================================================================

Folder:
BC_bridge/

Purpose:
Compare the Phase B post-collapse light-curve vector domain against the Phase C
post-collapse spectral line-evolution vector domain.

Inputs:
BC_bridge/inputs/
  B_5D_VECTOR_SUMMARY_v2.csv
  C_5D_VECTOR_SUMMARY_v2.csv

Important script:
  tools/bc_bridge_compare.py

Outputs:
BC_bridge/comparisons/
  BC_VECTOR_PAIRWISE_COMPARISON.csv
  BC_DOMAIN_CENTROID_COMPARISON.csv
  BC_OBJECT_ALIGNMENT.csv

BC_bridge/summaries/
  BC_BRIDGE_SUMMARY.csv
  BC_BRIDGE_INTERPRETATION.txt
  BC_BRIDGE_RESULT_RECORD.txt

Main B-C result:
  centroid distance = 1.31753512889
  separation label = strong_separation

Closest B-C pair:
  B_SN2012aw <-> C1_SN1993J
  distance = 0.64829362306

Most separated B-C pair:
  B_SN1987A <-> C2_SN2012aw
  distance = 2.6457282231

Object-matched alignment:
  SN1993J:
    B_SN1993J <-> C1_SN1993J
    distance = 0.712109467708
    matched pair is nearest = yes

  SN2012aw:
    B_SN2012aw <-> C2_SN2012aw
    distance = 1.92329396256
    matched pair is nearest = no

Interpretation:
Light-curve response and spectral line-evolution are strongly separated
post-collapse observables.

SN1993J behaves coherently across B and C.

SN2012aw remains special, but its light-curve and spectral forms do not align as
a simple nearest-neighbor pair.

This means the spectral layer adds independent structural information rather
than duplicating the light-curve layer.

==============================================================================
OVERALL SCIENTIFIC GAIN
==============================================================================

This folder now contains a working three-layer astrophysical boundary dataset.

The dataset shows:

1. A pre-boundary support/composition layer:
   A — pre-supernova radial profiles.

2. A post-boundary brightness-response layer:
   B — supernova light curves.

3. A post-boundary spectral-redistribution layer:
   C — spectral line evolution.

The complete processing chain demonstrates that very different physical data
types can be transformed into a common structural workflow:

raw data
-> domain ladder
-> STRUC-PERC-I canonical input
-> numeric ladder
-> STRUC-PERC-I result
-> alpha-application grid
-> 5D vector
-> normalization-reviewed v2 vector
-> bridge comparison

Main empirical pattern:

A-B:
  weak separation

B-C:
  strong separation

SN1993J:
  contact/coherence case

SN2012aw:
  persistent high-tail / high-kappa / representation-dependent anomaly

Interpretation:
The stellar boundary does not collapse into one observable coordinate. It routes
through multiple admissible but structurally distinct observational regimes.

This supports a boundary-transition picture:

pre-supernova radial support/composition structure
-> collapse/explosion boundary
-> post-collapse light-curve relaxation
-> post-collapse spectral line redistribution

==============================================================================
RELATION TO THE WIDER UNNS SUBSTRATE PROGRAM
==============================================================================

This dataset adds a catastrophic boundary-transition corpus to the existing
UNNS / STRUC-PERC / CLE / admissibility program.

Earlier manuscripts and corpora established:

  admissibility regions
  connectivity margins
  phase classes
  percolative realizability
  local boundary geometry
  structural trajectories
  cluster formation
  representation-dependent rigidity

This folder adds:

  terminal support failure
  catastrophic transition
  post-boundary routing
  multi-observable separation
  persistent anomaly tracking
  bridge geometry across observational channels

In UNNS terms:

A:
  pre-boundary Phi/tau support-composition ladder

B:
  post-boundary luminosity-response ladder

C:
  post-boundary spectral-redistribution ladder

AB_bridge:
  pre-boundary to post-boundary contact/separation test

BC_bridge:
  post-boundary observable-channel separation test

The key theoretical contribution is that a physical boundary event can be
represented not as one trajectory but as a linked cluster of admissible ladders
connected through bridge geometry.

==============================================================================
WHAT THIS DOES NOT CLAIM
==============================================================================

This dataset does not claim direct supernova prediction.

It does not perform full hydrodynamical explosion modeling.

It does not perform radiative-transfer modeling.

It does not recover nucleosynthesis yields.

It does not claim spectra are direct abundance maps.

It does not claim two Phase A profiles represent all massive-star progenitors.

It does not claim six Phase B light curves represent all core-collapse
supernovae.

It does not claim two Phase C spectra sets represent all spectral behavior.

The valid claim is structural:

The dataset provides a first multi-layer structural comparison of a catastrophic
stellar boundary transition using pre-supernova profiles, light curves, and
spectral time series.

==============================================================================
NEXT LOGICAL STEP
==============================================================================

Create the tri-domain bridge:

ABC_bridge/

Required inputs:
  A_mesa_precollapse_tracks/alpha_application/normalization_review/A_5D_VECTOR_SUMMARY_v2.csv
  B_supernova_light_curves/alpha_application/normalization_review/B_5D_VECTOR_SUMMARY_v2.csv
  C_spectral_time_series/alpha_application/normalization_review/C_5D_VECTOR_SUMMARY_v2.csv

Purpose:
Compare A, B, and C together as one structural boundary system.

Questions for ABC bridge:

1. Does the three-layer system form a transition chain?
   A -> B -> C

2. Does C branch away from B as an independent post-collapse observable regime?

3. Does SN2012aw remain a persistent boundary anomaly across all available
   layers?

4. Does SN1993J remain the best contact object across the full chain?

5. Does the stellar boundary system behave as a cluster of linked admissible
   regions rather than a single trajectory?

==============================================================================
STATUS
==============================================================================

Phase A complete through normalization-reviewed v2 vectors.
Phase B complete through normalization-reviewed v2 vectors.
Phase C complete through normalization-reviewed v2 vectors.

A-B bridge complete.
B-C bridge complete.

Ready for:
  ABC_bridge initialization.
