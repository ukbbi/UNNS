TCV SUSPECT SHOT REVIEWER
UNNS-H Mode Project

FILE
  components/tcv_suspect_shot_reviewer.py

PURPOSE
  This script performs the immediate post-fragment-mapping analytical step.
  It does not run another chamber. It creates a focused one-row-per-shot table
  around recurrent TCV shots identified by the fragment/isolate mapping stage.

WHY THIS EXISTS
  STRUC-I showed that the TCV L-H scalar ladders are broadly admissible.
  STRUC-PERC-I showed that selected variables fragment, especially variables
  connected to power balance, transport, timing, and edge/divertor response.
  The fragment-isolate mapper localized those fragment branches to candidate
  shots. This reviewer turns those candidate shots into a physical inspection
  table.

DEFAULT REVIEWED SHOTS
  69807
  68001
  69668
  69892
  66445
  68719
  69913
  67992
  68206

INPUTS
  data/processed/tcv_lh_events_canonical.csv
  outputs/reports/tcv_suspect_transition_families.csv

OUTPUTS
  outputs/reports/tcv_suspect_shot_review.csv
  outputs/reports/tcv_suspect_shot_review.md
  outputs/reports/tcv_suspect_shot_review_summary.json

RUN COMMAND FROM PROJECT ROOT
  python components\tcv_suspect_shot_reviewer.py --canonical data\processed\tcv_lh_events_canonical.csv --families outputs\reports\tcv_suspect_transition_families.csv --out-dir outputs\reports

WHAT THE CSV CONTAINS
  One row per recurrent shot, including:

  SHOT
  TIME
  ILH
  P_LH_candidate_MW
  P_total_candidate_MW
  P_total_aux_candidate_MW
  P_loss_candidate_MW
  dWmhd_dt_candidate_MW
  Wmhd_J
  n_e_1e20_m3
  I_p_MA
  B_t_T
  q95
  kappa
  delta
  hydrogen_fraction_candidate
  helium_fraction_candidate
  Z_eff
  n_Ryter
  P_Ryter
  chi_eff_candidate
  divertor_signal_candidate
  divertor_signal_150_candidate
  fragment_variables
  fragment_count

  The table also includes helper columns:

  canonical_event_rows
  event_time_min
  event_time_max
  fragment_subsets
  fragment_roles
  fragment_component_ids
  fragment_tags
  P_total_level
  P_loss_level
  n_e_level
  helium_fraction_level
  chi_eff_level
  divertor_signal_level

HOW TO READ THE RESULT
  fragment_variables lists which fragmented variables touched the shot.
  fragment_count counts how many mapped fragment-family records involve the shot.
  fragment_tags gives a preliminary physical grouping:

  power_balance_branch
  transport_branch
  edge_divertor_response_branch
  timing_branch
  density_threshold_branch
  species_branch

IMPORTANT CAUTION
  A recurrent shot is not automatically a bad shot or a causal explanation.
  It is a candidate member of a structural transition family. The next step is
  physical review: compare these rows against the source README/notebook and, if
  possible, inspect machine-specific diagnostic traces for those shots.
