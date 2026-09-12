README.txt
TCV Fragment-Isolate Mapper
UNNS-H Mode Project

File:
components/tcv_fragment_isolate_mapper.py

Purpose:
This component identifies which actual TCV shots / rows are responsible for the hard-fragmentation signals found by STRUC-PERC-I in the UNNS-H Mode project.

It is the bridge between chamber-level structural output and physical plasma-event interpretation.

The chambers told us that some scalar ladders fragment. This mapper answers the next question:

Which shots, event times, plasma conditions, species settings, power-balance values, and edge/divertor indicators sit on those fragmented branches?

Context:
The TCV L-H transition dataset was first converted into a canonical event table:

data/processed/tcv_lh_events_canonical.csv

Then two chamber families were run:

1. STRUC-I v1.0.4
   Purpose: perturbation admissibility of ordered scalar ladders.

2. STRUC-PERC-I v2.5.0
   Purpose: gap-graph connectivity, percolation, hard fragmentation, and isolated branch detection.

The mapper should be used after STRUC-PERC-I has produced batch JSON outputs.

Primary Inputs:
1. Canonical TCV event table:
   data/processed/tcv_lh_events_canonical.csv

2. STRUC-PERC-I all-events batch result:
   outputs/reports/struc_perc_batch_results.json

3. STRUC-PERC-I L-H-only batch result:
   outputs/reports/struc_perc_batch_results_lh_only.json

Target Variables:
The mapper focuses on variables that showed hard fragmentation or near-branching behavior:

- chi_eff_candidate
- P_total_candidate_MW
- P_total_aux_candidate_MW
- P_loss_candidate_MW
- event_time
- divertor_signal_candidate

These variables are important because they sit close to the physical H-mode problem: transport, power balance, transition timing, and edge/divertor response.

Main Outputs:
The script writes its results into:

outputs/reports/

Expected output files:

1. tcv_fragment_component_summary.csv
   Summary of connected / fragmented components per target variable.

2. tcv_fragment_gap_map.csv
   Gap-level map showing which values create isolated or non-giant branches.

3. tcv_suspect_transition_families.csv
   Main physical interpretation table. This maps suspect branches back to shots, event times, labels, species, density, power, and geometry.

4. tcv_fragment_isolate_mapping_report.md
   Human-readable report summarizing the mapping results.

5. tcv_fragment_isolate_mapping_summary.json
   Machine-readable summary for downstream pipeline use.

Recommended Documentation Copy:
Also copy the human-readable report into:

docs/07_FRAGMENT_ISOLATE_MAPPING_REPORT.md

Run Command:
From the project root, run:

python components/tcv_fragment_isolate_mapper.py --canonical data/processed/tcv_lh_events_canonical.csv --all-perc-json outputs/reports/struc_perc_batch_results.json --lh-perc-json outputs/reports/struc_perc_batch_results_lh_only.json --out-dir outputs/reports

Windows PowerShell form:

python components\tcv_fragment_isolate_mapper.py --canonical data\processed\tcv_lh_events_canonical.csv --all-perc-json outputs\reports\struc_perc_batch_results.json --lh-perc-json outputs\reports\struc_perc_batch_results_lh_only.json --out-dir outputs\reports

Required Python Packages:
- pandas
- numpy

Install if needed:

python -m pip install pandas numpy

How to Read the Results:
Start with:

outputs/reports/tcv_suspect_transition_families.csv

Inspect HIGH-priority rows first.

A HIGH-priority row does not mean the shot is wrong or should be discarded. It means the shot or row sits on a structurally unusual branch relative to the rest of the TCV L-H transition corpus.

Interpretation Guide:
- FULL_PERCOLATION variables are structurally connected across the sampled corpus.
- HARD_FRAGMENTATION variables contain isolated or non-giant branches.
- Isolated branches may indicate distinct physical regimes, special transition pathways, unusual operating conditions, or data-quality cases requiring inspection.

UNNS Interpretation:
The mapper helps test the working hypothesis:

H-mode access is not explained by total heating power alone. Instead, it may depend on whether the plasma edge enters a boundary-admissible configuration involving power balance, transport response, timing, and edge/divertor structure.

The mapper therefore searches for candidate transition families: groups of shots or rows that may represent different H-mode access corridors.

What Not to Claim Yet:
This component does not prove the physical origin of H-mode.
It does not prove causality.
It does not replace plasma diagnostics or tokamak transport modeling.
It identifies structurally exceptional branches that deserve physical inspection.

Immediate Next Analysis After Running:
1. Open tcv_suspect_transition_families.csv.
2. Sort by priority, then by variable and branch/component size.
3. Compare recurring shots across different fragmented variables.
4. Check whether the same shots appear in power-balance, timing, and transport branches.
5. Use those recurring shots as candidates for deeper time-series/profile analysis.

Project Rule:
Do not create new chamber runs before inspecting the mapped shots. The purpose of this stage is to move from abstract structural classification to actual plasma-event interpretation.
