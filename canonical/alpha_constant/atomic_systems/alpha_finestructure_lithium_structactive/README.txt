alpha_finestructure_lithium_structactive
========================================

What this pack is
-----------------
This pack upgrades the observed lithium spectrum into a structurally active alpha-family.

Source:
    lithium_levels_raw.csv

Input table summary
-------------------
Observed levels parsed: 182
Distinct configurations: 91
Distinct (Configuration, Term) multiplets: 92

Why this is different from uniform alpha^2 scaling
--------------------------------------------------
Simple uniform rescaling leaves ladder geometry unchanged.
This pack instead applies a non-uniform proxy deformation seeded from the real observed lithium multiplet structure.

Model used
----------
Each observed level is decomposed as:

    Level = configuration_centroid + term_offset + J_resolved_fine_structure_offset

Then alpha variation is applied as:

    Level(alpha) =
        configuration_centroid
        + term_offset * (alpha/alpha0)^p_term
        + fine_structure_offset * (alpha/alpha0)^q_fs

where p_term and q_fs vary by configuration/term proxies:
    - principal shell n
    - orbital character l
    - multiplicity

Files
-----
For each alpha_scale in the sweep:
    - lithium_structactive_levels_alpha_XX.csv
    - lithium_structactive_gaps_alpha_XX.csv
    - lithium_structactive_fs_alpha_XX.csv

Ladder meanings:
    levels: full transformed level ladder
    gaps: adjacent-gap ladder from transformed levels
    fine_structure_splittings: positive J-resolved splittings within each multiplet

Sweep included
--------------
Coarse:
    0.80 to 1.20 step 0.05

Refined:
    0.95 to 1.05 step 0.01

Structural-activity sanity check
--------------------------------
Mean absolute difference between normalized gap profiles:
    alpha 0.80 vs 1.00 : 3.972335
    alpha 1.00 vs 1.20 : 4.705811
    alpha 0.80 vs 1.20 : 8.678104

Recommended first run
---------------------
Start with:
    lithium_structactive_gaps_alpha_0.80.csv
    lithium_structactive_gaps_alpha_1.00.csv
    lithium_structactive_gaps_alpha_1.20.csv

Then compare:
    - mean rho
    - max rho
    - regime
    - state
