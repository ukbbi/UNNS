MU Tier-A molecular packs generated from uploaded HITRAN .par files.

Contents
- co_transition_table_tierA.csv
- h2_transition_table_tierA.csv
- co/ and h2/ subfolders with 17 beta-swept levels and gaps ladders each
- per-molecule manifest CSVs

Method
- Parsed raw HITRAN .par files for CO and H2.
- Extracted vibrational labels from global quanta.
- Extracted rotational branch/J from local lower quanta.
- Built empirical state-energy decomposition:
  E_state = E_v_base + E_r_resid
  where E_v_base is the minimum observed state energy within each vibrational manifold
  (for H2, within each vibrational+symmetry manifold), and E_r_resid is the residual.
- Applied mu deformation:
  E_v -> beta^(-1/2)
  E_r -> beta^(-1)
- Built deformed transition ladders from absolute upper-lower state energy differences.
- Sorted values ascending for levels ladders; gaps ladders are adjacent differences.

Beta grid
[0.8, 0.85, 0.9, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0, 1.01, 1.02, 1.03, 1.04, 1.05, 1.1, 1.15, 1.2]

Notes
- CO: clean Tier-A path.
- H2: Tier-A path validated from branch decoding O/Q/S and lower-state J extraction.
- H2 produces some sign reversals in raw upper-lower differences away from beta=1.00;
  the exported transition energies use absolute state-energy differences, which preserves
  physical line frequencies under deformation.
- CSV format: single column header 'value' for chamber-style ingestion.

Source files
- Uploaded archive: co_h2.zip
- Raw files: CO.par, H2.par
