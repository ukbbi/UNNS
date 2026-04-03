alpha_finestructure_helium_structactive
=======================================

What this pack is
-----------------
This pack upgrades the observed helium spectrum into a structurally active alpha-family.

Source:
    helium_levels_raw.txt

Why this is different from uniform alpha^2 scaling
--------------------------------------------------
Simple uniform rescaling leaves ladder geometry unchanged.
This pack instead applies a non-uniform proxy deformation seeded from the real observed helium multiplet structure.

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

This makes alpha structurally active because different parts of the spectrum deform with different exponents.

Important boundary
------------------
This is not an ab initio helium calculation.
It is a physically motivated proxy extension built from the observed helium level table so that alpha changes spacing geometry rather than only scale.

Files
-----
For each alpha_scale in the sweep:
    - helium_structactive_levels_alpha_XX.csv
    - helium_structactive_gaps_alpha_XX.csv
    - helium_structactive_fs_alpha_XX.csv

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

Chamber format
--------------
All ladders are chamber-ready:
    - single column
    - header: value
    - sorted ascending

Structural-activity sanity check
--------------------------------
Mean absolute difference between normalized gap profiles:
    alpha 0.80 vs 1.00 : 1234389.765855
    alpha 1.00 vs 1.20 : 537819.974443
    alpha 0.80 vs 1.20 : 1772209.736646

Non-zero differences here mean the ladder geometry changes with alpha.
That is the property missing from the earlier uniform-scaling packs.

Recommended first run
---------------------
Start with these gap ladders:
    helium_structactive_gaps_alpha_0.80.csv
    helium_structactive_gaps_alpha_0.90.csv
    helium_structactive_gaps_alpha_1.00.csv
    helium_structactive_gaps_alpha_1.10.csv
    helium_structactive_gaps_alpha_1.20.csv

Then compare:
    - mean rho
    - max rho
    - regime
    - state

If the chamber is more sensitive to multiplet structure, also test:
    helium_structactive_fs_alpha_0.80.csv
    helium_structactive_fs_alpha_1.00.csv
    helium_structactive_fs_alpha_1.20.csv
