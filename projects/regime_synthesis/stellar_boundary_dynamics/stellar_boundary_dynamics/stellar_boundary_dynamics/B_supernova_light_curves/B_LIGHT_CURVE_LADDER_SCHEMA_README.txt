# B_LIGHT_CURVE_LADDER_SCHEMA_README.txt
# STELLAR_BOUNDARY_DYNAMICS_I
# Phase B — Supernova Light-Curve Ladder Schema

PURPOSE:
Define the canonical STRUC_PERC_I-compatible schema for Phase B supernova
light-curve ladders.

PHASE:
B_supernova_light_curves

SCHEMA_FILE:
B_light_curve_ladder_schema.csv

UNNS ROLE:
Phase B turns observed supernova brightness-time records into ordered
post-boundary observable ladders. These ladders do not represent the hidden
pre-collapse stellar interior. They represent the observable response after the
collapse/explosion event has routed the progenitor into ejecta and remnant
basins.

PRIMARY SOURCES:
B1 — Open Supernova Catalog / AstroCats
B2 — Zwicky Transient Facility public releases / IRSA / AWS Open Data
B3 — Transient Name Server

CANONICAL LIGHT-CURVE STAGES:
pre_discovery_or_baseline
rise
peak
early_decline
plateau_or_shoulder
break
tail_decay
late_relaxation

CONTROLLED VALUES:

brightness_unit:
mag
flux
normalized_flux
unknown

phase_name:
pre_discovery_or_baseline
rise
peak
early_decline
plateau_or_shoulder
break
tail_decay
late_relaxation
unclassified

transition_marker:
none
rise_onset
peak
decline_onset
plateau_onset
plateau_end
break
tail_onset
late_relaxation
data_gap
ambiguous

boundary_role:
baseline_context
boundary_response_rise
maximum_observable_response
post_boundary_relaxation
plateau_or_buffer_regime
transition_break
tail_decay
late_basin_relaxation
unknown

struc_perc_role:
observable_ladder_state
transition_state
boundary_response_state
relaxation_state
quality_excluded

support_regime_proxy:
unknown
shock_cooling
ejecta_cooling
recombination_plateau
radioactive_tail
circumstellar_interaction
late_remnant_relaxation
ambiguous

MINIMUM REQUIRED COLUMNS FOR FIRST PILOT:
ladder_id
source_id
source_name
object_name
supernova_type
band
stage_index
phase_name
time_mjd
brightness_value
brightness_unit
boundary_role
struc_perc_role
unns_interpretation

FIRST PILOT OBJECTS:
SN 1987A
SN 1993J
SN 1999em
SN 2011dh
SN 2012aw
SN 2013ej

PIPELINE POSITION:
B1/B2/B3 source records
→ raw photometry/metadata
→ B_light_curve_ladder_schema.csv
→ object-specific canonical ladder CSV files
→ STRUC_PERC_I ladder conversion
→ α-application / deformation grid
→ 5D structural vector

NOTES:
The schema is intentionally source-neutral. OSC, ZTF, and TNS fields should be
mapped into this structure rather than preserved as incompatible source-specific
tables.

Magnitude data must be handled carefully because lower magnitude means higher
brightness. Any normalization step must record whether the sequence is stored in
magnitude, flux, or normalized flux form.
