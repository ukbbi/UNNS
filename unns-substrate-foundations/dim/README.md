📁 Dimensional Regime Synthesis (UNNS Substrate)
Emergent Dimensionality from Structural Regime Transitions
🧭 Overview

This directory contains the Dimensional Regime Synthesis module of the UNNS (Unbounded Nested Number Sequences) Substrate, establishing how:

dimensionality is not assumed — it emerges from structural regime behavior

This is a post-STRUC-I layer, built on:

admissibility (USL)
regime classification (HARD / SOFT / CRITICAL)
ladder-based structural analysis
⚠️ What This Module Actually Does

This is NOT:

a geometric dimensional theory
a spatial embedding model
a coordinate-based reconstruction

This IS:

a mapping from structural scaling behavior → effective dimensional regimes

🔬 Core Principle

Dimensionality is inferred from:

scaling behavior of ladders
response under perturbation (κ, ε)
regime transitions

Thus:

Dimension = emergent property of structural response, not an input parameter

📂 Contents
📄 Core Manuscript
Emergent Dimensionality in the UNNS Substrate.pdf
→ formal definition of dimensional regimes
→ theoretical grounding of emergence
🌐 Interactive / Article Layer
unns_emergent_dimensionality_article.html
→ article-ready exposition for unns.tech
unns_phase_space_v2.html
→ visualization of regime transitions in phase space
🖼️ Visualizations
image1f.png → fundamental regime separation
image2f.png → scaling transitions
image3f.png → multi-regime interaction
image4f.png → emergent dimensional structure
⚙️ Pipeline

📁 UNNS_Dimensional_Regime_Synthesis_Pipeline/

This is the operational core of the module.

⚙️ Pipeline Structure
Inputs
atoms_input/
condensed-matter_band structures_input/
cosmo_ladders_input/
crystallography_cif_to_ladders_strict/

→ heterogeneous physical datasets converted into ladders

Processing
unns_scaling_extractor.py
→ extracts scaling behavior from ladders
transition_generator.py
→ generates structural transitions across regimes
Supporting Specs
UNNS Scaling Extraction — Dimensional Regime Analysis.md
Transition Generator — Purpose and Role.md
Outputs
output/
cw_generated_transition_data/

→ contain:

regime transitions
scaling fingerprints
dimensional classification signals
🔑 Core Results (Aligned with Manuscript)
1. Dimensionality Emerges from Scaling

No dimension is predefined.

Instead:

stable scaling → low-dimensional regime
unstable / fragmented scaling → higher-dimensional behavior
2. Regimes Encode Dimensional Structure
Regime	Interpretation
HARD	constrained / low-dimensional
SOFT	flexible / intermediate
CRITICAL	transitional / dimensional boundary
3. Phase Space is Structural, Not Geometric

The phase space shown in:

unns_phase_space_v2.html

is:

a regime transition space, not a coordinate space

4. Cross-Domain Consistency

Same dimensional behavior emerges from:

atomic ladders
cosmological ladders
crystallographic data

→ supports substrate-level universality

🚀 How to Use (GitHub)
Step 1 — Prepare Data

Place datasets into:

atoms_input/
cosmo_ladders_input/
...
Step 2 — Extract Scaling

Run:

python unns_scaling_extractor.py
Step 3 — Generate Transitions
python transition_generator.py
Step 4 — Inspect Results
open output/
open unns_phase_space_v2.html

🔗 Relation to UNNS Stack

This module sits above:

STRUC-I (admissibility)
PRP (fragmentation)
Local Geometry (boundaries)

and provides:

interpretation layer → what structure “looks like” globally

📌 Status

✔ Theory: defined
✔ Pipeline: operational
✔ Multi-domain inputs: integrated
✔ Visualization: complete
✔ Alignment with UNNS: consistent

🧠 Final Statement (Strict)

Dimensionality is not a property of space.

It is the structural signature of how systems scale and transition within the admissibility framework.