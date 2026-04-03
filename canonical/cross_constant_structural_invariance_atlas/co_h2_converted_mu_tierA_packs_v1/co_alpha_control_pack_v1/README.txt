CO alpha control pack v1

Purpose:
- Provide a direct alpha-column comparison for the same CO rovibrational transition ladder used in the mu study.

Status:
- Control-grade alpha conversion, not a new alpha-activity protocol.
- Uses physically conservative uniform non-relativistic molecular scaling: transition energies scale as alpha^2.
- Because the scaling is uniform, ordering and gap ratios are preserved exactly; STRUC-I is therefore expected to return a flat Type I / invariant response up to numerical noise.

Source:
- co_transition_table_tierA.csv from mu_tierA_packs_v1.zip

Sweep:
- alpha in {0.80, 0.85, 0.90, 0.95, 0.96, 0.97, 0.98, 0.99, 1.00, 1.01, 1.02, 1.03, 1.04, 1.05, 1.10, 1.15, 1.20}

Files:
- co/co_alpha_<alpha>_levels.csv
- co/co_alpha_<alpha>_gaps.csv
- co_alpha_manifest.csv
