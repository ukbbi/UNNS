Cross-Constant Structural Invariance Atlas

UNNS Substrate Program — Canonical Dataset

Overview

This repository contains the cross-constant structural admissibility atlas:
a unified evaluation of how fundamental constants act on real physical systems across domains.

The core question:

Do fundamental constants act as structural operators that change admissibility regimes — or are they structurally inert?

The atlas evaluates this using the STRUC-I admissibility framework applied consistently across:

Atomic systems
Molecular spectra
Cosmology / CMB
Planetary geoid fields
Nuclear spectra
Hadronic states
Core Result

Admissibility is never violated.

Across:

4 constants
7 domain types
26+ physical systems
1,500+ ladders

the inequality holds universally:

inv(Pε;L) ≤ ν(Vε(L))

There are:

0 hard violations
Only boundary approaches (no breakdown)
Constants Studied
Column	Constant	Role
I	α (fine-structure)	Electromagnetic coupling
II	μ (proton–electron mass ratio)	Mass-scale deformation
III	αₛ (strong coupling)	Nuclear / hadronic coupling
IV	αG (gravitational coupling)	Macroscopic gravitational structure
Key Structural Findings
1. Constants are domain-selective operators
α → active in atomic / nuclear
μ → active in molecular (H₂)
αₛ → inactive (tested domains)
αG → inactive within physical range

➡️ Constants do not act universally — they couple selectively.

2. Physical values sit at structural extrema

Two confirmed cases:

Na under α → pressure maximum
H₂ under μ → pressure maximum

➡️ Physical constants place systems at maximal structural stress, not equilibrium minima.

3. Same system can respond to one constant and ignore another

Example:

⁴⁸Ca
α → extreme structural activity (17/17 violations tendency)
αₛ → completely inert

➡️ Structural response depends on coupling channel, not system alone.

4. Some systems are universally stable
²⁰⁸Pb:
Aκ = 1.0000 across all tested constants
No structural response anywhere

➡️ Demonstrates deep structural invariance

5. Molecular domain splits into two regimes
H₂ → boundary system
Strong response under μ
Near admissibility limit
CO, N₂, HCl, HD → stable systems
No structural signal

➡️ Same domain contains both critical and inert structures

6. Gravitational structure is strictly stable (tested range)

Earth, Mars, Moon:

No structural signal under αG
No extrema within tested γ-range

➡️ Large-scale structure is highly constrained

Repository Structure
alpha_gamma/                      # Constant sweep grids
co_h2_converted_mu_tierA_packs_v1/  # Tier A molecular datasets
hcl_mu_pack_v1/                  # HCl μ-sweep results
HD_mu_tierA_pack_inferred/       # HD Tier A (inferred decomposition)
n2_mu_pack_v1/                   # N₂ μ results
raw_par_data/                    # Source datasets

cross_constant_analysis.html     # Full atlas (interactive)
unns_cross_constant_article.html # Article-form presentation
chamber_struc_i_v1_0_4.html      # STRUC-I instrument interface

Structural Invariance and Domain-Selective Response Under Fundamental Constant Deformation.pdf
Main Artifact

The full atlas is provided here:

👉

This contains:

Full 4-column matrix
All system classifications
Structural pressure distributions
Cross-domain comparisons
Verified admissibility outcomes
Interpretation

This dataset establishes:

Admissibility is a structural invariant across physical reality.

But:

Not all systems respond to all constants
Not all domains reach structural boundaries
Structural response depends on how the constant couples to the system
What This Repository Is
Not a simulation
Not synthetic data
Not heuristic modeling

This is:

Direct structural analysis of real physical datasets under controlled constant deformation

What This Enables

This atlas is the first complete map of:

Structural response across constants
Domain-selective coupling
Boundary behavior of real systems

It provides the basis for:

Structural classification of physical systems
Identification of boundary regimes
Comparative analysis across physics domains
Status
α → structurally active
μ → structurally active (molecular)
αₛ → no detected structural activity
αG → no detected structural activity (within tested range)

USL: holds universally

Next Steps
Extend αG sweep below current range (to reach predicted extrema)
Perform exact Tier A decomposition for HD
Test heavier hadronic systems (e.g., bottomonium)
Isolate coupling mechanisms behind constant-selectivity
License

Research dataset — part of the UNNS Substrate Program