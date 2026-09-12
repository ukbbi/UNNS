README_ab_bridge_compare.txt
STELLAR_BOUNDARY_DYNAMICS_I
A–B Bridge Comparator

SCRIPT:
tools/ab_bridge_compare.py

PURPOSE:
Compare Phase A normalization-reviewed v2 vectors against Phase B
normalization-reviewed v2 vectors.

INPUTS:
AB_bridge/inputs/A_5D_VECTOR_SUMMARY_v2.csv
AB_bridge/inputs/B_5D_VECTOR_SUMMARY_v2.csv

OUTPUTS:
AB_bridge/comparisons/AB_VECTOR_PAIRWISE_COMPARISON.csv
AB_bridge/comparisons/AB_DOMAIN_CENTROID_COMPARISON.csv
AB_bridge/comparisons/AB_OBJECT_RANKING.csv

AB_bridge/summaries/AB_BRIDGE_SUMMARY.csv
AB_bridge/summaries/AB_BRIDGE_INTERPRETATION.txt

RECOMMENDED RUN:
Open PowerShell in:

stellar_boundary_dynamics/

Then run:

python tools/ab_bridge_compare.py AB_bridge/inputs/A_5D_VECTOR_SUMMARY_v2.csv AB_bridge/inputs/B_5D_VECTOR_SUMMARY_v2.csv AB_bridge

RUN FROM INSIDE AB_bridge:
python ../tools/ab_bridge_compare.py inputs/A_5D_VECTOR_SUMMARY_v2.csv inputs/B_5D_VECTOR_SUMMARY_v2.csv .

FEATURES COMPARED:
mean_GR
var_GR
anisotropic_persistence_bounded
admissibility_persistence
collapse_onset_radius
kappa_connect_reference
tail_dominance_reference

METHOD:
The script performs min-max normalization across A+B vectors, then computes:

pairwise A-B Euclidean distance
pairwise A-B Manhattan distance
pairwise cosine similarity
A-domain centroid
B-domain centroid
centroid distance
nearest Phase A object for each Phase B object
Phase B ranking by nearest Phase A distance

INTERPRETATION:
This is a structural bridge, not an astrophysical explosion simulator.
It compares processed vector domains:

A = pre-boundary radial support/composition profiles
B = post-boundary observable brightness-response trajectories
